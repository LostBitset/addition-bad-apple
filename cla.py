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
    outputs = [
        f"sum {i}" for i in range(n_bits)
    ]
    carryless_adders = [
        NandInstance(
            carryless_fa,
            {"a": f"a {i}", "b": f"b {i}"},
            {
                "clsum": f"clsum {i}",
                "c prop": f"prop {i}:{i+1}",
                "c gen": f"gen {i}:{i+1}",
            },
        )
        for i in range(n_bits)
    ]
    gp_modules = []
    for level in range(1, n_levels + 1):
        step = 2 ** level
        for i in range(0, n_bits, step):
            bgn0, end0 = i, i + (step // 2)
            bgn1, end1 = i + (step // 2), i + step
            gp_modules.append(NandInstance(
                cla_gp,
                {
                    "gen h": f"gen {bgn1}:{end1}",
                    "prop h": f"prop {bgn1}:{end1}",
                    "gen l": f"gen {bgn0}:{end0}",
                    "prop l": f"prop {bgn0}:{end0}",
                },
                {
                    "gen hl": f"gen {bgn0}:{end1}",
                    "prop hl": f"prop {bgn0}:{end1}",
                },
            ))
    carry_modules = [
        SimpleBinding(f"carry 0:{n_bits}", False),
    ]
    for level in reversed(range(1, n_levels + 1)):
        step = 2 ** level
        for i in range(0, n_bits, step):
            bgn0, end0 = i, i + (step // 2)
            bgn1, end1 = i + (step // 2), i + step
            carry_modules.append(NandInstance(
                carry_unit,
                {
                    "c in": f"carry {bgn0}:{end1}",
                    "g in": f"gen {bgn0}:{end1}",
                    "p in": f"prop {bgn0}:{end1}",
                },
                {
                    "c h": f"carry {bgn1}:{end1}",
                    "c l": f"carry {bgn0}:{end0}",
                },
            ))
    carry_epilogues = [
        NandInstance(
            carry_epilogue,
            {"clsum": f"clsum {i}", "c in": f"carry {i}:{i+1}"},
            {"sum": f"sum {i}"},
        )
        for i in range(n_bits)
    ]
    return NandCircuit(
        inputs,
        outputs,
        [
            *carryless_adders,
            *gp_modules,
            *carry_modules,
            *carry_epilogues,
        ],
    )


