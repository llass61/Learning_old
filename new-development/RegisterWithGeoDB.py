import arcpy, os

class RegisterWithGeoDB():

    def __init__(self, sde=None):

        self.backend = os.getenv("GS_BACKEND")
        self.server = os.getenv("GS_SERVER")
        self.sde = sde #os.getenv("GS_SDE")


    def registerTable(self, tables, sde=None):
        if sde != None:
            self.sde = sde

        for table in tables:

            registerTable = os.path.join(self.backend, self.sde, table)

            try:
                arcpy.RegisterWithGeodatabase_management(registerTable)

            except BaseException as error:
                print ("%s" % error.message)



if __name__ == '__main__':

    tables = ['int_data_load_profile','int_model_load','int_res_pf','int_res_study']

    reg = RegisterWithGeoDB()

    sde  = r'C:\Users\llassetter\tmp\operations.sde'
    reg.registerTable(tables,sde)

    sde  = r'C:\Users\llassetter\tmp\planning.sde'
    reg.registerTable(tables,sde)

    # sde  = r'C:\Users\llassetter\tmp\planning2.sde'
    # reg.registerTable(tables,sde)

    # sde  = r'C:\Users\llassetter\tmp\planning3.sde'
    # reg.registerTable(tables,sde)

    # sde  = r'C:\Users\llassetter\tmp\planning4.sde'
    # reg.registerTable(tables,sde)

    # sde  = r'C:\Users\llassetter\tmp\planning5.sde'
    # reg.registerTable(tables,sde)

    # reg.registerTable('int_data_load_profile')
    # reg.registerTable('int_model_load')
    # reg.registerTable('int_res_pf')
    # reg.registerTable('int_res_study')


    print "in script"
