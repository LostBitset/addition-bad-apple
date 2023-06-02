from placed_gates import PlacedGate

import numpy as np
import cv2

import sys
import random
import pickle as pkl

sf = 2

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

        wires = None
        with open(f"out_routes/frame{frame}.route.pkl", "rb") as f:
            wires = pkl.load(f)

        print(f"{len(gates)} gates, {len(wires)} wires")

    pad = 2
    sc = 3

    def port_position(port, posmap):
        (i, is_output, t) = port
        (tlx, tly) = posmap[i]
        if is_output:
            return (tlx, tly + int(t * sc))
        else:
            return (tlx + sc, tly + int(t * sc))

    def adj():
        return 0
        #upad = pad // 2
        #return random.randint(-upad, upad + 1)

    img = np.zeros((360 * sf, 480 * sf, 3), np.uint8)

    if not skipme:
        gate_positions = [ (gate.y + adj(), gate.x + adj()) for gate in gates ]
        gate_positions = [ (x * sf, y * sf) for (x, y) in gate_positions ]

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
                w, h = sc * sf, sc * sf
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

