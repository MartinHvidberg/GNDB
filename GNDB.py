#-------------------------------------------------------------
#
# Name:       GNDBtoolbox.pyt
# Purpose:    A python-toolbox to work with the "Greenlandic Names Data Base" (GNDB) and NIS.
# Author:     Martin Hvidberg
# e-mail:     mahvi@gst.dk, Martin@Hvidberg.net
# Created:    2014-09-16
# Copyright:  CopyLeft - I want my humble inventions to be freely available to others ...
# ArcGIS ver: 10.2.0
# Python ver: 2.7.3
#
# Error numbers strategy:
#    1xx : Fundamental program logic fails
#    2xx : Something 'fishy' with the input data ...
#
# History
#    Ver. 0.1.0 - Creating class GNDBruninTOC() 
#        Sceleton works, but no changes written to output, yet.
#        Obey Selection and obey Definition querries on input data. '141001/mahvi
#    Ver. 0.2.0 - Splitting execute() into seperate .py file
#
# ToDo
#    Look for XXX in the code
#
#-------------------------------------------------------------

strToolboxName = "GNDB toolbox"
strToolboxVer = "0.2.0"
strToolboxBuild = "141021"

from datetime import datetime # for datetime.now()

import reloader
reloader.enable()

import arcpy
import arcEC

import GNDB_executes


# ====== Main Toolbox Class ===================================================

class Toolbox(object):
    
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "The_GNDB_Toolbox"
        self.alias = "Toolbox to work with GNDB and NIS"
        self.description = "This is the description of the toolbox..."

        # List of tool classes associated with this toolbox
        self.tools = [GNDBruninTOC]
    

# ====== Individual Tools Classes =============================================

class GNDBruninTOC(object):

    """
    GNDB update NIS - assuming feature classes all ready opened in TOC
    Created on 27 Sep 2014
    @author: mahvi@gst.dk / Martin@Hvidberg.net
    
    """
    
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""   
        
        self.label = "GNDB_update_NIS_run_in_TOC"
        self.description = "This tool will update the selected NIS FC, which must be in the TOC"
        self.canRunInBackground = True # True = Obey "Background Processing setting" in the Geoprocessing Options dialog.
        
        self.strClassName = "GNDB, update NIS, run in TOC"
        self.strClassVer = "1.2.0"
        self.strClassBuild = "'141022,1504"
        
        arcEC.SetMsg("Class '"+self.strClassName+"' ver. "+self.strClassVer+" build "+self.strClassBuild,0)

    def getParameterInfo(self):
        """Define parameter definitions"""

        # 0. The Feature layer to receive GNDB names
        param0 = arcpy.Parameter(
            displayName="Input Features (feature class to put names on).",
            name="in_features",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param0.value = "(Local) NamesA"
    
        # 1. The point feature class holding the GNDB
        param1 = arcpy.Parameter(
            displayName="GNDB points",
            name="GNDB",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")    
        param1.value = "NIS.NamesP"
    
        # 2. The Mode
        param2 = arcpy.Parameter(
            displayName="The Mode",
            name="Mode",
            datatype="GPString",
            parameterType="Required",
            direction="Input")            
        param2.filter.type = "ValueList"
        param2.filter.list = ["Berit", "Test"]
        param2.value = param2.filter.list[0]
    
        # 3. Overwrite
        param3 = arcpy.Parameter(
            displayName="Overwrite Existing OBJNAM and NOBJNM",
            name="Overwrite",
            datatype="GPBoolean",
            parameterType="Optional",
            direction="Input")    
        param3.value = False       
        
        params = [param0, param1, param2, param3]
    
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

    
        reloader.reload(GNDB_executes) # Only relevant while debugging the GNDB_executes.py source
        result = GNDB_executes.GNDBruninTOC_execute(parameters, messages)
        arcEC.SetMsg("Execute() returned: "+str(result),0)
        
        return result