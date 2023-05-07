from logic import *

from dataclasses import dataclass
import typing as t

@dataclass
class And(Com):
    @property
    def inputs(self) -> t.List[Pin]:
        return [Pin("a"), Pin("b")]

    @property
    def outputs(self) -> t.List[Pin]:
        return [Pin("q")]

    def apply(self, inputs: t.Dict[Pin, bool]) -> t.Dict[Pin, bool]:
        return {
            Pin("q"): inputs[Pin("a")] or inputs[Pin("b")]
        }

