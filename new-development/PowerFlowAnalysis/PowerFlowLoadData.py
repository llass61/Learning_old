import arcpy
import os
import datetime
import logging

from Connection import Connection
from DBStructs import DB_STRUCT


class PowerFlowLoadData():
    """Loads data for power flow analysis"""
    # BRANCH_ELEMENTS = [DB_STRUCT.GRID_EQUIP_SRC, DB_STRUCT.GRID_POW_LINE_FC,
    #                             DB_STRUCT.GRID_EQUIP_TRANS, DB_STRUCT.GRID_EQUIP_SWITCH,
    #                             DB_STRUCT.GRID_EQUIP_REG, DB_STRUCT.GRID_EQUIP_PROT]
    # TOP_ELEMENTS = [DB_STRUCT.GRID_EQUIP_GEN, 'grid_loads', DB_STRUCT.GRID_EQUIP_CAP]
    MODEL_CIR = 'model_circuit'
    ALL_CIRCUITS = []

    def __init__(self, conn, circuitFilter, loadScenario, genScenario):
        self.net = dict()
        self.model = dict()
        self.directRun = False
        self.conn = conn
        self.defaultSpatialRef = arcpy.SpatialReference(2277)
        self.circuitFilter = circuitFilter
        self.loadScenario = loadScenario
        self.genScenario = genScenario
        # self.protConductor = None
        # self.protConstruction = None
        # self.switchConductor = None
        # self.switchConstruction = None

        self.circs = []
        self.circuitsWhereClause = None

        logging.basicConfig(filename='%s.log' %
                            __file__, level=logging.CRITICAL)
        logging.info('HI')

    def fullPath(self, name):
        return os.path.join(self.conn.getSdeFullPath(), name)

    def getFeatureDesc(self, featureClass):
        featureClassPath = self.fullPath(featureClass)
        return arcpy.Describe(featureClassPath)

    def loadFeatureClass(self, featureClass, fields='*',
                         whereClause=None, keyField='secname', sr=None):
        featureClassPath = self.fullPath(featureClass)
        features, dups = {}, []
        sr = self.defaultSpatialRef if sr is None else sr
        desc = self.getFeatureDesc(featureClass)

        # if polyline type, then get length of line
        isPolyline = True if desc.shapeType == 'Polyline' else False
        if isPolyline:
            fields = ['*', 'SHAPE@LENGTH']

        # print featureClassPath

        try:
            with arcpy.da.SearchCursor(featureClassPath, fields, where_clause=whereClause,
                                       spatial_reference=sr) as rows:
                flds = rows.fields
                lenIndex = flds.index('SHAPE@LENGTH') if isPolyline else -1

                for r in rows:
                    f = dict(zip(flds, r))
                    if f[keyField] in features:
                        dups.append(f)
                        print("Duplicate %s detected: %s in %s." %
                              (keyField, f[keyField], featureClass))
                        continue
                    else:
                        if isPolyline:
                            f['length'] = r[lenIndex]

                        features[f[keyField]] = f

        except BaseException as e:
            print("Could not load %s: %s" % (featureClass, str(e)))

        return features

    def loadTable(self, tableName, fields='*', whereClause=None, keyField='equipref'):
        tableNamePath = os.path.join(self.conn.getSdeFullPath(), tableName)
        tables, dups = {}, []

        try:
            with arcpy.da.SearchCursor(tableNamePath, fields, where_clause=whereClause) as rows:
                flds = rows.fields
                for r in rows:
                    f = dict(zip(flds, r))
                    if f[keyField] in tables:
                        dups.append(f)
                        print("Duplicate %s detected: %s in %s." %
                              (keyField, f[keyField], tableNamePath))
                        continue
                    else:
                        tables[f[keyField]] = f

        except BaseException as e:
            print("Could not load %s: %s" % (tableName, str(e)))

        return tables

    # create circuit list for those that are in model_circuits
    # if circuitFilter is an empty array - means all circuits
    def setSelectedCircuits(self):
        self.circs = []
        if len(self.circuitFilter) == 0:
            self.circs = self.net[self.MODEL_CIR].keys()
        else:
            self.circs = [
                c for c in self.net[self.MODEL_CIR].keys() if c in self.circuitFilter]


    # creates the where clause based on filtered circuits (for other features/tables)
    def formatCircuitsWhereClause(self):
        self.circuitsWhereClause = None
        if len(self.circs) > 0:
            self.circuitsWhereClause = "circuit in ('" + "','".join(self.circs) + "')"
        else:
            self.circuitsWhereClause = "circuit is not null and circuit <> ''"


    def buildBranchElems(self):

        self.allBr, self.allId = {}, {}
        for elem in (DB_STRUCT.BRANCH_ELEMENTS + DB_STRUCT.TOP_ELEMENTS):

            if not elem in self.net:
                print("%s data not loaded" % elem)
                continue

            for elemId, elemValue in self.net[elem].items():
                if elemId in self.allId:
                    print("Global duplicate id found at %s in %s." %
                          (elemId, elemValue))
                    continue
                else:
                    self.allId[elemId] = elemValue
                    if elem in DB_STRUCT.BRANCH_ELEMENTS:
                        self.allBr[elemId] = elemValue
        # print("buildBranchElems Done")

    def findMissingCircuitSources(self):
        """
        """
        newEquipment = {}
        for circ in self.circs:
            circuitSecName = self.net[self.MODEL_CIR][circ]['secname']
            if circuitSecName in self.allBr:
                elem = self.allBr[circuitSecName]

                while elem['otype'] != 'source':
                    isEquip = True
                    elemPar = self.loadFeatureClass(
                        DB_STRUCT.GRID_EQUIP_FC, whereClause="secname='%(parentsec)s'" % elem)

                    if not elemPar:
                        isEquip = False
                        elemPar = self.loadFeatureClass(
                            DB_STRUCT.GRID_POW_LINE_FC, whereClause="secname='%(parentsec)s'" % elem)

                    if elemPar:
                        elem = elemPar[elem['parentsec']]
                        self.allBr[elem['secname']] = elem
                        if isEquip:
                            newEquipment[elem['secname']] = elem
                        else:
                            self.net[DB_STRUCT.GRID_POW_LINE_FC][elem['secname']] = elem
                    else:
                        print(
                            "Cannot find the root [%(secname)s] for circuit %(equipref)s." % self.net['model_circuit'][circ])

    def validateParams(self):
        print("validateParams Done")

    def loadData(self):

        self.net[self.MODEL_CIR] = self.loadTable(self.MODEL_CIR)

        self.setSelectedCircuits()
        self.formatCircuitsWhereClause()

        arcpy.AddMessage("Feeders: %s" %
                         ','.join(sorted(self.circs)))

        # getting all featureclass
        self.net[DB_STRUCT.GRID_POW_LINE_FC] = self.loadFeatureClass(
            DB_STRUCT.GRID_POW_LINE_FC, whereClause=self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_LOADS_FC] = self.loadFeatureClass(
            DB_STRUCT.GRID_LOADS_FC, whereClause=self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_TRANS] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                     whereClause="%s and otype='transformer'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_CAP] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                   whereClause="%s and otype='capacitor'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_PROT] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                    whereClause="%s and otype in ('fuse', 'recloser', 'breaker')" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_REG] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                   whereClause="%s and otype='regulator'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_SWITCH] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                      whereClause="%s and otype='switch'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_SRC] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                   whereClause="%s and otype='source'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.GRID_EQUIP_GEN] = self.loadFeatureClass(DB_STRUCT.GRID_EQUIP_FC,
                                                                   whereClause="%s and otype='generator'" % self.circuitsWhereClause)
        self.net[DB_STRUCT.CIRCUIT] = {}
        self.net[DB_STRUCT.SHUNT] = {}
        self.net[DB_STRUCT.SCENARIO] = {}

        # get model data (tables)
        self.net[DB_STRUCT.MOD_SRC_TBL] = self.loadTable(DB_STRUCT.MOD_SRC_TBL)
        self.net[DB_STRUCT.MOD_TRANS_TBL] = self.loadTable(
            DB_STRUCT.MOD_TRANS_TBL)
        self.net[DB_STRUCT.MOD_REG_TBL] = self.loadTable(DB_STRUCT.MOD_REG_TBL)
        self.net[DB_STRUCT.MOD_WIRE_TBL] = self.loadTable(
            DB_STRUCT.MOD_WIRE_TBL)
        self.net[DB_STRUCT.MOD_COND_TBL] = self.loadTable(
            DB_STRUCT.MOD_COND_TBL, keyField='id')
        self.net[DB_STRUCT.MOD_UG_TBL] = self.loadTable(
            DB_STRUCT.MOD_UG_TBL, keyField='id')
        self.net[DB_STRUCT.MOD_CONSTR_TBL] = self.loadTable(
            DB_STRUCT.MOD_CONSTR_TBL, keyField='id')
        self.net[DB_STRUCT.MOD_CAP_TBL] = self.loadTable(DB_STRUCT.MOD_CAP_TBL)
        self.net[DB_STRUCT.MOD_LOAD_TBL] = self.loadTable(DB_STRUCT.MOD_LOAD_TBL,
                                                          whereClause="lscen='%s'" % self.loadScenario)
        self.net[DB_STRUCT.MOD_PROT_TBL] = self.loadTable(
            DB_STRUCT.MOD_PROT_TBL)
        self.net[DB_STRUCT.MOD_GEN_TBL] = self.loadTable(DB_STRUCT.MOD_GEN_TBL)
        self.net[DB_STRUCT.MOD_GEN_PROF_TBL] = self.loadTable(DB_STRUCT.MOD_GEN_PROF_TBL,
                                                              whereClause="gscen='%s'" % self.genScenario)
        # model_switch
        # model_wire
        # model_circuit
        # model_motor
        self.buildBranchElems()
        self.findMissingCircuitSources()

        print("Done")


if __name__ == '__main__':

    conn = Connection()
    # pfld = PowerFlowLoadData(conn, [], 'TT2', 'GS1')
    pfld = PowerFlowLoadData(conn,['BARCLAY-2401', 'BARCLAY-2402'], 'TT2', 'GS1')
    pfld.loadData()
