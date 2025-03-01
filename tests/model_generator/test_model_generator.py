from dataclasses_avroschema import ModelGenerator, field_utils, types
from dataclasses_avroschema.model_generator.avro_to_python_utils import render_datetime


def test_model_generator_primitive_types(schema: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses


@dataclasses.dataclass
class User(AvroModel):
    age: types.Int32
    weight: types.Int32
    money_available: float
    name: str = "marcos"
    pet_age: types.Int32 = 1
    height: types.Float32 = 10.1
    is_student: bool = True
    encoded: bytes = b"Hi"

    class Meta:
        namespace = "test"
        schema_doc = "An User"
        aliases = ['schema', 'test-schema']
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema)
    assert result.strip() == expected_result.strip()


def test_model_generator_primitive_types_with_default_null(schema_with_nulls: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import typing


@dataclasses.dataclass
class User(AvroModel):
    weight: types.Int32
    money_available: float
    name: typing.Optional[str] = None
    age: typing.Optional[types.Int32] = None
    pet_age: types.Int32 = 1
    height: types.Float32 = 10.1
    is_student: bool = True
    encoded: bytes = b"Hi"
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_nulls)
    assert result.strip() == expected_result.strip()


def test_model_generator_primitive_types_with_unions(schema_with_unions: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import typing


@dataclasses.dataclass
class User(AvroModel):
    name: typing.Union[types.Int32, str]
    money_available: float
    age: typing.Union[types.Int32, str] = 10
    pet_age: typing.Union[str, bool] = "bond"
    height: types.Float32 = 10.1
    weight: typing.Optional[typing.Union[types.Float32, types.Int32]] = None
    is_student: bool = True
    encoded: bytes = b"Hi"
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_unions)
    assert result.strip() == expected_result.strip()


def test_model_generator_array_type(schema_with_array_types: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import typing


@dataclasses.dataclass
class User(AvroModel):
    pets: typing.List[str]
    total: typing.List[typing.Union[types.Int32, types.Float32]]
    cars: typing.List[str] = dataclasses.field(default_factory=list)
    bank_accounts: typing.Optional[typing.List[str]] = None
    favourites_numbers: typing.List[int] = dataclasses.field(default_factory=lambda: [7, 13])
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_array_types)
    assert result.strip() == expected_result.strip()


def test_model_generator_map_type(schema_with_map_types: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import typing


@dataclasses.dataclass
class User(AvroModel):
    accounts_money: typing.Dict[str, types.Float32]
    cars: typing.Dict[str, typing.Union[str, bytes]]
    cars_brand_total: typing.Dict[str, int] = dataclasses.field(default_factory=dict)
    family_ages: typing.Dict[str, int] = dataclasses.field(default_factory=lambda: {'father': 50})
    bank_accounts: typing.Optional[typing.Dict[str, str]] = None
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_map_types)
    assert result.strip() == expected_result.strip()


def test_schema_with_fixed_types(schema_with_fixed_types: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses


@dataclasses.dataclass
class User(AvroModel):
    md5: types.Fixed = types.Fixed(16, namespace="md5", aliases=['md5', 'hash'])
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_fixed_types)
    assert result.strip() == expected_result.strip()


def test_schema_with_enum_types(schema_with_enum_types: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
import dataclasses
import enum
import typing


class FavoriteColor(enum.Enum):
    BLUE = "Blue"
    YELLOW = "Yellow"
    GREEN = "Green"


class Superheros(enum.Enum):
    BATMAN = "batman"
    SUPERMAN = "superman"
    SPIDERMAN = "spiderman"


class Cars(enum.Enum):
    BMW = "bmw"
    FERRARY = "ferrary"
    DUNA = "duna"


@dataclasses.dataclass
class User(AvroModel):
    favorite_color: FavoriteColor
    superheros: Superheros = Superheros.BATMAN
    cars: typing.Optional[Cars] = None
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_enum_types)
    assert result.strip() == expected_result.strip()


def test_schema_one_to_one_relationship(schema_one_to_one_relationship: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
import dataclasses
import typing


@dataclasses.dataclass
class Address(AvroModel):
    street: str
    street_number: int

    class Meta:
        schema_doc = "An Address"


@dataclasses.dataclass
class User(AvroModel):
    name: str
    age: int
    address: Address
    extra_address: Address
    crazy_union: typing.Union[str, Address]
    optional_address: typing.Optional[Address] = None
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_one_to_one_relationship)
    assert result.strip() == expected_result.strip()


def test_schema_one_to_many_array_relationship(schema_one_to_many_array_relationship: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
import dataclasses
import typing


@dataclasses.dataclass
class Address(AvroModel):
    street: str
    street_number: int

    class Meta:
        schema_doc = "An Address"


@dataclasses.dataclass
class User(AvroModel):
    name: str
    age: int
    addresses: typing.List[Address]
    crazy_union: typing.Union[str, typing.List[Address]]
    optional_addresses: typing.Optional[typing.List[Address]] = None
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_one_to_many_array_relationship)
    assert result.strip() == expected_result.strip()


def test_schema_one_to_many_map_relationship(schema_one_to_many_map_relationship: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
import dataclasses
import typing


@dataclasses.dataclass
class Address(AvroModel):
    street: str
    street_number: int

    class Meta:
        schema_doc = "An Address"


@dataclasses.dataclass
class User(AvroModel):
    name: str
    age: int
    addresses: typing.Dict[str, Address]
    crazy_union: typing.Union[str, typing.Dict[str, Address]]
    optional_addresses: typing.Optional[typing.Dict[str, Address]] = None
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_one_to_many_map_relationship)
    assert result.strip() == expected_result.strip()


def test_schema_one_to_self_relathionship(schema_one_to_self_relationship: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
import dataclasses
import typing


@dataclasses.dataclass
class User(AvroModel):
    name: str
    age: int
    friend: typing.Optional[typing.Type["User"]] = None
    relatives: typing.List[typing.Type["User"]] = dataclasses.field(default_factory=list)
    teammates: typing.Dict[str, typing.Type["User"]] = dataclasses.field(default_factory=dict)
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_one_to_self_relationship)
    assert result.strip() == expected_result.strip()


def test_decimal_field(schema_with_decimal_field: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import decimal


@dataclasses.dataclass
class Demo(AvroModel):
    foo: decimal.Decimal = types.Decimal(scale=3, precision=10)
"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_decimal_field)
    assert result.strip() == expected_result.strip()


def test_schema_logical_types(schema_with_logical_types: types.JsonDict) -> None:
    release_datetime = render_datetime(value=1570903062000, format=field_utils.TIMESTAMP_MILLIS)
    release_datetime_micro = render_datetime(value=1570903062000000, format=field_utils.TIMESTAMP_MICROS)

    expected_result = f"""
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses
import datetime
import decimal
import typing
import uuid


@dataclasses.dataclass
class LogicalTypes(AvroModel):
    birthday: datetime.date
    birthday_time: datetime.time
    birthday_datetime: datetime.datetime
    uuid_1: uuid.uuid4
    money: decimal.Decimal = types.Decimal(scale=2, precision=3)
    meeting_date: typing.Optional[datetime.date] = None
    release_date: datetime.date = datetime.date(2019, 10, 12)
    meeting_time: typing.Optional[datetime.time] = None
    release_time: datetime.time = datetime.time(17, 57, 42)
    release_time_micro: types.TimeMicro = datetime.time(17, 57, 42, 0)
    meeting_datetime: typing.Optional[datetime.datetime] = None
    release_datetime: datetime.datetime = {release_datetime}
    release_datetime_micro: types.DateTimeMicro = {release_datetime_micro}
    uuid_2: typing.Optional[uuid.uuid4] = None
    event_uuid: uuid.uuid4 = "ad0677ab-bd1c-4383-9d45-e46c56bcc5c9"
    explicit_with_default: decimal.Decimal = types.Decimal(scale=2, precision=3, default=decimal.Decimal('3.14'))

"""
    model_generator = ModelGenerator()
    result = model_generator.render(schema=schema_with_logical_types)
    assert result.strip() == expected_result.strip()


def test_model_generator_render_module_from_multiple_schemas(schema: types.JsonDict, schema_2: types.JsonDict) -> None:
    expected_result = """
from dataclasses_avroschema import AvroModel
from dataclasses_avroschema import types
import dataclasses


@dataclasses.dataclass
class User(AvroModel):
    age: types.Int32
    weight: types.Int32
    money_available: float
    name: str = "marcos"
    pet_age: types.Int32 = 1
    height: types.Float32 = 10.1
    is_student: bool = True
    encoded: bytes = b"Hi"

    class Meta:
        namespace = "test"
        schema_doc = "An User"
        aliases = ['schema', 'test-schema']


@dataclasses.dataclass
class Address(AvroModel):
    street: str
    street_number: int

    class Meta:
        schema_doc = "An Address"
"""
    model_generator = ModelGenerator()
    result = model_generator.render_module(schemas=[schema, schema_2])
    assert result.strip() == expected_result.strip()
