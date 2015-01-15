#-------------------------------------------------------------
#
# Name:       GNDB_executes.py (This should only be called from GNDB.pyt)
# Purpose:    A python-tool to work with the "Greenlandic Names Data Base" (GNDB) and NIS.
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

import arcEC
        
# ====== Helper functions =====================================================

def CorrectNaming(mode, dicN):
    bGL = str(type(dicN["Name_GL"]))=="<type 'unicode'>"
    if bGL:
        bGL = len(dicN["Name_GL"])!=0
    bDA = str(type(dicN["Name_DK"]))=="<type 'unicode'>"
    if bDA:
        bDA = len(dicN["Name_DK"])!=0
    bEN = str(type(dicN["Name_UK"]))=="<type 'unicode'>"
    if bEN:
        bEN = len(dicN["Name_UK"])!=0

    ### This section decides the rules for how 3 Potential names is transfered to 2 Place holders
    ### The earlier destinction beween Old and New greenlandiv spelling, is now handled by only maintaining one in GNDB
    strN = ""   # Name
    strL = ""   # Local name
    numS = 999  # Return code. 0 = Success
    if mode == "Berit":
        if bGL: # If Greenlandic name exists
            strN = dicN["Name_GL"]
            if bDA: # If Danish name exists
                strL = dicN["Name_DK"]
            elif bEN: # If English name exists
                strL = dicN["Name_UK"]
            numS = 0
        elif bDA: # If Danish name exists
            strN = dicN["Name_DK"]
            if bEN: # English name exists
                strL = dicN["Name_UK"]
            numS = 0
        elif bEN: # If English name exists
            strN = dicN["Name_UK"]
            numS = 0
        else:
            numS = 1

    lstCorrect = [numS,strN,strL]
    return lstCorrect


def encodeIfUnicode(strval):
    """Encode if string is unicode."""
    if isinstance(strval, unicode):
        return strval.encode('ISO-8859-1')
    return str(strval)

dic_NT = {"0" : "Ukendt",
            "1" : "GNDB=1 Sø",
            "2" : "GNDB=2 Elv",
            "3" : "GNDB=3 Fjord",
            "4" : "GNDB=4 Bugt",
            "5" : "GNDB=5 Hav",
            "6" : "GNDB=6 Ø",
            "7" : "GNDB=7 Øgruppe",
            "8" : "GNDB=8 Sund",
            "9" : "GNDB=9 Kyst",
            "10" : "GNDB=10 Bredning",
            "11" : "GNDB=11 Vig",
            "12" : "GNDB=12 Snævring",
            "13" : "GNDB=13 Munding",
            "14" : "GNDB=14 Skær",
            "15" : "GNDB=15 Stræde",
            "16" : "GNDB=16 Tørt",
            "17" : "GNDB=17 Banke",
            "18" : "GNDB=18 Ankerplads",
            "19" : "GNDB=19 Sejlløb",
            "20" : "GNDB=20 Nor ()",
            "21" : "GNDB=21 Isfjord (Ice Fjord)",
            "22" : "GNDB=22 Station (Station)",
            "23" : "GNDB=23 Station Nedlagt (Station Abandoned)",
            "24" : "GNDB=24 Forsøgsstation (Research station)",
            "25" : "GNDB=25 Bygd (Settlement )",
            "26" : "GNDB=26 By (Town)",
            "27" : "GNDB=27 Nedlagt bygd (Abandoned Settelment)",
            "28" : "GNDB=28 Teltplads (Camp Site)",
            "29" : "GNDB=29 Fangsthytte",
            "35" : "GNDB=35 Mine",
            "31" : "GNDB=31 Ruin",
            "30" : "GNDB=30 Bygning (Building)",
            "34" : "GNDB=34 Havn (Habour)",
            "33" : "GNDB=33 Kors (Cross)",
            "32" : "GNDB=32 Kraftværk (Powerplant)",
            "36" : "GNDB=36 Base",
            "37" : "GNDB=37 Kirkegård (Cemetary)",
            "38" : "GNDB=38 Tegning i klippen",
            "39" : "GNDB=39 Varde (Cairn)",
            "40" : "GNDB=40 Skisportssted",
            "41" : "GNDB=41 Kaj (Quay)",
            "50" : "GNDB=50 Næs/Pynt (Point)",
            "51" : "GNDB=51 Landareal (Land Area)",
            "52" : "GNDB=52 Halvø (Peninsula)",
            "53" : "GNDB=53 Tange (Isthmus)",
            "54" : "GNDB=54 Ødel (Part of Island)",
            "55" : "GNDB=55 Odde (Spit)",
            "56" : "GNDB=56 Kap (Cape)",
            "57" : "GNDB=57 Klint (Cliff)",
            "58" : "GNDB=58 Bakke (Hill)",
            "60" : "GNDB=60 Fjeld (Mountain)",
            "61" : "GNDB=61 Skråning (Hillside)",
            "62" : "GNDB=62 Dal (Valley)",
            "63" : "GNDB=63 Forbjerg (Promontory)",
            "64" : "GNDB=64 Skrænt (Slope)",
            "65" : "GNDB=65 Kløft (Cleft)",
            "67" : "GNDB=67 Afsats (Ledge)",
            "68" : "GNDB=68 Nunatak",
            "69" : "GNDB=69 Top",
            "70" : "GNDB=70 Slette (Plain)",
            "71" : "GNDB=71 Mose (Bog)",
            "72" : "GNDB=72 Moræne (Moraine)",
            "73" : "GNDB=73 Skred (Landslide)",
            "74" : "GNDB=74 Kilde (Spring)",
            "75" : "GNDB=75 Vandfald (Waterfall)",
            "76" : "GNDB=76 Delta",
            "77" : "GNDB=77 Elvmunding ()",
            "78" : "GNDB=78 Elvleje ()",
            "79" : "GNDB=79 Skov (Wood)",
            "80" : "GNDB=80 Eng (Meadow)",
            "81" : "GNDB=81 Elvslette",
            "82" : "GNDB=82 Søudløb",
            "83" : "GNDB=83 Dyndvulkan",
            "90" : "GNDB=90 Sten (Stone)",
            "91" : "GNDB=91 Hule (Cave)",
            "92" : "GNDB=92 Rullesten (Pebble)",
            "93" : "GNDB=93 Hul (Hole)",
            "100" : "GNDB=100 Plateau",
            "101" : "GNDB=101 Bjergpas (Pass)",
            "102" : "GNDB=102 Lavning",
            "103" : "GNDB=103 Højland (Highland)",
            "104" : "GNDB=104 Højdedrag ()",
            "105" : "GNDB=105 Tinde (Pinnacle)",
            "106" : "GNDB=106 Bjerg (Mountain)",
            "110" : "GNDB=110 Isareal (Icearea)",
            "111" : "GNDB=111 Bræ (Glacier)",
            "112" : "GNDB=112 Sneklat (Snow area)",
            "113" : "GNDB=113 Snefane ()",
            "115" : "GNDB=115 Brækant (Glacier edge)",
            "116" : "GNDB=116 Bræleje ()",
            "117" : "GNDB=117 Isslette ()",
            "118" : "GNDB=118 Snekuppel ()",
            "119" : "GNDB=119 Firn",
            "120" : "GNDB=120 Isfjelde på banke ()",
            "121" : "GNDB=121 Bassin (Bassin)",
            "122" : "GNDB=122 Brandplet (Fire Spot)",
            "123" : "GNDB=123 Bro (Bridge)",
            "124" : "GNDB=124 Basalt, basaltsøjle",
            "125" : "GNDB=125 Bydel (Townpart)",
            "126" : "GNDB=126 Bærplukningssted",
            "127" : "GNDB=127 Dam",
            "128" : "GNDB=128 Depot",
            "129" : "GNDB=129 Diabas",
            "130" : "GNDB=130 Fangstplads",
            "131" : "GNDB=131 Fiskested",
            "132" : "GNDB=132 Flyveplads",
            "133" : "GNDB=133 Grafitforekomst",
            "134" : "GNDB=134 Kulforekomst",
            "135" : "GNDB=135 Fælde",
            "136" : "GNDB=136 Garnfangststed",
            "137" : "GNDB=137 Grav",
            "138" : "GNDB=138 Hajfiskeplads",
            "139" : "GNDB=139 Helikopterlandingsplads",
            "140" : "GNDB=140 Bjørnehi",
            "141" : "GNDB=141 Hustomt",
            "142" : "GNDB=142 Hvælvning",
            "143" : "GNDB=143 Indløb",
            "144" : "GNDB=144 Kanal",
            "145" : "GNDB=145 Varm kilde",
            "146" : "GNDB=146 Knold, knovs",
            "147" : "GNDB=147 Kommune",
            "148" : "GNDB=148 Kær",
            "149" : "GNDB=149 Laksefangststed",
            "150" : "GNDB=150 Landingssted, færgested",
            "151" : "GNDB=151 Nedlagt amerikansk mine",
            "152" : "GNDB=152 Nedkørsel",
            "153" : "GNDB=153 Næs",
            "154" : "GNDB=154 Ophaling, bedding",
            "155" : "GNDB=155 Opkørsel",
            "156" : "GNDB=156 Opstigningssted",
            "157" : "GNDB=157 Overbæringssted",
            "158" : "GNDB=158 Overgangssted",
            "159" : "GNDB=159 Rasteplads",
            "160" : "GNDB=160 Rensdyrområde",
            "161" : "GNDB=161 Rute",
            "162" : "GNDB=162 Rævehuler",
            "163" : "GNDB=163 Skydeskjul",
            "164" : "GNDB=164 Slædeopkørsel",
            "165" : "GNDB=165 Slædevej",
            "166" : "GNDB=166 Sommerplads",
            "167" : "GNDB=167 Stribe i fjeldet",
            "168" : "GNDB=168 Strømsted",
            "169" : "GNDB=169 Terrasser"}


def Make_NT(num_NT):
    if num_NT != None:
        if str(num_NT) in dic_NT.keys():
            return dic_NT[str(num_NT)]
        else:
            arcEC.SetMsg( " !!! dic too short, missing: "+str(num_NT), 0)
            return "GNDB="+str(num_NT)
    else:
        return None

# ====== Individual Tools Execute functions ===================================

def GNDBruninTOC_execute(parameters, messages):

    from datetime import datetime # for datetime.now()
    #import arcpy # have gone global

    strExecuName  = "GNDBruninTOC_execute()"
    strExecuVer   = "0.3.0"
    strExecuBuild = "'150115,"

    timStart = datetime.now()
        
    # *** Begin
    arcEC.SetMsg("Exec. '"+strExecuName+"' ver. "+strExecuVer+" build "+strExecuBuild,0)
    
    # *** Manage input parameters ***
    
    # ** Harvest strings from GUI
    
    arcEC.SetMsg("GUI said",0)
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
    arcEC.SetMsg(" Feature classe(s)  : "+strFC,0)
    arcEC.SetMsg(" GNDB table         : "+strGN,0)
    arcEC.SetMsg(" Mode               : "+strMode,0)
    arcEC.SetMsg(" Overwrite          : "+str(bolOverwrite),0)
    
    
    # *** Open Feature Layer(s) ***                
    arcEC.SetMsg("Open Feature Layer",0)
    
    # ** find Feature Layer & GNDB
    mxd = arcpy.mapping.MapDocument('CURRENT')
    #arcEC.SetMsg(" MXD: "+str(mxd),0)
    if (len(arcpy.mapping.ListDataFrames(mxd)) != 1):
        arcEC.SetMsg("Multiple Data frames... Picking the first one.", 1)
    daf = arcpy.mapping.ListDataFrames(mxd)[0] # Only first data frame is considered, others are ignored... Improve this later XXX
    
    # * find Layer
    #arcEC.SetMsg(" daf: "+str(daf),0)
    for lay_i in arcpy.mapping.ListLayers(mxd, "", daf): # list of Layers from the first frame in TOC
        if str(lay_i) in strFC:
            arcEC.SetMsg(" TOC input layer    : "+str(lay_i),0)
            lay_in = lay_i
    # XXX show number of records, and number of selected records...    
            
    # * find GNDB
    for lay_i in arcpy.mapping.ListLayers(mxd, "", daf): # list of Layers from the first frame in TOC
        if str(lay_i) in strGN:
            arcEC.SetMsg(" TOC GNDB           : "+str(lay_i),0)
            lay_gndb = lay_i
        
    del lay_i, daf, mxd # Keep lay_in and lay_gndb

    
    # *** Load GNDB to memory ***
    dic_GNDB = dict()
    arcpy.SelectLayerByAttribute_management (lay_gndb, "CLEAR_SELECTION") # Make sure no records are selected
    # Handled by the cursor # lay_gndb.definitionQuery = "TO_DATE IS NULL"  # Excluding obsolete records
    lst_fields = ["NID", "NAMETYPE", "GST_GL_name", "GST_DK_name", "GST_UK_name", "SHAPE@XY"]
    try:
        #with arcpy.da.SearchCursor(lay_gndb, lst_fields, "TO_DATE IS NULL and NAME_GREENLAND_NEW = 'Nuuk'") as cursor:
        with arcpy.da.SearchCursor(lay_gndb, lst_fields, "NID IS NOT NULL and TO_DATE IS NULL") as cursor: # if TO_DATE != NULL then info is obsolete ...
            for row in cursor:
                dic_new = dict()
                dic_new["NameType"] = row[1]
                dic_new["Name_GL"] = row[2] # don't use .strip() here as object may be None
                dic_new["Name_DK"] = row[3]
                dic_new["Name_UK"] = row[4]
                dic_new["XY_tuple"] = row[5]
                dic_GNDB[row[0]] = dic_new
                del dic_new
                
                #arcEC.SetMsg("{}".format(row[0]),0)          
                # Don't try Msg Danish, nor Grenlandic name with strance characters  
    except arcpy.ExecuteError:
        arcpy.AddError("Error 201: arcpy.ExecuteError: "+arcpy.GetMessages(2))
    except Exception as e:
        arcpy.AddError("Error 202: Exception: "+e.args[0])
    
    arcEC.SetMsg("  - count GNDB keys : "+str(len(dic_GNDB.keys())),0)
    #=======================================================================
    # key_samp = "{687F98C5-49AF-44BA-8905-8C2A76CA7EA5}" # <--- This record is known to be free of special characters
    # dic_samp = dic_GNDB[key_samp]
    # arcEC.SetMsg(" - sample           : "+key_samp,0)
    # arcEC.SetMsg("   - name type      : "+str(dic_samp["NameType"]),0)
    # arcEC.SetMsg("   - Greenland      : "+str(dic_samp["Name_GL"]),0)
    # arcEC.SetMsg("   - Danish         : "+str(dic_samp["Name_DK"]),0)
    # arcEC.SetMsg("   - English        : "+str(dic_samp["Name_UK"]),0)
    # arcEC.SetMsg("   - X,Y            : "+str(dic_samp["XY_tuple"]),0)
    #=======================================================================
    
    lst_fields_we_want = ["GST_NID","OBJNAM","NOBJNM","NIS_EDITOR_COMMENT","NAMETYPE"]
    
    # *** for each record:
    arcEC.SetMsg("\nRunning through the rows ...",0)
    arcEC.SetMsg("Overwrite: "+str(bolOverwrite),0)
    
    num_row_count = 0
    num_row_changed = 0
    with arcpy.da.UpdateCursor(lay_in, lst_fields_we_want, "GST_NID IS NOT NULL") as cursor:
        for row in cursor:
            if row[0] in dic_GNDB.keys():
                num_row_count += 1
                bolChanges = False
                arcEC.SetMsg(" Hit GNDB           : "+str(row[0]),0)
                
                # *** Process the row <----------------------------------------- This is where the real business is going on
                # ** Handle names (OBJNAM & NOBJNM)
                # * Calculate the official values from GNDB
                lstOfficialNames = CorrectNaming(strMode, dic_GNDB[row[0]])
                OBJNAM_off = encodeIfUnicode(lstOfficialNames[1])
                NOBJNM_off = encodeIfUnicode(lstOfficialNames[2])
                # * read current values from GNDB
                OBJNAM_cur = encodeIfUnicode(row[1])
                NOBJNM_cur = encodeIfUnicode(row[2])
                
                arcEC.SetMsg("     GNDB     off   : ("+str(OBJNAM_off)+" / "+str(NOBJNM_off)+")",0)
                arcEC.SetMsg("     GNDB     cur   : ("+str(OBJNAM_cur)+" / "+str(NOBJNM_cur)+")",0)
                
                # * OBJNAM
                if OBJNAM_off != None and len(OBJNAM_off) > 1: # official OBJNAM is a valid data
                    if (OBJNAM_off != OBJNAM_cur) and (OBJNAM_off != None and OBJNAM_off != ""): # There is a need for update...
                        if bolOverwrite or OBJNAM_cur == "" or OBJNAM_cur == None: # Edits are allowed
                            arcEC.SetMsg("     OBJNAM   <<<   : "+OBJNAM_cur+" << "+OBJNAM_off,0)
                            row[1] = OBJNAM_off
                            bolChanges = True
                        else:
                            arcEC.SetMsg("     OBJNAM      !!!  "+OBJNAM_cur+" != "+OBJNAM_off,0)
                            
                # * NOBJNM
                if NOBJNM_off != None and len(NOBJNM_off) > 1: # official NOBJNM is a valid data
                    if (NOBJNM_off != NOBJNM_cur) and (NOBJNM_off != None and NOBJNM_off != ""): # There is a need for update...
                        if bolOverwrite or NOBJNM_cur == "" or NOBJNM_cur == None: # Edits are allowed
                            arcEC.SetMsg("     NOBJNM   <<<   : "+NOBJNM_cur+" << "+NOBJNM_off,0)
                            row[2] = NOBJNM_off
                            bolChanges = True
                        else:                            
                            arcEC.SetMsg("     NOBJNM      !!!  "+NOBJNM_cur+" != "+NOBJNM_off,0)
                                            
                # ** Handle NIS_EDITOR_COMMENT       
                # * search for existing string
                NISECo_cur = encodeIfUnicode(row[3])         
                # Assuming form "GNDB=13 Munding", i.e. some string + "GNDB=<int> <string>" + more string, so I split tail on ' 's  
                if "GNDB" in NISECo_cur:
                    num_pos1 = NISECo_cur.find("GNDB")    
                    num_poseq = NISECo_cur.find("=",num_pos1)   
                    num_posfs = NISECo_cur.find(" ",num_poseq)
                    if " " in NISECo_cur[num_posfs+1:]:
                        num_pos2 = NISECo_cur.find(" ",num_posfs+1)
                    else:
                        num_pos2 = len(NISECo_cur)
                    if NISECo_cur[num_pos1:num_pos2][-1] in (",",";"): # if last is , then move 1
                        num_pos2 -= 1 
                    str_head = NISECo_cur[:num_pos1]
                    str_GNDB = NISECo_cur[num_pos1:num_pos2]
                    str_tail = NISECo_cur[num_pos2:]
                    lst_NISECo_cur = [str_head,str_GNDB,str_tail]
                    del num_pos1, num_poseq, num_posfs, num_pos2, str_head, str_GNDB, str_tail
                else:
                    NISECo_cur = NISECo_cur.replace("None","") # to get rid of 'None' as a string
                    lst_NISECo_cur = [NISECo_cur,"",""]
                    
                # * find official GNDB= ...
                num_NT = row[4]
                NISECo_off = Make_NT(num_NT)
                
                arcEC.SetMsg("     NISECo   off   : "+NISECo_off,0) 
                arcEC.SetMsg("     NISECo   cur   : "+str(lst_NISECo_cur),0)
                
                # * NIS_EDITORS_COMMENT
                if NISECo_off != None and len(NISECo_off) > 1: # official NISECo_off is a valid data
                    if lst_NISECo_cur[1] != NISECo_off: # There is a need for update...
                        lst_NISECo_new = list(lst_NISECo_cur) # list() to avoid _new and _cur to be same actual object ...
                        lst_NISECo_new[1] = NISECo_off # replace current GNDB with official
                        NISECo_new = lst_NISECo_new[0]+" "+lst_NISECo_new[1]+" "+lst_NISECo_new[2] # add it back together
                        while "  " in NISECo_new: # ... and clean up the resulting string
                            NISECo_new = NISECo_new.replace("  "," ")
                        NISECo_new = NISECo_new.strip()
                        if bolOverwrite or (len(lst_NISECo_cur[1]) < 1): # Edits are allowed
                            row[3] = NISECo_new
                            bolChanges = True
                            arcEC.SetMsg("     NISECo   <<<   : "+NISECo_cur+" << "+NISECo_new,0)
                        else:
                            arcEC.SetMsg("     NISECo   !!!   : "+NISECo_cur+" != "+NISECo_new +"!!!"+str(len(lst_NISECo_cur[1]))+lst_NISECo_cur[1],0) # XXXX
                    
                    
                # * Write back to row
                if bolChanges:
                    cursor.updateRow(row)
                    num_row_changed += 1
                    
                # *** -------------------------------------------------------------------------- End of real business ------
                    
            else:
                arcEC.SetMsg(" !*! No Hit in GNDB : "+str(row[0]),0)
                
        # ** End of - Process row.
    
    arcEC.SetMsg("Processed rows      : "+str(num_row_count),0)
    arcEC.SetMsg("    Changed rows    : "+str(num_row_changed),0)
    
    # *** All Done - Cleaning up ***
    
    timEnd = datetime.now()
    durRun = timEnd-timStart
    arcEC.SetMsg("Python stript duration (h:mm:ss.dddddd): "+str(durRun),0)
    
    return 0

    # *** End of function GNDBruninTOC()
    
if __name__ == "__main__":
    # This allows the 'executes' to be called from classic .tbx
    parameters = [arcpy.GetParameterAsText(0), arcpy.GetParameterAsText(1), arcpy.GetParameterAsText(2), arcpy.GetParameterAsText(3)]
    messages = []
    result = GNDBruninTOC_execute(parameters, messages)

# *** End of Script ***

# Music that accompanied the coding of this script:
#   Pink Floyd - Dark side of the moon
#   London Grammer - If you Wait