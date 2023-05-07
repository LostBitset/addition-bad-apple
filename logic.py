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
class Inst:
    com: Com
    inputs: t.Dict[Pin, Wire]
    outputs: t.Dict[Wire, Pin]

@dataclass
class Block(Com):
    circuit: "Circuit"
    input_bindings: t.Dict[Pin, Wire]
    output_bindings: t.Dict[Pin, Wire]

    @property
    def inputs(self) -> t.List[Pin]:
        return list(self.input_bindings.keys())

    @property
    def outputs(self) -> t.List[Pin]:
        return list(self.output_bindings.keys())

    def apply(self, inputs: t.Dict[Pin, bool]) -> t.Dict[Pin, bool]:
        setup = self.circuit.run_with({
            self.input_bindings[pin]: value
            for pin, value in inputs.items()
        })
        return {
            pin: setup.probe(wire)
            for pin, wire in self.output_bindings.items()
        }

class Circuit:
    def __init__(self, insts: t.List[Inst]):
        self.provider_index = {
            out_wire: inst
            for inst in insts
            for out_wire in inst.outputs.keys()
        }

    def run_with(self, set_wires: t.Dict[Wire, bool]) -> "CircuitSetup":
        return CircuitSetup(self.insts, set_wires)

@dataclass
class CircuitSetup:
    circuit: Circuit
    set_wires: t.Dict[Wire, bool]

    def probe(self, wire: Wire) -> bool:
        # TODO
        pass

