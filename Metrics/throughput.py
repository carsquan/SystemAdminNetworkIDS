import speedtest  
import pandas as pd
import datetime
import time
  
st = speedtest.Speedtest()

# Find download speed
def findDownload():
    dwn = toMB(st.download())
    print(dwn)
    return dwn

# Find upload speed
def findUpload():
    up = toMB(st.upload())
    print(up)
    return up

# Converts speed to MB
def toMB(speed):
    return round((speed/ 1048576), 2)

# Adds upload/download to the data set
def addUpDownToDF(df,time):
    time_now = datetime.datetime.now().strftime("%H:%M")
    #up = findUpload()
    down = findDownload()
    lst = [[down,time_now]]
    newDF = pd.DataFrame(lst,columns=["X","Time"])
    if df.empty:
        return newDF
    
    df.loc[len(df.index)] = [down, time_now] 
    return df

