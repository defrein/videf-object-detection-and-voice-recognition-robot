import numpy as np

lower_color = None
upper_color = None


def whichColor(color_data):
    global lower_color, upper_color
    if color_data == "hijau":
        lower_color = np.array([40, 86, 6])
        upper_color = np.array([64, 255, 255])
    elif color_data == "kuning":
        lower_color = np.array([25, 80, 30])
        upper_color = np.array([35, 255, 255])
    elif color_data == "jingga" or color_data == "orange":
        lower_color = np.array([0, 120, 50])
        upper_color = np.array([20, 255, 255])
    elif color_data == "ungu":
        lower_color = np.array([110, 86, 36])
        upper_color = np.array([140, 255, 255])
    elif color_data == "merah muda":
        lower_color = np.array([150, 86, 36])
        upper_color = np.array([170, 255, 255])
    elif color_data == "merah":
        lower_color = np.array([160, 150, 30])
        upper_color = np.array([190, 255, 255])
    elif color_data == "biru":
        lower_color = np.array([100, 100, 60])
        upper_color = np.array([140, 255, 255])
    else:
        lower_color = None
        upper_color = None

    return lower_color, upper_color
