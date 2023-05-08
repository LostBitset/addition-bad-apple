from nandlogic import NandCircuit, NandInstance, SimpleBinding
from nandlogic_std import and_g, or_g, xor_g

# Citation: https://www.youtube.com/watch?v=i1tUBZLWD3o

carryless_fa = NandCircuit(
    ["a", "b"],
    ["clsum", "c prop", "c gen"],
    [
        NandInstance(xor_g, {"a": "a", "b": "b"}, {"q": "clsum"}),
        NandInstance(or_g, {"a": "a", "b": "b"}, {"q": "c prop"}),
        NandInstance(and_g, {"a": "a", "b": "b"}, {"q": "c gen"}),
    ],
)

carry_epilogue = NandCircuit(
    ["clsum", "c in"],
    ["sum"],
    [
        NandInstance(xor_g, {"a": "clsum", "b": "c in"}, {"q": "sum"}),
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

carry_unit = NandCircuit(
    ["c in", "g in", "p in"],
    ["c h", "c l"],
    [
        NandInstance(and_g, {"a": "p in", "b": "c in"}, {"q": "c prop"}),
        NandInstance(or_g, {"a": "g in", "b": "c prop"}, {"q": "c h"}),
        SimpleBinding("c l", "c in"),
    ],
)

def carry_lookahead_adder(n_levels):
    n_bits = 2 ** n_levels
    inputs = [
        *( f"a {i}" for i in range(n_bits) ),
        *( f"b {i}" for i in range(n_bits) ),
    ]
    carryless_adders = [
        NandInstance(
            carryless_fa,
            {"a": f"a {i}", "b": f"b {i}"},
            {
                "clsum": f"clsum {i}",
                "c prop": f"prop {i}",
                "c gen": f"prop {i}",
            },
        )
        for i in range(n_bits)
    ]

