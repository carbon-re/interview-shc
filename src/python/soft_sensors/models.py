from dataclasses import dataclass
from typing import TypeVar

T = TypeVar("T")
E = TypeVar("E")


@dataclass(frozen=True)
class Ok(T):
    value: T


@dataclass(frozen=True)
class Fail(E):
    value: E
