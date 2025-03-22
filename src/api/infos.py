import math

INFOS_POSITION = 0x01
INFOS_LED = 0x02
INFOS_MOTORS = 0x04
INFOS_WHEELS = 0x08
INFOS_SPEED = 0x10
INFOS_RANGEFINDER = 0x20

def readInfosPos(data):
    try:
        mask = struct.unpack(">B", data[:1])

        if (mask & INFOS_POSITION):
            position_x, position_y, position_a = struct.unpack(">xfff", data)

            finalX = round(position_x * 1000)
            finalY = round(position_y * 1000)
            rad = round(position_a * 180 / math.pi)
            print(f"posX: {finalX} mm, posY: {finalY} mm , posA: {rad} deg")
            return((finalX, finalY, rad))
    except:
        print('err')

def readInfosLed(data):
    try:
        mask = struct.unpack(">B", data[:1])

        if (mask & INFOS_LED):
            led_r, led_g, led_b = struct.unpack(">Bcc", data)

            print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
            return((led_r, led_g, led_b))
        else:
            raise ValueError
    except:
        print('err')
        raise

def readInfosMotors(data):
    try:

        mask = struct.unpack(">B", data[:1])

        if (mask & INFOS_MOTORS):
            ml, mr = struct.unpack(">xff", data)

            print(f"Motor left: {ml}, motor right: {mr}")
            return((ml, mr))
        else:
            raise ValueError
    except:
        print('err')
        raise

def readInfosWheels(data):
    try:

        mask = struct.unpack(">B", data[:1])
        pos += 1

        if (mask & INFOS_WHEELS):
            wl, wr, tl, tr = struct.unpack(">xHHH", data)

            pos += 4*2

            print(f"Wheel left: {wl}, tl: {tr}, wheel right: {wr}, tr: {tr} ")
            return((wl, wr, tl, tr))
        else:
            raise ValueError
    except:
        print('err')
        raise

def readInfosSpeed(data):
    try:
        mask = struct.unpack(">B", data[:1])

        if (mask & INFOS_SPEED):
            w, v = struct.unpack(">xff", data)

            print(f"Speed w: {w}, speed v: {v}")
            return((w,v))
        else:
            raise ValueError
    except:
        print('err')
        raise

def readInfosRangefinder(data):
    try:
        mask = struct.unpack(">B", data[:1])

        if (mask & INFOS_RANGEFINDER):
            rf = struct.unpack(">xH", data)

            print(f"Rangefinder: {rf} ")
            return(rf)
        else:
            raise ValueError
    except:
        print('err')
        raise


def readInfos(data):
    try:
        readInfosLed(data)
        readInfosPos(data)
        readInfosMotors(data)
        readInfosWheels(data)
        readInfosSpeed(data)
        readInfosRangefinder(data)
    except:
        print('err')

