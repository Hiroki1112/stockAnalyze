import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib

spPrefix = 'japan-all-stock-prices-2_'
siPrefix = 'japan-all-stock-data_'
sinPrefix = 'japan-all-stock-margin-transactions'
finPrefix = 'japan-all-stock-financial-results_'
prefixList = [spPrefix,siPrefix,finPrefix,sinPrefix]

def makedir(dirName):
    #IPOもあるので、毎回確認する。
    #ファイルはdataディレクトリ下に保存
    os.makedirs('data/'+dirName,exist_ok=True)

def getFileName(dirName):
    #引数で受け取ったディレクトリ下にあるファイル名を返す関数
    #引数のディレクトリ下のファイル名のみリストで返す
    files = os.listdir(dirName)
    return [file for file in files if os.path.isfile(os.path.join(dirName, file))]

def checkFiles(fileNames):
    #4ファイルを使用する。別のファイルが入っていたらエラーを出す。
    files = []
    for f in fileNames:
        for pre in prefixList:
            if pre in f:
                files.append(f)
    
    if len(files) != 4:
        print('◆◇'*20)
        print('ERROR')
        print('ファイル数が不正です。\ndailyファイルを確認してください。')
        print('◆◇'*20)
    
    #print(files)
    return file

