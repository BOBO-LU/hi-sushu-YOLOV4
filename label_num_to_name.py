import os

PATH = "/home/oplabsushi/Desktop/bobo/darknet/hi-sushi"
SUSHI_NUM = {0: 'Botan Prawn', 1: 'Tamago', 2: 'Smoked Cherry Duck Breast', 3: 'Salmon with Onion', 4: 'Marinated Mackerel', 5: 'Tuna Fish', 6: 'Salmon', 7: 'Squid', 8: 'Sea Perch', 9: 'Salmon Belly', 10: 'Cobia', 11: 'Fresh Tuna with Own Spicy Sauce', 12: 'Grass Shrimp', 13: 'Hokkigai', 14: 'Yellowtail', 15: 'Japanese Amberjack', 16: 'Sweet Shrimp', 17: 'Scallop', 18: 'Japanese Fatty Tuna', 19: 'Roasted Scallop with Fleur de sel', 20: 'Roasted Mushroom with Truffle', 21: 'Roasted flounder', 22: 'Roasted Duck', 23: 'Roasted Salmon', 24: 'Roasted US Rib with Fleur de sel & Garlic', 25: 'Roasted US Rib with Spicy Miso(Mildly Spicy)', 26: 'Roasted Flounder', 27: 'Caramel Salmon with Pomelo', 28: 'Roasted Squid With Cod Roes Sauce', 29: 'Roasted Salmon with Cod Roes Sauce', 30: 'Crispy Garlic Beef', 31: 'Roasted Cobia with Fleur de sel', 32: 'Roasted Shrimp with Cod Roes Sauce', 33: 'Roasted Conger Eel', 34: 'Eel', 35: 'Roasted Australian Wagyu Beef with Fleur de sel', 36: 'Twin Sashimi Combo', 37: 'Sashimi Platter', 38: 'Luxurious Sashimi Platter', 39: 'Japanese Sweet Bean Curd', 40: 'Sushi Roll', 41: 'Asparagus Roll', 42: 'Fermented Soybeans Roll', 43: 'Pickled Rolled Sushi', 44: 'Tuna Roll', 45: 'Hisushi Jumbo Roll', 46: 'Tuna Roll with Scallions', 47: 'Lobster Salad Roll', 48: 'Crab Meat Handroll', 49: 'Shrimp & Asparagus Roll', 50: 'Salmon Roes Roll', 51: 'Miso Soup', 52: 'Botan Prawn Miso Soup', 53: 'Sea Urchin', 54: 'Corn', 55: 'Shrimp Roes', 56: 'Sea Snail in Korean Style', 57: 'Minced Lobster Salad', 58: 'Octopus with Green Mastard', 59: 'Tuna with Scallions', 60: 'Crab Meat', 61: 'Sweet Freshwater Shrimp', 62: 'Salmon Roes', 63: 'Roasted Tamago with Cod Roes Sauce', 64: 'Gratinating Squid with Cod Roes Sauce'}

def convert(folder, write_file):
    file_path = PATH + folder
    list_dir = [_ for _ in os.listdir(file_path) if _.endswith(".txt")]
    sushi_list = [[]] * len(list_dir)
    
    for data_file in list_dir:

        sushi_info = []        
        
        with open(os.path.join(file_path, data_file), 'r') as f:
            img_num = int(data_file.split('.')[0])
            for line in f:
                num = int(line.split()[0])
                sushi_info.append(' '.join([str(num), SUSHI_NUM[num]]))

            sushi_list[img_num] = sushi_info
    print(sushi_list)
 
    with open(PATH + write_file, 'w') as f:
        for index, info in enumerate(sushi_list):
            f.write(f'FILE: {index}.jpg\n')
            
            for sushi in info:
                print(sushi)
                f.write(sushi+"\n")
            f.write("\n")

        return




if __name__ == "__main__":

    convert("/yolo_test", "/ground_truth_test_label.txt")
    convert("/yolo_train", "/ground_truth_train_label.txt")