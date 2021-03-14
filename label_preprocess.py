import csv

counter = 0
sushi_dict = {}

with open('/home/bobo/hi-sushi/Yolo/name.txt', mode='r') as infile:
    reader = csv.reader(infile, delimiter=' ')
    for row in reader:
        
        sushi_dict[' '.join(row[1:])] = counter
        counter += 1

print(sushi_dict)
print('*************')
print(sorted(sushi_dict, key=sushi_dict.get))