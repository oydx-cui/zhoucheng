from PyQt5.QtGui import QColor

red_ = QColor(255, 0, 0)
blue_ = QColor(0, 0, 255)
green_ = QColor(0, 255, 0)
purple_ = QColor(255, 0, 255)
yellow_ = QColor(218,165,32)


def translate_pos(pos):
    textt = ""
    if pos == 0:
        textt = "滚珠"
    elif pos == 1:
        textt = "内圈"
    elif pos == 2:
        textt = "外圈，3点钟方向"
    elif pos == 3:
        textt = "外圈，6点钟方向"
    elif pos == 4:
        textt = "外圈，12点钟方向"
    return textt


def show_size(size):
    textt = ""
    if size == 0:
        textt = ''
    elif size == 1:
        textt = "7 mils"
    elif size == 2:
        textt = "14 mils"
    elif size == 3:
        textt = "21 mils"
    return textt


def show_color(pos):
    color_ = red_
    if pos == 1:
        color_ = blue_
    elif pos == 2:
        color_ = green_
    elif pos == 3:
        color_ = purple_
    return color_


def show_color_rul(pos):
    if 0.0 < pos <= 50.0:
        return red_
    elif 50.0 < pos <= 100.0:
        return yellow_
    else:
        return green_


def show_color_rul_text(pos):
    if 0.0 < pos <= 50.0:
        return "异常（需要更换）"
    elif 50.0 < pos <= 100.0:
        return "缺陷（需要定期排查）"
    else:
        return "健康（可使用时间充足）"

