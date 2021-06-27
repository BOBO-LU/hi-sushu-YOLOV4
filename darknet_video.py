from ctypes import *
import random
import os
import cv2
import time
import darknet
import argparse
from threading import Thread, enumerate
from queue import Queue

from datetime import datetime
from collections import Counter

BEST = "20210529-1"
BASE_PATH = "/home/oplabsushi/Desktop/bobo/training_result/"

FONT = cv2.FONT_HERSHEY_SIMPLEX


def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default=0,
                        help="video source. If empty, uses webcam 0 stream")
    parser.add_argument("--out_filename", type=str, default="",
                        help="inference video name. Not saved if empty")
    parser.add_argument("--weights", default=BASE_PATH + BEST + "/yolov4-tiny-obj_best.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--config_file", default=BASE_PATH + BEST + "/yolov4-tiny-obj.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/cfg/sushi.data",
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with confidence below this value")
    return parser.parse_args()


def str2int(video_path):
    """
    argparse returns and string althout webcam uses int (0, 1 ...)
    Cast to int if needed
    """
    try:
        return int(video_path)
    except ValueError:
        return video_path


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(
            os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(
            os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(
            os.path.abspath(args.data_file))))
    if str2int(args.input) == str and not os.path.exists(args.input):
        raise(ValueError("Invalid video path {}".format(os.path.abspath(args.input))))


def set_saved_video(input_video, output_video, size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(input_video.get(cv2.CAP_PROP_FPS))
    video = cv2.VideoWriter(output_video, fourcc, fps, size)
    return video


def video_capture(frame_queue, darknet_image_queue):
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)
        frame_queue.put(frame_resized)
        img_for_detect = darknet.make_image(width, height, 3)
        darknet.copy_image_from_bytes(img_for_detect, frame_resized.tobytes())
        darknet_image_queue.put(img_for_detect)
    cap.release()


def inference(darknet_image_queue, detections_queue, fps_queue):
    while cap.isOpened():
        darknet_image = darknet_image_queue.get()
        prev_time = time.time()
        detections = darknet.detect_image(
            network, class_names, darknet_image, thresh=args.thresh)
        detections_queue.put(detections)

        print(sushi.get_local_time())

        fps = int(1/(time.time() - prev_time))
        fps_queue.put(fps)
        print("FPS: {}".format(fps))
        darknet.print_detections(detections, args.ext_output)
        darknet.free_image(darknet_image)
    cap.release()


def drawing(frame_queue, detections_queue, fps_queue):
    random.seed(3)  # deterministic bbox colors
    video = set_saved_video(cap, args.out_filename, (width, height))
    while cap.isOpened():
        frame_resized = frame_queue.get()
        detections = detections_queue.get()
        fps = fps_queue.get()
        if frame_resized is not None:
            image = darknet.draw_boxes(detections, frame_resized, class_colors)
            image = sushi.add_timestamp_and_line(
                detections, frame_resized, class_colors)
            image = sushi.verify_sushi(image, detections)

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if args.out_filename is not None:
                video.write(image)
            if not args.dont_show:
                cv2.imshow('Inference', image)
            if cv2.waitKey(fps) == 27:
                break
        if sushi.add_frame_count(video) == False:
            break
    cap.release()
    video.release()
    cv2.destroyAllWindows()


class DetectSushi():
    def __init__(self) -> None:
        self.frame_count = 0  # 模擬計數器，每一個frame多一
        self.sushi_slot_1 = []  # slot 1 暫存
        self.sushi_slot_2 = []  # slot 2 暫存
        self.round_count = 0  # 第幾輪
        self.sushi_memory = []  # slot 1 的壽司紀錄
        self.sushi_memory_2 = []  # slot 2 的壽司紀錄
        self.sushi_pointer = {1: 0, 2: 0}  # slot 1 緩衝空間清除的壽司數 (最多清除5個)
        # slot 2 緩衝空間清除的壽司數

    # def start_rount(self):  # 開始新的一輪
    #     self.round_count += 1
    #     round_name = "round" + str(self.round_count)
    #     self.sushi_memory[round_name] = []

    def get_sushi_slot(self, slot=1):  # 取得sushi slot
        if slot == 1:
            return self.sushi_slot_1
        else:
            return self.sushi_slot_2

    def get_sushi_memory(self, slot=1):
        if slot == 1:
            return self.sushi_memory
        else:
            return self.sushi_memory_2

    def reset_slot(self, slot):
        if slot == 1:
            self.sushi_slot_1 = []
        else:
            self.sushi_slot_2 = []

    def verify_sushi(self, image, detections):
        unique = []
        for label, confidence, bbox in detections:
            if label in unique:
                continue
            unique.append(label)
            left, top, right, bottom = darknet.bbox2points(bbox)
            if left > 40 and right < 220:  # slot 1
                image = self.add_sushi_name(image, label, 130)
                self.get_sushi_slot(1).append(label)
                self.check_slot(1)
            if left > 220 and right < 400:  # slot 2
                image = self.add_sushi_name(image, label, 310)
                self.get_sushi_slot(2).append(label)
                self.check_slot(2)
        return image

    def check_slot(self, slot):
        most_sushi = self.most_frequent_sushi(self.get_sushi_slot(slot))
        if most_sushi[1] == 13:  # 當初前最多的壽司達到15個
            # 紀錄現在的貞數
            self.sushi_pointer[slot] = self.frame_count

        # 在過6貞之後，清除slot，放進memory
        if most_sushi[1] > 13 and self.frame_count - self.sushi_pointer[slot] > 8:
            print("sushi_slot1: ", self.get_sushi_slot(1))
            self.get_sushi_memory(slot).append(most_sushi[0])
            self.reset_slot(slot)

    def add_timestamp_and_line(self, detections, image, colors):

        cv2.line(image, (40, 0), (40, 352), (255, 255, 255), 1)
        cv2.line(image, (220, 0), (220, 352), (255, 255, 255), 1)
        cv2.line(image, (400, 0), (400, 352), (255, 255, 255), 1)

        local_time = self.get_local_time()

        cv2.putText(image, "{} ".format(local_time),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)
        return image

    def add_sushi_name(self, image, label, offset):
        textsize = cv2.getTextSize(label, FONT, 0.5, 2)[0]
        textX = int(offset - (textsize[0] / 2))
        cv2.putText(image, "{}".format(label),
                    (textX, 40), FONT, 0.5,
                    (255, 255, 255), 2)
        return image

    def add_frame_count(self, video):
        self.frame_count += 1
        if self.frame_count % 100 == 0:
            print("-"*10)
            print("slot 1: ", self.most_frequent_sushi(self.get_sushi_slot(1)))
            print("slot 2: ", self.most_frequent_sushi(self.get_sushi_slot(2)))
            print("-"*10)

        if self.frame_count == 1000:
            print("-"*10)
            print(Counter(self.sushi_slot_1))
            print(Counter(self.sushi_slot_2))
            print("-"*10)
            print(self.get_sushi_memory(1))
            print(self.get_sushi_memory(2))
            print("-"*10)
            return False

    # class utils, needs refactor

    def get_local_time(self) -> str:
        local_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return local_time

    # return tuple, (sushi_name, most frequency)
    def most_frequent_sushi(self, sushi_list) -> tuple:
        return Counter(sushi_list).most_common(1)[0]


if __name__ == '__main__':
    sushi = DetectSushi()
    # sushi.start_rount()

    frame_queue = Queue()
    darknet_image_queue = Queue(maxsize=1)
    detections_queue = Queue(maxsize=1)
    fps_queue = Queue(maxsize=1)

    args = parser()
    check_arguments_errors(args)
    network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=1
    )
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    input_path = str2int(args.input)
    cap = cv2.VideoCapture(input_path)
    Thread(target=video_capture, args=(
        frame_queue, darknet_image_queue)).start()
    Thread(target=inference, args=(darknet_image_queue,
           detections_queue, fps_queue)).start()
    Thread(target=drawing, args=(frame_queue,
           detections_queue, fps_queue)).start()
