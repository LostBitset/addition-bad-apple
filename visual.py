from placed_gates import PlacedGate

import numpy as np
import cv2

import sys
import random

def make_visual(frame, asframe=None):
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

        print(f"{len(gates)} gates, {len(wires)} wires")

    pad = 5
    sc = 10

    def port_position(port, posmap):
        (i, is_output, t) = port
        (tlx, tly) = posmap[i]
        if is_output:
            return (tlx, tly + int(t * sc))
        else:
            return (tlx + sc, tly + int(t * sc))

    def adj():
        upad = pad // 2
        return random.randint(-upad + 1, upad)

    img = np.zeros((360, 480, 3), np.uint8)

    if not skipme:
        gate_positions = [ (gate.y + adj(), gate.x + adj()) for gate in gates ]

        def draw_wires():
            print("Drawing wires...")

            for wire in wires:
                (a, b) = wire
                a_pos = port_position(a, gate_positions)
                b_pos = port_position(b, gate_positions)
                cv2.line(img, a_pos, b_pos, (0, 0, 255), 1)

        def draw_gates():
            print("Drawing gates...")

            for (x, y) in gate_positions:
                w, h = sc, sc
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        draw_gates()
        draw_wires()

        print("Correcting...")

        translate = np.float32([[1, 0, (pad // 2)], [0, 1, (pad // 2)]])
        img = cv2.warpAffine(img, translate, (img.shape[1], img.shape[0]))

        print("Image creation complete.")

    if skipme:
        prevframe = frame - 1
        if prevframe != 0 and frame < 6516:
            if asframe is None:
                make_visual(prevframe, frame)
                return
            else:
                make_visual(prevframe, asframe)
                return
        else:
            print("FRAME MUST BE EMPTY")

    if asframe is None:
        savepath = f"outframes/AddApple_{frame}.jpg"
    else:
        savepath = f"outframes/AddApple_{asframe}.jpg"
    print(f"Saving as {savepath}")

    cv2.imwrite(savepath, img)

