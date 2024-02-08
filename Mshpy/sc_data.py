import numpy as np
import matplotlib.pyplot as plt
from sunpy.net import Fido, attrs as a
from sunpy.timeseries import TimeSeries
from sunpy.time import TimeRange
from sys import argv
from datetime import datetime, timedelta

def main(run,ts,te,sc):

#    t0=datetime.strptime(ts,'%Y-%m-%dT%H:%M')
#    t1=t0+timedelta(days=1)

    if sc=='cluster4':
        dataset=a.cdaweb.Dataset('C4_CP_FGM_SPIN')
        result=Fido.search(a.Time(ts,te),dataset)
        downloaded_files=Fido.fetch(result[0])
        fgm=TimeSeries(downloaded_files,concatenate=True)
        tr=TimeRange(ts,te)
        fgm_trunc=fgm.truncate(tr)
        df_fgm=fgm_trunc.to_dataframe()
        df_fgm2=df_fgm.iloc[:,1:4]
        df_fgm2.columns=['Bx','By','Bz']
        df_fgm2.index.names=['time']
        df_fgm2.to_csv(f'{run}/c4_fgm.lst')


        dataset=a.cdaweb.Dataset('C4_PP_CIS')
        result=Fido.search(a.Time(ts,te),dataset)
        downloaded_files=Fido.fetch(result[0])
        cis=TimeSeries(downloaded_files,concatenate=True)
        tr=TimeRange(ts,te)
        cis_trunc=cis.truncate(tr)
        df_cis=cis_trunc.to_dataframe()
        df_cis2=df_cis.iloc[:,[4,11,12,16,17,18]].copy()
        df_cis2.columns=['n','T_par','T_perp','Vx','Vy','Vz']
        df_cis2['Tev']=(df_cis2.T_par+df_cis2.T_perp)*1e6/(2*11600)
        df_cis3=df_cis2.drop(columns=['T_par','T_perp'])
        df_cis3.index.names=['time']
        df_cis3.to_csv(f'{run}/c4_cis.lst')
        return

if __name__=='__main__':
    main(*argv[1:])
