
import sys
import os

import arcEC

def GNDBruninTOC_exe_G2N(parameters, messages):


    
    # *** Start Edtiting etc. the receiving layer
    # http://resources.arcgis.com/en/help/main/10.2/index.html#//00s300000008000000
    # XXX Check that we are actually in an edit session ...
    workspace = r"C:\Users\b004218\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\EC_nis_editor@green3.sde"#\NIS.Vores_Navne" #os.path.dirname(lay_in.dataSource)
    lay_in = "\NIS.Vores_Navne\NIS.NamesAtest"
    arcEC.SetMsg(" WS : "+str(workspace), 0)
    edit = arcpy.da.Editor(workspace)
    edit.startEditing() # Edit session is started without (False) an undo/redo stack for versioned data    
    edit.startOperation() # Start an edit operation
    
    # *** for each record:
    arcEC.SetMsg("\nRunning through the rows ...", 0)
    lst_fields_we_want = ["GST_NID","OBJNAM","NOBJNM","NIS_EDITOR_COMMENT","NAMETYPE"]
    lst_Fails = list()

    with arcpy.da.UpdateCursor(workspace+lay_in, lst_fields_we_want, "GST_NID IS NOT NULL") as cursor:
        for row in cursor:
            pass
                
    # *** Start Edtiting etc. the receiving layer
    edit.stopOperation() # Stop the edit operation.
    edit.stopEditing(True) # Stop the edit session and save the changes   
    
    arcEC.SetMsg("Processed rows      : "+str(num_row_count), 0)
    arcEC.SetMsg("    Changed rows    : "+str(num_row_changed), 0)
    arcEC.SetMsg("    Failed rows     : "+str(len(lstFails)), 0)
        
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
