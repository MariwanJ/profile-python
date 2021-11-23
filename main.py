import os
import sys
from  InstrumentationTimer import *

def maa():
    timer =InstrumentationTimer(__name__ )
    for i in range(0, 10):
        print(i)
    timer.StopIt()


def main():
    t = Instrumentor()
    t.Get(t).BeginSession(t,__name__ )
    maa()
    t.Get(t).EndSession(t)



main()
