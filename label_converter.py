"""
https://medium.com/ching-i/%E5%A6%82%E4%BD%95%E8%BD%89%E6%8F%9B%E7%82%BAyolo-txt%E6%A0%BC%E5%BC%8F-f1d193736e5c
"""

import os
import shutil
from bs4 import BeautifulSoup

def run_convert(all_classes, train_img, train_annotation, yolo_path, write_txt):
    now_path = os.getcwd()
    data_counter = 0

    for data_file in os.listdir(train_annotation):
        try:
            with open(os.path.join(train_annotation, data_file), 'r') as f:
                print("read file...")
                soup = BeautifulSoup(f.read(), 'xml')
                img_name = soup.select_one('filename').text

                for size in soup.select('size'):
                    img_w = int(size.select_one('width').text)
                    img_h = int(size.select_one('height').text)
                    
                img_info = []
                for obj in soup.select('object'):
                    xmin = int(obj.select_one('xmin').text)
                    xmax = int(obj.select_one('xmax').text)
                    ymin = int(obj.select_one('ymin').text)
                    ymax = int(obj.select_one('ymax').text)
                    objclass = all_classes.get(obj.select_one('name').text)

                    x = (xmin + (xmax-xmin)/2) * 1.0 / img_w
                    y = (ymin + (ymax-ymin)/2) * 1.0 / img_h
                    w = (xmax-xmin) * 1.0 / img_w
                    h = (ymax-ymin) * 1.0 / img_h
                    img_info.append(' '.join([str(objclass), str(x),str(y),str(w),str(h)]))

                # copy image to yolo path and rename
                img_path = os.path.join(train_img, img_name)
                img_format = img_name.split('.')[1]  # jpg or png
                shutil.copyfile(img_path, yolo_path + str(data_counter) + '.' + img_format)
                
                # create yolo bndbox txt
                with open(yolo_path + str(data_counter) + '.txt', 'a+') as f:
                    f.write('\n'.join(img_info))

                # create train or val txt
                with open(write_txt, 'a') as f:
                    path = os.path.join(now_path, yolo_path)
                    line_txt = [path + str(data_counter) + '.' + img_format, '\n']
                    f.writelines(line_txt)

                data_counter += 1
                    
        except Exception as e:
            print(e)
           
    print('the file is processed')


all_classes = {'Asparagus Roll': 41, 'Tuna Roll with Scallions': 46, 'Tuna Roll': 44, 'Roasted US Rib with Fleur de sel & Garlic': 24, 'Roasted Cobia with Fleur de sel': 31, 'Twin Sashimi Combo': 36, 'Roasted Duck': 22, 'Lobster Salad Roll': 47, 'Salmon with Onion': 3, 'Roasted Tamago with Cod Roes Sauce': 63, 'Roasted Flounder': 26, 'Fresh Tuna with Own Spicy Sauce': 11, 'Roasted Conger Eel': 33, 'Pickled Rolled Sushi': 43, 'Hokkigai': 13, 'Minced Lobster Salad': 57, 'Sushi Roll': 40, 'Smoked Cherry Duck Breast': 2, 'Salmon Roes': 62, 'Roasted Shrimp with Cod Roes Sauce': 32, 'Sweet Shrimp': 16, 'Corn': 54, 'Roasted US Rib with Spicy Miso(Mildly Spicy)': 25, 'Salmon': 6, 'Roasted Australian Wagyu Beef with Fleur de sel': 35, 'Shrimp Roes': 55, 'Crispy Garlic Beef': 30, 'Botan Prawn Miso Soup': 52, 'Tuna with Scallions': 59, 'Miso Soup': 51, 'Roasted flounder': 21, 'Japanese Amberjack': 15, 'Sea Perch': 8, 'Grass Shrimp': 12, 'Tuna Fish': 5, 'Hisushi Jumbo Roll': 45, 'Japanese Sweet Bean Curd': 39, 'Caramel Salmon with Pomelo': 27, 'Botan Prawn': 0, 'Roasted Salmon with Cod Roes Sauce': 29, 'Roasted Squid With Cod Roes Sauce': 28, 'Fermented Soybeans Roll': 42, 'Gratinating Squid with Cod Roes Sauce': 64, 'Roasted Scallop with Fleur de sel': 19, 'Crab Meat': 60, 'Crab Meat Handroll': 48, 'Sweet Freshwater Shrimp': 61, 'Sashimi Platter': 37, 'Salmon Roes Roll': 50, 'Roasted Mushroom with Truffle': 20, 'Marinated Mackerel': 4, 'Eel': 34, 'Japanese Fatty Tuna': 18, 'Squid': 7, 'Cobia': 10, 'Shrimp & Asparagus Roll': 49, 'Scallop': 17, 'Salmon Belly': 9, 'Sea Snail in Korean Style': 56, 'Roasted Salmon': 23, 'Tamago': 1, 'Sea Urchin': 53, 'Yellowtail': 14, 'Luxurious Sashimi Platter': 38, 'Octopus with Green Mastard': 58}
train_img = "/home/bobo/hi-sushi/Yolo/image"
train_annotation = "/home/bobo/hi-sushi/Yolo/train_label"
yolo_path = "yolo_train/"
write_txt = 'cfg/train.txt'

if not os.path.exists(yolo_path):
    os.mkdir(yolo_path)
else:
    lsdir = os.listdir(yolo_path)
    for name in lsdir:
        if name.endswith('.txt') or name.endswith('.jpg') or name.endswith('.png'):
            os.remove(os.path.join(yolo_path, name))

cfg_file = write_txt.split('/')[0]
if not os.path.exists(cfg_file):
    os.mkdir(cfg_file)
    
if os.path.exists(write_txt):
    file=open(write_txt, 'w')

run_convert(all_classes, train_img, train_annotation, yolo_path, write_txt)