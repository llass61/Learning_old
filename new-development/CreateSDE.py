import arcpy, os

class CreateSDE():
    """Creates an SDE file.  This is used to create the sde's that will
       will be used for the geoservices.
    """

    PLATFORM       = "POSTGRESQL"
    AUTH_CONN_TYPE = "DATABASE_AUTH"
    SDE_USER_NAME  = "sde"
    SDE_USER_PW    = "epeconsulting"
    SAVE_USER_INFO = "SAVE_USERNAME"
    SDE_SCHEMA     = "sde"
    VERSION_NAME   = "SDE.DEFAULT"
    SAVE_VERSION_INFO   = "SAVE_VERSION"

    def __init__(self):

        self.backend = os.getenv("GS_BACKEND")
        self.tools = os.path.join(self.backend,"..","gs_tools")
        self.server = os.getenv("GS_SERVER")
        self.sde = os.path.join(self.backend, os.getenv("GS_SDE"))

        # set defaults
        self.folderName = self.backend
        self.fileName = None
        self.platform = self.PLATFORM
        self.instance = self.sde
        self.authType = self.AUTH_CONN_TYPE
        self.username = self.SDE_USER_NAME
        self.password = self.SDE_USER_PW
        self.saveUserInfo = self.SAVE_USER_INFO
        self.databaseName = None
        self.schema = self.SDE_SCHEMA
        self.versionName = self.VERSION_NAME
        self.saveVersionInfo = self.SAVE_VERSION_INFO

        self.newConnSde = None


    def createSDE(self, filename, instance, databaseName, **kwargs):
        # Set variables
        self.folderName = kwargs.get('folderName', self.folderName)
        self.fileName = filename
        self.platform =  kwargs.get('platform', self.platform)
        self.instance = instance
        self.authType = kwargs.get('platform', self.authType)
        self.username = kwargs.get('platform', self.username)
        self.password = kwargs.get('platform', self.password)
        self.saveUserInfo = kwargs.get('platform', self.saveUserInfo)
        self.databaseName = databaseName
        self.schema = kwargs.get('platform', self.schema)
        self.versionName = kwargs.get('versionName', self.versionName)
        self.saveVersionInfo = kwargs.get('saveVersionInfo', self.saveVersionInfo)

        # Process: Use the CreateArcSDEConnectionFile function
        try:

            self.newConnSde = arcpy.CreateDatabaseConnection_management (self.folderName,
                                                    self.fileName,
                                                    self.platform,
                                                    self.instance,
                                                    self.authType,
                                                    self.username,
                                                    self.password,
                                                    self.saveUserInfo,
                                                    self.databaseName,
                                                    self.schema)
            print("Create %s sde complete!" % self.fileName)
            return self.newConnSde
        except BaseException as error:
            print("Error creating sde: %s" % error.message)
            return None


if __name__ == '__main__':

    c = CreateSDE()

    folderName  = r'C:\Users\llassetter\tmp'
    c.folderName = folderName

    # class properties will retain last setting unless overridden in
    # createSDE method call!

    c.password = "Hotec_23688"
    # new app version
    c.createSDE("operations.sde", "gridsight", "hotec")
    c.createSDE("planning.sde", "gridsight", "hotec_planning")
    # c.createSDE("hotec_planning2_gridsight.sde", "gridsight", "hotec_planning2")
    # c.createSDE("hotec_planning3_gridsight.sde", "gridsight", "hotec_planning3")
    # c.createSDE("hotec_planning4_gridsight.sde", "gridsight", "hotec_planning4")
    # c.createSDE("hotec_planning5_gridsight.sde", "gridsight", "hotec_planning5")

    print("Finished!")
