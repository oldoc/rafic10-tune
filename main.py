import csv
import numpy as np
from numpy import array

interval = [0, 1300, 2600, 3900, 5200, 6500, 7800, 9100, 10400, 11700, 13000]

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
        if data[i][-1]:
            total += 1
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

def compare(rafic10, cifar10):
    sum = 0.0
    for i in range(8):
        sum += abs(rafic10[i] - cifar10[i])
    return sum

def disable_one_most_influential(classnum, data, cifar10_precision):
    total = 0
    hit = np.zeros([8])
    for i in range(interval[classnum], interval[classnum+1]):
        if data[i][-1]:
            total += 1
            for j in range(8):
                hit[j] += data[i][j]

    min = 8
    total -= 1
    index = -1
    for i in range(interval[classnum], interval[classnum+1]):
        if data[i][-1]:

            precision = (hit - data[i][0:8]) / total

            diff = compare(precision, cifar10_precision)
            if diff < min:
                min = diff
                index = i
    if index != -1:
        data[index][-1] = 0
        print(min)
    else:
        print("index error!")
    return min


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
ratio /= 100

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

file_precision = open('final-precision.csv','w')
file_mask = open('mask.csv', 'w')
for num in range(10):
    diff = 8
    for i in range(300):
        current_diff = disable_one_most_influential(num, data, ratio[num])
        if current_diff < diff:
            diff = current_diff
        else:
            break
    pre = compute_precision(num, data)
    for j in range(len(pre)):
        file_precision.write("{0:1.8f},".format(pre[j]))
    file_precision.write("\n")

for i in range(interval[-1]):
    file_mask.write("{0}\n".format(data[i][-1]))

for num in range(10):
    sums = 0
    for i in range(interval[num], interval[num+1]):
        if data[i][-1]:
            sums += 1
    print(sums)

file_mask.close()
file_precision.close()


