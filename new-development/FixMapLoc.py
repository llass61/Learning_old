import arcpy
import os
from gridsight import maploc

gs_backend = os.getenv('GS_BACKEND')
sde = os.path.join(gs_backend, "hotec.sde", "grid_loads")
#arcpy.env.workspace = sde

def getLoadLocations():
    locs = []

    with arcpy.da.SearchCursor(sde, ['OBJECTID', 'SECNAME', 'MAPLOC', 'MAPLOC_XF', 'SHAPE@X', 'SHAPE@Y']) as cursor:
        for r in cursor:
            locs.append(r)

    with open('mapLocData.txt','w') as mapLocFile:
        for l in locs:
            ll = list(l)
            if l[4] and l[5]:
                mapLoc = maploc.getMapLoc(l[4], l[5], gspec)
                loc = maploc.formatMapLoc(mapLoc)
                ll.insert(2,loc.replace("-",""))
            mapLocFile.write(",".join(str(elem) for elem in ll))
            mapLocFile.write("\n")

    return locs

gspec = maploc.mapLocGetGridSpec()
# locs = getLoadLocations()

#val = mapLocGetN()
#val2 = mapLocGetDet()
fc = r"C:\Users\llassetter\gs_backend\gridi.sde\g_key"
maploc.getCoordinateSystem(fc, 18, 2)

# gspec = maploc.mapLocGetGridSpec()
# loc = maploc.getMapLoc(-97.36221811, 31.66433554,gspec)
# toloc = maploc.toMapLoc('347234025046')
pass
