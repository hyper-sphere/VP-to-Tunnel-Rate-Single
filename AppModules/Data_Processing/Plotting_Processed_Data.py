import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 


def GetData(DATA_FRAME, chan1='Smooth diss', chan2='Smooth freq'): 
    
    #print( DATA_FRAME.columns ) # 'ADC1-SP (V)' == Freq, 'ADC4 (V)' == Diss

    BIAS = np.asarray( DATA_FRAME['Bias (V)'] )
    DISS = np.asarray( DATA_FRAME[chan1] )
    FREQ = np.asarray( DATA_FRAME[chan2] )

    ###### Getting rid of NaNs from the moving-average filtering/smoothing #########
    onlyFloats = ~( np.isnan(DISS) )
    BIAS = BIAS[onlyFloats]
    DISS = DISS[onlyFloats]
    FREQ = FREQ[onlyFloats]

    onlyFloats = ~( np.isnan(FREQ) )
    BIAS = BIAS[onlyFloats]
    DISS = DISS[onlyFloats]
    FREQ = FREQ[onlyFloats]
    
    return (BIAS, DISS, FREQ)


def NewRange(BIAS, DISS, FREQ, left=-10, right=10):
    
    newRange = np.logical_and(BIAS >= left, BIAS <= right)
    
    BIAS = BIAS[newRange]
    DISS = DISS[newRange]
    FREQ = FREQ[newRange]
    
    #return (BIAS, DISS, FREQ)
    
def PlotSetup(PARAMS):
    
    fig, axDISS, axFREQ, FILE, FREQ_COLOR = PARAMS
    plotTitle = FILE.split(".csv")[0]

    plt.rcParams.update({'font.size': 35})
    plt.subplots_adjust(wspace=0.01,hspace=0)
    axDISS.set_title( f'{plotTitle}' ) 

    # Plot Formatting
    axDISS.set_ylabel('Dissipation [Hz]')
    axDISS.spines['bottom'].set_visible(False)
    axDISS.spines['right'].set_color(FREQ_COLOR)

    axFREQ.set_ylabel('Frequency Shift [Hz]', color=FREQ_COLOR)
    axFREQ.yaxis.tick_right()
    axFREQ.yaxis.set_label_position("right")
    axFREQ.tick_params(axis ='y', labelcolor= FREQ_COLOR)
    axFREQ.spines['right'].set_color(FREQ_COLOR)
    axFREQ.spines['top'].set_visible(False)
    axFREQ.set_xlabel('Bias [V]')

    
    
    
