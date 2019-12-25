import arcpy
import os


feat = "grid_powerlines"
fGdb = r"C:\Users\llassetter\Documents\ArcGIS\Default.gdb"
sGdb = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde"
sGdb2 = r"C:\Users\llassetter\Grid-I\hotec_gsdev.sde"
hotecMap = r"C:\Users\llassetter\Grid-I\mxd\hotec_larry.mxd"
hotecMap2 = r"C:\Users\llassetter\Grid-I\mxd\hotec_gsdev.mxd"
sFc = arcpy.os.path.join(r"C:\Users\llassetter\Grid-I\epedev005-ll.sde\hotec.sde.grid_powerlines")
gridIDir = r"C:\Users\llassetter\Grid-I"

arcpy.env.workspace = gridIDir

mapDoc = arcpy.mapping.MapDocument(hotecMap2)

###
# testing stuff
###
# print (mapDoc.filePath)
# print(mapDoc.author)
# mapDoc.title = "New Title"
# print(mapDoc.title)

###
# dataframes!
###
# dfList = arcpy.mapping.ListDataFrames(mapDoc)
# idx = 0
# for df in dfList:
#     print(df.name)
#     print(df.spatialReference.name)
#     df.spatialReference.scale = 5000000
#     df.name = "Frame {0}".format(idx)
#     print (df.name)
#     df.zoomToSelectedFeatures()
#
# # change the scale of map
# mapDoc.save()


###
# make a feature layer to use in other tests
###
# fcLyr = r"C:\Users\llassetter\Grid-I\myfeat.lyr"
#
# if os.path.isfile(fcLyr):
#     os.remove(fcLyr)
#
# result = arcpy.MakeFeatureLayer_management(sFc, "newFeat_lyr")
# result = arcpy.SaveToLayerFile_management("newFeat_lyr", fcLyr)
#
# lyr = arcpy.mapping.Layer(fcLyr)
# lyrs = arcpy.mapping.ListLayers(mapDoc) # another way to get a layer
# for l in lyrs:
#     print (l.name)


###
# make a feature layer to use in other tests
###
# lyr = arcpy.mapping.Layer(sFc)
# print ("\n*** layer properties")
# print (lyr.name)
# print (lyr.datasetName)
# print (lyr.dataSource)

###
# any broken data sources?
###
brokenList = arcpy.mapping.ListBrokenDataSources(mapDoc)
for l in brokenList:
    print (l.name)



del mapDoc