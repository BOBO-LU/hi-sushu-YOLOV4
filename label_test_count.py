
"""
PATTERN:
Enter Image Path:  Detection layer: 139 - type = 28 
 Detection layer: 150 - type = 28 
 Detection layer: 161 - type = 28 
/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/yolo_train/0.jpeg: Predicted in 29.131000 milli-seconds.
Grass Shrimp: 93%
Gratinating Squid with Cod Roes Sauce: 98%

DATA STRUCTURE:
[{
    image: 0,
    count: 2,
    object: {
        Grass Shrimp: 1, 
        Gratinating Squid with Cod Roes Sauce: 1
    }
}]
"""
import os
import matplotlib
# TEST_FILE_PATH = "/result_test.txt"
TEST_FILE_PATH = "/result_train.txt"
# LABEL_PATH = "/yolo_test/"
LABEL_PATH = "/yolo_train"

PATH = "/home/oplabsushi/Desktop/bobo/darknet/hi-sushi"
SUSHI_NUM = {0: 'Botan Prawn', 1: 'Tamago', 2: 'Smoked Cherry Duck Breast', 3: 'Salmon with Onion', 4: 'Marinated Mackerel', 5: 'Tuna Fish', 6: 'Salmon', 7: 'Squid', 8: 'Sea Perch', 9: 'Salmon Belly', 10: 'Cobia', 11: 'Fresh Tuna with Own Spicy Sauce', 12: 'Grass Shrimp', 13: 'Hokkigai', 14: 'Yellowtail', 15: 'Japanese Amberjack', 16: 'Sweet Shrimp', 17: 'Scallop', 18: 'Japanese Fatty Tuna', 19: 'Roasted Scallop with Fleur de sel', 20: 'Roasted Mushroom with Truffle', 21: 'Roasted flounder', 22: 'Roasted Duck', 23: 'Roasted Salmon', 24: 'Roasted US Rib with Fleur de sel & Garlic', 25: 'Roasted US Rib with Spicy Miso(Mildly Spicy)', 26: 'Roasted Flounder', 27: 'Caramel Salmon with Pomelo', 28: 'Roasted Squid With Cod Roes Sauce', 29: 'Roasted Salmon with Cod Roes Sauce', 30: 'Crispy Garlic Beef', 31: 'Roasted Cobia with Fleur de sel', 32: 'Roasted Shrimp with Cod Roes Sauce', 33: 'Roasted Conger Eel', 34: 'Eel', 35: 'Roasted Australian Wagyu Beef with Fleur de sel', 36: 'Twin Sashimi Combo', 37: 'Sashimi Platter', 38: 'Luxurious Sashimi Platter', 39: 'Japanese Sweet Bean Curd', 40: 'Sushi Roll', 41: 'Asparagus Roll', 42: 'Fermented Soybeans Roll', 43: 'Pickled Rolled Sushi', 44: 'Tuna Roll', 45: 'Hisushi Jumbo Roll', 46: 'Tuna Roll with Scallions', 47: 'Lobster Salad Roll', 48: 'Crab Meat Handroll', 49: 'Shrimp & Asparagus Roll', 50: 'Salmon Roes Roll', 51: 'Miso Soup', 52: 'Botan Prawn Miso Soup', 53: 'Sea Urchin', 54: 'Corn', 55: 'Shrimp Roes', 56: 'Sea Snail in Korean Style', 57: 'Minced Lobster Salad', 58: 'Octopus with Green Mastard', 59: 'Tuna with Scallions', 60: 'Crab Meat', 61: 'Sweet Freshwater Shrimp', 62: 'Salmon Roes', 63: 'Roasted Tamago with Cod Roes Sauce', 64: 'Gratinating Squid with Cod Roes Sauce'}
SUSHI_NAME = {'Botan Prawn': 0, 'Tamago': 1, 'Smoked Cherry Duck Breast': 2, 'Salmon with Onion': 3, 'Marinated Mackerel': 4, 'Tuna Fish': 5, 'Salmon': 6, 'Squid': 7, 'Sea Perch': 8, 'Salmon Belly': 9, 'Cobia': 10, 'Fresh Tuna with Own Spicy Sauce': 11, 'Grass Shrimp': 12, 'Hokkigai': 13, 'Yellowtail': 14, 'Japanese Amberjack': 15, 'Sweet Shrimp': 16, 'Scallop': 17, 'Japanese Fatty Tuna': 18, 'Roasted Scallop with Fleur de sel': 19, 'Roasted Mushroom with Truffle': 20, 'Roasted flounder': 21, 'Roasted Duck': 22, 'Roasted Salmon': 23, 'Roasted US Rib with Fleur de sel & Garlic': 24, 'Roasted US Rib with Spicy Miso(Mildly Spicy)': 25, 'Roasted Flounder': 26, 'Caramel Salmon with Pomelo': 27, 'Roasted Squid With Cod Roes Sauce': 28, 'Roasted Salmon with Cod Roes Sauce': 29, 'Crispy Garlic Beef': 30, 'Roasted Cobia with Fleur de sel': 31, 'Roasted Shrimp with Cod Roes Sauce': 32, 'Roasted Conger Eel': 33, 'Eel': 34, 'Roasted Australian Wagyu Beef with Fleur de sel': 35, 'Twin Sashimi Combo': 36, 'Sashimi Platter': 37, 'Luxurious Sashimi Platter': 38, 'Japanese Sweet Bean Curd': 39, 'Sushi Roll': 40, 'Asparagus Roll': 41, 'Fermented Soybeans Roll': 42, 'Pickled Rolled Sushi': 43, 'Tuna Roll': 44, 'Hisushi Jumbo Roll': 45, 'Tuna Roll with Scallions': 46, 'Lobster Salad Roll': 47, 'Crab Meat Handroll': 48, 'Shrimp & Asparagus Roll': 49, 'Salmon Roes Roll': 50, 'Miso Soup': 51, 'Botan Prawn Miso Soup': 52, 'Sea Urchin': 53, 'Corn': 54, 'Shrimp Roes': 55, 'Sea Snail in Korean Style': 56, 'Minced Lobster Salad': 57, 'Octopus with Green Mastard': 58, 'Tuna with Scallions': 59, 'Crab Meat': 60, 'Sweet Freshwater Shrimp': 61, 'Salmon Roes': 62, 'Roasted Tamago with Cod Roes Sauce': 63, 'Gratinating Squid with Cod Roes Sauce': 64}

def convert_test_result(test_file_path: str) -> list:
    result_path = PATH + test_file_path
    img_count = -1 #use to count the testing image
    same_flag = 0
    result= []
    sushi_dict = {} #save results of each photos like the DS above

    with open(result_path) as f:
        for line in f:
            
            if line.startswith("Enter Image Path:"): #start a new image, reset counter                
                if same_flag: #end the last img, push the sushidict to result
                    result.append(sushi_dict)

                img_count += 1
                same_flag = 0
                sushi_dict = {"image": img_count, "count": 0, "object":{}}
                continue

            if line.startswith("/home"): #next line will be sushi
                same_flag = 1
                continue

            if same_flag: #same image, add result
                sushi_dict["count"] += 1
                sushi, confidence = line.split(":")
                
                if sushi in sushi_dict["object"].keys(): #if already in object, add one sushi. else set value = 1
                    sushi_dict["object"][SUSHI_NAME[sushi]] += 1
                else: 
                    sushi_dict["object"][SUSHI_NAME[sushi]] = 1
                continue

            else: #start a new image
                continue

    return result

def convert_groud_truth(label_path: str) -> list:
    result = []
    
    yolo_test_path = PATH + label_path
    for test_file in os.listdir(yolo_test_path): #iterate the yolo_test folder
        if test_file.endswith(".txt"): # for every file ends with .txt
            img_count = test_file.split(".")[0] #get the image number
            sushi_dict = {"image": img_count, "count": 0, "object":{}}

            with open(yolo_test_path + "/" + test_file) as f:  #read every line in the txt and update sushi_dict
                for line in f:
                    label = line.split()[0]  
                    sushi_dict["count"] += 1

                    if label in sushi_dict["object"].keys(): #if already in object, add one sushi. else set value = 1
                        sushi_dict["object"][int(label)] += 1
                    else: 
                        sushi_dict["object"][int(label)] = 1

            result.append(sushi_dict)
    
    
    # sort the list by image and return 
    result = sorted(result, key=lambda k: int(k['image'])) 
    return result

def calc_image_difference(predict, label) -> int:
    image_difference = len(predict) - len(label)
    if image_difference == 0:
        print("Image: Same Image Count")
    else:
        print("Image: {image_difference}")
    return image_difference

def calc_object_difference(predict, label) -> int:
    count_diff_list = []
    sushi_diff_list = []
    
    for i, j in zip(predict, label):
        # get differnt counts
        if i["count"] != j["count"]:
            diff_count = abs(i["count"] - j["count"])
            error_string = f"Count: {i['image']}.jpeg has {diff_count} different count than label"
            count_diff_list.append(error_string)
            print(error_string)
        
    if len(count_diff_list) == 0:
        print("Count: All Images Detect Same Amount of Objects")
    
    return len(count_diff_list)

def calc_sushi_difference(predict, label) -> int:
    sushi_diff_list = []

    # get all different obejcts
    for i, j in zip(predict, label):
        diff = dict(set(i["object"].items()) ^ set(j["object"].items()))
        if diff: #there is something different
            img = i["image"]

            for k in diff.keys(): #change from sushi num to sushi name
                diff[k] = SUSHI_NUM[k]
                
            sushi_diff_list.append({str(img)+".jpeg": diff})
            print("Sushi: ", {str(img)+".jpeg": diff})
    
    if len(sushi_diff_list) == 0:
        print("Sushi: All Detected Sushi are same")
    return len(sushi_diff_list)

if __name__ == "__main__":
    
    test_result = convert_test_result(TEST_FILE_PATH)
    # print(test_result)
    ground_truth = convert_groud_truth(LABEL_PATH)
    # print(ground_truth)


    img_diff = calc_image_difference(test_result, ground_truth)
    print("*"*10)
    obj_diff = calc_object_difference(test_result, ground_truth)
    print("*"*10)
    sushi_diff = calc_sushi_difference(test_result, ground_truth)


    max_count = 0
    total_image = len(ground_truth)
    total_count = 0

    for i in ground_truth:
        if max_count < i["count"]: max_count = i["count"]
        total_count += i["count"]
    
    print("max_count: ", max_count)
    print("avg_count: ", total_count/total_image)
