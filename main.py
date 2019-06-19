import csv
import numpy as np
from numpy import array

data = []
ratio = []

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

num = np.zeros([2,8])
total = 0

for i in range(data.shape[0]):
    if (data[i][-4] == 0):
        total += 1
        for j in range(8):
            num[0][j] += data[i][j]

num[0] /= total # the rafic10 precision of class 0 on eight models
num[1] = num[0] / ratio[0] # percentage of rafic10 on cifar10

print(num)