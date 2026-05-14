from PIL import ImageFont
myFont = ImageFont.truetype('STZHONGS.TTF', 50)


def labelling(a, x, y, z, times):
    if labelling_Order1(y) == '':
        return
    textt = labelling_Order1(y) + " " + z
    if x == 0:
        a.rectangle(((740, 205), (875, 335)), fill=None, outline=(255, 0, 0), width=6)  # 滚珠
        a.text((765, 140 - times[x] * 55), textt, font=myFont, fill=(255, 0, 0))
        times[x] += 1
    elif x == 1:
        a.ellipse([(243, 225), (852, 832)], fill=None, outline=(0, 0, 255), width=10)  # 内圈
        a.text((380, 285 + times[x] * 55), textt, font=myFont, fill=(0, 0, 255))
        times[x] += 1
    elif x == 2:
        a.rectangle(((945, 472), (1030, 590)), fill=None, outline=(0, 255, 0), width=6)  # 3点钟外圈
        a.text((770, 590 + 55 * times[x]), textt, font=myFont, fill=(0, 255, 0))
        times[x] += 1
    elif x == 3:
        a.rectangle(((485, 928), (610, 1005)), fill=None, outline=(255, 0, 255), width=6)  # 6点钟外圈
        a.text((630, 830 + times[x] * 55), textt, font=myFont, fill=(255, 0, 255))
        times[x] += 1
    elif x == 4:
        a.rectangle(((485, 50), (610, 140)), fill=None, outline='red', width=6)  # 12点钟外圈（实际无）
        a.text((155, 25 + times[x] * 50), textt, font=myFont, fill=(255, 0, 0))
        times[x] += 1
    else:
        return


def labelling_Order1(x):
    text = ''
    if x == 0:
        text = ''
    elif x == 1:
        text = "7 mils,"
    elif x == 2:
        text = "14 mils,"
    elif x == 3:
        text = "21 mils,"
    return text

