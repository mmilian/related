import enum
import json
import uuid
from decimal import Decimal

import attr

import related

EXAMPLE_UUID = uuid.uuid4()


@enum.unique
class DataType(enum.Enum):
    STRING = 'string'
    NUMBER = 'number'
    INTEGER = 'integer'
    BOOLEAN = 'boolean'
    ARRAY = 'array'
    OBJECT = 'object'


@enum.unique
class IntEnum(enum.Enum):
    a = 1
    b = 2
    c = 3


@related.immutable
class MyChild(object):
    my_test_field = related.IntegerField(key="int", metadata={'exclude': True})


@related.immutable
class MyModel(object):
    boolean_field = related.BooleanField(key="bool", metadata={'exclude': True})
    child_field = related.ChildField(DataType, required=False, key="type", metadata={'exclude': True})
    date_field = related.DateField(key="date", required=False, metadata={'exclude': True})
    date_time_field = related.DateTimeField(key="date_time", required=False, metadata={'exclude': True})
    time_field = related.TimeField(key="time", required=False, metadata={'exclude': True})
    float_field = related.FloatField(key="float", required=False, metadata={'exclude': True})
    int_field = related.IntegerField(key="int", required=False, metadata={'exclude': True})
    mapping_field = related.MappingField(MyChild, "int", key="dict", required=False, metadata={'exclude': True})
    regex_field = related.RegexField("[^@]+@[^@]+", required=False, key="regex", metadata={'exclude': True})
    sequence_field = related.SequenceField(str, required=False, key="sequence", metadata={'exclude': True})
    set_field = related.SetField(str, required=False, key="set", metadata={'exclude': True})
    string_field = related.StringField(required=False, key="string", metadata={'exclude': True})
    url_field = related.URLField(required=False, key="url", metadata={'exclude': True})
    uuid_field = related.UUIDField(required=False, key="uuid", metadata={'exclude': True})
    decimal_field = related.DecimalField(required=False, key="decimal", metadata={'exclude': True})
    # criss = related.StringField(key="cross")
    # cross = related.StringField(key="criss")
    # is_list = related.SequenceField(str, key="list")
    # is_enum = related.ChildField(IntEnum, key="enum", required=False)


def test_metadata():
    assert attr.fields(MyModel).boolean_field.metadata['exclude']
    assert attr.fields(MyModel).boolean_field.metadata['key'] == "bool"
    assert attr.fields(MyModel).child_field.metadata['exclude']
    assert attr.fields(MyModel).child_field.metadata['key'] == "type"
    assert attr.fields(MyModel).date_field.metadata['exclude']
    assert attr.fields(MyModel).date_field.metadata['key'] == "date"
    assert attr.fields(MyModel).date_time_field.metadata['exclude']
    assert attr.fields(MyModel).date_time_field.metadata['key'] == "date_time"
    assert attr.fields(MyModel).time_field.metadata['exclude']
    assert attr.fields(MyModel).time_field.metadata['key'] == "time"
    assert attr.fields(MyModel).float_field.metadata['exclude']
    assert attr.fields(MyModel).float_field.metadata['key'] == "float"
    assert attr.fields(MyModel).int_field.metadata['exclude']
    assert attr.fields(MyModel).int_field.metadata['key'] == "int"
    assert attr.fields(MyModel).mapping_field.metadata['exclude']
    assert attr.fields(MyModel).mapping_field.metadata['key'] == "dict"
    assert attr.fields(MyModel).regex_field.metadata['exclude']
    assert attr.fields(MyModel).regex_field.metadata['key'] == "regex"
    assert attr.fields(MyModel).sequence_field.metadata['exclude']
    assert attr.fields(MyModel).sequence_field.metadata['key'] == "sequence"
    assert attr.fields(MyModel).set_field.metadata['exclude']
    assert attr.fields(MyModel).set_field.metadata['key'] == "set"
    assert attr.fields(MyModel).string_field.metadata['exclude']
    assert attr.fields(MyModel).string_field.metadata['key'] == "string"
    assert attr.fields(MyModel).url_field.metadata['exclude']
    assert attr.fields(MyModel).url_field.metadata['key'] == "url"
    assert attr.fields(MyModel).uuid_field.metadata['exclude']
    assert attr.fields(MyModel).uuid_field.metadata['key'] == "uuid"
    assert attr.fields(MyModel).decimal_field.metadata['exclude']
    assert attr.fields(MyModel).decimal_field.metadata['key'] == "decimal"


def test_override_metadata_by_key():
    obj = MyModel(boolean_field=True, decimal_field=Decimal(0.0))
    assert json.loads(related.to_json(obj))['bool'] == True
