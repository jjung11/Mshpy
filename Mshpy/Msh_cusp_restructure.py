import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.interpolate import interp1d


for i in range(0,7):
    a=pd.read_csv('modeling/xz_cusp_cn_n.'+str(1200*i).zfill(6),header=None,sep='\s+',skiprows=1)
    
