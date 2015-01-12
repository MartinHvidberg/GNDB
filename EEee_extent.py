import arcpy  
  
mxd = arcpy.mapping.MapDocument(r"C:\Martin\Work_Eclipse\BuildGreen\src\All_NIS_layers.mxd")  

lst_EE = [180,90,-180,-90] # West and South, East and North
limit = 2
  
for lyr in arcpy.mapping.ListLayers(mxd):
    
    if "CoastlineA" in str(lyr):
        
        print "\n"+str(lyr), 
        
        # Count records
        lst_fc_ee = [180,90,-180,-90] # West and South, East and North
        i = 0
        ie = 0
        for row in arcpy.da.SearchCursor(lyr, ["SHAPE@"]):
            i += 1
            try:
                ext_f = row[0].extent
                ie += 1
                print("    W:%s, S:%s E:%s, N:%s" % (ext_f.XMin,ext_f.YMin,ext_f.XMax,ext_f.YMax))
                lst_fc_ee[0] = min(float(lst_fc_ee[0]),float(ext_f.XMin)) # W
                lst_fc_ee[1] = min(float(lst_fc_ee[1]),float(ext_f.YMin)) # S
                lst_fc_ee[2] = max(float(lst_fc_ee[2]),float(ext_f.XMax)) # E
                lst_fc_ee[3] = max(float(lst_fc_ee[3]),float(ext_f.YMax)) # N
            except:
                print "*",
                
        if i>0:
            print str(i), "records ", str(ie), "features"
            lst_extent = str(lyr.getExtent()).replace(',','.').split()[:4]
            
            #calc extent discrepancy
            if (float(lst_fc_ee[2])-float(lst_fc_ee[0])) > 0: 
                ratioEW = (float(lst_extent[2])-float(lst_extent[0])) / (float(lst_fc_ee[2])-float(lst_fc_ee[0]))
            else:
                ratioEW = "n/a"
            if (float(lst_fc_ee[3])-float(lst_fc_ee[1])) > 0:
                ratioNS = (float(lst_extent[3])-float(lst_extent[1])) / (float(lst_fc_ee[3])-float(lst_fc_ee[1]))
            else:
                ratioNS = "n/a"

            try:
                print " rEW, rNS :", round(ratioEW,2), round(ratioNS,2), "(", round((ratioEW+ratioNS)/2,2), ")",
                for i in range(int(round((ratioEW+ratioNS)/2,0))-1):
                    print "*",
                print
                if ratioEW>limit or ratioNS>limit:
                    print "FC extent:", lst_extent
                    print "features :", lst_fc_ee
                    
            except:
                print "Ratios can't be calculated... Data span seems to be Zero"
            
            # Find Extent of Extents    
            if i > 0: # fc do have records
                for i in (0,1): # West and South
                    lst_EE[i] = min(float(lst_EE[i]),float(lst_extent[i]))
                for i in (2,3): # East and North
                    lst_EE[i] = max(float(lst_EE[i]),float(lst_extent[i]))
                    
        else:
            print " No records..."

#print  "\n\nWest, South, East and North", lst_EE
