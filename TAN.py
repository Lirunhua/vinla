# coding=utf-8
# tan class;
# argument: trainDataSet
from __future__ import division
import pickle
import prim as par
import Global_V
import sys
from decimal import *
from sklearn import preprocessing
import numpy as np

getcontext().prec = 10000  # don't know how much is the max, so 10000

class TAN:
    def __init__(self, TrainSet, TestSet):
        self.TrainSet = TrainSet
        self.TestSet = TestSet
        # 如何使得self.trainDataSet, self.TestSet
        self.parents = []
        self.cmi_temp = [[0]*self.TrainSet.getNoAttr() for i in range(self.TrainSet.getNoAttr())]
        self.cmi = self.TrainSet.getCondMutInf(self.cmi_temp)  # get the cmi with the trainDataSet

    def train(self):
        # input argument: cmi, split_ratio (default: 0.9(交叉验证比例))
        # output:
        # the parents node of each attribute node;
        # the bayes structure of TAN tree      (Tree-Augmented Naive Bayes)
        self.parents = par.prim(self.cmi, len(self.cmi))  # we get the parents of each node;
                                                         # the prim is find the mintree, use -cmi to find maxtree

    def classify(self):
        # P(y(i)|X) = P(y(i)) *　ｐ(xr|y(i)) *　|¯| P(xi|par(xi),y(i))
        # for each_test_instance in range(0, self.TestSet.row):    # classify for each row in TestSet
        getcontext().prec = 100 # don't know how much is the max, so 10000

        p_y = []  # used to save P(yi|X)
        result_y = []   # save the result in each instance of the test data
        for each_test_instance in self.TestSet.data:
            p_y_each_inst = []
            for eachy in range(0, self.TrainSet.getNoClass()):
                p = Decimal(self.TrainSet.getP_yi(eachy)) * Decimal(self.TrainSet.getCondP_xi_ya(0, each_test_instance[0], eachy)) * Decimal(sys.maxsize)   # caution: it's !!!TrainSet!!!.getP_yi
                # print p                                                                                                      # here we calculate p(y_i) * p(x0|yi)
                # 后期代码应该把每一个p_yi用pickle存起来，加快速度
                for eachx in range(1, self.TrainSet.getNoAttr()):    # and here we cal from x1: P(x1|x0,yi)
                        p = Decimal(p) * Decimal((self.TrainSet.getCondP_xi_xayb(eachx, each_test_instance[eachx], self.parents[eachx], each_test_instance[self.parents[eachx]], eachy)))
                    # caution: the arguments: a1, v1, a2, v2, yi should be transform to the number
                    # not the real string attributes
                p_y_each_inst.append(p)   # 属于每个类的概率
                # print "p_y_each_inst", p_y_each_inst[1]
                # print p
                # if all the p_y_each_inst is zero, than we should deal with this situation specifically

            result_y.append(p_y_each_inst.index(max(p_y_each_inst)))  # 分类结果
            flag = True
            for each_ele in p_y_each_inst:
                if each_ele != 0:
                    flag = False
                    break
            # p_y_each_inst = self.Scaler(p_y_each_inst)
            if flag == False:
                p_y_each_inst = self.Scaler(p_y_each_inst)
            else:
                for i, each_ele in enumerate(p_y_each_inst):
                    p_y_each_inst[i] = 1 / len(p_y_each_inst)
            p_y_each_inst = map (float, p_y_each_inst)
            p_y.append(p_y_each_inst)
        #print self.Scaler(p_y)
        return p_y, result_y    # 任何classify函数都必须给出父节点序列(type: list)以及分类结果(type: list)

    def Scaler(self, x):
        x__ = []
        sum__ = sum(x)
        scale__ = 1/sum__
        for each in x:
            x__.append(each * scale__)
        return x__

if __name__ == '__main__':
    data_initial = pickle.load(open('data_list_file.pkl', 'rb'))  # data_list_file.pkl 还是原始数据，并且是字符，不是数字矩阵，不是数字！！！
    if Global_V.PRINTPAR == 3:
        print(len(data_initial))
        # data_initial_DS = DS.Dataset(data_initial)
        # trainSet, testSet = data_initial_DS.splitdataset(0.9, 90)
        # if Global_V.PRINTPAR == 3:
        #     print(len(trainSet), len(testSet))
        #
        # TrainData_DS = DS.Dataset(trainSet)
        # TestData_DS = DS.Dataset(testSet)
        # column, row = data_initial_DS.getSize()
        # # test the methods of class Dataset
        # # print('\n', , '\n')
        # if Global_V.PRINTPAR == 3:
        #     print('column:\n', column, '\n', 'row', row, '\n')
        #     print('count of class:\n', data_initial_DS.getNoClass(), '\n')
        #     print('AttrName_array:\n', data_initial_DS.getAttrName_array(), '\n')
        #     print('Number of Attributes:\n', data_initial_DS.getNoAttr(), '\n')
        #     print('Count of Attr 3: \n', data_initial_DS.getCountOfAttr_i(3), '\n')
        #     print('Count of class 2:\n', data_initial_DS.getClassCount(2), '\n')
        #     print('count of：attr(1) = 2: \n', data_initial_DS.getXCount(1, 2), '\n')
        #     print('count of:　attr(1) = 2, attr(2) = 3:\n', data_initial_DS.getXXCount(1, 2, 2, 3), '\n')
        #     print('count of: attr(2) = 1, ci = 2:\n', data_initial_DS.getXYCount(2, 1, 2), '\n')
        #
        #
        #
        #
        #
        # mi = []
        # cmi = [[0]*TrainData_DS.getNoAttr() for i in range(TrainData_DS.getNoAttr())]
        # graph = TrainData_DS.getCondMutInf(cmi)
        # if Global_V.PRINTPAR == 3:
        #     print('the mutual information of traindata is:\n', TrainData_DS.getMutualInformation(mi), '\n')
        #     print('the conditional mutual information of traindata is:\n', graph, '\n')

        # n = len(graph)
        # print(n,'\n')
        # dis, pre = par.prim(graph, n)
        # print(dis, '\n', pre)
        # 经验证，互信息的求解数值没有任何问题；在OneNote上有图片记录
        # 在设计计算预测概率的结果的时候，要记得预留得到概率的方法，这样有助于程序的拓展；
        # 分类
        # for each in [eachy[-1] for eachy in testSet]:
        # find the probality of each test instance
        # p_eachy.append(germanTestData.getClassCount(each)/germanTestData.totalcount)
        # every class in testSet
    # for each in testSet:

    TAN_car = TAN(data_initial)
    TAN_car.train()
    if Global_V.PRINTPAR == 3:
        print('parents of each nodes(attributes):\n', TAN_car.parents, '\n')
    p_c, result = TAN_car.classify()

    # 每个分类的过程，必须保存：1. 每一个testdata里的instance分类到每个Ci的概率p_y    2. 分类结果：result

    # output(result, TAN_car.testData,1)    # output 函数的输入为：
    # output的输出，应该要有：1.每个testdata分到每个类的概率  2.分类结果result  3.testData，(以及参数1,2,3;不同的参数，输出不同)
    #
    # compare the prediction results with the real results
    compare = list(zip(result, [each[-1] for each in TAN_car.testData]))
    if Global_V.PRINTPAR == 3:
        print('testset:\n', TAN_car.testData, '\n')
        print('p_ci= \n', p_c, '\n', 'result:\n', result)
        print('the first element is the result of prediction, second is real result!\n')
        print('---------------------------------compare---------------------------------\n', compare)
    right = 0
    wrong = 0
    for each in compare:
        if each[1] == each[0]:
            right += 1
        else:
            wrong += 1
    print('right:\n', right, '\n')
    print('wrong:\n', wrong, '\n')









































