# 图像矫正
import numpy as np
import cv2 as cv


def shape_correction(img):
    (height, width) = img.shape[:2]
    # print(img.shape)
    img_gau = cv.GaussianBlur(img, (5, 5), 0)
    canny = cv.Canny(img_gau, 60, 200)
    kernel = cv.getStructuringElement(cv.MORPH_CROSS, (4, 3))
    dilated = cv.dilate(canny, kernel, iterations=8)
    # 寻找轮廓
    contours, hierarchy = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # 找到最外层面积最大的轮廓
    area = 0
    index = 0
    for i in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[i])
        # 排除非文本区域
        if w < 35 and h < 35:
            continue
        # 防止矩形区域过大不精准
        if h > 0.99 * height or w > 0.99 * width:
            continue
        tmpArea = w * h
        if tmpArea >= area:
            area = tmpArea
            index = i

    # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    rect = cv.minAreaRect(contours[index])
    angle = rect[-1]
    # 角度大于85度或小于5度不矫正
    if angle > 85 or angle < 5:
        angle = 0
    elif angle < 45:
        angle = angle - 0
    else:
        angle = angle - 90
    M = cv.getRotationMatrix2D(rect[0], angle, 1)
    # 填补空白区域
    rotated = cv.warpAffine(img, M, (width, height), flags=cv.INTER_CUBIC, borderValue=(255, 255, 255))
    return rotated

