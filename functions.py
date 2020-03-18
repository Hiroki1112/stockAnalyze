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


class loadAndSaveData:
    #データの読み込み
    def __init__(self,stockPrice,stockData,transactionData,financialData):
        #self.current = pd.read_csv('../data/currentData.csv')
        self.stockPrice = stockPrice
        self.stockData = stockData
        self.transactionData = transactionData
        self.financialData = financialData
    
    def saveNikkeiTOPIX(self,df):
        df = df[df['市場']=='東証']
        Nikkei = pd.read_csv('../stockdata/NikkeiTOPIX.csv')
        Nikkei = pd.concat([Nikkei,df],sort=True)
        Nikkei.to_csv('../stockdata/NikkeiTOPIX.csv')
    
    def dataPreProcessing(self,df,props=0):
        
        if props == 1:
            #株価データに含まれるデータを別で保存
            self.saveNikkeiTOPIX(df)
            
        #日銀、TOPIX、日経平均の削除
        
        df = df[df['市場'].isin(['東証一部', 'JQS', 'JQG', '東証マザ', '東証二部', '名証二部', '札証アンビ', '札証',
       '福証', '名証セント', '福証QB', '名証一部'])]
        
        #重複列の削除
        if props == 1:
            df = df.drop(['名称','時価総額(百万円)','高値日付','年初来高値','安値日付','年初来安値'],axis=1)
            
        elif props == 2:
            df = df.drop(['名称','市場','業種'],axis=1)
        
        return df
    
    def margeData(self,df1,df2,df3,df4):
        
        #市場を統一
        df1 = self.dataPreProcessing(df1,props=1)
        df2 = self.dataPreProcessing(df2,props=2)
        
        df = pd.merge(df1,df2,on='SC')
        df = pd.merge(df,df3,on='SC')
        df = pd.merge(df,df4,on='SC')
        
        return df
    
    def main(self):
        df = self.margeData(self.stockPrice,self.stockData,self.transactionData,self.financialData)
        df.to_csv('../data/currentData.csv')
        return df 

class Analyze():
    def __init__(self,df):
        try:
            #過去データの読み込み
            self.df = df
        except:
            print("データの読み込みに失敗しました。")
            print("エラー箇所：クラス Analyze内 コンストラクタ")
    
    def todaysReport(self):
        dfCopy = self.df
        #市場ごとの売買代金
        
        #業種別平均PER
        
        #業種別平均PBR
        
        #市場別時価総額の変動
        
        #業種別時価総額の変動