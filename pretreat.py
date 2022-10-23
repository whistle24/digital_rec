import cv2
import numpy as np
import rotate
import recognize


# 整体形态学处理
def morphTreat_all(img):
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 1))
    res = cv2.erode(img, element)
    res = cv2.erode(res, element)
    res = cv2.erode(res, element)
    res = cv2.erode(res, element)
    res = cv2.erode(res, element)
    return res


# 局部形态学处理
def morphTreat(img):
    element = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 3))

    res = cv2.erode(img, element)
    res = cv2.erode(res, element)
    res = cv2.dilate(res, element)
    res = cv2.dilate(res, element)
    return res


# 区域定位
def findY(img):
    for x in range(img.shape[0]):  # 图片的高
        num = 0
        for y in range(img.shape[1]):  # 图片的宽
            px = img[x, y]
            if (px == 0):
                num = num + 1
        if (num / img.shape[1] > 0.7):
            return x
    return img.shape[0]


# 颜色反转
def colorReverse(img):
    res = img
    for x in range(res.shape[0]):  # 图片的高
        for y in range(res.shape[1]):  # 图片的宽
            px = img[x, y]
            img[x, y] = 255 - px
    return res

# 数字位置排序
def contours_sort(contours_num):
    c_num = []
    for cnt_num in contours_num:
        [x_num, y_num, w_num, h_num] = cv2.boundingRect(cnt_num)
        if h_num > 5 and w_num < 20:
            tmp = {'x_num': x_num, 'y_num': y_num, 'w_num': w_num, 'h_num': h_num}
            c_num.append(tmp)
    ans = sorted(c_num, key=lambda x: x['x_num'])
    return ans


def treat(src):
    image = src
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 图像矫正
    gray = rotate.shape_correction(gray)
    retval, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    mid = morphTreat_all(binary)
    contours, hierarchy = cv2.findContours(mid, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    topY = findY(binary)
    daima = ''
    haoma = ''
    date = ''
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        # 筛选需识别的区域
        if h > 10 and h < 30 and w / h > 5 and w / h < 17 and y + h < topY and x > src.shape[1] * 0.6:
            # cv2.rectangle(src, (x, y), (x + w, y + h), (0, 0, 255), 1)
            block = binary[y:(y + h), x:(x + w)]
            block = morphTreat(block)
            block_reverse = colorReverse(block)
            # cv2.imshow('mmm', block_reverse)
            contours_num, hierarchy_num = cv2.findContours(block_reverse, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            # print(contours_num)
            contours_num_sorted = contours_sort(contours_num)
            for cnt_num in contours_num_sorted:
                x_num = cnt_num['x_num']
                y_num = cnt_num['y_num']
                w_num = cnt_num['w_num']
                h_num = cnt_num['h_num']
                cv2.rectangle(src, (x + x_num, y + y_num), (x + x_num + w_num, y + y_num + h_num), (0, 0, 255), 1)
                num_block = block_reverse[y_num:(y_num + h_num), x_num:(x_num + w_num)]
                # cv2.imshow('mmm', num_block)
                num = recognize.rec(num_block)
                if w / h > 12:
                    date = date + num
                elif w / h > 10:
                    daima = daima + num
                else:
                    haoma = haoma + num

    ans = daima.ljust(14) + haoma.ljust(10) + date

    cv2.imshow('mmm', src)
    return ans
