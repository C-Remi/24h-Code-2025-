import math
import struct

INFOS_POSITION = 0x01
INFOS_LED = 0x02
INFOS_MOTORS = 0x04
INFOS_WHEELS = 0x08
INFOS_SPEED = 0x10
INFOS_RANGEFINDER = 0x20

def readInfos(data):
    try:
        (mask, *rest) = struct.unpack(">B", data[:1])

        if (mask & INFOS_POSITION):
            position_x, position_y, position_a = struct.unpack(">xfff", data)

            finalX = round(position_x * 1000)
            finalY = round(position_y * 1000)
            rad = round(position_a * 180 / math.pi)
            print(f"posX: {finalX} mm, posY: {finalY} mm , posA: {rad} deg")
            return (True,(finalX, finalY, rad))

        elif (mask & INFOS_LED):            
            led_r, led_g, led_b = struct.unpack(">xBBB", data)

            print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
            return (True,(led_r, led_g, led_b))
        elif (mask & INFOS_MOTORS):
            ml, mr = struct.unpack(">xff", data)

            print(f"Motor left: {ml}, motor right: {mr}")
            return (True,(ml, mr))
        elif (mask & INFOS_WHEELS):
            wl, wr, tl, tr = struct.unpack(">xHHHH", data)

            print(f"Wheel left: {wl}, tl: {tr}, wheel right: {wr}, tr: {tr} ")
            return (True,(wl, wr, tl, tr))
        elif (mask & INFOS_SPEED):
            w, v = struct.unpack(">xff", data)

            print(f"Speed w: {w}, speed v: {v}")
            return (True,(w,v))
        elif (mask & INFOS_RANGEFINDER):
            rf = struct.unpack(">xH", data)

            print(f"Rangefinder: {rf} ")
            return(True,(rf))
        else:
            return (False,())
    except Exception as e:
        print('err')
        print(e)
        return (False,())


