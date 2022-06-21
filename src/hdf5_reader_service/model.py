from enum import Enum
from typing import Any, Generic, List, Mapping, Optional, Tuple, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class DatasetMacroStructure(BaseModel):
    shape: Tuple[int, ...]
    chunks: Optional[Tuple[int, ...]] = None


class ByteOrder(Enum):
    NATIVE = "NATIVE"
    LITTLE_ENDIAN = "LITTLE_ENDIAN"
    BIG_ENDIAN = "BIG_ENDIAN"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    @classmethod
    def from_numpy_byte_order(cls, np_order: str) -> "ByteOrder":
        return {
            "=": cls.NATIVE,
            "<": cls.LITTLE_ENDIAN,
            ">": cls.BIG_ENDIAN,
            "|": cls.NOT_APPLICABLE,
        }[np_order]


class DatasetMicroStructure(BaseModel):
    itemsize: int
    kind: str
    byte_order: ByteOrder = ByteOrder.NOT_APPLICABLE


class DatasetStructure(BaseModel):
    macro: DatasetMacroStructure
    micro: DatasetMicroStructure


class MetadataNode(BaseModel):
    name: str
    attributes: Mapping[str, Any]
    structure: Optional[DatasetStructure] = None


T = TypeVar("T")


class TreeMap(GenericModel, Generic[T]):
    name: str
    contents: T
    subnodes: List["TreeMap"]
