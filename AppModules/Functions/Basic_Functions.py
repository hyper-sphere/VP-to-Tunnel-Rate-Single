import os
import time
import shutil
from tkinter import Tk, filedialog

def timestamp(OutputText='Executed'):
    current_time = time.localtime()
    formatted_time = time.strftime("%Y/%m/%d %I:%M:%S %p", current_time)
    print( f'\n{OutputText}: {str(formatted_time)}' )


def GetFile(WindowName="Select File"): 
    
    root = Tk()                       # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()                   # Hides small tkinter window.
    root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.

    filename = filedialog.askopenfilename(title=WindowName) # Returns opened path as str
    
    return filename 


def GetFolder(WindowName="Select Folder"): 
    
    root = Tk()                            # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()                        # Hides small tkinter window.
    root.attributes('-topmost', True)      # Opened windows will be active. above all windows despite of selection.
    foldername = filedialog.askdirectory(title=WindowName) # Returns opened path as str
    return foldername 


def CreateFolders(*folders):
    for folder in folders:
        if not os.path.exists(folder):
            os.mkdir(folder)

                
                
                