import time
import threading
import multiprocessing
import sys
import keyboard
import mouse
import os
import numba
import warnings
import numba.core.errors

warnings.simplefilter('ignore', category=numba.core.errors.NumbaDeprecationWarning)
warnings.simplefilter('ignore', category=numba.core.errors.NumbaPendingDeprecationWarning)
warnings.simplefilter('ignore', category=numba.core.errors.NumbaWarning)

class Event:
    def __init__(self):
        global Events
        self.Flag = False #When the flag is true clicker stops
        Events.append(self)
        self.Index = len(Events)-1
    
    def SetTrue(self):
        global Events
        self.Flag = True
    
    def SetFalse(self):
        global Events
        self.Flag = False
    
    @numba.jit()
    def SetALL(self):
        global Events
        Flags = [x.Flag for x in Events]
        if any(Flags):
            for x in Events:
                sys.stdout.write(f"{Flags.count(True)}\r")
                x.SetFalse()
        else:
            for x in Events:
                sys.stdout.write(f"{Flags.count(False)}\r")
                x.SetTrue()

    def BlockingFunc(self):
        global Events
        Start = time.perf_counter()
        while True:
            time.sleep(.5)
            if time.perf_counter()-Start >= 15: #if nothing happens for 15 seconds then thread/process SHOULD end
                Events.pop(self.Index)
                return "Done"
            if not self.Flag:
                break
            
Events: list[Event] = []

#@numba.jit(nogil=True)
def F():
    FEvent = Event()
    keyboard.add_hotkey("space", lambda: threading.Thread(target=FEvent.SetALL).start())
    Start = time.perf_counter()
    while True:
        mouse.double_click()
        if FEvent.Flag:
            if FEvent.BlockingFunc() == "Done":
                Stop = time.perf_counter()
                sys.stdout.write(f"Done in {Stop-Start}\t")
                print(f"{threading.current_thread().name}")
                break
            
if __name__ == "__main__":
    import os
    threading.Thread(target=os.system, args=(f"python {os.path.dirname(__file__)}\CPSMeasurer.py",), daemon=True).start()
    TotalStart = time.perf_counter()
    L = []
    for x in range(10):
        L.append(threading.Thread(target=F))
        #L.append(multiprocessing.Process(target=F, daemon=True))
    L = tuple(L)
    print("Ready to start. Press 'space' to start and to pause/resume.\n")
    MinusAmount = time.perf_counter()
    keyboard.wait('space')
    MinusAmount = time.perf_counter()-MinusAmount
    print("Started")
    for x in L:
        x.start()
    for x in L:
        x.join()
    TotalEnd = time.perf_counter()
    print(f"\n\nTotal program time: {TotalEnd-TotalStart} ({TotalEnd-TotalStart-MinusAmount})")