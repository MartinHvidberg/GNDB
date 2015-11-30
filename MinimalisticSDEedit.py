
#import os
import arcpy


#db = "Database Connections\green2_nis@nis_editor.sde/NIS.Nautical"
db = r"C:/Users/b004218/AppData/Roaming/ESRI/Desktop10.3/ArcCatalog/EC_nis_editor@green3.sde"

# Set the workspace for ListFeatureClasses
arcpy.env.workspace = db
featureclasses = arcpy.ListFeatureClasses()
for fc in featureclasses:
    if "NIS.NamesAtest" in fc:
        fc_edit = fc
        print "Yes: "+fc+" "+str(type(fc_edit))+" "+str(fc_edit)
        break
    else:
        print "not: "+fc

workspace = db + "/NIS.Vores_Navne/"
print "WS: "+workspace

# Set up database connection and edit session
#db_str, edit = SetUpDB(dataset)

# START AN EDIT SESSION. Must provide the workspace.
#  http://resources.arcgis.com/en/help/main/10.2/index.html#//018w00000005000000
edit = arcpy.da.Editor(db)

# Edit session is started without an undo/redo stack for versioned data
#  (for second argument, use False for unversioned data)
edit.startEditing(False, True)

# Start an edit operation
edit.startOperation()


#for fc in featureclasses:


arcpy.CalculateField_management(workspace+fc_edit, fld_Errorcode, "!OBJNAM!", "PYTHON_9.3")
##arcpy.CalculateField_management(workspace+fc, GST_NID,    "!KMS_NID!", "PYTHON_9.3")
    #with arcpy.da.UpdateCursor(dataset+fc, , where_clause="KMS_LINtxt IS NOT NULL OR KMS_NID IS NOT NULL") as uc:
    #    for row in uc:
    #        count += 1
    #        logStr = "Rule {} ({}): updating " .format(rule.id, rule.title)
    #        i = defaultFieldsNum
    #        for i in range(len(rule.fixLst)): # do each of the fixes
    #            logStr += "{} = {} (was {}), ".format(rule.fixLst[i][0], rule.fixLst[i][1], row[defaultFieldsNum+i])
    #            fixVal = rule.fixLst[i][1] # set the update value
    #            row[defaultFieldsNum+i] = fixVal
    #            i += 1
    #        logStr = logStr[0:-2] + " for OBJECTID = {} in {}".format(row[0], fc)
    #        utils.log(logStr)
    #        uc.updateRow(row) # do the actual update
    #        pass



# Stop the edit operation
edit.stopOperation()

# Stop the edit session and save the changes
edit.stopEditing(True)

