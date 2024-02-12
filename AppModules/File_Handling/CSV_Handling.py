import os
import glob
import shutil
from tqdm import tqdm

import pandas as pd
import numpy as np
from .VP_Handling import GetData_VP, HasRetrace


def Group_VP(VP_folder):
    
    VP_unsorted = glob.glob('*.vpdata')
    if len(VP_unsorted) > 0:
        print(f'Unsorted VP Files Found: Attempting to Move [{len(VP_unsorted)}] Files')
        for file in tqdm(VP_unsorted):
            if not os.path.exists(os.path.join(VP_folder, file)):
                shutil.move(file, VP_folder)
                
                
def Check_CSV(CSV_FOLDER, FILE):

    csv_files = glob.glob(f'{CSV_FOLDER}{os.path.sep}*.csv')
    csv_files = [os.path.splitext(os.path.basename(file))[0] for file in csv_files]
    csv_files = tuple([file[::-1].split("_", 1)[1][::-1] for file in csv_files])

    return (os.path.splitext(FILE)[0] in csv_files)        


def Make_CSV(file, output_folder):

    # Reading Data
    headers, data = GetData_VP(file)
    for i in range( len(headers) ): headers[i] = headers[i].replace('"','')


    # Getting rid of unnecessary data
    blockIndex = []
    for i in range(len(headers)): 
        if('Block' in headers[i]): blockIndex.append(i)

    if(blockIndex != [] ):
        blockIndex.sort(reverse=True)
        for i in blockIndex: 
            del headers[i] 
            data = np.delete(data, i, 0 ) 

    del blockIndex


    timeIndex = []
    for i in range(len(headers)): 
        if('Time' in headers[i]): timeIndex.append(i)

    if(timeIndex != [] ):
        timeIndex.sort(reverse=True)
        for i in timeIndex: 
            del headers[i] 
            data = np.delete(data, i, 0 ) 

    del timeIndex


    biasIndex = [] 
    for i in range(len(headers)):
        if('Bias'  in headers[i]): biasIndex.append(i)

    if( len(biasIndex) > 1):
        biasIndex.sort()
        del headers[biasIndex[1]]
        data = np.delete(data, biasIndex[1], 0 )

    del biasIndex

    # Seeing if data has retrace and bias array
    biasArr = None 
    for i,h in enumerate(headers): 
        if( 'Bias' in h ): 
            biasArr = data[i]       
            break 

    if( biasArr is not None ): 

        savePath = str( os.path.join(output_folder, os.path.basename(file).split(".vpdata")[0] ) )
        if( HasRetrace(biasArr) ):

            mid = int( len(biasArr)/2 )

            data0, data1 = data.T[:mid], data.T[mid:]

            dataFrame0 = pd.DataFrame(data0, columns= headers )
            dataFrame1 = pd.DataFrame(data1, columns= headers )

            dataFrame0.to_csv(f'{ savePath }_Trace.csv', index=False)
            dataFrame1.to_csv(f'{ savePath }_ReTrace.csv', index=False)

        else: 
            dataFrame = pd.DataFrame(data.T, columns= headers )
            dataFrame.to_csv(f'{ savePath }.csv', index=False)

            
            
            
            
def GetData_CSV(FILE_PATH, channel=None):

    df   = pd.read_csv(FILE_PATH)

    headers = list(df.columns)
    data    = np.asarray(df).T
    
    if  (channel == 'bias' ): 
        indx = 0 
        for i, h in enumerate(headers): 
            if('Bias' in h ): 
                indx = i 
                break
                
        return data[indx]
            
    elif(channel == 'freq' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('ADC1' in h ): 
                indx = i 
                break
                
        return data[indx]
        
        
    elif(channel == 'amp'  ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('ADC2' in h ): 
                indx = i 
                break
                
        return data[indx]
        
    elif(channel == 'diss' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('ADC4' in h ): 
                indx = i 
                break
                
        return data[indx]
    
    
    elif(channel == 'Fitted diss' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('Fitted diss' in h ): 
                indx = i 
                break
                
        return data[indx]
    
    
    elif(channel == 'Fitted freq' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('Fitted freq' in h ): 
                indx = i 
                break
                
        return data[indx]
    
    
    elif(channel == 'Smooth diss' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('Smooth diss' in h ): 
                indx = i 
                break
                
        return data[indx]
 

    elif(channel == 'Smooth freq' ):
        indx = 0 
        for i, h in enumerate(headers): 
            if('Smooth freq' in h ): 
                indx = i 
                break
                
        return data[indx]
        
        
    else: return (headers, data)            
    
    
    
    
def GetHeaders_CSV(FILE_PATH, LIST=False):
    
    df = pd.read_csv(FILE_PATH)
    
    headers = list(df.columns)
    
    if(not LIST): return headers
    else:
        print('\nHeaders Found in File:\n')
        for h in headers: 
            print('\t-', h)
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    