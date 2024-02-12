import os
import glob
import shutil
import pandas as pd
import numpy as np
from tqdm import tqdm


def Group_VP(VP_folder):
    VP_unsorted = glob.glob('*.vpdata')
    if len(VP_unsorted) > 0:
        print(f'Unsorted VP Files Found: Attempting to Move [{len(VP_unsorted)}] Files')
        for file in tqdm(VP_unsorted):
            if not os.path.exists(os.path.join(VP_folder, file)):
                shutil.move(file, VP_folder)


def GetData_VP(fileName):
    
    dataFrame = pd.read_fwf(fileName, sep='\t', header=None)

    keyword = '#C Index'
    index   = 45
    for j in range(len( dataFrame[0]) ): 
        if( dataFrame[0][j].split('\t')[0] == keyword ): 
            index = j 
            break

    dataHeaders = dataFrame[0][index].split('\t')[1:]

    index  += 1
    keyword = '#C'

    data    = []  
    for j in range(index, len( dataFrame[0]) ): 
        if( dataFrame[0][j].split('\t')[0] == keyword ): break
        d = np.asarray( dataFrame[0][j].split('\t')[1:] ).astype(float)
        data.append(d)
    
    # Avoiding data without all the array values
    badIndex = []
    for i in range( len(data) ): 
        if( len( data[i] ) != len(dataHeaders) ): badIndex.append(i) 
            
    if( badIndex != [] ):
        for i in sorted(badIndex, reverse=True): del data[i]
        del badIndex 
        
    # Prepping data array 
    data = np.asarray(data).T
    data = data.astype(float)
    
    return (dataHeaders, data)



def HasRetrace(arr):
    
    split = False 
    mid   = int(len(arr)/2)
    Ml    = np.polyfit( np.arange(0, len( arr[:mid] ) ), arr[:mid], 1)[0]
    Mr    = np.polyfit( np.arange(0, len( arr[mid:] ) ), arr[mid:], 1)[0]

    if( round(Mr/Ml, 3) <= 0 ): split = True  

    return split

    

