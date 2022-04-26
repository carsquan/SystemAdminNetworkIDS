import numpy as np
import pandas as pd
from scipy import stats

def findOutliers(df):
    q1=df.quantile(0.25)

    q3=df.quantile(0.75)

    IQR=q3-q1
    outliers = df[(np.abs(stats.zscore(df["X"])) >= 3)]

    #outliers = df[((df<(q1-1.5*IQR)) | (df>(q3+1.5*IQR)))]
    #outliers = outliers.dropna(axis=0, how='all')
    #outliers = df.dropna(axis=1).join(df.drop(labels="Time",axis=1))
    return outliers
