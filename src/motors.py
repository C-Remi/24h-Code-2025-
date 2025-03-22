import struct

K_R = 0.9
K_L = 0.9

def motor_setpoint(compensation_factor):

    if compensation_factor is None:
        vl, vr = K_L, K_R
    else:
        vl = K_L - compensation_factor
        vr = K_R
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))

    vl, vr = 0.5, 0.5
    print(vl, vr)

    return struct.pack('ff', vl, vr)