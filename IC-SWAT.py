import numpy as np
import pandas as pd
import datetime
import copy
import math
import sys
import os
import glob
sys.setrecursionlimit(10000)
sys.getrecursionlimit()

dirPath = r'C:\Users\yezouhua\Desktop\master\胶体\栅格模型\数据\csv'
swaPPath = r'D:\Study\PAPRE2\DATA\DaNingSWAT\Scenarios\CUP\CUP1.Sufi2.SwatCup'


def swat(paraDict):
    def SWAPParameterChange(TheFileDir, TheValue, TheLineNo, TheStartSpaceNo, TheSpaceLenght):
        # Read, save in a library, delete
        File = open(TheFileDir, "r")  # open the file
        lines = File.readlines()  # Read lines
        Lines = {}
        for i in range(1, len(lines) + 1):
            Lines[i] = lines[i - 1]  # Lines copy lines and order it from 1
        File.close()
        os.remove(TheFileDir)  # remove the file
        TheNewValue = ""
        TheNewValue += str(round((TheValue), 4)).rjust(TheSpaceLenght, " ")
        # Change the line
        firsPPart = Lines[TheLineNo][:TheStartSpaceNo] + TheNewValue
        secondpart = Lines[TheLineNo][len(firsPPart):]
        Lines[TheLineNo] = firsPPart + secondpart
        # rewrite the file
        File = open(TheFileDir, "w")
        for i in range(1, len(Lines) + 1):
            File.write(Lines[i])
        File.close()
    PSP = paraDict['PSP']
    SWAPParameterChange(swaPPath+r'\basin.bsn', PSP, 33, 12, 5)
    CMN = paraDict['CMN']
    SWAPParameterChange(swaPPath+r'\basin.bsn', CMN, 27, 10, 7)
    RSDCO = paraDict['RSDCO']
    SWAPParameterChange(swaPPath+r'\basin.bsn', RSDCO, 34, 12, 5)
    PPERCO = paraDict['PPERCO']
    SWAPParameterChange(swaPPath+r'\basin.bsn', PPERCO, 31, 11, 6)
    SOL_BD = paraDict['SOL_BD']
    for path in glob.glob(os.path.join("./", '*.sol')):
        SWAPParameterChange(path, SOL_BD, 9, 36, 4)
    SOL_CBN = paraDict['SOL_CBN']
    for path in glob.glob(os.path.join("./", '*.sol')):
        SWAPParameterChange(path, SOL_CBN, 12, 36, 4)
    CLAY = paraDict['CLAY']
    for path in glob.glob(os.path.join("./", '*.sol')):
        SWAPParameterChange(path, CLAY, 14, 35, 4)
    SOL_AWC = paraDict['SOL_AWC']
    for path in glob.glob(os.path.join("./", '*.sol')):
        SWAPParameterChange(path, SOL_AWC, 10, 36, 4)
    RSDIN = paraDict['RSDIN']
    for path in glob.glob(os.path.join("./", '*.hru')):
        SWAPParameterChange(path, RSDIN, 12, 12, 5)
    os.system(swaPPath + r'\SWAT.exe')
    PP_pre = 0
    SY_pre = 0
    # ouPPut extract  -> here is an example , the PP_pre and SY_pre should be extracted here and make it a .tif file
    SYDF = pd.read_csv(r'yourSY.csv',index_col=0).values.tolist()
    concDF = pd.read_csv(r'yourConc.csv',index_col=0).values.tolist()
    ICDF = pd.read_csv(r'yourIC.csv',index_col=0).values.tolist()
    ICMax = np.max(ICDF)
    for y in range(0,len(ICDF)):
        for x in range(0,len(ICDF)):
            SDR = ICMax / (1+math.exp((paraDict['IC0']-ICDF[y][x])/paraDict['kIC']))
            SY_pre += SYDF[y][x]*SDR
            PP_pre += SYDF[y][x]*SDR*0.0001*math.exp(2-0.2*math.log(SYDF[y][x]))*concDF[y][x]
    return PP_pre,SY_pre
# your observe data here
PP_obs = []
SY_obs = []
monList = []
def r2(obs, pre):
    fenMu1 = 0
    fenMu2 = 0
    fenZi = 0
    obsMean = np.mean(obs)
    preMean = np.mean(pre)
    for i in range(0, len(obs)):
        fenZi += (obs[i] - obsMean) * (pre[i] - preMean)
        fenMu1 += abs(obs[i] - obsMean) ** 2
        fenMu2 +=  abs(pre[i] - preMean) ** 2
    fenMu = (fenMu1**0.5)*(fenMu2**0.5)
    return -(fenZi / fenMu) ** 2
def NSE(obs, pre):
    fenMu = 0
    fenZi = 0
    obsMean = np.mean(obs)
    for i in range(0, len(obs)):
        fenZi += (pre[i] - obs[i]) ** 2
        fenMu += (obs[i] - obsMean) ** 2
    print('NSE:', 1 - fenZi / fenMu)
    return -(1 - fenZi / fenMu)
def PP_R2(PSP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
    r2List = []
    time = 0
    for PSP, SOL_SOLP, SOL_ORGP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0 in zip(
              PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
        time += 1
        paraDict = {
            'PSP': PSP,  # 0.01-0.7
            'RSDIN': RSDIN,  # 0-10000
            'SOL_BD': SOL_BD,  # 0.9-2.5
            'SOL_CBN': SOL_CBN,  # 0.05-10
            'CMN': CMN,  # 0.001-0.003
            'CLAY': CLAY,  # 0-100
            'SOL_AWC': SOL_AWC,  # 0-1
            'RSDCO': RSDCO,  # 0.02-0.1
            'RSDCO_PL': RSDCO_PL,  # 0.01-0.099
            'PPERCO': PPERCO,  # 10-17.5
            'kIC': kIC,
            'IC0': IC0
        }
        PP_pre,SY_pre = swat(paraDict)
        r2List.append(r2(PP_obs, PP_pre))
    return r2List
def PP_NSE(PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
    NSEList = []
    time = 0
    for PSP, SOL_SOLP, SOL_ORGP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0 in zip(
              PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
        time += 1
        # a set of parameters
        paraDict = {
            'PSP': PSP,  # 0.01-0.7
            'RSDIN': RSDIN,  # 0-10000
            'SOL_BD': SOL_BD,  # 0.9-2.5
            'SOL_CBN': SOL_CBN,  # 0.05-10
            'CMN': CMN,  # 0.001-0.003
            'CLAY': CLAY,  # 0-100
            'SOL_AWC': SOL_AWC,  # 0-1
            'RSDCO': RSDCO,  # 0.02-0.1
            'RSDCO_PL': RSDCO_PL,  # 0.01-0.099
            'PPERCO': PPERCO,  # 10-17.5
            'kIC':kIC,
            'IC0':IC0
        }
        PP_pre,SY_pre = swat(paraDict)
        NSEList.append(NSE(PP_obs, PP_pre))
    return NSEList


def SY_R2(PSP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
    r2List = []
    time = 0
    for PSP, SOL_SOLP, SOL_ORGP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0 in zip(
              PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
        time += 1
        paraDict = {
            'PSP': PSP,  # 0.01-0.7
            'RSDIN': RSDIN,  # 0-10000
            'SOL_BD': SOL_BD,  # 0.9-2.5
            'SOL_CBN': SOL_CBN,  # 0.05-10
            'CMN': CMN,  # 0.001-0.003
            'CLAY': CLAY,  # 0-100
            'SOL_AWC': SOL_AWC,  # 0-1
            'RSDCO': RSDCO,  # 0.02-0.1
            'RSDCO_PL': RSDCO_PL,  # 0.01-0.099
            'PPERCO': PPERCO,  # 10-17.5
            'kIC': kIC,
            'IC0': IC0
        }
        PP_pre,SY_pre = swat(paraDict)
        r2List.append(r2(SY_obs, SY_pre))
    return r2List


def SY_NSE(PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
    NSEList = []
    time = 0
    for PSP, SOL_SOLP, SOL_ORGP, RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0 in zip(
              PSP,  RSDIN, SOL_BD, SOL_CBN, CMN, CLAY, SOL_AWC, RSDCO, RSDCO_PL, PPERCO,kIC,IC0):
        # 保存每一组参数得到的结果
        time += 1
        # 一组参数
        paraDict = {
            'PSP': PSP,  # 0.01-0.7
            'RSDIN': RSDIN,  # 0-10000
            'SOL_BD': SOL_BD,  # 0.9-2.5
            'SOL_CBN': SOL_CBN,  # 0.05-10
            'CMN': CMN,  # 0.001-0.003
            'CLAY': CLAY,  # 0-100
            'SOL_AWC': SOL_AWC,  # 0-1
            'RSDCO': RSDCO,  # 0.02-0.1
            'RSDCO_PL': RSDCO_PL,  # 0.01-0.099
            'PPERCO': PPERCO,  # 10-17.5
            'kIC':kIC,
            'IC0':IC0
        }
        PP_pre,SY_pre = swat(paraDict)
        NSEList.append(NSE(SY_obs, SY_pre))
    return NSEList




import autograd.numpy as anp
from pymoo.core.problem import Problem
import numpy as np

start1 = datetime.datetime.now()

class MyProblem(Problem):
    def __init__(self):
        super().__init__(n_var=12,  # variables
                         n_obj=4,  # objectives
                         n_constr=0,
                         xl=anp.array(
                             [0.01,  0, 1.2, 3, 0.001, 90, 0, 0.02, 0.01, 10, 0, 0]),  # down
                         xu=anp.array(
                             [0.5,  10000, 1.9, 4, 0.003, 100, 1, 0.1, 0.099, 12, 1, 1]),  # up
                         )

    def _evaluate(self, x, out, *args, **kwargs):

        f1 = PP_R2(x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4], x[:, 5], x[:, 6], x[:, 7], x[:, 8], x[:, 9], x[:, 10],x[:, 11])

        f2 = PP_NSE(x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4], x[:, 5], x[:, 6], x[:, 7], x[:, 8], x[:, 9], x[:, 10],x[:, 11])

        f3 = SY_R2(x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4], x[:, 5], x[:, 6], x[:, 7], x[:, 8], x[:, 9], x[:, 10],x[:, 11])

        f4 = SY_NSE(x[:, 0], x[:, 1], x[:, 2], x[:, 3], x[:, 4], x[:, 5], x[:, 6], x[:, 7], x[:, 8], x[:, 9], x[:, 10],x[:, 11])

        # todo
        out["F"] = anp.column_stack([f1,f2,f3,f4])


from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.factory import get_sampling, get_crossover, get_mutation
from pymoo.optimize import minimize

# NSGA-3
algorithm = NSGA3(
    pop_size=40,
    n_offsprings=10,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True
)

# resolve eq
res = minimize(MyProblem(),
               algorithm,
               ('n_gen', 500),
               seed=1,
               return_least_infeasible=True,
               verbose=True
               )
from pymoo.config import Config

Config.show_compile_hint = False
print('res.X', res.X)
print('res.F', res.F)  # result

end1 = datetime.datetime.now()
