import csv


class SUSHI():
    def __init__:
        counter = 0
        sushi_dict = {}
        sushi_dict_ch = {}
        preprocess()

    def preprocess(self):

        with open("/home/oplabsushi/Desktop/bobo/darknet/hi-sushi/name.txt", mode='r') as infile:
            reader = csv.reader(infile, delimiter=' ')
            for row in reader:
                
                sushi_dict[' '.join(row[1:])] = counter
                sushi_dict_ch[' '.join(row[:1])] = counter
                counter += 1

        sushi_name = sorted(sushi_dict, key=sushi_dict.get)
        sushi_name_ch = sorted(sushi_dict_ch, key=sushi_dict_ch.get)
        sushi_num = dict((y,x) for x,y in sushi_dict.items())
        sushi_num_ch = dict((y,x) for x,y in sushi_dict_ch.items())


    def get_sushi_dict(ch=False):
        return sushi_dict


    def get_sushi_name(ch=False):
        return sushi_name

    def get_sushi_num(ch=False):
        return sushi_num
    

if __name__ == "__main__":
    S = SUSHI()
    

    # print(sushi_dict)
    # print('*'*20)
    # print(sushi_dict_ch)
    # print('*'*20)
    # print(sushi_name)
    # print('*'*20)
    # print(sushi_name_ch)
    # print('*'*20)
    # print(sushi_num)
    # print('*'*20)
    # print(sushi_num_ch)

