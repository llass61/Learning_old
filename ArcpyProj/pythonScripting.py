import arcpy


sGdb = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde"

arcpy.env.workspace = sGdb

featureClasses = arcpy.ListFeatureClasses()

print (arcpy.Exists('hotec.sde.g_det'))

fcDescribe = arcpy.Describe(featureClasses[0])
print (fcDescribe.shapeType)
print (fcDescribe.spatialReference)
print (fcDescribe.path)
print (fcDescribe.catalogPath)
print (fcDescribe.baseName)
print (fcDescribe.name)

myWorkspaces = arcpy.ListWorkspaces()
#myIndexes = arcpy.ListIndexes()
myDataSets = arcpy.ListDatasets()
myFiles = arcpy.ListFiles()
myRasters = arcpy.ListRasters()
myTables = arcpy.ListTables()
myVersions = arcpy.ListVersions(arcpy.env.workspace)

install = arcpy.GetInstallInfo()
for key in install:
    print ("{0}: {1}".format(key,install[key]))

pass


