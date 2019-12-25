import arcpy
import os
import subprocess
import ConfigParser
import xml.dom.minidom as DOM
import ManageServices

PYTHON = r"C:\Python27\ArcGIS10.5\python.exe"
ADMIN_DIR = r"C:\Program Files\ArcGIS\Server\tools\admin"


class PublishServicesNew():
    """Publish all EPE's geoservices to ArcGIS server"""

    def __init__(self, arcgisServer=None):
        self.arcgisServer = arcgisServer
        self.connected = False

    def connect(self, arcgisServer):
        self.arcgisServer = arcgisServer

    def getMap(self, mapFilename):
        return arcpy.mapping.MapDocument(mapFilename)


    def createServiceDescDraft(self, mxd, sddraft, service, serviceType,
                               arcgisConn, copyData, folder, summary, tags, overwrite=False):
        
        arcpy.mapping.CreateMapSDDraft(mxd, sddraft, service, serviceType,
                                       arcgisConn, copyData, folder, summary, tags)

        # set service type to esriServiceDefinitionType_Replacement
        if overwrite:
            newType = 'esriServiceDefinitionType_Replacement'
            xml = sddraft
            doc = DOM.parse(xml)
            descriptions = doc.getElementsByTagName('Type')
            for desc in descriptions:
                if desc.parentNode.tagName == 'SVCManifest':
                    if desc.hasChildNodes():
                        desc.firstChild.data = newType
            outXml = xml
            f = open(outXml, 'w')
            doc.writexml(f)
            f.close()


    def analyzeServiceDescDraft(self, sddraft):
        analysis = arcpy.mapping.AnalyzeForSD(sddraft)

        # Print errors, warnings, and messages returned from the analysis
        print "The following information was returned during analysis of the MXD:"
        for key in ('messages', 'warnings', 'errors'):
            print '----' + key.upper() + '---'
            vars = analysis[key]
            for ((message, code), layerlist) in vars.iteritems():
                print '    ', message, ' (CODE %i)' % code
                print '       applies to:',
                for layer in layerlist:
                    print layer.name,
                print
        return  0 if analysis['errors'] == {} else 1


    def stageSeviceDesc(self, sddraft, sd, overwrite=False):
        if os.path.exists(sd):
            os.remove(sd)

        arcpy.StageService_server(sddraft, sd)


    def uploadService(self, sd, arcgisConn):
        arcpy.UploadServiceDefinition_server(sd, arcgisConn)
        print "Service successfully published"


if __name__ == '__main__':

    arcgisConn = r"C:\Users\llassetter\gs_tools\arcgis_epedev005-ll.ags"
    sdeConn = os.path.join(os.getenv("GS_BACKEND"),"gridi.sde")
    pgs = PublishServices(arcgisConn)
    
    ds = pgs.getDataStores()
    pgs.registerDataStore(arcgisConn, "DATABASE", 
                            "gridi3", sdeConn, sdeConn)


    exit(0)

    arcgisDir = r"C:\Users\llassetter\Documents\ArcGIS\ArcGISSetup"
    arcgisManageSvc = os.path.join(ADMIN_DIR, "manageservice.py")
    arcgisSite = "http://epedev005-ll:6080"
    arcgisConn = os.path.join(arcgisDir, "arcgisOn_epedev005-ll.ags")
    mapFilename = os.path.join(os.getenv("GS_BACKEND"),"mxd", "gridi.mxd")
    sdeConn = os.path.join(os.getenv("GS_BACKEND"),"gridi.sde")

    pgs = PublishGeoservicesNew()
    existingServices = pgs.listServices(PYTHON, arcgisManageSvc, 'siteadmin', 'epeconsulting', arcgisSite)

    if 'outageAnalysis.GPServer' in existingServices.keys():
        print "YES"
    os._exit(1)
    mxd = pgs.getMap(mapFilename)

    service = "gridi"
    dataStoreConnName = "gridi2"
    serviceType = "FROM_CONNECTION_FILE"
    sddraft = os.path.join(arcgisDir, "%s.sddraft" % service)
    sd = os.path.join(arcgisDir, "%s.sd" % service)
    summary = "GRID-i map"
    tags = "gridi"

    # setup datastore first
    pgs.registerDataStore(arcgisConn, "DATABASE", dataStoreConnName, sdeConn, sdeConn)

    pgs.createServiceDescDraft(mxd, sddraft, service, serviceType, arcgisConn, False, None, summary, tags, False)

    errors = pgs.analyzeServiceDescDraft(sddraft)
    print errors

    pgs.stageSeviceDesc(sddraft, sd)
    pgs.uploadService(sd, arcgisConn)

    pass


