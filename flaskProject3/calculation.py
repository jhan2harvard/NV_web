import math
import numpy as np
from math import radians, sin, cos, tan
from scipy.integrate import quad
import matplotlib.pyplot as plt

Window_types = ["Hopper", "Awing", "Casement"]

Window_type = Window_types[2]
Open_dir = "right"  # Just for Casement
Wall_dir = 180
Wind_angle = 150
Wind_velo = 10
Cp = 0.8
Opening_angle = 30

W_width = 1
W_height = 1
W_elev = 10

def WI_angle(Wind_angle, Wall_dir):
    WI_angle = Wall_dir - Wind_angle
    if WI_angle < 0:
        WI_angle = 360 - abs(WI_angle)
    return WI_angle

def Single_sided_Q(Window_type, Wind_velo, Cp,Opening_angle, W_width, W_height, W_elev):

    if Window_type == "Hopper":
        Cd_H = min((0.92 / 0.62) * ((math.sin(math.radians(Opening_angle)) / 2) ** 0.5), 1)
        a = quad(lambda x: (x ** (2 / 7) - (W_elev + W_height / 2) ** (2 / 7)) ** 0.5, (W_elev + W_height / 2),
                 (W_elev + W_height))[0]
        Q = (Cd_H * 0.62 * W_width * abs(Cp) ** 0.5 * a) / (10 ** (1 / 7)) * Wind_velo
    elif Window_type == "Awing":
        h_1 = W_height - cos(radians(Opening_angle)) * W_height
        w_2 = W_height * sin(radians(Opening_angle))
        Z_01 = W_elev + h_1 / 2
        Z_02 = W_elev + h_1 + (W_height - h_1) / 2
        a = quad(lambda x: (x ** (2 / 7) - Z_01 ** (2 / 7)) ** 0.5, Z_01, W_elev + h_1)[0]
        b = quad(lambda x: (x ** (2 / 7) - Z_02 ** (2 / 7)) ** 0.5, Z_02, W_elev + W_height)[0]
        Q1 = 0.62 * W_width * abs(Cp) ** 0.5 * a * Wind_velo / (10 ** (1 / 7))
        Q2 = (1 - 0.5 * abs(cos(radians(WI_angle())))) / 2 * (W_width / (W_width + w_2 / 2)) * 0.62 * w_2 * abs(
            Cp) ** 0.5 * b * Wind_velo / (10 ** (1 / 7))
        Q = Q1 + Q2
    elif Window_type == "Casement":
        Open_dir = "right"
        if Open_dir == "right":
            if WI_angle() <= 90 and WI_angle() >= 0:
                c = 1
            else:
                c = 0.5
        elif Open_dir == "left":
            if WI_angle() < 360 and WI_angle() >= 270:
                c = 1
            else:
                c = 0.5
        a = quad(lambda x: (x ** (2 / 7) - (W_elev + W_height / 2) ** (2 / 7)) ** 0.5, (W_elev + W_height / 2),
                 (W_elev + W_height))[0]
        Q1 = 0.62 * min(1, (1 - cos(radians(Opening_angle)))) * W_width * abs(Cp) ** 0.5 * a * Wind_velo / (10 ** (1 / 7))
        Q2 = c * abs(sin(radians(WI_angle()))) * cos(radians(Opening_angle / 2)) * 0.62 * W_width * sin(
            radians(Opening_angle)) * abs(Cp) ** 0.5 * a * Wind_velo / (10 ** (1 / 7))
        Q = Q1 + Q2

    return Q