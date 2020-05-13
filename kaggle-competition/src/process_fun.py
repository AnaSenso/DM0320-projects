import pandas as pd
import numpy as np

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.pipeline import make_pipeline

le = preprocessing.LabelEncoder()
def to_num(df):
    for col in df.columns:
        if df[col].dtype == 'O':
            df[col] = le.fit_transform(df[col])
    return df

def to_num_con(df, col, lis):
    for i,e in enumerate(lis):
        df[col].replace({e:int(i+1)},inplace=True)
    return df

def drop_outliers(df, col):
    out_minlis = list(df[df[col] > df[col].mean() + (3 * df[col].std())].index)
    out_maxlis = list(df[df[col] < df[col].mean() - (3 * df[col].std())].index)
    out = out_minlis + out_maxlis
    ndf = df.drop(index=out)
    return ndf

scaler = preprocessing.StandardScaler()
def stand(df):
    scal = scaler.fit_transform(df)
    ndf = pd.DataFrame(scal, columns=[df.columns])
    return ndf

normalizer = preprocessing.Normalizer()
def norm(df):
    norm = scaler.fit_transform(df)
    ndf = pd.DataFrame(norm, columns=[df.columns])
    return ndf

pipeline = [
    StandardScaler(),
    Normalizer(),
]

normpip = make_pipeline(*pipeline)
def stnorm(df):
    stn = normpip.fit_transform(df)
    ndf = pd.DataFrame(stn, columns=[df.columns])
    return ndf

def tocsv(arr):
    columns=['id','price']
    df = pd.DataFrame(arr)
    df = df.reset_index(level=0)
    df.columns = columns
    return (df)
