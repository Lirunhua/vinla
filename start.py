# coding=utf-8
# 可以通用的过程：
# 1. 交叉验证
# 2. 求 0-1 loss
from __future__ import division
import numpy as np
from sklearn.model_selection import KFold
import pickle
import Global_V
from TAN import TAN
from NB import NB
from output import estimate_Output
import DATA as DT




data_initial = pickle.load(open('./pickleFile/' + Global_V.TESTFILE + '_insts_list_file.pkl', 'rb'))
data_len = len(data_initial)
if Global_V.PRINTPAR == 3:
    print('\nThere are', data_len, 'instance in this data.\n')  # 输出数据的行数，检验数据是否载入正确
loss01 = []  # 保存每次交叉验证的01loss
data_array = np.array(data_initial)

kf = KFold(n_splits=10)
fold_count = 0

for train, test in kf.split(data_initial):
    TrainSet = DT.DataSet(data_array[train].tolist())
    TestSet = DT.DataSet(data_array[test].tolist())
    print TestSet.totalcount
    print TrainSet.totalcount

    if Global_V.SCHEME.upper() == 'TAN':
        '''
        1. 载入数据
        2. 训练数据
        3. 分类
        4. 输出结果评估
           '''
        result = []
        fold_count += 1
        print "fold", fold_count
        p_c_fold = []
        loss01_fold = 0
        TAN_data = TAN(TrainSet,TestSet)
        TAN_data.train()
        print TAN_data.parents
        p_c_fold, result_fold = TAN_data.classify()
        result.append(result_fold)
        print "-------------->Result of fold ", fold_count, "------------>"
        _, _,loss01_fold = estimate_Output(TAN_data.TestSet.data, p_c_fold, result_fold, 2)
        loss01.append(loss01_fold)
        # 每个分类的过程，必须保存：1. 每一个testdata里的instance分类到每个Ci的概率p_y    2. 分类结果：result
        # output(result, TAN_car.testData,1)    # output 函数的输入为：
        # output的输出，应该要有：1.每个testdata分到每个类的概率  2.分类结果result  3.testData，(以及参数1,2,3;不同的参数，输出不同)
        # compare the prediction results with the real results
        if Global_V.PRINTPAR == 3:
            print('testset:\n', TAN_data.TestSet.data, '\n')
            print('p_ci= \n', p_c_fold, '\n', 'result:\n', result)
            print('the first element is the result of prediction, second is real result!\n')
        if Global_V.PRINTPAR == 3:
            print('parents of each nodes(attributes):\n', TAN_data.parents, '\n')
print('\n------------>Averaged result:------------>\n', round(sum(loss01) / len(loss01), 3))



# if the schema is TAN:
# if Global_V.SCHEME.upper() == 'TAN':
#     '''
#     1. 载入数据
#     2. 训练数据
#     3. 分类
#     4. 输出结果评估
#        '''
#     result = []
#     fold_count = 0
#     for ct_count in range(0, data_len, data_len//10):   # 交叉验证
#         fold_count += 1
#         p_c_fold = []
#         loss01_fold = 0
#         TAN_data = TAN(data_initial, 0.8, ct_count)
#         TAN_data.train(TAN_data.cmi)
#         p_c_fold, result_fold = TAN_data.classify()
#         result.append(result_fold)
#         print "-------------->Result of fold " , fold_count, "------------>"
#         loss01_fold = estimate_Output(TAN_data.testData, p_c_fold, result_fold, 1)
#         loss01.append(loss01_fold)
#         # 每个分类的过程，必须保存：1. 每一个testdata里的instance分类到每个Ci的概率p_y    2. 分类结果：result
#         # output(result, TAN_car.testData,1)    # output 函数的输入为：
#         # output的输出，应该要有：1.每个testdata分到每个类的概率  2.分类结果result  3.testData，(以及参数1,2,3;不同的参数，输出不同)
#         # compare the prediction results with the real results
#         if Global_V.PRINTPAR == 3:
#             print('testset:\n', TAN_data.testData, '\n')
#             print('p_ci= \n', p_c_fold, '\n', 'result:\n', result)
#             print('the first element is the result of prediction, second is real result!\n')
#         if Global_V.PRINTPAR == 3:
#             print('parents of each nodes(attributes):\n', TAN_data.parents, '\n')
#
#     print('\n------------>Averaged result:------------>\n', round(sum(loss01)/len(loss01), 3))
#
# if Global_V.SCHEME.upper() == 'KDB':
#     pass
# if Global_V.SCHEME.upper() == 'AODE':
#     pass
# if Global_V.SCHEME.upper() == 'NB':
#     NB_data = NB(data_initial)
#     NB_data.train()
#     p_c, result = NB_data.classify()
#     estimate_Output(NB_data.testData, p_c, result, 2)
#     # 每个分类的过程，必须保存：1. 每一个testdata里的instance分类到每个Ci的概率p_y    2. 分类结果：result
#     # output(result, TAN_car.testData,1)    # output 函数的输入为：
#     # output的输出，应该要有：1.每个testdata分到每个类的概率  2.分类结果result  3.testData，(以及参数1,2,3;不同的参数，输出不同)
#     # compare the prediction results with the real results
#     if Global_V.PRINTPAR == 3:
#         print('testset:\n', NB_data.testDataSet, '\n')
#         print('p_ci= \n', p_c, '\n', 'result:\n', result)
#         print('the first element is the result of prediction, second is real result!\n')
