#coding:utf-8
import random
import DATA as DS
import re
import pickle
import Global_V
import random
import platform


# load a specific data file (we define the filename in Globle_V.py)
def openfile(filename):
    # filename: zoo.arff
    # find the operating system
    f = open(filename)
        ##### define the path is better
    return f




# 以下代码用于测试时，提供初始数据集
if __name__ == '__main__':
    data = [[1, 3, 34], [2, 87, 2], [3, 456], [4, 234, 42], [5, 324], [6, 562], [7, 2, 4], [8, 1, 0], [9, 1, 78],
            [10, 12, 56]]
#    trainData, testData = DS.splitdataset(data, 0.9, 0)

