import speedtest  
import pandas as pd

  
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
    #up = findUpload()
    down = findDownload()
    lst = []
    for i in range(time,time+10000):
        lst.append([down,i])
    newDF = pd.DataFrame(lst,columns=["down","time"])
    if df.empty:
        return newDF
    
    df = pd.concat([df,newDF])
    return df

