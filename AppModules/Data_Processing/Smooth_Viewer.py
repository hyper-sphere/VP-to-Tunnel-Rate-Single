import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd
import os

from ..File_Handling.CSV_Handling import GetData_CSV
from ..Functions.Basic_Functions import timestamp
from .Data_Functions import smooth

W = {'diss': 2, 'freq': 2}
FACTOR = 20
plt.close('all')

def CreatePlot(COLORS):
    
    dissColor, freqColor = COLORS
    fig, (axDISS, axFREQ) = plt.subplots(1, 2, figsize=(15, 6))
    fig.subplots_adjust(bottom=0.2)

    # Setup for axDISS
    axDISS.set_xlabel('Bias [V]')
    axDISS.set_ylabel('Diss. [V]')
    axDISS.set_title(f'Data Smoothing (DISS)')
    smoothLineDISS, = axDISS.plot([0], [0], label='Smoothed Data', color=dissColor)
    axDISS.legend(loc='upper right')

    # Setup for axFREQ
    axFREQ.set_xlabel('Bias [V]')
    axFREQ.set_ylabel('Freq. [V]')
    axFREQ.set_title(f'Data Smoothing (FREQ)')
    smoothLineFREQ, = axFREQ.plot([0], [0], label='Smoothed Data', color=freqColor)
    axFREQ.yaxis.tick_right()
    axFREQ.yaxis.set_label_position('right')
    axFREQ.legend(loc='upper right')

    return (fig, axDISS, axFREQ, smoothLineDISS, smoothLineFREQ)


def CreateSlider(ax, label, valmin, valmax, valstep, valinit):
    return Slider(ax=ax, label=label, valmin=valmin, valmax=valmax, valstep=valstep, valinit=valinit)


class VIEWER:
    def __init__(self, FILE_PATH, PLOT_PARAMS, SLIDERS):
        
        self.file_path = FILE_PATH
        self.plot_params = PLOT_PARAMS
        self.sliders = SLIDERS
        
        # Initialize plot with data
        self.plotXY('Fitted diss', self.plot_params['smoothLineDISS'])
        self.plotXY('Fitted freq', self.plot_params['smoothLineFREQ'])
        
        self.setRange(chan='Fitted diss', axis=self.plot_params["axDISS"])
        self.setRange(chan='Fitted freq', axis=self.plot_params["axFREQ"])
        
        fileName = os.path.basename(self.file_path).split(".csv")[0]
        self.plot_params['axDISS'].set_title(f'{fileName} (DISS) ')
        self.plot_params['axFREQ'].set_title(f'{fileName} (FREQ) ')

    def getXY(self, chan):
        return (GetData_CSV(self.file_path, channel='bias'), 
                GetData_CSV(self.file_path, channel=chan))

    def setRange(self, chan, axis):
        
        x, y = self.getXY(chan)
        
        a = 0.1
        
        dx, dy = (max(x) - min(x)), (max(y) - min(y))
        axis.set_xlim(min(x) - a*dx, max(x) + a*dx)
        axis.set_ylim(min(y) - a*dy, max(y) + a*dy)

    def plotXY(self, chan, smoothline, factor=FACTOR):
        
        X, Y = self.getXY(chan)
        
        if(factor >= 10): X, Y = X[::factor], Y[::factor]
        
        smoothline.set_xdata(X)
        smoothline.set_ydata(self.smooth(Y, W[chan.split(" ")[1]]))

    def smooth(self, Y, window_len): return smooth(Y, window_len)

    def wSliderDISS_func(self, event): self.plotSmoothDISS(self.plot_params['smoothLineDISS'])
    def wSliderFREQ_func(self, event): self.plotSmoothFREQ(self.plot_params['smoothLineFREQ'])
        
    def plotSmoothDISS(self, smoothLine): 

        W['diss'] = self.sliders['w_sliderDISS'].val

        X, Y = self.getXY(chan='Fitted diss')

        smoothLine.set_xdata( X )
        smoothLine.set_ydata( smooth( Y, self.sliders['w_sliderDISS'].val ) )
        smoothLine.set_label(f"Smoothed Data (W = {self.sliders['w_sliderDISS'].val})" )
     
        self.plot_params['axDISS'].legend(loc='upper right')
        self.plot_params['fig'].canvas.draw_idle()
        
        
    def plotSmoothFREQ(self, smoothLine): 

        W['freq'] = self.sliders['w_sliderFREQ'].val

        X, Y = self.getXY(chan='Fitted freq')

        smoothLine.set_xdata( X )
        smoothLine.set_ydata( smooth( Y, self.sliders['w_sliderFREQ'].val ) )
        smoothLine.set_label(f"Smoothed Data (W = {self.sliders['w_sliderFREQ'].val})" )
     
        self.plot_params['axFREQ'].legend(loc='upper right')
        self.plot_params['fig'].canvas.draw_idle()
    
    
def AfterClosingPlot(event): 
    print('Smoothing Windows Used:', W)
    timestamp()
    

def SmoothFit(FILE_PATH, COLORS):
    
    fig, axDISS, axFREQ, smoothLineDISS, smoothLineFREQ = CreatePlot(COLORS)

    PLOT_PARAMS = {
        'fig': fig, 
        'axDISS': axDISS, 
        'axFREQ': axFREQ, 
        'smoothLineDISS': smoothLineDISS,
        'smoothLineFREQ': smoothLineFREQ
    }
    
    axWinDISS = fig.add_axes([0.13, 0.05, 0.34, 0.03])
    w_sliderDISS = CreateSlider(axWinDISS, 'Window', 1, 250, 1, W['diss'])

    axWinFREQ = fig.add_axes([0.56, 0.05, 0.33, 0.03])
    w_sliderFREQ = CreateSlider(axWinFREQ, 'Window', 1, 250, 1, W['freq'])

    SLIDERS = {
        'w_sliderDISS': w_sliderDISS, 
        'w_sliderFREQ': w_sliderFREQ
    }
    
    Viewer = VIEWER(FILE_PATH, PLOT_PARAMS, SLIDERS)
    
    w_sliderDISS.on_changed(Viewer.wSliderDISS_func)
    w_sliderFREQ.on_changed(Viewer.wSliderFREQ_func)
    
    fig.canvas.mpl_connect('close_event', AfterClosingPlot)

    plt.show()
    

    
##################################################################################


def SmoothData(FILE_PATH, WINDOW=W):

    for key in ['diss', 'freq']:

        X = GetData_CSV(FILE_PATH, channel='bias')
        Y = GetData_CSV(FILE_PATH, channel=key)

        Y_smooth = smooth(Y, WINDOW[key])

        newdf = pd.read_csv(FILE_PATH)

        smooth_column_name = f'Smooth {key}'
        if smooth_column_name in newdf.columns:
            newdf[smooth_column_name] = Y_smooth  # Update the column if it exists
        else:
            newdf.insert(loc=(newdf.shape[1]), column=smooth_column_name, value=Y_smooth)  # Insert new column

        newdf.to_csv(FILE_PATH, index=False)

        del newdf  

