import arcpy
import os

class CreateOfflineMap():
    """Creates offline map as 'mmpk' package"""


    def __init__(self):
        self.gs_backend = os.getenv("GS_BACKEND")
        self.user = os.getenv("GS_BACKEND")
        self.password = os.getenv("GS_BACKEND")
        self.map = "Map"
        self.mmpkFile = r"C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMapChase\map.mmpk"
        self.mapTitle = "My Map"
        self.mapSummary = mapTitle
        self.mapDesc = mapTitle


    def bacupExistingOutputFile():




aprx = arcpy.mp.ArcGISProject(proj)

print (aprx.defaultGeodatabase);
#select map
maps = aprx.listMaps()

# remove mmpk if exists
if (arcpy.Exists(mmpkFile)):
    print ("It Exists")
    os.remove(mmpkFile)

aprx.save()

mapObj = ""
for m in maps:
    if (m.name == map):
        mapObj = m

#create mmpk from map
arcpy.management.CreateMobileMapPackage([mapObj],
                                        mmpkFile, None,
                                        None,
                                        "DEFAULT", "CLIP",
                                        mapTitle,
                                        mapSummary,
                                        mapDesc,
                                        "mobile, map, offline")
print (mapObj)
print ("finished creating mmpk!")

print ("Sharing Package")
# arcpy.SharePackage_management(mmpkFile, "llassetter", "!OsuBeavers1989",
#                               mapSummary, "hotec, mobile", "Credits",
#                               "MYGROUPS", None, "MYORGANIZATION")
arcpy.SharePackage_management(mmpkFile, "llassetter", "!OsuBeavers1989",
                              mapSummary, "hotec, mobile", organization="MYORGANIZATION")

print ("finished sharing package")
aprx.save()

pass