import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler,LabelEncoder
from sklearn.impute import SimpleImputer


def getColumnsList(df):
    return df.columns.tolist()

def getNaNIndex(df):
    df_null=df.isnull().unstack()
    return df_null[df_null]

def encodeColumns(df,colToEncode=[]):
    encoder=LabelEncoder()
    if colToEncode!=[]:
        for col in colToEncode:
            df[col]=encoder.fit_transform(df[col])
    return df

def transformNan(df): 
    imptr=SimpleImputer(missing_values=np.NaN, strategy='mean')

    for col in  df.select_dtypes(exclude='object'):
        imptr.fit(df[col].values.reshape(-1,1))
        df[col]=imptr.transform(df[col].values.reshape(-1,1))[0:,0]

    return df

def createTestAndTrainSet(df):
    
    train_set = df.sample(frac=0.75, random_state=0)
    test_set = df.drop(train_set.index)

    return train_set,test_set

def scaleFeatures(df,colToScale):

    df[colToScale]=pd.DataFrame(StandardScaler().fit_transform(df[colToScale]))
    return df


def getDataSet(name,sep=","):

    df=pd.read_csv(name, sep=sep)
    return df