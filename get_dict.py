#coding=utf-8
# get all possible model off-line
import json
import pickle

#{
# "smid":"201611251115456e2ffca144da2c7ebf9db1e37656c520617ad53333a2a06d",
# "org":"gRL4WvhlaH8030fvC5Fx",
# "os":"android",
# "model":"vivo X7",
# "ro.product.brand":"vivo",
# "abi":"arm64-v8a"
# }

Dict_os_model_cpu = {}
FILENAME = 'result_brand_model.txt'
FILEPATH = '/Users/yaya/shumei/'
f = open(FILEPATH + FILENAME)
count_has_key = 0
count_inst = 0
count_conflict = 0
for each_line in f:
    count_inst += 1
    info_list = []
    each_line.rstrip("\n")
    instance = json.loads(each_line)
    if (instance["os"] == "android"):
        if(instance.has_key("ro.product.model")):
            count_has_key += 1
            inst_key_model = instance["ro.product.model"]
#            inst_key_brand = instance["ro.product.brand"]
            inst_abi = instance["abi"]
            inst_os = instance["os"]
            if (Dict_os_model_cpu.has_key(inst_key_model) == False):
                OS_name = instance["os"]
                info_list.append(instance["os"])
                info_list.append(instance["abi"])
                Dict_os_model_cpu[inst_key_model] = info_list
            if (Dict_os_model_cpu.has_key(inst_key_model) == True):
                model_abi = Dict_os_model_cpu[inst_key_model][1]
                if (model_abi.find("arm") != -1):   # the value of key_model is a list, the 1st ele is "os", 2nd is "abi"
                    pass
                else:
                    if (model_abi.find("x86") != -1):
                        if inst_abi.find("arm") != -1: # if inst_abi include "arm"
                            count_conflict = count_conflict + 1
                            print "inst_abi", inst_abi
                            Dict_os_model_cpu[inst_key_model][1] = "arm"

# for key in Dict_os_model_cpu:
#     print key,Dict_os_model_cpu[key][1]
print count_conflict
f.close()
f_Dict_model_cpu_pkl = open("Dict_match_abi.pkl", 'wb')
pickle.dump(Dict_os_model_cpu, f_Dict_model_cpu_pkl)
f_Dict_model_cpu_pkl.close()





