from utils.dataview import DataView
import math

INFOS_POSITION = 0x01
INFOS_LED = 0x02
INFOS_MOTORS = 0x04
INFOS_WHEELS = 0x08
INFOS_SPEED = 0x10
INFOS_RANGEFINDER = 0x20

def readInfosPos(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_POSITION):
            position_x = view.get_float_32(pos + 0)
            
            position_y = view.get_float_32(pos + 4)
            position_a = view.get_float_32(pos + 8)
            pos += 3*4

            finalX = round(position_x * 1000)
            finalY = round(position_y * 1000)
            rad = round(position_a * 180 / math.pi)
            print(f"posX: {finalX} mm, posY: {finalY} mm , posA: {rad} deg")
            return((finalX, finalY, rad))
    except:
        print('err')
        
def readInfosLed(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_LED):
            led_r = view.get_uint_8(pos + 0)
            led_g = view.get_uint_8(pos + 1)
            led_b = view.get_uint_8(pos + 2)
            pos += 3

            print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
            return((led_r, led_g, led_b))
    except:
        print('err')
    
def readInfosMotors(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_MOTORS):
            ml = view.get_float_32(pos + 0)
            mr = view.get_float_32(pos + 4)
            pos += 2*4

            print(f"Motor left: {ml}, motor right: {mr}")
            return((ml, mr))
    except:
        print('err')

def readInfosWheels(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_WHEELS):
            wl = view.get_uint_16(pos + 0)
            wr = view.get_uint_16(pos + 2)
            tl = view.get_uint_16(pos + 4)
            tr = view.get_uint_16(pos + 6)
            pos += 4*2

            print(f"Wheel left: {wl}, tl: {tr}, wheel right: {wr}, tr: {tr} ")
            return((wl, wr, tl, tr))
    except:
        print('err')

def readInfosSpeed(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_SPEED):
            w = view.get_float_32(pos + 0)
            v = view.get_float_32(pos + 4)
            pos += 4*2

            print(f"Speed w: {w}, speed v: {v}")
            return((w,v))
    except:
        print('err')
        
def readInfosRangefinder(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_RANGEFINDER):
            rf = view.get_uint_16(pos + 0)
            pos += 2

            print(f"Rangefinder: {rf} ")
            return(rf)
    except:
        print('err')
        

def readInfos(data):
    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFOS_POSITION):
            position_x = view.get_float_32(pos + 0)
            
            position_y = view.get_float_32(pos + 4)
            position_a = view.get_float_32(pos + 8)
            pos += 3*4

            print(f"posX: {round(position_x * 1000)} mm, posY: {round(position_y * 1000)} mm , posA: {round(position_a * 180 / math.pi) } deg")    

        if (mask & INFOS_LED):
            led_r = view.get_uint_8(pos + 0)
            led_g = view.get_uint_8(pos + 1)
            led_b = view.get_uint_8(pos + 2)
            pos += 3

            print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
    except:
        print('err')
    
