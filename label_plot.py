
#!/usr/bin/env python
#coding:utf-8
# plot sushi count in training/testing images

"""
TODO:
1. OK remove sushi count == 0
2. OK plot clean sushi chart
3. add argument into command
"""

import matplotlib.font_manager
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
# print(mpl.__file__)
# print(mpl.get_cachedir())
# mpl.rcParams[u'font.sans-serif'] = ['Noto Sans CJK JP']

# # mpl.rcParams['axes.unicode_minus'] = False
# print(mpl.matplotlib_fname())
# exit()
PLOT= False
SUSHI_NUM = {0: '牡\n丹\n蝦', 1: '玉\n子', 2: '煙\n燻\n櫻\n桃\n鴨', 3: '洋\n蔥\n鮭\n魚', 4: '漬\n鯖\n魚', 5: '鮪\n魚', 6: '鮭\n魚', 7: '花\n枝', 8: '日\n本\n真\n鱸', 9: '鮭\n魚\n腹', 10: '海\n鱺', 11: '辛\n醬\n鮪\n魚', 12: '海\n老', 13: '北\n寄\n貝', 14: '紅\n甘', 15: '日\n本\n青\n甘', 61: '甜\n蝦', 17: '干\n貝', 18: '日\n本\n大\n腹', 19: '鹽\n之\n花\n炙\n干\n貝', 20: '黑\n松\n露\n杏\n胞\n菇', 21: '比\n目\n魚\n緣\n側', 22: '炙\n合\n鴨', 23: '炙\n燒\n鮭\n魚', 24: '鹽\n之\n花\nP\nr\ni\nm\ne\n牛\n小\n排', 25: '辛\n味\n噌\nP\nr\ni\nm\ne\n牛\n小\n排', 26: '炙\n黑\n鰈', 27: '香\n柚\n焦\n糖\n鮭\n魚', 28: '明\n太\n子\n花\n枝', 29: '明\n太\n子\n炙\n鮭\n魚', 30: '蒜\n香\n牛\n肉', 31: '鹽\n之\n金\n蟹\n肉\n手\n捲', 49: '蘆\n筍\n蝦\n手\n捲', 50: '花\n炙\n海\n鱺', 32: '明\n太\n子\n海\n老', 33: '穴\n子\n(\n星\n鰻\n)', 34: '鰻\n魚', 35: '鹽\n之\n花\n炙\n和\n牛', 36: '雙\n拼\n生\n魚\n片', 37: '綜\n合\n生\n魚\n片', 38: '盛\n合\n生\n魚\n片', 39: '稻\n禾\n壽\n司', 40: '太\n捲', 41: '蘆\n筍\n手\n捲', 42: '納\n豆\n細\n捲', 43: '甘\n瓢\n細\n捲', 44: '鐵\n火\n捲', 45: '花\n壽\n司', 46: '鮪\n魚\n蔥\n花\n捲', 47: '龍\n蝦\n沙\n拉\n手\n捲', 48: '黃\n金\n蟹\n肉\n手\n捲', 49: '蘆\n筍\n蝦\n手\n捲', 50: '鮭\n魚\n子\n手\n捲', 51: '味\n噌\n湯', 52: '牡\n丹\n蝦\n味\n噌\n湯', 53: '海\n膽', 54: '玉\n米', 55: '海\n老\n子', 56: '韓\n風\n螺\n片', 57: '龍\n蝦\n沙\n拉', 58: '芥\n末\n章\n魚', 59: ' \n鮪\n魚\n蔥\n花', 60: '黃\n金\n蟹\n肉', 62: '鮭\n魚\n子', 63: '明\n太\n子\n玉\n子\n燒', 64: '明\n太\n子\n花\n枝\n小\n物'}
BASE_PATH = "/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/"

def plot_sushi(x_list: list, y_list: list, title: str, xlabel: str, ylabel: str, figpath: str) -> None:
    plt.figure(num=title, figsize=(24, 10))
    plt.bar(x_list, y_list)
    plt.xticks(rotation=0)
    plt.title(title)
    plt.xlabel(xlabel, )
    plt.ylabel(ylabel, )
    plt.subplots_adjust(bottom=.4)
    plt.savefig(figpath)


def remove_zero_sushi(originSushi: dict) -> dict:
    cleanDict = {}
    
    for i, j in originSushi.items():
        if j == 0:
            continue
        cleanDict[i] = j

    return cleanDict


def count_sushi(path: str) -> dict:
    sushiCount = {i: 0 for i in SUSHI_NUM.values()}

    for dataFile in os.listdir(path):
        if dataFile.endswith(".txt"):

            with open(path + "/" + dataFile) as f:
                for line in f:
                    num = int(line.split()[0])
                    # print(num)
                    name = SUSHI_NUM[num]
                    # print(name)
                    sushiCount[name] += 1
                    # print(f"{name}: {sushi_count[name]}")

    xList, yList = [], []
    for i, j in sushiCount.items():
        xList.append(i)
        yList.append(j)

    if PLOT:
        plot_sushi(xList, yList, path[52:]+" sushi quantity", u"壽司", "quantity", "img_"+path[52:]+"_sushi_count")

    return sushiCount


def sort_sushi(sushi: dict) -> None:
    sortedSushi = {k: v for k, v in sorted(sushi.items(), key=lambda item: item[1], reverse=True)}

    return sortedSushi
    
def process(label: str) -> None:
    path = BASE_PATH+"yolo_"+label
    sushiCount = count_sushi(path)

    cleanSushi = remove_zero_sushi(sushiCount)

    sortedSushi = sort_sushi(cleanSushi)

    print(f"sushi name: {len(cleanSushi)}")
    print(sortedSushi)


    plot_sushi(list(sortedSushi.keys()), list(sortedSushi.values()), "clean sushi quantity", "sushi", "quantity", "img_clean_sushi_count")



if __name__ == "__main__":

    process("train")

    process("test")
    
    
    print("\n---finish counting---")