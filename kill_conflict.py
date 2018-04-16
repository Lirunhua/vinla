#coding=utf-8
import pickle
import json

FILENAME = 'result_brand_model.txt'
FILEPATH = '/Users/yaya/shumei/'
# FILENAME = "result.txt"
match_dict = pickle.load(open('Dict_match_abi.pkl'))

f_inst = open(FILEPATH + FILENAME)
count_killed = 0
for each_inst in f_inst:
    each_inst.rstrip("\n")
    print each_inst
    inst = json.loads(each_inst) # inst is a dict
    if inst.has_key("os") and inst.has_key("ro.product.model") and inst.has_key("abi"): #
        inst_model = inst["ro.product.model"]
        inst_abi = inst["abi"]
        if inst_abi.find("arm") != -1:  # if "arm" is found
            inst_abi = "arm"
        if inst_abi.find("x86") == -1:  # if "x86" can't find, then it may be "error" or else
            inst_abi = "null"
        supposed_abi = match_dict[inst_model]

        if inst_abi!= "null":
            if inst_abi != supposed_abi:
                count_killed = count_killed+1
                print each_inst

print count_killed