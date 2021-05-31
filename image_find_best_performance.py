"""
1. get all the test path
2. run detector test with each kind of threshold
3. calculate avg acc
4. plot it
"""

import glob
import os

import matplotlib.pyplot as plt
import numpy as np

from label_test_count import *

# TEST_FILE_PATH = "/result/result_test_20210522-1-60.txt"
RESULT_PATH = "/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/result"
LABEL_PATH = "/yolo_test/"


def calc_avg(TEST_FILE_PATH):
    dash_len = len("Result of ") + len(TEST_FILE_PATH)
    print("-"*(dash_len+4))
    print("| Result of " + TEST_FILE_PATH + " |")
    print("-"*(dash_len+4))
    test_result = convert_test_result(TEST_FILE_PATH)
    print(test_result[0])
    ground_truth = convert_groud_truth(LABEL_PATH)
    print(ground_truth[0])

    img_diff = calc_image_difference(test_result, ground_truth)
    # print("*"*(dash_len+4))
    obj_diff, more_sushi, less_sushi = calc_object_difference(
        test_result, ground_truth)
    # print("*"*(dash_len+4))
    sushi_diff, fp, tn = calc_sushi_difference(test_result, ground_truth)
    # print("*"*(dash_len+4))

    return calc_statitics(ground_truth, sushi_diff, more_sushi, less_sushi, fp, tn)


def detector_test():
    threshold_list = np.arange(30, 100, 2).tolist()
    for thresh in threshold_list:
        commands = [
            f'./darknet detector test hi-sushi/cfg/sushi.data /home/oplabsushi/Desktop/bobo/training_result/20210529-1/yolov4-tiny-obj.cfg /home/oplabsushi/Desktop/bobo/training_result/20210529-1/yolov4-tiny-obj_best.weights < /home/oplabsushi/Desktop/bobo/darknet/hi-sushi/cfg/test.txt -dont_show -thresh {thresh/100}  > /home/oplabsushi/Desktop/bobo/darknet/hi-sushi/result/result_test_20210529-1-{thresh}.txt']
        os.system(' '.join(commands))


detector_test()


performance = []
for file in sorted(os.listdir(RESULT_PATH)):
    if not file.endswith(".txt"):
        continue
    file_path = "/result/"+file
    avg = calc_avg(file_path)
    performance.append(avg)

p = list(zip(*performance))
print(p)
total = [p[0][i] + p[1][i] for i in range(len(p[0]))]

plt.figure(figsize=(9, 5))
plt.bar(np.arange(30, 100, 2)+1/4, total,
        width=1.5, label="Total Error", alpha=0.5, color='g')
plt.bar(np.arange(30, 100, 2)+1/2, list(p[1]), width=1, label="True Negative")
plt.bar(np.arange(30, 100, 2), list(p[0]), width=1, label="False Postive")


# plt.xticks(rotation=0)
plt.title("performance under different threshold")
plt.xlabel("threshold", )
plt.ylabel("amount", )
plt.legend(loc="upper left")
# plt.subplots_adjust(bottom=.4)
plt.savefig(RESULT_PATH+"/performance.png")
