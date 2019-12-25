import arcpy
from os.path import join

tGdb = r"C:\Users\llassetter\Documents\ArcGIS\Default.gdb"
sGdb = r"C:\Users\llassetter\Grid-I\epedev005-ll.sde"

arcpy.env.workspace = sGdb;
sFeatClasses = arcpy.ListFeatureClasses()
sTables = arcpy.ListTables()

arcpy.env.workspace = tGdb
tFeatClasses = arcpy.ListFeatureClasses()
tTables = arcpy.ListTables()

# lets make schemas match
for fc in sFeatClasses:
    print ('feature class: ' + fc)
for t in sTables:
    print ('Table: ' + t)


#arcpy.AcceptConnections(tGdb, False)
#arcpy.DisconnectUser(tGdb, "ALL")

for fc in sFeatClasses+sTables:
    flds = arcpy.ListFields(join(sGdb, fc))

    for fld in flds:
        arcpy.AddField_management(join(tGdb, fc), field_name=fld.name,
                                  field_type=fld.type,
                                  field_precision=fld.precision,
                                  field_scale=fld.scale,
                                  field_length=fld.length,
                                  field_alias=fld.aliasName,
                                  field_is_nullable=fld.isNullable,
                                  field_is_required=fld.required,
                                  field_domain=fld.domain
                                  )
    print (flds)

