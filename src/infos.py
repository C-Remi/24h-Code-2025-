from dataview import DataView
import math

INFO_POSITION = 0x01
INFO_LED = 0x02

def readInfos(data):

    out = {}

    try:
        view = DataView(data)
        pos = 0

        mask = view.get_uint_8(pos)
        pos += 1

        if (mask & INFO_POSITION):
            position_x = view.get_float_32(pos + 0)

            position_y = view.get_float_32(pos + 4)
            position_a = view.get_float_32(pos + 8)
            pos += 3*4

            out["x"] = position_x
            out["y"] = position_y
            out["a"] = position_a

            #print(f"posX: {round(position_x * 1000)} mm, posY: {round(position_y * 1000)} mm , posA: {round(position_a * 180 / math.pi) } deg")

        if (mask & INFO_LED):
            led_r = view.get_uint_8(pos + 0)
            led_g = view.get_uint_8(pos + 1)
            led_b = view.get_uint_8(pos + 2)
            pos += 3

            out["color_r"] = led_r
            out["color_g"] = led_g
            out["color_b"] = led_b

            #print(f"ledR: {led_r}, ledG: {led_g}, ledB: {led_b}")
    except:
        print('err')
        return None
    return out

