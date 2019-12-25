import arcpy
import os

def printFor(list, name):
    print ("Type {0}: ".format(name))
    for l in list:
        print ("\t" + l)

roadsFc = r"C:\Users\llassetter\Learning\ArcGIS\PythonScriptingForArcGISResources\Data\Exercise07\roads.shp"
hawaiiFc = r"C:\Users\llassetter\Learning\ArcGIS\PythonScriptingForArcGISResources\Data\Exercise08\hawaii.shp"
fGdb = r"C:\Users\llassetter\Documents\ArcGIS\Default.gdb"
sGdb = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde"
sFc = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde\grid_powerlines"

arcpy.env.workspace = sGdb
fclist = arcpy.ListFeatureClasses()

# total = 0
# cnt = 0
# with arcpy.da.SearchCursor("hotec.sde.grid_powerlines",["SHAPE@LENGTH"]) as cursor:
#     for row in cursor:
#         print (row[0])
#         cnt += 1
#         total += row[0]
# print (total)
# print (cnt)


#
# get all feature classes where feature type is Point
#

# pointList = []
# polylineList = []
# polygonList = []
# multiPointList = []
# multiPatch = []
# for fc in fclist:
#     describeFc = arcpy.Describe(fc)
#     if hasattr(describeFc, 'shapeType') and describeFc.shapeType == "Point":
#         pointList.append(fc)

#     if hasattr(describeFc, 'shapeType') and describeFc.shapeType == "Polyline":
#         polylineList.append(fc)

#     if hasattr(describeFc, 'shapeType') and describeFc.shapeType == "Polygon":
#         polygonList.append(fc)

#     if hasattr(describeFc, 'shapeType') and describeFc.shapeType == "MultiPoint":
#         multiPointList.append(fc)

#     if hasattr(describeFc, 'shapeType') and describeFc.shapeType == "MultiPatch":
#         multiPatch.append(fc)

# printFor(pointList, "Point")
# printFor(polylineList, "Polyline")
# printFor(polygonList, "Polygon")
# printFor(multiPointList, "MultiPoint")
# printFor(multiPatch, "MultiPatch")

#
# print out centroid of a Point Feature 'map_poles'
#
# with arcpy.da.SearchCursor("hotec.sde.map_poles", ["SHAPE@"]) as cursor:
#     for row in cursor:
#         x,y = row[0]  # is a tuple
#         print("{0},{1}".format(x,y))

#
# lets output the roads.shp points
#
fc = roadsFc
# with arcpy.da.SearchCursor(fc, ["OID@","SHAPE@"]) as cursor:
#     for row in cursor:
#         print("Feature {0}:".format(row[0]))
#
#         for point in row[1].getPart(0):
#             print ("{0},{1}".format(point.X, point.Y))

# version 2
# fc = hawaiiFc
# with arcpy.da.SearchCursor(fc, ["OID@","SHAPE@"]) as cursor:
#     for row in cursor:
#         print("Feature {0}:".format(row[0]))
#
#         partnum = 0
#         parts = row[1].getPart()
#         for part in row[1].getPart():
#             print ("\tfor part {0}".format(partnum))
#             partnum += 1
#             for point in part:
#                 print ("\t\t{0},{1}".format(point.X, point.Y))


#
# multipart shapes - Hawaii
#




#
# let's pull in a shape file and
# loop over all points
#
# shapeFilews = r"C:\Users\llassetter\Documents\Amata"
# arcpy.env.workspace = shapeFilews
# fc = "Amata.shp"
# with arcpy.da.SearchCursor(fc,["OID@", "SHAPE@"]) as cursor:
#     for row in cursor:
#         print ("Feature {0}:".format(row[0]))
#
#         for point in row[1].getPart(0):
#             print ("{0},{1}".format(point.X,point.Y))

#
# lets loop over all point's and include logic for MultiPoint
#
# with arcpy.da.SearchCursor("hotec.sde.cost_roads", ["OID@","SHAPE@"]) as cursor:
#     for row in cursor:
#         print ("Feature {0}: ".format(row[0]))
#
#         partnum =0
#         for part in row[1]:
#             print ("Part {0}: ".format(partnum))
#
#             for point in part:
#                 print("{0},{1}".format(point.X, point.Y))

#
# lets create a new feature class by reading in data from a file
# the data is in geom.txt
#
# mydir = r"C:\Users\llassetter\Learning\ArcGIS\MyGeom"
# infile = r"C:\Users\llassetter\Learning\ArcGIS\geom.txt"
# fc = "newpoly.shp"
# # first create feature class
# arcpy.CreateFeatureclass_management(mydir, fc) # Polygon is default
#
# cursor = arcpy.da.InsertCursor(os.path.join(mydir,fc),["SHAPE@"])
# array = arcpy.Array()
# point = arcpy.Point()
# fh = open(infile)
# for line in fh.readlines():
#     pointID,point.X,point.Y = line.split()
#     array.add(point)
#
# polygon = arcpy.Polygon(array)
# cursor.insertRow([polygon])
# fh.close()
# del cursor

#
# let's transform the spatial reference
#
# fc = r"C:\Users\llassetter\Learning\ArcGIS\PythonScriptingForArcGISResources\Data\Exercise05\hospitals.shp"
# prjFile = r"C:\Users\llassetter\Learning\ArcGIS\GCS_NAD_1983.prj"
# spatialRef = arcpy.SpatialReference(prjFile) # converting to GCS_NAD_1983
#
# output = open(r"C:\Users\llassetter\Learning\ArcGIS\result.txt","w")
#
# with arcpy.da.SearchCursor(fc, ["SHAPE@"], "", spatialRef) as cursor:
#     for row in cursor:
#         point = row[0].getPart(0)
#         output.write(str(point.X) + " " + str(point.Y) + "\n")


#
# Lets use geometry objects for an analysis (instead of creating a feature class
#
# mydir = r"C:\Users\llassetter\Learning\LearningArcJS\Buffer"
# coordList = [[17.0,20.0], [125.0, 32.0], [4.0, 87.0]]
# pointList = []
# for x,y in coordList:
#     point = arcpy.Point(x,y)
#     pointGeometry = arcpy.PointGeometry(point)
#     pointList.append(pointGeometry)
#
# results = arcpy.Buffer_analysis(pointList, os.path.join(mydir, "buffer.shp"), "10 METERS")

#
# Let's read all features spatial reference coord system
#

# for fc in fclist:
#     with arcpy.da.SearchCursor(fc, ["SHAPE@"]) as cursor:
#         for row in cursor:
#             #print ("{0}: {1}".format(fc, row[0].WKT))
#             print ("{0}: {1}".format(fc, row[0].spatialReference.name))
#             break
gcs = arcpy.SpatialReference(4326)
fc = r"C:\Users\llassetter\gs_backend\gridi.sde\g_key"
with arcpy.da.SearchCursor(fc, ["objectid", "SHAPE@"], "objectid in ('%d','%d')" % (18,2),gcs) as cursor:
        for row in cursor:
            #print ("{0}: {1}".format(fc, row[0].WKT))
            print ("{0}: {1}".format(fc, row[1].spatialReference.name))
            for p in row[1].getPart():
                dv = [ p[1].X - p[0].X, p[1].Y - p[0].Y ]
                print("objectid=%s x=%s  y=%s" % (row[0], str(p[0]),str(p[1])))                
                print ("dx=%s dy=%s" % (dv[0], dv[1]))
            # point = row[0].getPart(0)
            # break