import struct

def motor_setpoint(compensation_factor):

    print('motor_setpoint')

    if compensation_factor is None:
        vl, vr = 1, 1
    else:
        vl = 0.5 - compensation_factor
        vr = 0.5
        vl = max(-1, min(vl, 1))
        vr = max(-1, min(vr, 1))

    print(vl, vr)

    return struct.pack('ff', vl, vr)