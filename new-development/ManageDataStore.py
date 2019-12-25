import arcpy, os

class ManageDataStore():
    """Manages (add,remove) datastores on an arcgis server"""

    POSTGRES_CONN_STR = "SERVER=%s;INSTANCE=sde:postgresql:%s;DBCLIENT=postgresql;DB_CONNECTION_PROPERTIES=%s;DATABASE=%s;USER=sde;PASSWORD=%s;VERSION=sde.DEFAULT;"
    # POSTGRES_CONN_STR = "SERVER=%s;INSTANCE=sde:postgresql:%s;DBCLIENT=postgresql;DB_CONNECTION_PROPERTIES=%s;DATABASE=%s;USER=sde;PASSWORD=%s;"


    def __init__(self, agsServer):

        self.backend = os.getenv("GS_BACKEND")
        self.tools = os.path.join(self.backend,"..","gs_tools")
        self.server = os.getenv("GS_SERVER")
        self.sde = os.path.join(self.backend, os.getenv("GS_SDE"))
        self.agsServer = os.path.join(self.tools, agsServer)

        self.existingDataStores = None


    def printDataStores(self, dsType):
        if not self.existingDataStores:
            self.getDataStores(dsType)

        for ds in self.existingDataStores:

            print ds[0]
            for elem in ds[1].split(';'):
                if not elem.startswith("ENCRYPTED"):
                    print "   %s" % elem


    def getDataStores(self, dsType):
        self.existingDataStores = arcpy.ListDataStoreItems(
                                        self.agsServer, dsType)


    def removeDataStores(self, dsType):
        if not self.existingDataStores:
            self.getDataStores(dsType)

        for ds in self.existingDataStores:
            self.removeDataStore(dsType, ds[0])


    def removeDataStore(self, dsType, dsConnName):
        if not self.existingDataStores:
            self.getDataStores(dsType)

        # if dsConnName in self.getDataStores
        try:
            arcpy.RemoveDataStoreItem (self.agsServer, dsType, dsConnName)
            print ("Removed Datastore: %s" % dsConnName)
            self.getDataStores(dsType)

        except Exception as ex:
            print ("Error removing %s" % dsConnName)
            print (ex.message)


    def getConnStr(self, server, db, password):
            return ManageDataStore.POSTGRES_CONN_STR % (server, server, server, db, password)


    def registerDataStore(self, dsConnName, serverPath, clientPath,
                          db, password, dsType="DATABASE", replace=False):
        returnValue = True

        if not self.existingDataStores:
            self.getDataStores(dsType)

        print("Registering %s" % dsConnName)

        sp = self.getConnStr(serverPath, db, password)
        cp = self.getConnStr(clientPath, db, password)

        returnValue = True
        try:
            if replace and dsConnName in [ds[0] for ds in self.existingDataStores]:
                self.removeDataStore(dsType, dsConnName)

            ret = arcpy.AddDataStoreItem(self.agsServer, dsType,
                                         dsConnName, sp, cp)

            if ret != 'Success':
                print("Error: Registering %s" % dsConnName)
                print(ret)

            # reload the list of existing datastores
            self.getDataStores(dsType)

        except Exception as ex:
            print ("Error registering %s" % dsConnName)
            print (ex.message)
            returnValue = False

        return returnValue


    def registerDataStoreSde(self, dsConnName, serverPath,
                             clientPath, dsType="DATABASE", replace=False):
        if not self.existingDataStores:
            self.getDataStores(dsType)

        client = os.path.join(self.backend, clientPath)
        server = os.path.join(self.backend, serverPath)
        returnValue = True

        print("Registering %s" % dsConnName)

        try:
            if replace and dsConnName in [ds[0] for ds in self.existingDataStores]:
                self.removeDataStore(dsType, dsConnName)

            ret = arcpy.AddDataStoreItem(self.agsServer, dsType,
                                         dsConnName, server, client)

            if len(ret) == 0:
                print("Error: Registering %s" % dsConnName)

            # reload the list of existing datastores
            self.getDataStores(dsType)

        except Exception as ex:
            print ("Error registering %s" % dsConnName)
            print (ex.message)
            returnValue = False

        return returnValue


if __name__ == '__main__':



    # agsServer =os.path.join(tools, "epeeng042-as.ags")
    # agsServer =os.path.join(tools, "epedev005-ll.ags")
    # agsServer =os.path.join(tools, "gssrvdev.ags")
    # agsServer =os.path.join(tools, "gssrvrel.ags")
    # agsServer =os.path.join(tools, "gridsight.ags")

    # agsServer = r"C:\Users\llassetter\gs_tools\gssrvdev.ags"
    # agsServer = r"C:\Users\llassetter\gs_tools\arcgis_epedev005-ll.ags"
    # sdeConn = os.path.join(os.getenv("GS_BACKEND"),"eneri_planning.sde")

    # sdeConn = r'C:\Users\llassetter\gs_clients\hotec\backend\sde\eneri.sde'

    # rds.printDataStores(dsType)

    # rds.removeDataStore(dsType, "eneri")
    # rds.removeDataStore(dsType, "eneri_planning")
    # rds.removeDataStore(dsType, "eneri_planning2")
    # rds.removeDataStore(dsType, "eneri_planning3")
    # rds.removeDataStore(dsType, "eneri_planning4")
    # rds.removeDataStore(dsType, "eneri_planning5")

    agsServer = "gridsight.ags"
    rds = ManageDataStore(agsServer)

    dsType = "DATABASE"
    client = 'localhost'
    server = 'gridsight'

    rds.printDataStores(dsType)
    rds.removeDataStores(dsType)
    # rds.removeDataStore(dsType, "eneri_planning")

    rds.registerDataStore("operations", server, client, "hotec", "Hotec_23688")
    rds.registerDataStore("planning", server, client, "hotec_planning", "Hotec_23688")


    # rds.getDataStores(dsType)
    # cp = ManageDataStore.POSTGRES_CONN_STR % (client, client, client, "hotec", "epeconsulting")
    # sp = ManageDataStore.POSTGRES_CONN_STR % (server, server, server, "hotec", "epeconsulting")
    # rds.registerDataStore("Operations", sp, cp, dsType, True)
    # rds.registerDB("Operations", server, client, "hotec", "epeconsulting")
    # rds.registerDB("Planning", server, client, "hotec_planning", "epeconsulting")


    # rds.registerDataStore("hotec", server, client, "hotec", "epeconsulting")
    # rds.registerDataStore("hotec_planning", server, client, "hotec_planning", "epeconsulting")
    # rds.registerDataStore("hotec_planning2", server, client, "hotec_planning2", "epeconsulting")
    # rds.registerDataStore("hotec_planning3", server, client, "hotec_planning3", "epeconsulting")
    # rds.registerDataStore("hotec_planning4", server, client, "hotec_planning4", "epeconsulting")
    # rds.registerDataStore("hotec_planning5", server, client, "hotec_planning5", "epeconsulting")

    # rds.registerDataStore(dsType, "eneri", sde, sde,True)
    # rds.registerDataStore(dsType, "eneri_planning", sde, sde,True)
    # rds.registerDataStore(dsType, "eneri", sde, sde,True)
    # rds.registerDataStore(dsType, "eneri", sde, sde,True)
    # rds.registerDataStore(dsType, "eneri", sde, sde,True)
    # rds.registerDataStore(dsType, "eneri", sde, sde,True)

    print("Finished!")
