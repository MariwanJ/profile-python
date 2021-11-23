import os
import sys
import InstrumentationTimer

def maa():
    for i in range(0, 10000):
        print(i)


def main():
    inst = InstrumentationTimer.InstrumentationTimer("main")
    maa()
    inst.StopIt()
    

main()
