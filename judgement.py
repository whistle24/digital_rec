# 准确率判断
def res_judge():
    ans_pic = 0
    ans_num = 0
    res_pic = 0
    res_num = 0

    f = open("answer.txt", 'r')
    byt = f.readlines()
    answer = {}
    for ans in byt:
        if len(ans) > 2:
            ans_pic += 1
            ans_num += 28
            tmp = {}
            ans_daima = ans[:12]
            tmp['daima'] = ans_daima
            tmp['haoma'] = ans[14:22]
            tmp['date'] = ans[24:32]
            answer[ans_daima] = tmp

    f2 = open("result.txt", 'r')
    byt2 = f2.readlines()
    result = dict()
    for res in byt2:
        if len(res) > 2:
            res_tmp = {}
            res_filename = res[:12]
            res_tmp['daima'] = res[14:26]
            res_tmp['haoma'] = res[28:36]
            res_tmp['date'] = res[38:46]
            result[res_filename] = res_tmp
    count = 1
    text = ''
    for x in result:

        if x in answer:
            flag = 0
            if len(result[x]['daima'])==12:
                for i in range(12):

                    if result[x]['daima'][i] == answer[x]['daima'][i]:
                        res_num += 1
                    else:
                        flag = 1
            if len(result[x]['haoma']) == 8:
                for i in range(8):
                    if result[x]['haoma'][i] == answer[x]['haoma'][i]:
                        res_num += 1
                    else:
                        flag = 1
            if len(result[x]['date']) == 8:
                for i in range(8):
                    if result[x]['date'][i] == answer[x]['date'][i]:
                        res_num += 1
                    else:
                        flag = 1

            if flag == 0:
                res_pic += 1
                text += str(count) + '\n' + str(answer[x]) + '\n' + str(result[x]) + '\n' + '识别无误\n'
            else:
                flag = 0
                text += str(count) + '\n' + str(answer[x]) + '\n' + str(result[x]) + '\n' + '识别有误\n'
            count += 1
    text += '图像总数：' + str(ans_pic) + '    识别正确张数：' + str(res_pic) + '    准确率：' + str(
        res_pic / ans_pic) + '\n'
    text += '总数字数量：' + str(ans_num) + '    识别正确数量：' + str(res_num) + '    正确率：' + str(
        res_num / ans_num) + '\n'
    print(text)

    with open("judge.txt", "a", encoding='utf-8') as file:
        file.write(text)
