import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import os,sys

spPrefix = 'japan-all-stock-prices-2_'
siPrefix = 'japan-all-stock-data_'
traPrefix = 'japan-all-stock-margin-transactions'
finPrefix = 'japan-all-stock-financial-results_'
prefixList = [spPrefix,siPrefix,finPrefix,traPrefix]

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
    return files


def saveNikkeiTOPIX(df):
    df = df[df['市場']=='東証']
    Nikkei = pd.read_csv('../stockdata/NikkeiTOPIX.csv')
    Nikkei = pd.concat([Nikkei,df],sort=True)
    Nikkei.to_csv('../stockdata/NikkeiTOPIX.csv')


def DataPreprocessing(df,props=None):
    if props == 0:
        #株価データの処理
        #日経平均、TOPIX、日銀などのデータを別で保存
        saveNikkeiTOPIX(df)
        
        #札証などは削除しておく
        df = df[df['市場'].isin(['東証一部', 'JQS', 'JQG', '東証マザ', '東証二部'])]
        
        #株価が-の時は前日終値を値として使う
        df.loc[df["株価"]=='-',"株価"] = df.loc[df["株価"]=='-',"前日終値"]
        df.loc[df["始値"]=='-',"始値"] = df.loc[df["始値"]=='-',"前日終値"]
        
        #型のキャスト
        df = df.astype({'株価':float,'始値':float,'VWAP':float,'出来高':float,'出来高率(％)':float,
                       '売買代金(千円)':float,'時価総額(百万円)':float,'値幅下限':float,'値幅上限':float,
                        '年初来高値':float,'年初来高値乖離率(％)':float,'年初来安値':float,'年初来安値乖離率(％)':float
                       })
        
        return df
        
    elif props == 1:
        #指標データの加工
        deleteColumns = ['名称','市場','業種','時価総額(百万円)','高値日付','安値日付','年初来安値','年初来高値']
        df = df.drop(deleteColumns,axis=1)
        
        #札証などは削除しておく
        df = df[df['市場'].isin(['東証一部', 'JQS', 'JQG', '東証マザ', '東証二部'])]

        #発行済み株式数が=のものを削除する。
        df = df[df["発行済株式数"]!='-']

        df = df.astype({"発行済株式数":float,"配当利回り":float,"1株配当":float,"PER（予想）":float,
                    "PBR（実績）":float,"EPS（予想）":float,"BPS（実績）":float,"最低購入額":float,"単元株":int
                    })
        df.info()
    
    elif props == 2:
        #信用残等
        pass
    
    elif props == 3:
        #財務データ
        pass
    
    else:
        print('◆◇'*20)
        print('ERROR')
        print('DataPreprocessingの引数が不正です。')
        print('◆◇'*20)
        

def returnCsv(FileNameList):
    #dailyからデータを読み込み、Dataframeとして読み込む
    try:
        for name in FileNameList:
            if spPrefix in name:
                sp = pd.read_csv('../daily/'+name)
            elif traPrefix in name:
                si = pd.read_csv('../daily/'+name)
            elif traPrefix in name:
                tra = pd.read_csv('../daily/'+name)
            elif finPrefix in name:
                fin = pd.read_csv('../daily/'+name)
        
        #データの加工を行う
        

        return sp,si,tra,fin
    
    except:
        print('◆◇'*20)
        print('ERROR')
        print('必要ファイルがありません。\n dailyファイルを確認してください。')
        print('◆◇'*20)
