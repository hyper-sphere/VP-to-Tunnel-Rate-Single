import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
import pandas as pd
import os
from ..File_Handling.CSV_Handling import GetData_CSV
from ..Functions.Basic_Functions import timestamp


DEG = {'diss': 2, 'freq': 2}
FACTOR = 20
plt.close('all')

def CreatePlot(COLORS):

    dissColor, freqColor = COLORS
    fig, (axDISS, axFREQ) = plt.subplots(1, 2, figsize=(15, 6))
    fig.subplots_adjust(bottom=0.2)

    # Setup for axDISS
    axDISS.set_xlabel('Bias [V]')
    axDISS.set_ylabel('Diss. [V]')
    dataLineDISS, = axDISS.plot([0], [0], label='Raw Data', color=dissColor)
    polyLineDISS, = axDISS.plot([0], [0], label=f'Poly Fit (Deg = {DEG["diss"]})', color='orange')
    axDISS.legend(loc='upper right')

    # Setup for axFREQ
    axFREQ.set_xlabel('Bias [V]')
    axFREQ.set_ylabel('Freq. [V]')
    dataLineFREQ, = axFREQ.plot([0], [0], label='Raw Data', color=freqColor)
    polyLineFREQ, = axFREQ.plot([0], [0], label=f'Poly Fit (Deg = {DEG["freq"]})', color='orange')
    axFREQ.yaxis.tick_right()
    axFREQ.yaxis.set_label_position('right')
    axFREQ.legend(loc='upper right')

    return (fig, axDISS, axFREQ, dataLineDISS, polyLineDISS, dataLineFREQ, polyLineFREQ)


def CreateSlider(ax, label, valmin, valmax, valstep, valinit):
    return Slider(ax=ax, label=label, valmin=valmin, valmax=valmax, valstep=valstep, valinit=valinit)


class VIEWER:

    def __init__(self, FILE_PATH, PLOT_PARAMS, SLIDERS, DEG):
        
        self.file_path = FILE_PATH
        self.plot_params = PLOT_PARAMS
        self.sliders = SLIDERS
        
        self.plotXY(chan='diss', dataline=self.plot_params['dataLineDISS'] )
        self.plotXY(chan='freq', dataline=self.plot_params['dataLineFREQ'] )

        self.setRange(chan='diss', axis=self.plot_params['axDISS'])
        self.setRange(chan='freq', axis=self.plot_params['axFREQ'])

        fileName = os.path.basename(self.file_path).split(".csv")[0]
        self.plot_params['axDISS'].set_title(f'{fileName} (DISS) ')
        self.plot_params['axFREQ'].set_title(f'{fileName} (FREQ) ')

    def getXY(self, chan):
        return ( GetData_CSV(self.file_path, channel= 'bias'), 
                 GetData_CSV(self.file_path, channel= chan) )

    def setRange(self, chan, axis):

        x, y = self.getXY(chan)

        a   = 0.1
        
        dx, dy = ( max(x) - min(x) ), ( max(y) - min(y) )
        axis.set_xlim( min(x) - a*dx, max(x) + a*dx)
        axis.set_ylim( min(y) - a*dy, max(y) + a*dy )


    def plotXY(self, chan, dataline, factor=FACTOR): 

        X, Y = self.getXY(chan)
        
        if(factor >= 10): X, Y = X[::factor], Y[::factor]

        dataline.set_xdata(X)
        dataline.set_ydata(Y)


    def degSliderDISS_func(self, event): self.plotPolyDISS(self.plot_params['polyLineDISS'])
    def degSliderFREQ_func(self, event): self.plotPolyFREQ(self.plot_params['polyLineFREQ'])

    def plotPolyDISS(self, polyline): 

        DEG['diss'] = self.sliders['deg_sliderDISS'].val

        X, Y = self.getXY(chan='diss')

        p = np.polyfit( X, Y, self.sliders['deg_sliderDISS'].val )
        p = np.poly1d(p)

        polyline.set_xdata( X )
        polyline.set_ydata( p( X ) )
        polyline.set_label(f"Poly Fit (Deg = {self.sliders['deg_sliderDISS'].val})" )
        self.plot_params['axDISS'].legend(loc='upper right')

        self.plot_params['fig'].canvas.draw_idle()

    def plotPolyFREQ(self, polyline): 

        DEG['freq'] = self.sliders['deg_sliderFREQ'].val

        X, Y = self.getXY(chan='freq')

        p = np.polyfit( X, Y, self.sliders['deg_sliderFREQ'].val )
        p = np.poly1d(p)

        polyline.set_xdata( X )
        polyline.set_ydata( p( X ) )
        polyline.set_label(f"Poly Fit (Deg = {self.sliders['deg_sliderFREQ'].val})" )
        self.plot_params['axFREQ'].legend(loc='upper right')

        self.plot_params['fig'].canvas.draw_idle()

                 
def AfterClosingPlot(event): 
    print('Polynomial Degrees Used:', DEG)
    timestamp()
       
        
def PolyFit(FILE_PATH, COLORS):

    dissColor, freqColor = COLORS
    fig, axDISS, axFREQ, dataLineDISS, polyLineDISS, dataLineFREQ, polyLineFREQ = CreatePlot(COLORS)

    PLOT_PARAMS = {
        'fig': fig, 
        'axDISS': axDISS, 
        'axFREQ': axFREQ, 
        'dataLineDISS': dataLineDISS,
        'polyLineDISS': polyLineDISS,
        'dataLineFREQ': dataLineFREQ,
        'polyLineFREQ': polyLineFREQ
    }
    
    axdegDISS = fig.add_axes([0.13, 0.05, 0.34, 0.03])
    deg_sliderDISS = CreateSlider(axdegDISS, 'Deg', 0, 10, 1, DEG['diss'])

    axdegFREQ = fig.add_axes([0.56, 0.05, 0.33, 0.03])
    deg_sliderFREQ = CreateSlider(axdegFREQ, 'Deg', 0, 10, 1, DEG['freq'])
    
    SLIDERS = {
        'deg_sliderDISS': deg_sliderDISS, 
        'deg_sliderFREQ': deg_sliderFREQ, 
    }
    
    
    Viewer = VIEWER(FILE_PATH, PLOT_PARAMS, SLIDERS, DEG)
    
    deg_sliderDISS.on_changed(Viewer.degSliderDISS_func)
    deg_sliderFREQ.on_changed(Viewer.degSliderFREQ_func)
    
    fig.canvas.mpl_connect('close_event', AfterClosingPlot)

    plt.show()
    

    
##################################################################################



def RemoveBackground(FILE_PATH, DEGREE=DEG):

    for key in ['diss', 'freq']:

        X = GetData_CSV(FILE_PATH, channel='bias')
        Y = GetData_CSV(FILE_PATH, channel=key)
        Y_fitted = Y - np.poly1d(np.polyfit(X, Y, DEGREE[key]))(X)

        newdf = pd.read_csv(FILE_PATH)

        fitted_column_name = f'Fitted {key}'
        if fitted_column_name in newdf.columns:
            newdf[fitted_column_name] = Y_fitted  # Update the column if it exists
        else:
            newdf.insert(loc=(newdf.shape[1]), column=fitted_column_name, value=Y_fitted)  # Insert new column

        newdf.to_csv(FILE_PATH, index=False)

        del newdf  
    
    
    
   