from nandlogic import Var

import typing as t

def to_binary(n: int, width: int) -> t.List[bool]:
    curr = n
    result = []
    for i in range(width - 1, -1, -1):
        pos = 2 ** i
        should_set = curr >= pos
        if should_set:
            curr -= pos
        result.append(should_set)
    return list(reversed(result))

def make_adder_inputs(a_int: int, b_int: int, width: int) -> t.Dict[Var, bool]:
    return {
        *{ f"a {i}": v for i, v in enumerate(to_binary(a_int, width)) },
        *{ f"b {i}": v for i, v in enumerate(to_binary(b_int, width)) },
    }

