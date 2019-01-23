# -*- coding: utf-8 -*-
from decimal import Decimal
from future.moves.urllib.parse import ParseResult
from attr import attrib, NOTHING
from collections import OrderedDict
from uuid import uuid4, UUID
from datetime import date, datetime, time
from six import string_types

from . import _init_fields, types, converters, validators


def BooleanField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, metadata=None):
    """
    Create new bool field on a model.

    :param default: any boolean value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, bool)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata, type=bool)


def ChildField(cls, default=NOTHING, required=True, repr=True, cmp=True,
               key=None, metadata=None):
    """
    Create new child field on a model.

    :param cls: class (or name) of the model to be related.
    :param default: any object value of type cls
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    converter = converters.to_child_field(cls)
    validator = _init_fields.init_validator(
        required, object if isinstance(cls, str) else cls
    )
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp, metadata=metadata, type=cls)


def DateField(formatter=types.DEFAULT_DATE_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None, metadata=None):
    """
    Create new date field on a model.

    :param formatter: date formatter string (default: "%Y-%m-%d")
    :param default: any date or string that can be converted to a date value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, date)
    converter = converters.to_date_field(formatter)
    metadata = _field_metadata(metadata, formatter=formatter, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=metadata)


def DateTimeField(formatter=types.DEFAULT_DATETIME_FORMAT, default=NOTHING,
                  required=True, repr=True, cmp=True, key=None, metadata=None):
    """
    Create new datetime field on a model.

    :param formatter: datetime formatter string (default: "ISO_FORMAT")
    :param default: any datetime or string that can be converted to a datetime
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, datetime)
    converter = converters.to_datetime_field(formatter)
    metadata = _field_metadata(metadata, formatter=formatter, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=metadata, type=datetime)


def TimeField(formatter=types.DEFAULT_TIME_FORMAT, default=NOTHING,
              required=True, repr=True, cmp=True, key=None, metadata=None):
    """
    Create new time field on a model.

    :param formatter: time formatter string (default: "%H:%M:%S")
    :param default: any time or string that can be converted to a time value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, time)
    converter = converters.to_time_field(formatter)
    metadata = _field_metadata(metadata, formatter=formatter, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, cmp=cmp,
                  metadata=metadata)


def FloatField(default=NOTHING, required=True, repr=True, cmp=True,
               key=None, metadata=None):
    """
    Create new float field on a model.

    :param default: any float value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, float)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.float_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata, type=float)


def IntegerField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, metadata=None):
    """
    Create new int field on a model.

    :param default: any integer value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, int)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.int_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata, type=int)


def MappingField(cls, child_key, default=NOTHING, required=True, repr=False,
                 key=None, metadata=None):
    """
    Create new mapping field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param child_key: key field on the child object to be used as the map key.
    :param default: any mapping type
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, OrderedDict())
    converter = converters.to_mapping_field(cls, child_key)
    validator = _init_fields.init_validator(required, types.TypedMapping)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=metadata)


def RegexField(regex, default=NOTHING, required=True, repr=True, cmp=True,
               key=None, metadata=None):
    """
    Create new str field on a model.

    :param regex: regex validation string (e.g. "[^@]+@[^@]+" for email)
    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types,
                                            validators.regex(regex))
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata)


def SequenceField(cls, default=NOTHING, required=True, repr=False, key=None, metadata=None):
    """
    Create new sequence field on a model.

    :param cls: class (or name) of the model to be related in Sequence.
    :param default: any TypedSequence or list
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, [])
    converter = converters.to_sequence_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSequence)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=metadata, type=default)


def SetField(cls, default=NOTHING, required=True, repr=False, key=None, metadata=None):
    """
    Create new set field on a model.

    :param cls: class (or name) of the model to be related in Set.
    :param default: any TypedSet or set
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, set())
    converter = converters.to_set_field(cls)
    validator = _init_fields.init_validator(required, types.TypedSet)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converter, validator=validator,
                  repr=repr, metadata=metadata)


def StringField(default=NOTHING, required=True, repr=True, cmp=True,
                key=None, metadata=None):
    """
    Create new str field on a model.

    :param default: any string value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, string_types)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.str_if_not_none,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata)


def URLField(default=NOTHING, required=True, repr=True, cmp=True, key=None, metadata=None):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    cls = ParseResult
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, cls)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.str_to_url,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata)


def UUIDField(default=NOTHING, required=False, repr=True, cmp=True, key=None,  metadata=None):
    """
    Create new UUID field on a model.

    :param default: any value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    cls = UUID
    default = _init_fields.init_default(required, default, uuid4)
    validator = _init_fields.init_validator(required, cls)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=converters.str_to_uuid,
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata)


def DecimalField(default=NOTHING, required=True, repr=True, cmp=True,
                 key=None, metadata=None):
    """
    Create new decimal field on a model.

    :param default: any decimal value
    :param bool required: whether or not the object is invalid if not provided.
    :param bool repr: include this field should appear in object's repr.
    :param bool cmp: include this field in generated comparison.
    :param string key: override name of the value when converted to dict.
    :param dict metadata: an arbitrary mapping, might be used by third-party components.
    """
    default = _init_fields.init_default(required, default, None)
    validator = _init_fields.init_validator(required, Decimal)
    metadata = _field_metadata(metadata, key=key)
    return attrib(default=default, converter=lambda x: Decimal(x),
                  validator=validator, repr=repr, cmp=cmp,
                  metadata=metadata)


def _field_metadata(metadata, **preset):
    if metadata is None:
        metadata = {}
    metadata.update(preset)
    return metadata