import arcpy
import os

def findFirstField(fc, flds, val):

    cursor = arcpy.da.SearchCursor(fc,flds)
    for row in cursor:
        if val == row[0]:
            print ("found field {0}; value = {1}".format(flds[0], row[0]))
            return row

    return None

def findFirstField2(fc, flds, val):

    fieldName = "PHASECODE"
    delimField = arcpy.AddFieldDelimiters(fc,fieldName)
    cursor = arcpy.da.SearchCursor(fc,flds, delimField + " = '{0}'".format(val))
    for row in cursor:
        print (row[0])
    pass

    return None

def updateField(fc, flds, oldVal, newVal):

    with arcpy.da.UpdateCursor(fc,flds) as cursor:
        for row in cursor:
            if oldVal == row[0]:
                print ("changing field {0} value from {1} to {2}".format(flds[0], oldVal, newVal))
                row[0] = newVal
                cursor.updateRow(row)
                return True

    return False


sGdb = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde"
sFc = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde\hotec.sde.grid_equipment"

arcpy.env.workspace = sGdb

gridEquip = arcpy.ListFeatureClasses('hotec.sde.grid_equipment')

foundFc = findFirstField2(sFc, ['PHASECODE'], "A")
print (foundFc)

# udates data - then returns to correct value
#print (updateField(sFc, ['PHASECODE'], "A", "D"))
#print (updateField(sFc, ['PHASECODE'], "D", "A"))

#
# check if tabl/field name is valid
#
tblName = arcpy.ValidateTableName("all roads", arcpy.env.workspace)
print (tblName)
tblName = arcpy.ValidateTableName("grid_equipment")
print (tblName)
fldName = arcpy.ValidateFieldName("big poles")
print (fldName)

# CreateUniqueName only used on datasets (not fields)
uniqueNm = arcpy.CreateUniqueName("data_metering", os.path.join(sGdb))
print (uniqueNm)

# fcList = arcpy.ListFeatureClasses()
# for f in fcList:
#     print (f)

fTblNm = arcpy.ParseTableName("data_metering")
fFldNm = arcpy.ParseFieldName("STATUS")

pass