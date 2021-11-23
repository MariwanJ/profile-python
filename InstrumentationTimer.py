#
# Basic instrumentation profiler by Cherno

# Usage: include this header file somewhere in your code (eg. precompiled header), and then use like:
#
# Instrumentor::Get().BeginSession("Session Name");        // Begin session
# {
#     InstrumentationTimer timer("Profiled Scope Name");   // Place code like this in scopes you'd like to include in profiling
#     // Code
# }
# Instrumentor::Get().EndSession();                        // End Session
#
# You will probably want to macro-fy this, to switch on/off easily and use things like __FUNCSIG__ for the profile name.
#

import datetime
import time
import threading
import sys
from dataclasses import dataclass

#Struct in cpp


class ProfileResult(object):
    def __init__(self):
        # instance fields found by C++ to Python Converter:
        self.Name = ""
        self.Start = 0
        self.End = 0
        self.ThreadID = 0

#Struct in cpp


class InstrumentationSession(object):

    def __init__(self):
        # instance fields found by C++ to Python Converter:
        self.Name = ""


class Instrumentor(object):
    def __init__(self):
        # instance fields found by C++ to Python Converter:
        self.__m_CurrentSession = None
        self.__m_OutputStream = None
        self.__m_ProfileCount = 0
        self.current = self

    def BeginSession(self, name, filepath="results.json"):
        print("BeginSession")
        self.__m_OutputStream = open(filepath, "a")
        self.WriteHeader()
        self.__m_CurrentSession = InstrumentationSession()
        self.__m_CurrentSession.name = name

    def EndSession(self):
        print("EndSession")
        self.WriteFooter()
        #self.__m_OutputStream.close()
        del self.__m_CurrentSession
        self.__m_CurrentSession = None
        self.__m_ProfileCount = 0
        self.current = None

    def WriteProfile(self, result):
        print("WriteProfile")
        if self.__m_ProfileCount > 0:
            self.__m_OutputStream.write(",")

        self.__m_ProfileCount += 1
        name = result.Name
        name.replace('"', '\'')
        self.__m_OutputStream.write("{")
        self.__m_OutputStream.write("\"cat\":\"function\",")
        self.__m_OutputStream.write(
            "\"dur\":" + str(result.End - result.Start) + ',')
        self.__m_OutputStream.write("\"name\":\"" + name + "\",")
        self.__m_OutputStream.write("\"ph\":\"X\",")
        self.__m_OutputStream.write("\"pid\":0,")
        self.__m_OutputStream.write("\"tid\":" + str(result.ThreadID) + ",")
        self.__m_OutputStream.write("\"ts\":" + str(result.Start))
        self.__m_OutputStream.write("}")
        self.__m_OutputStream.flush()

    def WriteHeader(self):
        print("writeHeader")
        self.__m_OutputStream.write("{\"otherData\": {},\"traceEvents\":[")
        self.__m_OutputStream.flush()

    def WriteFooter(self):
        print("writeFooter")
        self.__m_OutputStream.write("]}")
        self.__m_OutputStream.flush()

class InstrumentationTimer():
    def __init__(self, name):
        # instance fields found by C++ to Python Converter:
        self.__m_Stopped = False
        self.__m_Name = name
        self.__m_StartTimepoint = time.time_ns()
        self.current=None

    def __del__(self):
        print("Destructor")
        if not self.__m_Stopped:
            self.StopIt()

    def StopIt(self):
        print("stopit")
        endTimepoint = time.time_ns()

        start = self.__m_StartTimepoint
        end = endTimepoint
        threadID = threading.current_thread().ident
        pro = ProfileResult()
        pro.Name = self.__m_Name
        pro.Start = start
        pro.End = end
        pro.ThreadID = threadID
        self.current.WriteProfile(pro)
        self.__m_Stopped = True
