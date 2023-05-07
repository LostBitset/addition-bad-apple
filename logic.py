from abc import ABC, abstractmethod
from dataclasses import dataclass
import typing as t

PinName = str
WireName = str

class Component(ABC):
    @property
    @abstractmethod
    def pin_names():
        raise NotImplementedError("@abstractmethod")

    @abstractmethod
    def apply(pins: t.Dict[PinName, bool]):
        raise NotImplementedError("@abstractmethod")

@dataclass
class Connected:
    com: Component
    pins: t.Dict[WireName, PinName]

@dataclass
class Block(Component):
    circuit: "Circuit"
    pins: t.Dict[PinName, WireName]

@dataclass
class Circuit:
    elements: t.List[Connected]

