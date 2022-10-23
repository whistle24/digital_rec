import os
import formatNum
import cv2
import pretreat
import judgement

if __name__ == '__main__':
    address = r'C:\Users\35489\Desktop\src'
    for filename in os.listdir(address):
        if filename.endswith('jpg') or filename.endswith('jpeg') or filename.endswith('png'):
            print(filename+'识别中..........')
            with open(address + '\\' + filename, "rb") as f:
                image = f.read()
            src = cv2.imread(address + '\\' + filename, 1)
            if src is None:
                print(filename+'图片格式不符！')
                continue
            res = pretreat.treat(src)
            res = formatNum.adjust(image)
            filename = filename[:12]
            res = filename.ljust(14)+res
            with open("result.txt", "a") as file:
                file.write(res + "\n")
            cv2.waitKey(0)

    judgement.res_judge()

