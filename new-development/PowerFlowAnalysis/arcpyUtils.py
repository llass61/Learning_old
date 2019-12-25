import os, arcpy
from addaUtils import wrap, delKey, reKey

def fullFcPath(gsDb, gsPf, fcn):
    return os.path.join(gsDb, gsPf+fcn)

def readSettings(gsDb, gsPf, keys, **kwargs):
    settingsTab = kwargs.get('settings_tab', 'settings')
    settings= None
    with arcpy.da.SearchCursor(fullFcPath(gsDb, gsPf, settingsTab), ['key', 'val'], "key in ('"+ "','".join(keys)+"')") as sc:
        settings= {r[0]:r[1] for r in sc}
    return settings

def cleanFc(fc):
    with arcpy.da.UpdateCursor(fc, ["objectid"]) as gs: 
        for r in gs: gs.deleteRow()

def listFields(fc):
    with arcpy.da.SearchCursor(fc, ["*"]) as gs: 
        return list(gs.fields)

def updateDomain(env, domain, tabs, c_tok='equipref', **kwargs):
    cleanFirst = kwargs.get('clean_first', False)
    autoCreate = kwargs.get('auto_create', True)
    d_tok = kwargs.get('d_tok', None)
    desc = kwargs.get('desc', '')
    verbose = kwargs.get('verbose', True)
    justCreated = False

    domains = [d for d in arcpy.da.ListDomains(env) if d.name == domain]
    if len(domains) <= 0:
        if autoCreate:
            arcpy.CreateDomain_management(env, domain, desc, "TEXT", "CODED")
            justCreated = True
            print("Domain not found, created...")
        else:
            print("Domain not found, auto create disabled. No updates where made.")
            return

    if not justCreated:
        dom = domains[0]
        if dom.domainType != 'CodedValue':
            print("Error: requested domain (%s) is not a coded value domain" % (domain))
            return
    print("Obtaining coded values...")
    cl= {}
    for t in tabs:
        with arcpy.da.SearchCursor(env+'\\'+t, [c_tok, d_tok] if d_tok else [c_tok], sql_clause=('DISTINCT', None)) as s:
            cl.update({r[0]: (r[1] if d_tok else r[0]) for r in s})
    print("Coded values: %s"%str(cl))

    print("Obtaing exclusive access to schema...")
    arcpy.AcceptConnections(env, False)
    arcpy.DisconnectUser(env, 'ALL')
    try:
        if cleanFirst and not justCreated: 
            print("Cleaning the old domain...")
            arcpy.DeleteCodedValueFromDomain_management(env, domain, dom.codedValues.keys())
        print("Adding new values...")
        for c, v in cl.items():
            arcpy.AddCodedValueToDomain_management(env, domain, c, v)
    except:
        print("Something went wrong.")
    finally:
        arcpy.AcceptConnections(env, True)

def rebuildCodedDomain(w, domain, cl, cleanFirst = False, desc= None):
    ds= arcpy.da.ListDomains(w)
    dm= [d for d in ds if d.name == domain]
    if len(dm) == 0:
        arcpy.CreateDomain_management(w, domain, desc, 'TEXT', 'CODED')
    else: 
        if cleanFirst:
            for c in dm[0].codedValues.keys(): 
                arcpy.DeleteCodedValueFromDomain_management(w, domain, c)
    for c, v in cl.items():
        arcpy.AddCodedValueToDomain_management(w, domain, c, v)

def loadFc(featureClassName, **kwargs):
    keyField= kwargs.get('keyField', None)
    fields= kwargs.get('fields', None)
    whereClause= kwargs.get('whereClause', None)
    tWkid= kwargs.get('tWkid', 2277)

    features = {}
    desc = arcpy.Describe(featureClassName)
    isFc = True if desc.dataElementType=='DEFeatureClass' else False

    eFields = (['*','SHAPE@'] if isFc else '*') if fields is None else fields
    kf = 'OBJECTID' if keyField is None else keyField
    if '*' not in eFields and kf not in fields:
        eFields.insert(0, kf)
    fcType = desc.shapeType if isFc else None
    if fcType == 'Polyline' and 'SHAPE@LENGTH' not in eFields: eFields.append('SHAPE@LENGTH') 

    tsr = None if (isFc or twkid is None) else arcpy.SpatialReference(twkid)
    with arcpy.da.SearchCursor(featureClassName, eFields, whereClause, spatial_reference= tsr) as sc:
        if not hasattr(sc, 'fields') or kf not in sc.fields:
            print("Error in fields. %s"%('Fields: %s'%str(sc.fields) if hasattr(sc, 'fields') else 'No fields attribute on search cursor.'))
            return features
        sli = sc.fields.index('SHAPE@LENGTH') if fcType == 'Polyline' else -1
        for r in sc:
            f = dict(zip(sc.fields, r))
            reKey(f, 'SHAPE@LENGTH', 'length') #.getLength('PRESERVE_SHAPE') # always in meters
            for k in ['st_length(shape)', 'shape']: delKey(f, k)
            features[f[kf]] = f

    return features

def rebuildCodedDomainFromTables(w, domain, tabs, keyField, cleanFirst= False, desc= None):
    ids= []
    for t in tabs:
        with arcpy.da.SearchCursor(w+'\\'+t, [keyField]) as s:
            ids += [r[0] for r in s]
    return rebuildCodedDomain(w, domain, {r:r for r in ids}, cleanFirst, desc)

def createFieldFromTemplate(targetfc, template_field, name= None, alias_name= None):
    if name is None:
        name, an= template_field.name, template_field.aliasName
    else:
        name, an= name, name if alias_name is None else alias_name

    arcpy.AddField_management(targetfc, field_name= name, field_type= template_field.type, 
                              field_precision= template_field.precision, field_scale= template_field.scale, 
                              field_length= template_field.length, field_alias= an, 
                              field_is_nullable= template_field.isNullable, field_is_required= template_field.required, 
                              field_domain= template_field.domain)

def deleteFields(tGdb, fc_name, fl):
    arcpy.AcceptConnections(tGdb, False)
    arcpy.DisconnectUser(tGdb, 'ALL')
    fc= os.path.join(tGdb, fc_name)
    for fn in fl:
        try: arcpy.DeleteField_management(fc, fn)
        except: print("Error deleting field %s"%fn)
    arcpy.AcceptConnections(tGdb, True)

def printMsg(notGP, msg):
    """ Prints a message to the right channel depending on the run mode
    """
    if notGP:
        print(msg)
    else:
        arcpy.AddMessage(msg)

def printErr(notGP, msg):
    """ Prints an error to the right channel depending on the run mode
    """
    if notGP:
        print(msg)
        # exit()
    else:
        arcpy.AddError(msg)

def printWar(notGP, msg):
    """ Prints a warning to the right channel depending on the run mode
    """
    if notGP:
        print(msg)
    else:
        arcpy.AddWarning(msg)

def enterSafeSde(func, *args, **kwargs):
        tGdb= list(args)[0]
        arcpy.AcceptConnections(tGdb, False)
        arcpy.DisconnectUser(tGdb, 'ALL')

def exitSafeSde(func, *args, **kwargs):
        tGdb= list(args)[0]
        arcpy.AcceptConnections(tGdb, True)

safeRunSde= wrap(enterSafeSde, exitSafeSde)# note that this decorator expects the tGdb to be always the firs argument

