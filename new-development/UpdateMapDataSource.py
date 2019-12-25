import arcpy
import os
import datetime

class UpdateMapDataSource():
    """Replace all datasets in features and tables"""

    def __init__(self):
        pass
        # self.gs_backend = os.getenv("GS_BACKEND")
        # self.mapFilename = None
        # self.mxd = None
        #
        # if not self.gs_backend:
        #     print "warning: Invalid GS_BACKEND"

    def setMxd(self, mapFilename):

        self.mapFilename = mapFilename

        # if not os.path.isfile(mapFilename):
        #     mapFilename = os.path.join(self.gs_backend,"mxd", mapFilename)
        #     if not os.path.isfile(mapFilename):
        #         mapFilename = os.path.join(self.gs_backend, mapFilename)
        #         if not os.path.isfile(mapFilename):
        #             print "error: Could not find mdxFilename: " % self.mapFilename
        #             os._exit(1)

        self.mxd = arcpy.mapping.MapDocument(mapFilename)


    def replaceDataSets(self, mapFilename, fromSde, toSde, validate=True, replaceMap=False):

        self.setMxd(mapFilename)

        try:
            self.mxd.findAndReplaceWorkspacePaths(fromSde, toSde, validate)
            if replaceMap:
                self.mxd.save()
            else:
                newFilename = mapFilename[0:-4] + "_v1.mxd"
                self.mxd.saveACopy(newFilename)

            print "finished replacing datasources in %s" % mapFilename

        except BaseException as err:
            print "Error replacing datasources in %s" % mapFilename
            print err.message


if __name__ == '__main__':
    r = UpdateMapDataSource()
    gs_backend = os.getenv("GS_BACKEND")

    # mapFilename = os.path.join(gs_backend, "mxd", "Grid.mxd")
    # fromSde = r"\\gssrvdev\C\Users\gs\gs_backend\Operations.sde"
    # toSde = r"C:\epe\gs_backend\operations.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "Operations_Phase.mxd")
    # fromSde = r"\\gssrvdev\C\Users\gs\gs_backend\Operations.sde"
    # toSde = r"C:\epe\gs_backend\operations.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "Operations_Voltage.mxd")
    # fromSde = r"\\gssrvdev\C\Users\gs\gs_backend\Operations.sde"
    # toSde = r"C:\epe\gs_backend\operations.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "Planning_Phase.mxd")
    # fromSde = r"\\gssrvdev\C\Users\gs\gs_backend\Planning.sde"
    # toSde = r"C:\epe\gs_backend\planning.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)


    mapFilename = os.path.join(gs_backend, "mxd", "hotec_gridsight.mxd")
    fromSde = r"C:\Dropbox\EPE\Demo\hotec_gridsight.sde"
    toSde = r"c:\epe\gs_backend\hotec_gridsight.sde"
    r.replaceDataSets(mapFilename, "", toSde, False, True)


    # mapFilename = os.path.join(gs_backend, "mxd", "hotec_g_gridsight.mxd")
    # fromSde = r"C:\Dropbox\EPE\Demo\hotec_gridsight.sde"
    # toSde = r"c:\epe\gs_backend\hotec_gridsight.sde"
    # r.replaceDataSets(mapFilename, "", toSde, False, True)


    # os._exit(0)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_g.mxd")
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_v.mxd")
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_planning.mxd")
    # toSde = r"C:\Users\llassetter\gs_backend\gridi_planning.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_planning2.mxd")
    # toSde = r"C:\Users\llassetter\gs_backend\gridi_planning2.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_planning3.mxd")
    # toSde = r"C:\Users\llassetter\gs_backend\gridi_planning3.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_planning4.mxd")
    # toSde = r"C:\Users\llassetter\gs_backend\gridi_planning4.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)

    # mapFilename = os.path.join(gs_backend, "mxd", "gridi_planning5.mxd")
    # toSde = r"C:\Users\llassetter\gs_backend\gridi_planning5.sde"
    # r.replaceDataSets(mapFilename, fromSde, toSde, False, True)
