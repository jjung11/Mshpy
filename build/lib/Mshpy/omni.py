import numpy as np
import matplotlib.pyplot as plt
from sunpy.net import Fido, attrs as a
from sunpy.timeseries import TimeSeries
from sunpy.time import TimeRange
from datetime import datetime,timedelta
from sys import argv

def main(run,ts,te):
#    t0=datetime.strptime(ts,'%Y-%m-%dT%H:%M')
#    t1=t0+timedelta(days=1)

    dataset=a.cdaweb.Dataset('OMNI_HRO2_1MIN')
    result=Fido.search(a.Time(ts,te),dataset)
    downloaded_files=Fido.fetch(result[0])

    omni=TimeSeries(downloaded_files,concatenate=True)
    tr=TimeRange(ts,te)
    omni_trunc=omni.truncate(tr)

    # Convert TimeSeries to Pandas DataFrame
    df = omni_trunc.to_dataframe()
    df2=df[['YR','Day','HR','Minute','BX_GSE','BY_GSE','BZ_GSE','Vx','Vy','Vz','proton_density', 'Pressure', 'Mach_num', 'Mgs_mach_num']]
    df2.to_csv('test/omni.lst',index=False,header=None,sep='\t',na_rep='nan')

    return
#fig,ax=plt.subplots()
#plt.ion()
#omni_trunc.plot(y=['BZ_GSE'],axes=ax)
#plt.show()

if __name__=='__main__':
    main(*argv[1:])