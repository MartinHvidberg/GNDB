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
#        20x : While reading GNDB
#        21x : While reading NamesA
#    3xx : Data contains unforeseen things 
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

# ====== Helper functions =====================================================

# ====== Helper functions =====================================================

def CorrectNaming(mode, dicN):
    bGL = (str(type(dicN["Name_GL"]))=="<type 'unicode'>") and (len(dicN["Name_GL"])!=0)
    bDA = (str(type(dicN["Name_DK"]))=="<type 'unicode'>") and (len(dicN["Name_DK"])!=0)
    bEN = (str(type(dicN["Name_UK"]))=="<type 'unicode'>") and (len(dicN["Name_UK"])!=0)
        
    ### This section decides the rules for how 3 Potential names is transfered to 2 Place holders
    ### The earlier destinction beween Old and New greenlandiv spelling, is now handled by only maintaining one in GNDB
    strNameN = ""   # Name
    strNameL = ""   # Local name
    ##bolLockN = False # Unlocked by default <--- remove XXX
    ##bolLockL = False # Unlocked by default <--- remove XXX
    numS = 999  # Return code. 0 = Success
    if mode == "Berit":
        if bGL: # If Greenlandic name exists
            strNameN = dicN["Name_GL"]
            if bDA: # If Danish name exists
                strNameL = dicN["Name_DK"]
            elif bEN: # If English name exists
                strNameL = dicN["Name_UK"]
            numS = 0
        elif bDA: # If Danish name exists
            strNameN = dicN["Name_DK"]
            if bEN: # English name exists
                strNameL = dicN["Name_UK"]
            numS = 0
        elif bEN: # If English name exists
            strNameN = dicN["Name_UK"]
            numS = 0
        else:
            numS = 1

    lstCorrect = [numS,strNameN,strNameL]
    lstLockes  = [] # [bolLockN, bolLockL] <--- remove XXX
    return lstCorrect, lstLockes

# ====== Individual Tools Execute functions ===================================

def GNDBruninTOC_exe_G2N(parameters, messages):

    from datetime import datetime # for datetime.now()

    strExecuName  = "GNDBruninTOC_exeG2N()"
    strExecuVer   = "0.4.1" # Introducing logfile
    strExecuBuild = "'150828.x"

    timStart = datetime.now()
        
        
    # *** Begin
    fil_log = open("GNDB_execute.log", "w")
    arcEC.SetMsg("Exec. '"+strExecuName+"' ver. "+strExecuVer+" build "+strExecuBuild, 0, fil_log)
    
    lstFails = list()
    
    
    # *** Manage input parameters ***    
    # ** Harvest strings from GUI
    
    arcEC.SetMsg("GUI said", 0, fil_log)
    try: # this will work when called from a .pyt
        strFC = parameters[0].valueAsText # FeatureClasse(s)
        strGN = parameters[1].valueAsText # GNDB point FC
        strMode = parameters[2].valueAsText # Mode (string)
        strOverwrite = parameters[3].valueAsText # Overwrite (string (boolean))
    except: # this will work when called from a .bxt, though __main__ below
        strFC = parameters[0] # FeatureClasse(s)
        strGN = parameters[1] # GNDB point FC
        strMode = parameters[2] # Mode (string)
        strOverwrite = parameters[3] # Overwrite (string (boolean))
    if strOverwrite.lower() == "true":
        bolOverwrite = True
    else:
        bolOverwrite = False
    arcEC.SetMsg(" Feature classe(s)  : "+strFC, 0, fil_log)
    arcEC.SetMsg(" GNDB table         : "+strGN, 0, fil_log)
    arcEC.SetMsg(" Mode               : "+strMode, 0, fil_log)
    arcEC.SetMsg(" Overwrite          : "+str(bolOverwrite), 0, fil_log)
    
    
    # *** Open Feature Layer(s) ***                
    arcEC.SetMsg("Open Feature Layer", 0, fil_log)
    
    # ** find Feature Layer & GNDB
    mxd = arcpy.mapping.MapDocument('CURRENT')
    if (len(arcpy.mapping.ListDataFrames(mxd)) != 1):
        arcEC.SetMsg("Multiple Data frames... Picking the first one.", 1, fil_log)
    daf = arcpy.mapping.ListDataFrames(mxd)[0] # Only first data frame is considered, others are ignored... Improve this later XXX
    
    # * find Layer
    for lay_i in arcpy.mapping.ListLayers(mxd, "", daf): # list of Layers from the first frame in TOC
        if str(lay_i) in strFC:
            arcEC.SetMsg(" TOC input layer    : "+str(lay_i), 0, fil_log)
            lay_in = lay_i
    # XXX show number of records, and number of selected records...    
            
    # * find GNDB
    for lay_i in arcpy.mapping.ListLayers(mxd, "", daf): # list of Layers from the first frame in TOC
        if str(lay_i) in strGN:
            arcEC.SetMsg(" TOC GNDB           : "+str(lay_i), 0, fil_log)
            lay_gndb = lay_i
        
    del lay_i, daf, mxd # Keep lay_in and lay_gndb
    
    
    # *** Load GNDB to memory ***
    arcEC.SetMsg("Loading GNDB into memory ... ", 0, fil_log)
    dic_GNDB = dict()
    arcpy.SelectLayerByAttribute_management (lay_gndb, "CLEAR_SELECTION") # Make sure no records are selected
    lst_fields = ["GST_NID", "NAMETYPE", "GST_GL_NAME", "GST_DK_NAME", "GST_UK_NAME", "SHAPE@XY"]
    try:
        with arcpy.da.SearchCursor(lay_gndb, lst_fields, "GST_NID IS NOT NULL and TO_DATE IS NULL") as cursor: # if TO_DATE != NULL then info is obsolete ...
            for row in cursor:
                dic_new = dict()
                dic_new["NameType"] = row[1]
                dic_new["Name_GL"] = row[2] # don't use .strip() here as object may be None
                dic_new["Name_DK"] = row[3]
                dic_new["Name_UK"] = row[4]
                dic_new["XY_tuple"] = row[5]
                dic_GNDB[row[0]] = dic_new
                del dic_new
    except arcpy.ExecuteError:
        arcpy.AddError("Error 201: arcpy.ExecuteError: "+arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddError("Error 202: Exception: "+e.args[0])
        sys.exit()
    arcEC.SetMsg("Loading GNDB onto memory - Done ", 0, fil_log)
    
    arcEC.SetMsg("  - count GNDB keys : "+str(len(dic_GNDB.keys())), 0, fil_log)
    #=======================================================================
    # key_samp = "{687F98C5-49AF-44BA-8905-8C2A76CA7EA5}" # <--- This record is known to be free of special characters
    # dic_samp = dic_GNDB[key_samp]
    # arcEC.SetMsg(" - sample           : "+key_samp, 0, fil_log)
    # arcEC.SetMsg("   - name type      : "+str(dic_samp["NameType"]), 0, fil_log)
    # arcEC.SetMsg("   - Greenland      : "+str(dic_samp["Name_GL"]), 0, fil_log)
    # arcEC.SetMsg("   - Danish         : "+str(dic_samp["Name_DK"]), 0, fil_log)
    # arcEC.SetMsg("   - English        : "+str(dic_samp["Name_UK"]), 0, fil_log)
    # arcEC.SetMsg("   - X,Y            : "+str(dic_samp["XY_tuple"]), 0, fil_log)
    #=======================================================================    # *** for each record:
    
    
    # *** for each record:
    arcEC.SetMsg("\nRunning through the rows ...", 0, fil_log)
    arcEC.SetMsg("Overwrite: "+str(bolOverwrite), 0, fil_log)
    lst_fields_we_want = ["GST_NID","OBJNAM","NOBJNM","NIS_EDITOR_COMMENT","NAMETYPE"]
    lst_Fails = list()
    
    num_row_count = 0
    num_row_changed = 0
    with arcpy.da.UpdateCursor(lay_in, lst_fields_we_want, "GST_NID IS NOT NULL") as cursor:
        for row in cursor:
            
            try:
                ##arcEC.SetMsg("Trying    : "+str(row[0]), 0, fil_log)                
                if row[0] in dic_GNDB.keys():
                    num_row_count += 1
                    bolChanges = False
                    arcEC.SetMsg("Hit GNDB           : "+str(row[0]), 0, fil_log)
                
                    # *** Process the row <-------------------------------- This is where the real business is going on ------
                    # ** Handle names (OBJNAM & NOBJNM)
                    # * Calculate the official values from GNDB
                    lstOfficialNames, listOfLocks = CorrectNaming(strMode, dic_GNDB[row[0]])
                    OBJNAM_off = arcEC.encodeIfUnicode(lstOfficialNames[1])
                    NOBJNM_off = arcEC.encodeIfUnicode(lstOfficialNames[2])
                    # * read current values from GNDB
                    OBJNAM_cur = arcEC.encodeIfUnicode(row[1])
                    NOBJNM_cur = arcEC.encodeIfUnicode(row[2])
                    # Convert all Null's to empty string
                    if OBJNAM_off == "None": OBJNAM_off = ""
                    if NOBJNM_off == "None": NOBJNM_off = ""
                    if OBJNAM_cur == "None": OBJNAM_cur = ""
                    if NOBJNM_cur == "None": NOBJNM_cur = ""                
                
                    arcEC.SetMsg("    Name GNDB      : ("+str(OBJNAM_off)+" / "+str(NOBJNM_off)+")", 0, fil_log)
                    arcEC.SetMsg("    Name NamesA    : ("+str(OBJNAM_cur)+" / "+str(NOBJNM_cur)+")", 0, fil_log)
                
                    # * OBJNAM
                    if OBJNAM_off != None and len(OBJNAM_off) > 1: # official OBJNAM is a valid data
                        if (OBJNAM_off != OBJNAM_cur): # There is a need for update...
                            if bolOverwrite or OBJNAM_cur == "" or OBJNAM_cur == None:
                                arcEC.SetMsg("     OBJNAM   <<<   : "+OBJNAM_cur+" << "+OBJNAM_off, 0, fil_log)
                                row[1] = lstOfficialNames[1] # try to avoid utf8 error
                                bolChanges = True
                            else:
                                arcEC.SetMsg("     OBJNAM differs : "+OBJNAM_cur+" != "+OBJNAM_off, 0, fil_log)
                
                    # * NOBJNM
                    if NOBJNM_off != None and len(NOBJNM_off) > 1: # official NOBJNM is a valid data
                        if (NOBJNM_off != NOBJNM_cur): # There is a need for update...
                            if bolOverwrite or NOBJNM_cur == "" or NOBJNM_cur == None:
                                arcEC.SetMsg("     NOBJNM   <<<   : "+NOBJNM_cur+" << "+NOBJNM_off, 0, fil_log)
                                row[2] = lstOfficialNames[2] # try to avoid utf8 error
                                bolChanges = True
                            else:                            
                                arcEC.SetMsg("     NOBJNM differs : "+NOBJNM_cur+" != "+NOBJNM_off, 0, fil_log)
                
                    # * Write back to row
                    if bolChanges:
                        cursor.updateRow(row)
                        num_row_changed += 1
                
                    # *** End of - Process row <-------------------------------------------------- End of real business ------
                
                else:
                    arcEC.SetMsg("Error 302:  No GNDB Hit : "+str(row[0]), 0, fil_log)
                
            except:
                arcEC.SetMsg("Error 301:  Row fail in general try: loop (adding to fail list) : ", 0, fil_log)
                arcEC.SetMsg("    Filed on NID : "+str(row[0]), 0, fil_log)
                lst_Fails.append(str(row[0]))
    
    arcEC.SetMsg("Processed rows      : "+str(num_row_count), 0, fil_log)
    arcEC.SetMsg("    Changed rows    : "+str(num_row_changed), 0, fil_log)
    arcEC.SetMsg("    Failed rows     : "+str(len(lstFails)), 0, fil_log)
        
    return len(lstFails)
    # *** End of function GNDBruninTOC()

if __name__ == "__main__":
    # This allows the 'executes' to be called from classic .tbx
    parameters = [arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2), arcpy.GetParameterAsText(3)]
    messages = []
    result = GNDBruninTOC_exe_G2N(parameters, messages)

# *** End of Script ***

# Music that accompanied the coding of this script:
#   Kid Creole & the Coconuts - Tropical gangster
