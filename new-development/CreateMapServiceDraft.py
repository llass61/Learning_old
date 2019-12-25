import arcpy, os
import xml.dom.minidom as DOM


class CreateMapServiceDraft():
    """Publish all EPE's geoservices to ArcGIS server"""


    def __init__(self, arcgisServer):
        self.arcgisServer = arcgisServer


    def setArcgisServer(self, arcgisServer):
        if os.path.isfile(arcgisServer):
            self.arcgisServer = arcgisServer
            print ("arcgisServer set to: %s" % arcgisServer)
        else:
            print ("error: arcgisServer file not found: %s" % arcgisServer)


    def createMapServiceDefDraft(self, mxd, sddraft, service, 
                                 serviceType, copyData, folder, summary, tags, 
                                 overwrite=False):
        
        arcpy.mapping.CreateMapSDDraft(mxd, sddraft, service, serviceType,
                                       self.arcgisServer, copyData, folder, 
                                       summary, tags)

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


if __name__ == '__main__':

    backend = os.getenv("GS_BACKEND")
    server = os.getenv("GS_SERVER")
    sde = os.getenv("GS_SDE")
    agsServer = r"C:\Users\llassetter\gs_tools\arcgis_epedev005-ll.ags"
    sdeConn = os.path.join(backend, sde)    
    sddDir = os.path.join(backend, "serviceDefinitions")

    mapFilename = os.path.join(backend, "mxd", "gridi.mxd")

    sd = os.path.join(sddDir, "gridi.sd")
    sd2 = os.path.join(sddDir, "connectivityCheck.sd")
    serviceType = "FROM_CONNECTION_FILE"
    summary = "GRID-i map"
    tags = "gridi"
    service = "gridi"
    sddraft = os.path.join(backend, "serviceDefinitions", "%s.sddraft" % service)

    csd = CreateMapServiceDraft(agsServer)

    csd.loadServiceDefinitionFiles(sddDir)
    csd.uploadServiceDefinition(sd2)
    map = arcpy.mapping.MapDocument(mapFilename)
    csd.createMapServiceDefDraft(map, sddraft, service, serviceType,
                                 False, None, summary, tags, True)