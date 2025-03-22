import math
import struct

INFOS_POSITION = 0x01
INFOS_LED = 0x02
INFOS_MOTORS = 0x04
INFOS_WHEELS = 0x08
INFOS_SPEED = 0x10
INFOS_RANGEFINDER = 0x20

def readInfos(data):
    """
    Returns a dict with the data detected in the buffer
    dict keys:
        xpos ypos angle
        led_r led_g led_b
        motor_left motor_right
        wheel_left wheel_right torque_left torque_right
        speed_w speed_v
        range
    """
    (mask, ) = struct.unpack(">B", data[:1])

    if (mask == INFOS_POSITION):
        position_x, position_y, position_a = struct.unpack(">xfff", data)

        finalX = round(position_x * 1000)
        finalY = round(position_y * 1000)
        rad = round(position_a * 180 / math.pi)
        print(f"posX: {finalX} mm, posY: {finalY} mm , posA: {rad} deg")
        return dict(xpos=finalX, ypos=finalY, angle=rad)
    elif (mask == INFOS_LED):
        led_r, led_g, led_b = struct.unpack(">xBBB", data)

        print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
        return dict(led_r=led_r, led_g=led_g, led_b=led_b)
    elif (mask & INFOS_MOTORS):
        ml, mr = struct.unpack(">xff", data)

        print(f"Motor left: {ml}, motor right: {mr}")
        return dict(motor_left=ml, motor_right=mr)
    elif (mask == INFOS_WHEELS):
        wl, wr, tl, tr = struct.unpack(">xHHHH", data)

        print(f"Wheel left: {wl}, tl: {tr}, wheel right: {wr}, tr: {tr} ")
        return dict(wheel_left=wl, wheel_right=wr, torque_left=tl, torque_right=tr)
    elif (mask == INFOS_SPEED):
        w, v = struct.unpack(">xff", data)

        print(f"Speed w: {w}, speed v: {v}")
        return dict(speed_w=w, speed_v=v)
    elif (mask == INFOS_RANGEFINDER):
        (rf,) = struct.unpack(">xH", data)

        print(f"Rangefinder: {rf} ")
        return dict(range=rf)
    else:
        raise ValueError(f"invalid mask: {mask}")
