import re

def loaddata(stratege, filename):
    # stragege (char) : 'aode' or 'kdb'
    """load file, return a file - pointer: f"""
    stratege = str.lower(stratege)  # as the file path is lower-case, to be safe, it's necessity to lower the input.
    f = open('E:\\Bayes\data\\result-rate' +'\\'+ stratege + '\\' + filename + '.txt')
    return f

if __name__ == '__main__':
    pattern_index = re.compile(r'index:\d+')
    pattern_result = re.compile(r'result:\w')
    pattern_trueclass = re.compile(r'trueclass:\S')
    pattern_y__ = re.compile(r'y--')
    f_aode = loaddata('aode', 'abalone')
    for each in f_aode:
        # print(each)
        match_index = re.findall(pattern_index, each)
        match_result = re.findall(pattern_result, each)
        match_trueclass = re.findall(pattern_trueclass, each)
        match_y__ = re.findall(pattern_y__, each)
        # print(each)
        if match_index is not None:
            print(match_index)
        else:
            print('none')

    # print(line_temp)







