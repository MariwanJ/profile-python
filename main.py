import os
import sys
from  InstrumentationTimer import *

def maa( current):
    import sys
    fn_name = sys._getframe().f_code.co_name
    Ttimer =InstrumentationTimer(fn_name )
    Ttimer.current = current
    for i in range(0, 10):
        print(i)

def main():
    
    import sys
    fn_name = sys._getframe().f_code.co_name
   # Ttimer =InstrumentationTimer(fn_name )

    t=Instrumentor()
    #t.current = t
    t.BeginSession(fn_name)
    maa(t)
    t.EndSession()




main()