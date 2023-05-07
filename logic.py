from abc import ABC, abstractmethod
from dataclasses import dataclass
import typing as t

@dataclass
class Wire:
    name: str

@dataclass
class Pin:
    name: str

class Com(ABC):
    @property
    @abstractmethod
    def inputs(self) -> t.List[Pin]:
        raise NotImplementedError("method is abstract")

    @property
    @abstractmethod
    def outputs(self) -> t.List[Pin]:
        raise NotImplementedError("method is abstract")

    @abstractmethod
    def apply(self, inputs: t.Dict[Pin, bool]) -> t.Dict[Pin, bool]:
        raise NotImplementedError("method is abstract")

@dataclass
class Element:
    com: Com
    inputs: t.Dict[Pin, Wire]
    outputs: t.Dict[Wire, Pin]

