import arcpy
from os.path import join


def findFcField(fc, field):
    fields = arcpy.ListFields(fc)
    fld = [f for f in arcpy.ListFields(fc) if f.name == field]
    return fld[0]

def testUpdateCursor(fc):
    with arcpy.da.UpdateCursor(fc, '*', None) as uc:
        flds = uc.fields

        for r in uc:
            print (r)
            rd = dict(zip(flds, r))
            pass


myGDB = 'C:\Users\llassetter\Grid-I\epedev005-ll.sde'
ret = arcpy.env.workspace = myGDB

sFclasses = arcpy.ListFeatureClasses()

sTabs = arcpy.ListTables()

print (sFclasses)
print (sTabs)
print (sFclasses + sTabs)

symFld = findFcField( join(myGDB, 'hotec.sde.grid_powerlines'), 'sym')

desc = arcpy.Describe( join(myGDB, 'hotec.sde.grid_powerlines') )

pass