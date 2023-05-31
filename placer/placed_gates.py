from dataclasses import dataclass
import typing as t

@dataclass
class Gate:
    name: str
    inputs: t.List[int]
    outputs: t.List[int]

    def __init__(self, text):
        parts = text.split(" ")
        self.name = parts[0]
        inputs, outputs = [], []
        before = True
        for i in parts[1:]:
            if i == "~>":
                before = False
                continue
            if before:
                inputs.append(int(i))
            else:
                outputs.append(int(i))
        self.inputs = inputs
        self.outputs = outputs

@dataclass
class PlacedGate:
    x: int
    y: int
    gate: Gate

    def __init__(self, text):
        [gate, xy] = text.split("@")
        gate = gate.strip()
        [x, y] = xy.strip().split(",")
        self.gate = Gate(gate)
        self.x, self.y = x, y

