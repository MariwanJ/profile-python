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

#Struct in cpp


class ProfileResult(object):
    def __init__(self):
        # instance fields found by C++ to Python Converter:
        self.Name = ""
        self.Start = 0
        self.End = 0
        self.ThreadID = 0

#Struct in cpp



class Instrumentor():
    def __init__(self):
        # instance fields found by C++ to Python Converter:
        self.__m_CurrentSessionName = None
        self.__m_OutputStream = None
        self.__m_ProfileCount = 0

        self.__m_CurrentSessionName = None
        self.__m_ProfileCount = 0

    def BeginSession(self, name, filepath="results.json"):
        self.__m_OutputStream = open(filepath, "a")
        self.WriteHeader()
        self.__m_CurrentSessionName = name
    
    def EndSession(self):
        self.WriteFooter()
        self.__m_CurrentSessionName = None
        self.__m_ProfileCount = 0

    def WriteProfile(self, result):
        if self.__m_ProfileCount > 0:
            self.__m_ProfileCount += 1
            self.__m_OutputStream.write(",")
        else:
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
        self.__m_OutputStream.write("{\"otherData\": {},\"traceEvents\":[")
        self.__m_OutputStream.flush()

    def WriteFooter(self):
        self.__m_OutputStream.write("]}")
        self.__m_OutputStream.flush()
        self.__m_OutputStream.close()


class InstrumentationTimer():
    def __init__(self, name):
        # instance fields found by C++ to Python Converter:
        self.__m_Name = '\0'
        self.__m_StartTimepoint =  time.time_ns()
        self.__m_Stopped = False

        self.__m_Name = name
        self.__m_Stopped = False
        self.__m_StartTimepoint = time.time_ns()
        self.instrumentation = Instrumentor()
        self.instrumentation.BeginSession(self.__m_Name)

    def StopIt(self):
        endTimepoint = time.time_ns()

        start = self.__m_StartTimepoint
        end = endTimepoint

        threadID = threading.current_thread().ident
        pro = ProfileResult()
        pro.Name = self.__m_Name
        pro.Start = start
        pro.End = end
        pro.ThreadID = threadID

        self.instrumentation.WriteProfile(pro)
        self.__m_Stopped = True
        self.instrumentation.EndSession()
