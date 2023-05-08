from nandlogic import Var

import typing as t

def to_binary(n: int, width: int) -> t.List[bool]:
    string = bin(n)
    result = [ False for _ in range(width) ]
    for i, c in enumerate(reversed(string)):
        if c == "b":
            break
        elif c == "1":
            result[i] = True
    return result

def make_adder_inputs(a_int: int, b_int: int, width: int) -> t.Dict[Var, bool]:
    return {
        **{ f"a {i}": v for i, v in enumerate(to_binary(a_int, width)) },
        **{ f"b {i}": v for i, v in enumerate(to_binary(b_int, width)) },
    }

