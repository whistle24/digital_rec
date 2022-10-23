import cv2
import numpy as np


def getPixelSum(img):
    sum = 0
    img_array = np.array(img)
    shape = img_array.shape
    for i in range(shape[0]):
        for j in range(shape[1]):
            sum += img_array[i, j]
    return sum


def rec(img):
    min = 10e5
    for i in range(21):
        model = cv2.imread(r'C:\Users\35489\Desktop\nums\\' + str(i) + ".jpg", -1)
        model = cv2.resize(model, (32, 48), 0, 0, cv2.INTER_LINEAR)
        pic = cv2.resize(model, (32, 48), 0, 0, cv2.INTER_LINEAR)
        diffImg = cv2.absdiff(pic, model)
        sum = getPixelSum(diffImg)
        if sum < min:
            min = sum
    if min > 9:
        return ''
    return str(min)
