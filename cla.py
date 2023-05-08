from nandlogic import NandCircuit, NandInstance
from nandlogic_std import and_g, or_g, xor_g

# Citation: https://www.youtube.com/watch?v=i1tUBZLWD3o

partial_fa = NandCircuit(
    ["a", "b", "c in"],
    ["sum", "c prop", "c gen"],
    [
        NandInstance(xor_g, {"a": "a", "b": "b"}, {"q": "sum carryless"}),
        NandInstance(xor_g, {"a": "sum carryless", "b": "c in"}, {"q": "sum"}),
        NandInstance(or_g, {"a": "a", "b": "b"}, {"q": "c prop"}),
        NandInstance(and_g, {"a": "a", "b": "b"}, {"q": "c gen"}),
    ],
)

cla_gp = NandCircuit(
    ["gen h", "prop h", "gen l", "prop l"],
    ["gen hl", "prop hl"],
    [
        NandInstance(and_g, {"a": "prop h", "b": "gen l"}, {"q": "from l"}),
        NandInstance(or_g, {"a": "gen h", "b": "from l"}, {"q": "gen hl"}),
        NandInstance(and_g, {"a": "prop h", "b": "prop l"}, {"q": "prop hl"}),
    ],
)

