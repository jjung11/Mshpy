import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from sscws.sscws import SscWs
from datetime import datetime,timedelta
from sys import argv

def main(run,ts,te,sc):
    ssc=SscWs()

    result=ssc.get_locations([sc],[ts,te])
    data=result['Data'][0]
    coords=data['Coordinates'][0]
    df=pd.DataFrame(coords)
    df['t']=data['Time']
    df['formatted_datetime']=df.t.dt.strftime('%y/%m/%d %H:%M:%S')
    df2=df[['formatted_datetime','X','Y','Z']]
    df2.loc[:,'X']/=6378.16
    df2.loc[:,'Y']/=6378.16
    df2.loc[:,'Z']/=6378.16

    df2.to_csv('test/orbit.txt',header=False,index=False,sep='\t')
    return datetime,timedelta

if __name__=='__main__':
    main(*argv[1:])
