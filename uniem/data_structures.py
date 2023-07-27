from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict


class RecordType(str, Enum):
    PAIR = 'pair'
    TRIPLET = 'triplet'
    SCORED_PAIR = 'scored_pair'

# 导入dataclasses模块
from dataclasses import dataclass

# 定义一个装饰器函数，用来生成__slots__属性
def with_slots(cls):
    # 获取所有带有类型注解的字段名
    slots = [name for name, value in cls.__dict__.items() if isinstance(value, type)]
    # 如果有字段带有类型注解，就创建__slots__属性
    if slots:
        cls.__slots__ = slots
    # 返回类对象
    return cls

# 使用with_slots()函数和dataclass()函数，创建一个带有__slots__属性的类
@dataclass
@with_slots
class PairRecord:
    text: str
    text_pos: str


# @dataclass(slots=True)
# class PairRecord:
#     text: str
#     text_pos: str


# @dataclass(slots=True)
@dataclass
@with_slots
class TripletRecord:
    text: str
    text_pos: str
    text_neg: str


# @dataclass(slots=True)
@dataclass
@with_slots
class ScoredPairRecord:
    sentence1: str
    sentence2: str
    label: float


# * Order matters
record_type_cls_map: Dict[RecordType, Any] = {
    RecordType.SCORED_PAIR: ScoredPairRecord,
    RecordType.TRIPLET: TripletRecord,
    RecordType.PAIR: PairRecord,
}


def infer_record_type(record: dict) -> RecordType:
    record_type_field_names_map = {
        record_type: [field.name for field in fields(record_cls)] for record_type, record_cls in record_type_cls_map.items()
    }
    for record_type, field_names in record_type_field_names_map.items():
        if all(field_name in record for field_name in field_names):
            return record_type
    raise ValueError(f'Unknown record type, record: {record}')
