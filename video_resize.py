import cv2
import numpy as np

# SIZE = (672, 672)
SIZE = (480, 360)
cap = cv2.VideoCapture(
    '/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/video/GH010006.MP4')
# cap.set(cv2.CAP_PROP_POS_AVI_RATIO,1)
# frames = cap.get(cv2.CAP_PROP_POS_FRAMES)
# print(frames)
# print(cap.get(cv2.CAP_PROP_POS_MSEC))
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)


if not cap.isOpened():
    print("Error opening video")

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(
    '/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/video/output_360p.mp4', fourcc, fps, SIZE)
try:
    count = 0
    while True:
        ret, frame = cap.read()
        print(frame)
        print(ret)
        if ret == True:
            b = cv2.resize(frame, SIZE, fx=0, fy=0,
                           interpolation=cv2.INTER_CUBIC)
            out.write(b)
            print('write')
            count += 1

            # if count == 30:
            #     break
        else:
            pass
            # break
except KeyboardInterrupt:
    print('ctrl+c')
    pass

cap.release()
out.release()
cv2.destroyAllWindows()
print('finish')
