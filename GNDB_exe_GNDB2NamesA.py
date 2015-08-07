#-------------------------------------------------------------
#
# Name:       GNDB_exe_GNDB2NamesA.py (This should only be called from GNDB.pyt)
# Purpose:    A python-tool to work with the "Greenlandic Names Data Base" (GNDB) and NIS.
# Author:     Martin Hvidberg
# e-mail:     mahvi@gst.dk, Martin@Hvidberg.net
# Created:    2014-09-16
# Copyright:  CopyLeft - I want my humble inventions to be freely available to others ...
# ArcGIS ver: 10.2.0 .. 10.3.0
# Python ver: 2.7.3 .. 2.7.8
#
# Error numbers strategy:
#    1xx : Fundamental program logic fails
#    2xx : Something 'fishy' with the input data ...
#
# History
#    Ver. 0.4.0 - Initial Build on top of GNDB_execute.py ver 0.3.x
#
# ToDo
#    Look for XXX in the code
#
#-------------------------------------------------------------

import sys

import arcEC

import GNDB_constants

# ====== Helper functions =====================================================


# ====== Individual Tools Execute functions ===================================

def GNDBruninTOC_execute(parameters, messages):
    return 0
    # *** End of function GNDBruninTOC()

if __name__ == "__main__":
    # This allows the 'executes' to be called from classic .tbx
    parameters = [arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2), arcpy.GetParameterAsText(3)]
    messages = []
    result = GNDBruninTOC_execute(parameters, messages)

# *** End of Script ***

# Music that accompanied the coding of this script:
#   Kid Creole & the Coconuts - Tropical gangster
