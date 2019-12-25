import arcpy
import os

class EPEUtils(object):

    def __init__(self, workspace=None):
        self.workspace = workspace

        if (self.workspace == None):
            print("No workspace given")
        elif (arcpy.Exists(self.workspace) == False):
            print("Workspace {0} does not exist".format(self.workspace))
        else:
            arcpy.env.workspace = workspace

    def getSpatialRefs(self, featureList=None):
        if (featureList == None):
            featureList = arcpy.ListFeatureClasses()

        for fc in featureList:
            with arcpy.da.SearchCursor(fc, ["SHAPE@"]) as cursor:
                for row in cursor:
                    # print ("{0}: {1}".format(fc, row[0].WKT))
                    print ("{0}: {1}".format(fc, row[0].spatialReference.name))
                    break


    def isValid(self, obj, title=None):

        if (obj == None):
            print("No {0} given".format( title if title else "parameter"))
            return False

        if (arcpy.Exists(obj) == False):
            print("{0} does not exist".format(obj))
            return False

        return True



ws = r'C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMap\HotecOfflineMap.gdb'

epe = EPEUtils(ws)
epe.getSpatialRefs()



pass