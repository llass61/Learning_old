import arcpy, sys


shapeFileNm = r"C:\Users\llassetter\Documents\Amata\Amata.shp"
mapName = r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\map1.mxd"

map = arcpy.mapping.MapDocument(mapName)
df = arcpy.mapping.ListDataFrames(map,"Layers")[0]
layerList = arcpy.mapping.ListLayers(map, "hotec.sde.map_plat_lines")
platLinesLayer = layerList[0]

# create a FC from shapefile
AmataOrigFc = arcpy.mapping.Layer(shapeFileNm)
# print (AmataOrigFc.datasetName)
# print (AmataOrigFc.dataSource)
# print (AmataOrigFc.name)

# move the features in shapefile
with arcpy.da.UpdateCursor(AmataOrigFc, ['SHAPE@XY']) as cursor:
    for row in cursor:
        cursor.updateRow([[row[0][0] + (-18),
                           row[0][1] + (25)
                           ]])

# arcpy.MakeFeatureLayer_management(AmataOrigFc, "AmataN")
# addLayer = arcpy.mapping.Layer("AmataN")
# arcpy.mapping.AddLayer(df, addLayer)

arcpy.Append_management(AmataOrigFc, platLinesLayer, "NO_TEST", )

print (map)
print(df)

#map.save()