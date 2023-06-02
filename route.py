from placed_gates import PlacedGate

import numpy as np
import cv2

import math
import pickle as pkl
import random

def route_frame(frame):
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

        print(f"len(gates)={len(gates)}")

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

        img = cv2.imread(f"positioner/frames/BadApple_{frame}.jpg", 0)
        desired_ratio = 0.001
        desired_samples = int(desired_ratio * (img.sum() / 255))
        print(f"desired_samples = {desired_samples}")
        samples = []
        while len(samples) < desired_samples:
            x, y = random.randint(1, 480 - 1), random.randint(1, 360 - 1)
            if img[y, x] < 100:
                samples.append((x, y))
        print("got samples")

        def calc_angle(x1, y1, x2, y2):
            return math.atan2(y2 - y1, x2 - x1)

        def dist(x1, y1, x2, y2):
            sum_of_squares = ((x2 - x1) ** 2) + ((y2 - y1) ** 2)
            return sum_of_squares ** 0.5

        print("calculating forbidden angles...")
        forbidden_angles = [] # [[angle to sample]]
        # calculate forbidden angle ranges for each gate index
        for i, gate in enumerate(gates):
            forbidden_angles.append([])
            gy, gx = gate.x, gate.y
            for sx, sy in samples:
                forbidden_angles[i].append(
                    calc_angle(gx, gy, sx, sy)
                )
        print("done calculating")
        nf_angles = sum(map(len, forbidden_angles))
        print(f"nf_angles={nf_angles}")

        forbidden_ranges = [] # [[[lo, hi]]]
        adj_thresh = (20 / 360) * 2 * math.pi
        print("simplifying forbidden angles list (to ranges)...")
        for outer_i, ls in enumerate(forbidden_angles):
            forbidden_ranges.append([])
            ls.sort()
            last = None
            for i, angle in enumerate(ls):
                make_range = False
                if last is not None:
                    if (angle - last) < adj_thresh:
                        make_range = True
                last = angle
                if make_range:
                    forbidden_ranges[outer_i][-1][1] = angle + (adj_thresh / 2)
                else:
                    forbidden_ranges[outer_i].append([
                        angle - (adj_thresh / 2),
                        angle + (adj_thresh / 2),
                    ])
        nf_ranges = sum(map(len, forbidden_ranges))
        print("done simplifying")
        print(f"{nf_angles} angles -> {nf_ranges} ranges")
        print("ready to begin routing")

        forbidden_penalty = 200
        wires = []
        # route wires
        for positions in net_positions.values():
            st = positions[0]
            remaining = positions[1:] # slice creates a copy
            while len(remaining) != 0:
                distances = []
                st_gate_i, _, _ = st
                f_ranges = forbidden_ranges[st_gate_i]
                for pot_en_i, pot_en in enumerate(remaining):
                    # check to see if it in a forbidden range
                    en_gate_i, _, _ = pot_en
                    st_gate = gates[st_gate_i]
                    st_y, st_x = st_gate.x, st_gate.y
                    en_gate = gates[en_gate_i]
                    en_y, en_x = en_gate.x, en_gate.y
                    angle = calc_angle(st_x, st_y, en_x, en_y)
                    forbidden = False
                    for f_range in f_ranges:
                        [lo, hi] = f_range
                        if (angle > lo) and (angle < hi):
                            forbidden = True
                            break
                    # calculate distance +penalty
                    distance = dist(st_x, st_y, en_x, en_y)
                    if forbidden:
                        distance += forbidden_penalty
                    distances.append((pot_en_i, distance))
                # find the best option
                en_i, _ = min(distances, key=lambda x: x[1])
                # remove it from remaining
                en = remaining[en_i]
                del remaining[en_i]
                # add connection to wires
                wires.append((st, en))
                # set as next start
                st = en
        print("done routing")
        print(f"routed {len(wires)} wires")

        with open("out_routes/frame{frame}.route.pkl", "wb") as f:
            pkl.dump(wires, f)

