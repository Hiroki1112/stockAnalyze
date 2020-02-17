import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pathlib
import os,sys,datetime
import tkinter as tk 

spPrefix = 'japan-all-stock-prices-2_'
siPrefix = 'japan-all-stock-data_'
traPrefix = 'japan-all-stock-margin-transactions'
finPrefix = 'japan-all-stock-financial-results_'
prefixList = [spPrefix,siPrefix,finPrefix,traPrefix]

class loadAndSaveData:

    def __init__(self):
        self.df = pd.read_csv("../data/StockDatas.csv")
        

    def makedir(self,dirName):
        #IPOもあるので、毎回確認する。
        #ファイルはdataディレクトリ下に保存
        os.makedirs('data/'+dirName,exist_ok=True)


    def checkFiles(self,dirName):
        files = os.listdir(dirName)
        fileNames =  [file for file in files if os.path.isfile(os.path.join(dirName, file))]
        #4ファイルを使用する。別のファイルが入っていたらエラーを出す。
        files = []
        for f in fileNames:
            for pre in prefixList:
                if pre in f:
                    files.append(f)
        
        #check file length
        if len(files) != 4:
            print('◆◇'*20)
            print('ERROR')
            print('ファイル数が不正です。\ndailyファイルを確認してください。')
            print('◆◇'*20)
        
        #print(files)
        return files

    def DataPreprocessing(self,df,props=None):
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
            #StockIndexの前処理
            #札証などは削除しておく
            df = df[df['市場'].isin(['東証一部', 'JQS', 'JQG', '東証マザ', '東証二部'])]
            deleteColumns = ['名称','市場','業種','時価総額(百万円)','高値日付','安値日付','年初来安値','年初来高値']
            df = df.drop(deleteColumns,axis=1)

            #発行済み株式数が=のものを0で埋める(尚、発行済株式数が0のものは外国株であり、使用しないので0埋めして問題ない。)
            df.loc[df["発行済株式数"]=='-',"発行済株式数"]= 0
            df.loc[df["配当利回り"]=='-',"配当利回り"]= 0
            df.loc[df["1株配当"]=='-',"1株配当"]= 0
            #PERが - の時は0で埋める。(もっと良い方法があるかも、、、)
            df.loc[df["PER（予想）"]=='-',"PER（予想）"]= 0
            df.loc[df["PBR（実績）"]=='-',"PBR（実績）"]= 0
            df.loc[df["EPS（予想）"]=='-',"EPS（予想）"]= 0
            df.loc[df["BPS（実績）"]=='-',"BPS（実績）"]= 0
            df.loc[df["単元株"]=='-',"単元株"]= 1

            df = df.astype({"発行済株式数":float,"配当利回り":float,"1株配当":float,"PER（予想）":float,
                        "PBR（実績）":float,"EPS（予想）":float,"BPS（実績）":float,"最低購入額":float,"単元株":int
                        })
            return df
        
        elif props == 2:
            #信用残等
            #基本的に - はゼロ埋め
            df.loc[df["信用買残高"]=='-',"信用買残高"]= 0
            df.loc[df["信用買残高 前週比"]=='-',"信用買残高 前週比"]= 0
            df.loc[df["信用売残高"]=='-',"信用売残高"]= 0
            df.loc[df["信用売残高 前週比"]=='-',"信用売残高 前週比"]= 0
            df.loc[df["貸借倍率"]=='-',"貸借倍率"]= 0

            df = df.astype({"信用買残高":float,"信用買残高 前週比":float,"信用売残高":float,
                            "信用売残高 前週比":float,"貸借倍率":float
                        })
            
            return df
        
        elif props == 3:
            #財務データ

            return df
            
        else:
            print('◆◇'*20)
            print('ERROR')
            print('DataPreprocessingの引数が不正です。')
            print('◆◇'*20)
        

    def returnCsv(self,FileNameList):
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
            sp = DataPreprocessing(sp,props=0)
            si = DataPreprocessing(si,props=1)
            tra = DataPreprocessing(tra,props=2)
            fin = DataPreprocessing(fin,props=3)

            return sp,si,tra,fin
        
        except:
            print('◆◇'*20)
            print('ERROR')
            print('必要ファイルがありません。\n dailyファイルを確認してください。')
            print('◆◇'*20)

    def mergeDataFrame(self,sp,si,tra,fin):
        #データのマージ
        df = pd.merge(sp,si,on='SC')
        df = pd.merge(df,tra,on='SC')
        df = pd.merge(df,fin,on='SC')

        return df

    def saveDataFrame(self,df):

        df.to_csv("../data/StockDatas.csv",header=True,Index=False)
        #数日おきに別フォルダにバックアップを取る。
        dt_now = datetime.datetime.now()
        if int(dt_now)%3 == 0:
            df.to_csv("../tmp/StockDatas.csv",header=True,Index=False)

    def saveNikkeiTOPIX(self,df):
            df = df[df['市場']=='東証']
            Nikkei = pd.read_csv('../stockdata/NikkeiTOPIX.csv')
            Nikkei = pd.concat([Nikkei,df],sort=True)
            Nikkei.to_csv('../stockdata/NikkeiTOPIX.csv')

class analyzeData:
    def __init__(self):
        self.df = pd.read_csv('../data/StockDatas.csv')
    
    def makeColumns(self):
        #値が欠損しているものもあるため、一行ずつ計算ー＞strで保存する。

        #利益率
        df_tmp = []
        for row in self.df.iteritems():
            row_tmp = []

            #利益率
            if (row["売上高(百万円)"]!= '-') and (row['当期利益(百万円)']!='-'):
                row_tmp.append(float(row["売上高(百万円)"])/float(row['当期利益(百万円)']))
            else:
                row_tmp.append('-')

            #発行済み株式数 / 出来高
            
                


        return df_tmp