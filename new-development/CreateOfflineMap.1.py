import arcpy
import os

        
proj = r"C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMapChase\HOTEC Explorer Maps.aprx"

# map = "HOTEC Satellite Map"
# mmpkFile = r"C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMapChase\hotecOfflineSatellite.mmpk"
# mapTitle = "HOTEC Satellite Map"
# mapSummary = mapTitle
# mapDesc = mapTitle


# map = "HOTEC Street Map"
# mmpkFile = r"C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMapChase\hotecOfflineStreet.mmpk"
# mapTitle = "HOTEC Street Map"
# mapSummary = mapTitle
# mapDesc = mapTitle

map = "Map"
mmpkFile = r"C:\Users\llassetter\Documents\ArcGIS\Projects\HotecOfflineMapChase\map.mmpk"
mapTitle = "My Map"
mapSummary = mapTitle
mapDesc = mapTitle


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