#coding:utf-8
from __future__ import division
# function: transfer the string data to int data
# sample:

# vhigh,vhigh,2,2,small,low,unacc
# vhigh,vhigh,2,2,small,med,unacc
# high,vhigh,2,2,small,high,unacc
# vhigh,vhigh,2,2,med,low,unacc

# after the process, will be:
# [[0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 1, 0],
#  [0, 0, 0, 0, 0, 2, 0],
#  [0, 0, 0, 0, 1, 0, 0]]

import re
import pickle
import Global_V
import random
import loaddata
import numpy as np
from mdlp.discretization import MDLP

from mdlp.discretization import MDLP
import platform

"""
目前只能处理完整数据和离散数据！！！
"""



filePath = r'/Users/yaya/test/'
fileName = Global_V.TESTFILE
attr_list = [] # a list storing all the attributes

file = loaddata.openfile(filePath + Global_V.TESTFILE + '.arff')
# if windows : f = open('E:\\test\\' + filename)
# if linux   : f = open('~/test/')

for each_line in file:
    if each_line[0:10] == '@attribute':  # why it's 0:10, not 0:9 $ because 0:1 has just one element:@ ?
        # pattern_attr = re.compile(r'\t\w*')
        attr_temp = re.search(r'\t\w*', each_line)
        attr_list.append(str(attr_temp.group()))
        # successful find the attribute
# pattern_attr = re.compile('\{(.*)\}')
# car_attr = re.search(pattern_attr, car_data)
# print(car_attr.group())

attr_str_list = []
for each in attr_list:
    temp = each.strip()  # strip() 方法用来去除字符串中的空格、制表等符号；
    attr_str_list.append(temp)
# ***attr_str_list***sample***:　['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']


attr_num_list = []
ranknum = len(attr_str_list)
for each in range(0, len(attr_str_list), 1):
    attr_num_list.append(each)

# transfer each element in  attr_str_list from string type to int type, we get attr_num_list
# *****************************attr_str_list****************************-----------sample----------:　
# ['buying', 'maint', 'doors', 'persons', 'lug_boot', 'safety', 'class']

# *****************************attr_num_list****************************-----------sample----------:　
# [0, 1, 2, 3, 4, 5, 6]

attr_dict = dict(map(lambda x, y: [x, y], attr_num_list, attr_str_list))
# *****************************attr_dict****************************-----------sample----------:　
# {0: 'buying', 1: 'maint', 2: 'doors', 3: 'persons', 4: 'lug_boot', 5: 'safety', 6: 'class'}

# save attr_dict as attr_dict_pickle
attr_dict_pickle = open(r'./pickleFile/'+fileName + '_attr_dict.pkl', 'wb')
pickle.dump(attr_dict, attr_dict_pickle)
attr_dict_pickle.close()







# get info from xxxx.pmeta files.
attrname_list = []
each_attrVal_array = [] # to store all the attribute values of a data set;
attrnum_dict = {}
attrnum_replace_list = [[]]
file_pmeta = loaddata.openfile(filePath + Global_V.TESTFILE + '.pmeta')

attr_count = -1  # the number of attribute, initialize with -1 is because the index is begin with 0
continuous_features_list = []
for each in file_pmeta:
    if (each[0] == ':') or (each == '\n'):  # and (each[1] == ':'):   # deal with the ':', and '\n' in the file
        continue
    else:
        attr_count += 1
        attr_temp_name, attr_temp_val = each.split(':',1) # hair:0,1,2
        each_attrVal_array.append(attr_temp_val.strip())
        if attr_temp_val.strip() == "numeric" or attr_temp_val.strip() == "real": # record the continuous_features
            continuous_features_list.append(attr_count)
        attrname_list.append(attr_temp_name.strip())
continuous_features = np.array(continuous_features_list)
discretizationer = MDLP(continuous_features) # create a discretizationer

attrnum_list_temp = []
temp = []
for each in each_attrVal_array:
    temp.append(list(map(str, each.strip().split(','))))

each_attrVal_array = temp
print each_attrVal_array

# 处理后: each_attrVal_array
# [['vhigh', 'high', 'med', 'low'], ['vhigh', 'high', 'med', 'low'], ['2', '3', '4', '5more'],
# ['2', '4', 'more'], ['small', 'med', 'big'], ['low', 'med', 'high'], ['unacc', 'acc', 'good', 'vgood']]
## transform all the insts in filename.pdata from 'str' to 'int'

f_pdata = loaddata.openfile(filePath + Global_V.TESTFILE + '.pdata')
all_insts_str_list = []
rownum = 0

# split each inst
for each_line in f_pdata:
    all_insts_str_list.append(list(map(str, each_line.strip().split(','))))
    rownum += 1

print "continuous_features:", continuous_features
print "<----------------------------------------------------->"




# Think about how to improve !!!!!!!!!!
X=[]
y=[]
for each_ele in all_insts_str_list:
    y.append(float(each_ele[-1]))
    temp = []
    for index_cf, each_column in enumerate(continuous_features):
        temp.append(float(each_ele[each_column]))
    X.append(temp)

X_disc = discretizationer.fit_transform(X,y)
X_disc = X_disc.tolist()
for index_X, each_inst in enumerate(X_disc):
    X_disc[index_X] = map(int, each_inst)
# print X_disc
cut_dict = discretizationer.cut_points_
X_attr_count = []
for each in cut_dict:
    X_attr_count.append(len(cut_dict[each])+1)
print X_attr_count


for index_val, each in enumerate(each_attrVal_array):
    for index_val_disc, each_val_disv in enumerate(X_attr_count):
        for each_col in continuous_features:
            if index_val_disc == each_col:
                each_attrVal_array[each_col] = list(range(0,X_attr_count[index_val_disc]))

# add the discreted 'X_disc' to all_inst_str_list
for index_inst, each_inst in enumerate(all_insts_str_list):
    for index_inst_col, each_ele in enumerate(each_inst):
        for index_cf, each_col in enumerate(continuous_features):
            if index_inst_col == each_col:
                all_insts_str_list[index_inst][index_inst_col] = X_disc[index_inst][index_cf]








all_insts_num_list = []
for each_inst_str in all_insts_str_list:
    attCount = 0
    each_inst_num = []
    for each_element in each_inst_str:
        each_inst_num.append(each_attrVal_array[attCount].index(each_element))
        attCount += 1
    all_insts_num_list.append(each_inst_num)
f_pdata.close()
random.shuffle(all_insts_num_list)  # 重要！ 这里打乱了all_insts_num_list 的顺序，以防止训练集和测试集有规律的排序（这样会严重影响结果！）

# all_insts_num_list
# [[0, 0, 0, 0, 0, 0, 0],
#  [0, 0, 0, 0, 0, 1, 0],
#  [0, 0, 0, 0, 0, 2, 0],
#  [0, 0, 0, 0, 1, 0, 0],
#  [0, 0, 0, 0, 1, 1, 0],
#  [0, 0, 0, 0, 1, 2, 0],
#  [0, 0, 0, 0, 2, 0, 0],
#  [0, 0, 0, 0, 2, 1, 0],
#  [0, 0, 0, 0, 2, 2, 0]]
# save the all_insts_num_list as pickle  (data_pickle)

all_insts_num_list_pkl = open('./pickleFile/' + fileName + '_insts_list_file.pkl', 'wb')
pickle.dump(all_insts_num_list, all_insts_num_list_pkl)
all_insts_num_list_pkl.close()

each_attrVal_array_pkl = open('./pickleFile/' + fileName + '_each_attrVal_array.pkl', 'wb')
pickle.dump(each_attrVal_array, each_attrVal_array_pkl)
each_attrVal_array_pkl.close()

# check whether all instances are transformed
print('column:  ', ranknum, '\n', 'row:   ', rownum)