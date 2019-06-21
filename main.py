import csv
import numpy as np
from numpy import array

interval = [0, 1234, 2461, 3685, 4965, 6221, 7440, 8699, 9884, 11151, 12304]

total= [0] * 10
for i in range(10):
    total[i] = interval[i+1] - interval[i]

data = []
ratio = []
hit = np.zeros([10,8])

def compute_precision(classnum, data):
    total = 0
    global hit
    for i in range(8):
        hit[classnum][i] =0

    for i in range(interval[classnum], interval[classnum+1]):
        total += 1
        if data[i][-1]:
            for j in range(8):
                hit[classnum][j] += data[i][j]
    return hit[classnum] / total

def tune_step(classnum, netnum, data, reduce):
    pos = -1

    if reduce:
        min = 8
        for i in range(interval[classnum], interval[classnum + 1]):
            if (data[i][netnum] == 1) and (data[i][-5] < min):
                pos = i
                min = data[i][-5]
    else:
        max = 0
        for i in range(interval[classnum], interval[classnum + 1]):
            if (data[i][netnum] == 0) and (data[i][-5] > max):
                pos = i
                max = data[i][-5]
    return pos

with open('rafic10-result.csv','r', newline='') as file:
    file = csv.reader(file, delimiter=',')
    for row_list in file:
        row_list_int = [int(value) for value in row_list]
        data.append(row_list_int)
data = array(data)

with open('cifar10-ratio.csv','r', newline='') as file:
    file = csv.reader(file, delimiter=',')
    for row_list in file:
        row_list_int = [float(value) for value in row_list]
        ratio.append(row_list_int)
ratio = array(ratio)
ratio = ratio.T

#print(data.shape[0])
#print(ratio[0])


'''
for i in range(data.shape[0]):
    if (data[i][-4] == 0):
        total += 1
        for j in range(8):
            num[0][j] += data[i][j]

num[0] /= total # the rafic10 precision of class 0 on eight models
num[1] = num[0] / ratio[0] # percentage of rafic10 on cifar10
'''


for i in range(10):
    print(compute_precision(i, data))





