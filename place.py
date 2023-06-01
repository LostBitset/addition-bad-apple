from nandlogic import NandNetlist, NandOp
from serialize_netlists import serialize_netlist

from positioner.positions import get_positions

import pickle as pkl
import sys

def place_frame(frame):
    netlists = None
    with open("netlists.pkl", "rb") as f:
        netlists = pkl.load(f)

    result, gates = None, None
    for levels in [*range(6, 0, -1), 7, 8]:
        gates = netlists[levels]
        result = get_positions(frame, len(gates), "positioner/frames")
        if result is not None:
            break

    if (result is None) or (result == []):
        ser = "SKIPME"
    else:
        netlist_lines = serialize_netlist(
            NandNetlist(gates)
        ).split("\n")

        lines = []
        for i, op in enumerate(netlist_lines):
            (x, y) = result[i]
            lines.append(f"{op} @ {x},{y}")

        ser = "\n".join(lines)

    with open(f"out_placed/frame{frame}.placement.txt", "w") as f:
        f.write(ser)

