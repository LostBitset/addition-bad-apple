import numpy as np
import cv2

import sys
frame = int(sys.argv[1])

input_file = f"out_placed/frame{frame}.placement.txt"
gates = None
with open(input_file, "r") as f:
    lines = f.readlines()
skipme = False
if "SKIPME" in [ line.strip() for line in lines ]:
    skipme = True
    print("skipping")
else:
    gates = [ PlacedGate(i.strip()) for i in lines ]

    net_positions = dict() # net index => [(gate index, output?, t)]
    for i, gate in enumerate(gates):
        for j, net in enumerate([*gate.gate.inputs, *gate.gate.outputs]):
            if j >= len(gate.gate.inputs):
                if len(gate.gate.outputs) > 1:
                    t = (j - len(gate.gate.inputs)) / (len(gate.gate.outputs) - 1)
                elif len(gate.gate.outputs) == 1:
                    t = 0.5
                else:
                    raise "uh oh"
                loc = (i, True, t)
            else:
                if len(gate.gate.inputs) > 1:
                    t = j / (len(gate.gate.inputs) - 1)
                elif len(gate.gate.inputs) == 1:
                    t = 0.5
                else:
                    raise "uh oh"
                loc = (i, False, t)
            if net not in net_positions:
                net_positions[net] = []
            net_positions[net].append(loc)

    forbidden_angles = dict() # gate index => [(start angle, end angle)]
    # TODO calculate forbidden angle ranges for each gate index

    wires = []
    # TODO route wires

