
from collections import OrderedDict
from datetime import datetime

from bson import SON
from bson.py3compat import string_type
from bson.decimal128 import Decimal128
from bson.timestamp import Timestamp

from ..errors import WriteError
from .core import (
    _cmp_decimal,
    FieldWalker,
    Weighted,
    FieldWriteError,
)
from .queries import QueryFilter
from .helpers import is_numeric_type, is_duckument_type


def _update(fieldwalker,
            field,
            value,
            evaluator,
            array_filters):

    fieldwalker.go(field)
    try:
        fieldwalker.set(value, evaluator, array_filters)
    # Take error message and put error code
    except FieldWriteError as err:
        raise WriteError(str(err), code=err.code)


def _drop(fieldwalker, field, array_filters):

    fieldwalker.go(field)
    try:
        fieldwalker.drop(array_filters)
    # Take error message and put error code
    except FieldWriteError as err:
        raise WriteError(str(err), code=err.code)


class Updator(object):

    def __init__(self, spec, array_filters=None):

        self.update_ops = {

            # field update ops
            "$inc": parse_inc,
            "$min": parse_min,
            "$max": parse_max,
            "$mul": parse_mul,
            "$rename": parse_rename,
            "$set": parse_set,
            "$setOnInsert": self.parse_set_on_insert,
            "$unset": parse_unset,
            "$currentDate": parse_currentDate,

            # array update ops
            # $                 implemented in FieldWalker
            # $[]               implemented in FieldWalker
            # $[<identifier>]   implemented in FieldWalker
            "$addToSet": parse_add_to_set,
            "$pop": parse_pop,
            "$pull": parse_pull,
            "$push": parse_push,
            "$pullAll": parse_pull_all,
            "$each": None,
            "$position": None,
            "$slice": None,
            "$sort": None,

        }

        self.fields_to_update = []
        self.array_filters = self.array_filter_parser(array_filters or [])
        # sort by key (operator)
        self.operations = OrderedDict(sorted(self.parser(spec).items()))
        self.__insert = None
        self.__fieldwalker = None

    def __repr__(self):
        pass

    def __call__(self, fieldwalker, do_insert=False):
        """Update document and return a bool value indicate changed or not"""
        self.__fieldwalker = fieldwalker
        self.__insert = do_insert

        with fieldwalker:
            for operator in self.operations.values():
                operator(fieldwalker)

            return fieldwalker.commit()

    @property
    def fieldwalker(self):
        return self.__fieldwalker

    def array_filter_parser(self, array_filters):
        filters = {}
        for i, filter_ in enumerate(array_filters):
            top = ""
            conds = {}

            for identifier, cond in filter_.items():
                id_s = identifier.split(".", 1)

                if not top and id_s[0] in filters:
                    msg = ("Found multiple array filters with the same "
                           "top-level field name {}".format(id_s[0]))
                    raise WriteError(msg, code=9)

                if top and id_s[0] != top:
                    msg = ("Error parsing array filter: Expected a single "
                           "top-level field name, found {0!r} and {1!r}"
                           "".format(top, id_s[0]))
                    raise WriteError(msg, code=9)

                top = id_s[0]
                conds.update({identifier: cond})

            filters[top] = QueryFilter(conds)

        return filters

    def parser(self, spec):
        if not next(iter(spec)).startswith("$"):
            raise ValueError("update only works with $ operators")

        update_stack = {}
        idnt_tops = list(self.array_filters.keys())

        for op, cmd_doc in spec.items():
            if op not in self.update_ops:
                raise WriteError("Unknown modifier: {}".format(op))

            if not is_duckument_type(cmd_doc):
                msg = ("Modifiers operate on fields but we found type {0} "
                       "instead. For example: {{$mod: {{<field>: ...}}}} "
                       "not {1}".format(type(cmd_doc).__name__, spec))
                raise WriteError(msg, code=9)

            for field, value in cmd_doc.items():
                if field == "_id":
                    msg = ("Performing an update on the path '_id' would "
                           "modify the immutable field '_id'")
                    raise WriteError(msg, code=66)

                for top in list(idnt_tops):
                    if "$[{}]".format(top) in field:
                        idnt_tops.remove(top)

                update_stack[field] = self.update_ops[op](
                    field, value, self.array_filters)

                self.check_conflict(field)
                if op == "$rename":
                    self.check_conflict(value)

        if idnt_tops:
            msg = ("The array filter for identifier {0!r} was not "
                   "used in the update {1}".format(idnt_tops[0], spec))
            raise WriteError(msg, code=9)

        return update_stack

    def check_conflict(self, field):
        for staged in self.fields_to_update:
            if field.startswith(staged) or staged.startswith(field):
                msg = ("Updating the path {0!r} would create a "
                       "conflict at {1!r}".format(field, staged[:len(field)]))
                raise WriteError(msg, code=40)

        self.fields_to_update.append(field)

    def parse_set_on_insert(self, field, value, array_filters):
        def _set_on_insert(fieldwalker):
            if self.__insert:
                parse_set(field, value, array_filters)(fieldwalker)

        return _set_on_insert


def parse_inc(field, value, array_filters):
    if not is_numeric_type(value):
        val_repr_ = "{!r}" if isinstance(value, string_type) else "{}"
        val_repr_ = val_repr_.format(value)
        msg = ("Cannot increment with non-numeric argument: "
               "{{{0}: {1}}}".format(field, val_repr_))
        raise WriteError(msg, code=14)

    def _inc(fieldwalker):

        def inc(node, inc_val):
            old_val = node.value
            if node.exists and not is_numeric_type(old_val):
                _id = fieldwalker.doc["_id"]
                value_type = type(old_val).__name__
                msg = ("Cannot apply $inc to a value of non-numeric type. "
                       "{{_id: {0}}} has the field {1!r} of non-numeric type "
                       "{2}".format(_id, str(node), value_type))
                raise WriteError(msg, code=14)

            is_decimal128 = False
            if isinstance(old_val, Decimal128):
                is_decimal128 = True
                old_val = old_val.to_decimal()
            if isinstance(inc_val, Decimal128):
                is_decimal128 = True
                inc_val = inc_val.to_decimal()

            if is_decimal128:
                return Decimal128((old_val or 0) + inc_val)
            else:
                return (old_val or 0) + inc_val

        _update(fieldwalker, field, value, inc, array_filters)

    return _inc


def parse_min(field, value, array_filters):
    def _min(fieldwalker):
        def min(node, min_val):
            old_val = node.value
            if node.exists:
                old_val = Weighted(old_val)
                min_val = Weighted(min_val)
                return min_val.value if min_val < old_val else old_val.value
            else:
                return min_val

        _update(fieldwalker, field, value, min, array_filters)

    return _min


def parse_max(field, value, array_filters):
    def _max(fieldwalker):
        def max(node, max_val):
            old_val = node.value
            if node.exists:
                old_val = Weighted(old_val)
                max_val = Weighted(max_val)
                return max_val.value if max_val > old_val else old_val.value
            else:
                return max_val

        _update(fieldwalker, field, value, max, array_filters)

    return _max


def parse_mul(field, value, array_filters):
    if not is_numeric_type(value):
        val_repr_ = "{!r}" if isinstance(value, string_type) else "{}"
        val_repr_ = val_repr_.format(value)
        msg = ("Cannot multiply with non-numeric argument: "
               "{{{0}: {1}}}".format(field, val_repr_))
        raise WriteError(msg, code=14)

    def _mul(fieldwalker):
        def mul(node, mul_val):
            old_val = node.value
            if node.exists and not is_numeric_type(old_val):
                _id = fieldwalker.doc["_id"]
                value_type = type(old_val).__name__
                msg = ("Cannot apply $mul to a value of non-numeric type. "
                       "{{_id: {0}}} has the field {1!r} of non-numeric type "
                       "{2}".format(_id, str(node), value_type))
                raise WriteError(msg, code=14)

            is_decimal128 = False
            if isinstance(old_val, Decimal128):
                is_decimal128 = True
                old_val = old_val.to_decimal()
            if isinstance(mul_val, Decimal128):
                is_decimal128 = True
                mul_val = mul_val.to_decimal()

            if is_decimal128:
                return Decimal128((old_val or 0) * mul_val)
            else:
                return (old_val or 0.0) * mul_val

        _update(fieldwalker, field, value, mul, array_filters)

    return _mul


def _get_array_member(fieldvalues):
    for node in fieldvalues.nodes:
        if node.in_array:
            return node


def parse_rename(field, new_field, array_filters):
    if not isinstance(new_field, string_type):
        msg = ("The 'to' field for $rename must be a string: {0}: {1}"
               "".format(field, new_field))
        raise WriteError(msg, code=2)

    if field == new_field:
        msg = ("The source and target field for $rename must differ: "
               "{0}: {1!r}".format(field, new_field))
        raise WriteError(msg, code=2)

    if field.startswith(new_field) or new_field.startswith(field):
        msg = ("The source and target field for $rename must not be on the "
               "same path: {0}: {1!r}".format(field, new_field))
        raise WriteError(msg, code=2)

    def _rename(fieldwalker):

        probe = FieldWalker(fieldwalker.doc)

        probe.go(field).get()
        fieldvalues = probe.value

        if not fieldvalues.exists:
            return

        value = next(fieldvalues.iter_plain())

        array_member = _get_array_member(fieldvalues)
        if array_member is not None:
            _id = probe.doc["_id"]
            array_field = str(array_member.parent)
            msg = ("The source field cannot be an array element, "
                   "{0!r} in doc with _id: {1} has an array field "
                   "called {2!r}".format(field, _id, array_field))
            raise WriteError(msg, code=2)

        probe.go(new_field).get()
        fieldvalues = probe.value

        array_member = _get_array_member(fieldvalues)
        if array_member is not None:
            _id = probe.doc["_id"]
            array_field = str(array_member.parent)
            msg = ("The destination field cannot be an array element, "
                   "{0!r} in doc with _id: {1} has an array field "
                   "called {2!r}".format(new_field, _id, array_field))
            raise WriteError(msg, code=2)

        _drop(fieldwalker, field, array_filters)
        _update(fieldwalker, new_field, value, None, array_filters)

    return _rename


def parse_set(field, value, array_filters):
    def _set(fieldwalker):
        _update(fieldwalker, field, value, None, array_filters)

    return _set


def parse_unset(field, _, array_filters):
    def _unset(fieldwalker):
        _drop(fieldwalker, field, array_filters)

    return _unset


def parse_currentDate(field, value, array_filters):
    date_type = {
        "date": datetime.utcnow(),
        "timestamp": Timestamp(datetime.utcnow(), 1),
    }

    if not isinstance(value, bool):
        if not is_duckument_type(value):
            msg = ("{} is not valid type for $currentDate. Please use a "
                   "boolean ('true') or a $type expression ({{$type: "
                   "'timestamp/date'}}).".format(type(value).__name__))
            raise WriteError(msg, code=2)

        for k, v in value.items():
            if k != "$type":
                msg = "Unrecognized $currentDate option: {}".format(k)
                raise WriteError(msg, code=2)
            if v not in date_type:
                msg = ("The '$type' string field is required to be 'date' "
                       "or 'timestamp': {$currentDate: {field : {$type: "
                       "'date'}}}")
                raise WriteError(msg, code=2)

            value = date_type[v]
    else:
        value = date_type["date"]

    def _currentDate(fieldwalker):
        parse_set(field, value, array_filters)(fieldwalker)

    return _currentDate


def parse_add_to_set(field, value, array_filters):
    def _add_to_set(fieldwalker):
        def add_to_set(node, new_elem):
            old_val = node.value
            if node.exists and not isinstance(old_val, list):
                value_type = type(old_val).__name__
                msg = ("Cannot apply $addToSet to non-array field. Field "
                       "named {0!r} has non-array type {1}"
                       "".format(str(node), value_type))
                raise WriteError(msg, code=2)

            new_array = (old_val or [])[:]
            if new_elem not in new_array:
                new_array.append(new_elem)
            return new_array

        _update(fieldwalker, field, value, add_to_set, array_filters)

    return _add_to_set


def parse_pop(field, value, array_filters):
    if not is_numeric_type(value):
        msg = ("Expected a number in: {0}: {1!r}".format(field, value))
        raise WriteError(msg, code=9)
    else:
        try:
            value = float(value)
            msg_raw = "Expected an integer: {0}: {1!r}"
        except TypeError:
            msg_raw = "Cannot represent as a 64-bit integer: {0}: {1!r}"
            value = float(value.to_decimal())

        if value not in (1.0, -1.0):
            raise WriteError(msg_raw.format(field, value), code=9)

    def _pop(fieldwalker):
        def pop(node, pop_ind):
            old_val = node.value
            if node.exists and not isinstance(old_val, list):
                value_type = type(old_val).__name__
                msg = ("Path {0!r} contains an element of non-array type "
                       "{1!r}".format(str(node), value_type))
                raise WriteError(msg, code=14)

            if not node.exists:
                # do nothing
                return old_val

            if pop_ind == 1:
                return old_val[:-1]
            else:
                return old_val[1:]

        _update(fieldwalker, field, value, pop, array_filters)

    return _pop


def parse_pull(field, value_or_conditions, array_filters):
    if is_duckument_type(value_or_conditions):
        query_spec = {}
        for k, v in value_or_conditions.items():
            if not k[:1] == "$":
                query_spec[".".join((field, k))] = v
            else:
                query_spec[field] = {k: v}
        queryfilter = QueryFilter(query_spec)
    else:
        queryfilter = QueryFilter({field: value_or_conditions})

    def _pull(fieldwalker):
        def pull(node, _):
            old_val = node.value
            if node.exists and not isinstance(old_val, list):
                msg = "Cannot apply $pull to a non-array value"
                raise WriteError(msg, code=2)

            if not node.exists:
                # do nothing
                return old_val

            new_array = []
            for elem in old_val:
                result = queryfilter({field: elem})

                if not result:
                    new_array.append(elem)
            return new_array

        _update(fieldwalker, field, None, pull, array_filters)

    return _pull


def parse_push(field, value, array_filters):
    def _push(fieldwalker):
        def push(node, new_elem):
            old_val = node.value
            if node.exists and not isinstance(old_val, list):
                value_type = type(old_val).__name__
                _id = fieldwalker.doc["_id"]
                msg = ("The field {0!r} must be an array but is of type "
                       "{1} in document {{_id: {2}}}"
                       "".format(str(node), value_type, _id))
                raise WriteError(msg, code=2)

            new_array = (old_val or [])[:]
            new_array.append(new_elem)
            return new_array

        _update(fieldwalker, field, value, push, array_filters)

    return _push


def parse_pull_all(field, value, array_filters):
    if not isinstance(value, list):
        value_type = type(value).__name__
        msg = ("$pullAll requires an array argument but was given a {}"
               "".format(value_type))
        raise WriteError(msg, code=2)

    def _pull_all(fieldwalker):
        def pull_all(node, pull_list):
            old_val = node.value
            if node.exists and not isinstance(old_val, list):
                msg = "Cannot apply $pull to a non-array value"
                raise WriteError(msg, code=2)

            if not node.exists:
                # do nothing
                return old_val

            def convert(lst):
                for val in lst:
                    if isinstance(val, Decimal128):
                        yield _cmp_decimal(val)
                    else:
                        yield val

            pull_list = list(convert(pull_list))
            old_val = list(convert(old_val))

            new_array = [elem for elem in old_val if elem not in pull_list]
            return new_array

        _update(fieldwalker, field, value, pull_all, array_filters)

    return _pull_all
