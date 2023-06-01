from placed_gates import PlacedGate

import numpy as np
import cv2

import sys

gates = None
with open(sys.argv[1], "r") as f:
    lines = f.readlines()
gates = [ PlacedGate(i.strip()) for i in lines ]

wires = []
net_positions = dict()
for i, gate in enumerate(gates):
    for j, net in enumerate([*gate.gate.inputs, *gate.gate.outputs]):
        if j >= len(gate.gate.inputs):
            loc = (i, True)
        else:
            loc = (i, False)
        if net in net_positions:
            new_wire = (net_positions[net], loc)
            wires.append(new_wire)
        net_positions[net] = loc

print(wires)

tot, pad = int(480 / 20), 5
sc = tot - pad

img = np.zeros((360, 480, 3), np.uint8)

for gate in gates:
    x, y = gate.x * (sc + pad), gate.y * (sc + pad)
    w, h = sc, sc
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Test", img)
cv2.waitKey(0)

