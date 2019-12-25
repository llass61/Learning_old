import arcpy


def listDataFrames(mymap, dfFilter=""):
    dataFrames = arcpy.mapping.ListDataFrames(mymap, dfFilter)
    print (len(dataFrames))
    return dataFrames


def getLayerFile(lyr):
    return arcpy.mapping.Layer(lyr)


def getLayerFromMap(mymap, wcfilter, df):
    return arcpy.mapping.ListLayers(mymap, wcfilter, df)


def isLayerAdded(mymap, wcfilter, df):
    layer = arcpy.mapping.ListLayers(mymap, wcfilter, df)
    return True if len(layer) > 0 else False


def addLayerToMap(dataFrame, layer, tblContentsPos={}):
    print ("adding layer")
    arcpy.mapping.AddLayer(dataFrame, layer)


mymap = arcpy.mapping.MapDocument("C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\map1.mxd")
mymap.author = 'Larry Lassetter'
mymap.summary = 'learn how to use arcpy'

dataframes = listDataFrames(mymap, "Layers")

# add layer if not already on dataframe
hasBeenAdded = isLayerAdded(mymap, "Amata", dataframes[0])
print("Amata is on map: " + str(hasBeenAdded))

amataLyr = None
if not hasBeenAdded:
    amataLyr = getLayerFile(r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\Amata.lyr")
    addLayerToMap(dataframes[0], amataLyr)
    print("Added Amata to map")

# returns layer in a list, should only be one
amataLyr = getLayerFromMap(mymap, "Amata", dataframes[0])[0]


arcpy.mapping.ExportToPDF(mymap, r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\a.pdf")

#amataLyr.name = 'MyAmata'
amataLyr.visible = True;

# have to select one or more features in your layer
lyrExtent = amataLyr.getSelectedExtent()
dataframes[0].extent = lyrExtent

arcpy.mapping.ExportToPDF(mymap, r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\b.pdf")
pdfDoc = arcpy.mapping.PDFDocumentCreate(r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\c.pdf")
pdfDoc.appendPages(r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\a.pdf")
pdfDoc.appendPages(r"C:\Users\llassetter\Documents\ArcGIS\Projects\ArcMapProj1\b.pdf")
pdfDoc.saveAndClose()

mymap.save()

print ("map is saved")
