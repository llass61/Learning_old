import arcpy
import os

class PublishServiceDefinitions:
    """Publish EPE's geoservices to specified ArcGIS server
    """


    def __init__(self):
        self.backend = os.getenv("GS_BACKEND")
        self.tools = os.path.join(self.backend,"..","gs_tools")
        self.sdDir = os.path.join(self.backend, "serviceDefinitions")


    def uploadServiceDefinition(self, agsServer, sd):
        """ upload a service definition to a ArcGIS server
        """
        sdFullPath = os.path.join(self.sdDir, sd)
        agsServerFullPath = os.path.join(self.tools, agsServer)
        try:
            if os.path.isfile(sdFullPath):
                arcpy.UploadServiceDefinition_server(sdFullPath, agsServerFullPath)
            else:
                print "%s does not exist" % sdFullPath

        except Exception as ex:
            print "Could not complete publishing operation for " + sdFullPath
            print ex.message

        print arcpy.GetMessages()


    def uploadServiceDefinitions(self, agsServer, sdFilter = []):
        """ will upload all service definitions in a dirctory.  Includes
            ability to pass a filter array to filter out service definitions
        """
        if os.path.isdir(self.sdDir):
            sdFiles = [ f for f in os.listdir(self.sdDir) if f.endswith(".sd") ]

            if sdFilter:
                sdFiles = [x for x in sdFiles if x[0:-3] in sdFilter]

            for sd in sdFiles:
                # sdfile = os.path.join(self.sdDir, sd)
                self.uploadServiceDefinition(agsServer, sd)
                print ""
        else:
            print "%s directory does not exist" % self.sdDir


if __name__ == '__main__':

    pubSvc = PublishServiceDefinitions()

    # pdefs.backend = os.getenv("GS_BACKEND")
    # pdefs.tools = os.path.join(backend,"..","gs_tools")
    # pdefs.server = os.getenv("GS_SERVER")
    # pdefs.sde = os.getenv("GS_SDE")

    # pubSvc.uploadServiceDefinition("epedev002-ll.ags", "intPowerflowAnalysis.sd")
    # pubSvc.uploadServiceDefinition("epedev003-conv.ags", "connectivityCheck.sd")
    # pubSvc.uploadServiceDefinition("epedev005-ll.ags", "connectivityCheck.sd")
    # pubSvc.uploadServiceDefinition("epedev001.ags", "demandDispatch.sd")
    # pubSvc.uploadServiceDefinition("epeeng042-as.ags", "connectivityCheck.sd")
    # pubSvc.uploadServiceDefinition("gssrvdev.ags", "connectivityCheck.sd")
    # pubSvc.uploadServiceDefinition("gssrvrel.ags", "connectivityCheck.sd")
    # pubSvc.uploadServiceDefinition("gridsight.ags", "connectivityCheck.sd")


    # pubSvc.uploadServiceDefinition("epedev005-ll.ags", "eneri.sd")
    # pubSvc.uploadServiceDefinition("epedev005-ll.ags", "eneri_g.sd")
    # pubSvc.uploadServiceDefinition("epedev005-ll.ags", "eneri_v.sd")


    # pubSvc.uploadServiceDefinitions("epedev003-conv.ags")
    # pubSvc.uploadServiceDefinitions("epedev005-ll.ags")
    # pubSvc.uploadServiceDefinitions("epedev002-ll.ags")
    # pubSvc.uploadServiceDefinitions("epedev001-desk.ags")
    # pubSvc.uploadServiceDefinitions("epeeng042-as.ags")
    # pubSvc.uploadServiceDefinitions("gssrvdev.ags")
    # pubSvc.uploadServiceDefinitions("gssrvrel.ags")
    # pubSvc.uploadServiceDefinitions("epedev0001.ags")


    # hotec
    # pubSvc.uploadServiceDefinition("gridsight.ags", "Planning_phase.sd")
    pubSvc.uploadServiceDefinitions("gridsight.ags")

    print("Finished")
