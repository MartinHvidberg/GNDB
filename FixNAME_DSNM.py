# Run with 10.1 client to take advantage of some new GP tools in 10.1.
#  Can connect to 10.0 version of the geodatabase
import arcpy, traceback, os, string, math, time
from arcpy import env
from os import path

#Function to print messages in Python and Esri GP environment
# sev 0 = informational
# sev 1 = error
def printMsg(msg, sev):
    temp = msg
    print(temp)
    if sev <> 1:
        arcpy.AddMessage(temp)
    else:
        arcpy.AddError(temp)

def timeElapsed(timeS):
    seconds = time.time() - timeS
    hours = seconds // 3600
    seconds -= 3600*hours
    minutes = seconds // 60
    seconds -= 60*minutes
    if hours == 0 and minutes == 0:
        return "%02d seconds" % (seconds)
    if hours == 0:
        return "%02d:%02d seconds" % (minutes, seconds)
    return "%02d:%02d:%02d seconds" % (hours, minutes, seconds)

def calcFields(lyrview):
    fldExistsNAME = len(arcpy.ListFields(lyrview,"NAME")) > 0
    if fldExistsNAME:
        edit.startOperation()
        arcpy.CalculateField_management(lyrview,"NAME",'NULL')
        edit.stopOperation()
        printMsg("      Calculated NAME field to NULL",sevInfo)
    else:
        printMsg("    ** NAME field doesn't exist",sevInfo)
    
    fldExistsDSNM = len(arcpy.ListFields(lyrview,"DSNM")) > 0
    if fldExistsDSNM:
        edit.startOperation()
        arcpy.CalculateField_management(lyrview,"DSNM",'NULL')
        edit.stopOperation()
        printMsg("      Calculated DSNM field to NULL",sevInfo)
    else:
        printMsg("    ** DSNM field doesn't exist",sevInfo)

#Begin script
#Gather input parameters

#this should be an sde user connection to the workspace
inputWorkspace = arcpy.GetParameterAsText(0)
##inputWorkspace = r"C:\ConnectionFiles\oracle_pacific\nsbisdb4_pacific_nis@nis.sde"

env.workspace = inputWorkspace
edit = arcpy.da.Editor(inputWorkspace)

# Constants
sevInfo = 0
sevErr = 1

timeStartTotal = time.time()

printMsg("Loaded Workspace:" + env.workspace,sevInfo)

try:
    edit.startEditing(False,True)
    
    lstDS = arcpy.ListDatasets("*Nautical")
    for ds in lstDS:
        printMsg("\nOpened Dataset " + ds,sevInfo)

        # Loop through each feature class, calculating NAME and DSNM
        #  to NULL
        lstFC = arcpy.ListFeatureClasses("","",ds)
        for fc in lstFC:
            printMsg("  Opened Feature Class " + fc,sevInfo)
            
            lyrFC = "lyr"+fc
            arcpy.MakeFeatureLayer_management(fc,lyrFC)
            timeStart = time.time()
            calcFields(lyrFC)
            printMsg("    "+timeElapsed(timeStart)+" elapsed...",sevInfo)
            arcpy.Delete_management(lyrFC)

    collName = "PLTS_COLLECTIONS"
    lstTable = arcpy.ListTables("*"+collName)
    if len(lstTable) > 0:
        printMsg("  Opened Table "+collName,sevInfo)

        vwTable = "vw"+collName
        arcpy.MakeTableView_management(collName,vwTable)
        timeStart = time.time()
        calcFields(vwTable)
        printMsg("    "+timeElapsed(timeStart)+" elapsed...",sevInfo)
        arcpy.Delete_management(vwTable)
    else:
        printMsg("  "+collName+" doesn't exist",sevInfo)

    frelName = "PLTS_FREL"
    lstfrelTable = arcpy.ListTables("*"+frelName)
    if len(lstfrelTable) > 0:
        printMsg("  Opened Table "+frelName,sevInfo)

        vwfrelTable = "vw"+frelName
        arcpy.MakeTableView_management(frelName,vwfrelTable)
        timeStart = time.time()
        calcFields(vwfrelTable)
        printMsg("    "+timeElapsed(timeStart)+" elapsed...",sevInfo)
        arcpy.Delete_management(vwfrelTable)
    else:
        printMsg("  "+frelName+" doesn't exist",sevInfo)

    edit.stopEditing(True)
    
    printMsg("\nScript completed successfully",sevInfo)
    printMsg("  Total time elapsed: "+timeElapsed(timeStartTotal)+"...",sevInfo)

except arcpy.ExecuteError:
    # Get the geoprocessing error messages
    msgs = arcpy.GetMessage(0)
    msgs += arcpy.GetMessages(2)

    # Display arcpy error messages
    printMsg("Error in FixNAME_DSNM.py",sevInfo)
    printMsg(msgs,sevErr)
    
except Exception, ex:
    # Get the traceback object
    import traceback, sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]

    # Concatenate information together concerning the error into a message string
    pymsg = tbinfo + "\n" + str(sys.exc_type)+ ": " + str(sys.exc_value)

    # Display arcpy error messages
    printMsg("Error in FixNAME_DSNM.py",sevInfo)
    printMsg(pymsg,sevErr)

finally:
    arcpy.ClearWorkspaceCache_management()
