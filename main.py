# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
# ***************************************************************************
# *                                                                        *
# * This file is a part of the Open Source Design456 Workbench - FreeCAD.  *
# *                                                                        *
# * Copyright (C) 2021                                                     *
# *                                                                        *
# *                                                                        *
# * This library is free software; you can redistribute it and/or          *
# * modify it under the terms of the GNU Lesser General Public             *
# * License as published by the Free Software Foundation; either           *
# * version 2 of the License, or (at your option) any later version.       *
# *                                                                        *
# * This library is distributed in the hope that it will be useful,        *
# * but WITHOUT ANY WARRANTY; without even the implied warranty of         *
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      *
# * Lesser General Public License for more details.                        *
# *                                                                        *
# * You should have received a copy of the GNU Lesser General Public       *
# * License along with this library; if not, If not, see                   *
# * <http://www.gnu.org/licenses/>.                                        *
# *                                                                        *
# * Author : Mariwan Jalal   mariwan.jalal@gmail.com                       *
# **************************************************************************

#Sample file how to use the InstrumentationTimer.

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
