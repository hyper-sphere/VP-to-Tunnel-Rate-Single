import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd
import os
from scipy import sparse
from scipy.sparse.linalg import spsolve
from ..File_Handling.CSV_Handling import GetData_CSV
from .Data_Functions import baseline


def BaselineFit(baseDISS, baseFREQ, FILE_PATH, COLORS, CORRECT=False):
    
    dissColor, freqColor = COLORS
    
    # Calculating data baseline
    dissL, dissP, dissNiter = baseDISS
    freqL, freqP, freqNiter = baseFREQ
    
    BIAS = GetData_CSV(FILE_PATH, channel='bias')
    DISS = GetData_CSV(FILE_PATH, channel='diss')
    FREQ = GetData_CSV(FILE_PATH, channel='freq')

    baseDiss =  baseline(  DISS, lam=dissL, p=dissP, niter=dissNiter)
    baseFreq = -baseline( -FREQ, lam=freqL, p=freqP, niter=freqNiter)
    
    

    fig, (axDISS, axFREQ) = plt.subplots(1, 2, figsize=(15, 6))
    fig.subplots_adjust(bottom=0.2)
    
    fileName = os.path.basename(FILE_PATH).split(".csv")[0]

    # Setup for axDISS
    axDISS.set_xlabel('Bias [V]')
    axDISS.set_ylabel('Diss. [V]')
    axDISS.set_title(f'{fileName}: Baseline Fitting (DISS)')

    # Setup for axFREQ
    axFREQ.set_xlabel('Bias [V]')
    axFREQ.set_ylabel('Freq. [V]')
    axFREQ.set_title(f'{fileName}: Baseline Fitting (FREQ)')
    axFREQ.yaxis.tick_right()
    axFREQ.yaxis.set_label_position('right')
    
    lw = 2

    if(not CORRECT):

        axDISS.plot(BIAS, DISS, label='Diss.', color= dissColor, linewidth=lw )
        axFREQ.plot(BIAS, FREQ, label='Freq.', color= freqColor, linewidth=lw )

        # Showing baselines, comment out if not needed
        axDISS.plot(BIAS, baseDiss, color='gray',   label='Diss. Baseline', linestyle='--' )
        axFREQ.plot(BIAS, baseFreq, color='orange', label='Freq. Baseline', linestyle='--' )

        
    if(CORRECT):

        axDISS.plot(BIAS, DISS-baseDiss, label='Diss. Corrected', color= dissColor, linewidth=lw )
        axFREQ.plot(BIAS, FREQ-baseFreq, label='Freq. Corrected', color= freqColor, linewidth=lw )

        #axDISS.plot(BIAS, np.zeros(len(BIAS)), color=DISS_COLOR, linewidth=0.4)# linestyle='--')
        #axFREQ.plot(BIAS, np.zeros(len(BIAS)), color=FREQ_COLOR, linewidth=0.4)#linestyle='--')

        DISS, FREQ = DISS-baseDiss, FREQ-baseFreq
        
      
    if(np.nan in baseFreq): print('NaN found')
        
    axDISS.legend(loc='upper right')
    axFREQ.legend(loc='upper right')
     
    return DISS, FREQ
        
    
    
def RemoveBaseline(DISS_PARAMS, FREQ_PARAMS, FILE_PATH):
    
    
    # Calculating data baseline
    dissL, dissP, dissNiter = DISS_PARAMS
    freqL, freqP, freqNiter = FREQ_PARAMS
    
    BIAS = GetData_CSV(FILE_PATH, channel='bias')
    DISS = GetData_CSV(FILE_PATH, channel='diss')
    FREQ = GetData_CSV(FILE_PATH, channel='freq')

    baseDiss =  baseline(  DISS, lam=dissL, p=dissP, niter=dissNiter)
    baseFreq = -baseline( -FREQ, lam=freqL, p=freqP, niter=freqNiter)
    
    DISS, FREQ = DISS-baseDiss, FREQ-baseFreq
    
    data = {'diss': DISS, 'freq': FREQ}
    
    for key in ['diss', 'freq']:

        newdf = pd.read_csv(FILE_PATH)

        smooth_column_name = f'Smooth {key}'
        if smooth_column_name in newdf.columns:
            newdf[smooth_column_name] = data[key]  # Update the column if it exists
        else:
            newdf.insert(loc=(newdf.shape[1]), column=smooth_column_name, value=data[key])  # Insert new column

        newdf.to_csv(FILE_PATH, index=False)

        del newdf
    
    



















        
        
        