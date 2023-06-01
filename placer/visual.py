from placed_gates import PlacedGate

import numpy as np
import cv2

import sys
import random

gates = None
with open(sys.argv[1], "r") as f:
    lines = f.readlines()
gates = [ PlacedGate(i.strip()) for i in lines ]

wires = []
net_positions = dict()
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
        if net in net_positions:
            new_wire = (net_positions[net], loc)
            wires.append(new_wire)
        net_positions[net] = loc

print(wires)

tot, pad = 10, 5
sc = tot - pad

def port_position(port, posmap):
    (i, is_output, t) = port
    (tlx, tly) = posmap[i]
    if is_output:
        return (tlx, tly + int(t * sc))
    else:
        return (tlx + sc, tly + int(t * sc))

img = np.zeros((360, 480, 3), np.uint8)

gate_positions = []

for gate in gates:
    x, y = gate.x * (sc + pad), gate.y * (sc + pad)
    w, h = sc, sc
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    gate_positions.append((x, y))

for wire in wires:
    (a, b) = wire
    a_pos = port_position(a, gate_positions)
    b_pos = port_position(b, gate_positions)
    cv2.line(img, a_pos, b_pos, (0, 0, 255), 1)

translate = np.float32([[1, 0, (pad // 2)], [0, 1, (pad // 2)]])
img = cv2.warpAffine(img, translate, (img.shape[1], img.shape[0]))

cv2.imshow("Test", img)
cv2.waitKey(0)

