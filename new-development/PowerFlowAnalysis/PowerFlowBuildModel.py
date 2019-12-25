
import os
import json
import datetime
from collections import defaultdict, OrderedDict

import arcpy

from Connection import Connection
from PowerFlowLoadData import PowerFlowLoadData
from PowerFlowOptions import PowerFlowOptions
from PowerFlowWriteFiles import PowerFlowWriteFiles

from DBStructs import DB_STRUCT


class PowerFlowBuildModel():
    """Loads data for power flow analysis"""

    MODEL_CIR = 'model_circuit'
    ALL_CIRCUITS = '.*'

    def __init__(self, conn, pfLoadData,
                 protConductor=None,
                 protConstruction='SystemCnstDefault',
                 switchConductor=None,
                 switchConstruction='SystemCnstDefault',
                 defaultConstruction='defaultConstruction'):

        self.conn = conn
        self.directRun = False
        self.pfLoadData = pfLoadData
        self.reportParentPhaseMismatches = True
        self.protConductor = protConductor
        self.protConstruction = protConstruction
        self.switchConductor = switchConductor
        self.switchConstruction = switchConstruction
        self.defaultConstruction = defaultConstruction

        # self.protConductor = None
        # self.protConstruction = None
        # self.switchConductor = None
        # self.switchConstruction = None

        # building bus
        self.net = self.pfLoadData.net
        self.circs = self.pfLoadData.circs
        self.allBr = self.pfLoadData.allBr
        self.allId = self.pfLoadData.allId
        self.toBus = {}
        self.busParent= {}
        self.fromBus = {}
        self.busV = {}
        self.branches = {}
        self.seenElements = {}

    def validateModels(self):
        """ For all grid elements, check that the associated model exists """
        isModelValid = True
        for gridDataType, es in DB_STRUCT.MODELS_TO_CHECK.items():

            for idColumn, modelTbls in es:
                modelIds = set([mIds for modelTbl in modelTbls
                                for mIds in self.net[modelTbl].keys()])
                usedModels = set()
                for e, v in self.net[gridDataType].items():
                    usedModels.add(v[idColumn])
                    if v[idColumn] not in modelIds:
                        print('Model for %s (%s) not found in model set %s.' %
                              (e, v[idColumn], str(modelTbls)))
                        isModelValid = False

            # print(idColumn, modelIds)

        return isModelValid

    # For each grid data type, will get only the keys of the rows
    # to check against model data.  will remove model data if not
    # used in grid data type.
    def reduceModels(self):
        usedModels = defaultdict(set)
        usedModels[DB_STRUCT.MOD_SRC_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_SRC].values()])

        for v in self.net[DB_STRUCT.GRID_POW_LINE_FC].values():
            usedModels[DB_STRUCT.MOD_COND_TBL].update(
                [v['conductor'], v['neutral']])
            usedModels[DB_STRUCT.MOD_UG_TBL].update(
                [v['conductor'], v['neutral']])
            usedModels[DB_STRUCT.MOD_CONSTR_TBL].add(v['construction'])

        usedModels[DB_STRUCT.MOD_GEN_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_GEN].values()])
        usedModels[DB_STRUCT.MOD_PROT_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_PROT].values()])
        usedModels[DB_STRUCT.MOD_REG_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_REG].values()])
        usedModels[DB_STRUCT.MOD_CAP_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_CAP].values()])
        usedModels[DB_STRUCT.MOD_TRANS_TBL].update(
            [v['equipref'] for v in self.net[DB_STRUCT.GRID_EQUIP_TRANS].values()])

        # adding conductor and construction models for prot and sw devs
        for mc in ['protConductor', 'switchConductor']:
            if getattr(self, mc) is not None:
                usedModels[DB_STRUCT.MOD_COND_TBL].add(
                    getattr(self, mc))
            else:
                setattr(self, mc, list(usedModels[DB_STRUCT.MOD_COND_TBL])[0] if len(
                    usedModels[DB_STRUCT.MOD_COND_TBL]) else self.net[DB_STRUCT.MOD_COND_TBL][0])

        usedModels['model_construction'].update(
            {self.protConstruction, self.switchConstruction})

        # i think this is wrong!  check against production!
        for model in usedModels:
            for modelId in self.net[model].keys():
                if modelId not in usedModels[model]:
                    self.net[model].pop(modelId, None)
                    # print("poping %s %s" % (model, modelId))

        print("")

    def matchPhase(self, parentPhasecode, childPhasecode):
        return len(filter(lambda pi: pi in parentPhasecode, childPhasecode)) > 0

    def organizeParents(self):
        self.children = {}
        self.needBus = {}
        sortedKeys = sorted([k for k in self.net.keys() if not (
            k == 'circuit' or k[:6] == 'model_')])
        # sortedKeys = ['grid_equip_cap', 'grid_equip_gen', 'grid_powerlines', 'grid_loads',
        #               'grid_equip_prot', 'grid_equip_reg', 'scenario', 'shunt',
        #               'grid_equip_src', 'grid_equip_switch', 'grid_equip_trans']
        for fc in sortedKeys:
            nb = True if fc == DB_STRUCT.GRID_EQUIP_SRC or fc in DB_STRUCT.BRANCH_ELEMENTS else False
            for e, ev in self.net[fc].items():

                if nb:
                    self.needBus[e] = fc

                parentKey = ev.get('parentsec')
                parent = self.allBr.get(parentKey)

                if parentKey and parent:
                    if not parentKey in self.children:
                        self.children[parentKey] = []
                    self.children[parentKey].append(e)

                    if self.reportParentPhaseMismatches:
                        if ev.get('phasecode') is None:
                            print('Invalid phase code at %s' % e)
                        elif not self.matchPhase(parent.get('phasecode', ''), ev.get('phasecode', '')):
                            print('Parent phase mismatch at %s (%s vs %s)' % (
                                e, ev.get('phasecode', ''), parent.get('phasecode', '')))

                else:
                    if fc != DB_STRUCT.GRID_EQUIP_SRC:
                        print('Error - secname %s has no parent (%s)' %
                              (e, parentKey))
        print("")

    def updateConnectedRecords(self, branch):
        otc = defaultdict(lambda: 0)
        if branch in self.children:
            br = self.allId[branch]
            for c in self.children[branch]:
                cr = self.allId.get(c)
                if cr:
                    t = cr.get('otype')
                    otc[t] += 1
            for t, tc in otc.items():
                if tc != 0:
                    br['n_di_%s' % t] = tc

    def assignBusNumbers(self, branch, fromBus, toBus, baseV):
        """ Implements a DFS based bus number assignment. Also assigns base voltage and circuit id
        """
        n, v = toBus, baseV
        if branch in self.seenElements:
            arcpy.AddWarning('Warning - loop found at %s' % (branch))
        else:
            self.seenElements[branch] = ''
            self.fromBus[branch] = fromBus
            self.busV[branch] = v
            if branch in self.needBus:
                self.branches[(fromBus, toBus)] = branch
                self.toBus[branch] = n
                self.busParent[n] = branch
                n += 1

                if branch in self.children:
                    self.updateConnectedRecords(branch)
                    # if transformer, update base voltage
                    if self.needBus[branch] == DB_STRUCT.GRID_EQUIP_TRANS:
                        #v = v * self.net['model_trans'][self.net[DB_STRUCT.GRID_EQUIP_TRANS][branch]['equipref']]['ratio']
                        pars = json.loads(
                            self.net[DB_STRUCT.GRID_EQUIP_TRANS][branch]['pars']) if self.net[DB_STRUCT.GRID_EQUIP_TRANS][branch]['pars'] is not None else {}
                        v = round(float(pars['vOut']),
                                  2) if 'vOut' in pars else v
                    # recursively assign bus numbers and voltages
                    for c in self.children[branch]:
                          n = self.assignBusNumbers(c, toBus, n, v)
            else:
                self.toBus[branch] = 0
        return n


    def buildBus(self):

        self.nodes = []
        self.toBus = {}
        self.busParent = {}
        self.fromBus = {}
        self.busV = {}
        self.branches = {}
        self.seenElements = {}

        busNum = 1

        for s in self.net[DB_STRUCT.GRID_EQUIP_SRC].keys():
            vs = self.net[DB_STRUCT.MOD_SRC_TBL][self.net[DB_STRUCT.GRID_EQUIP_SRC]
                                                 [s]['equipref']]['vsource']
            busNum = self.assignBusNumbers(s, 0, busNum, vs)

        # organizing circuits
        for c in self.circs:
            bay= self.net['model_circuit'][c]['secname']
            if bay in self.fromBus:
                self.net['circuit'][c] = {'bus': self.toBus[bay], 'circuit': c}
            else:
                arcpy.AddError("Bay %s has not been assigned a from bus."%c)

        # process options including faults and motor start
        # self.ts = timeMessage(self.ts, 'Bus number assignemnt')


        print("buildBus finished")

    def build(self):

        self.validateModels()
        self.reduceModels()
        self.organizeParents()
        self.buildBus()

if __name__ == '__main__':

    conn = Connection()
    dir = r'C:\Users\llassetter\hotec'

    pfLoadData = PowerFlowLoadData(conn, [], 'TT2', 'GS1')
    pfLoadData.loadData()

    pfbuildModel = PowerFlowBuildModel(None, pfLoadData)
    pfbuildModel.validateModels()
    pfbuildModel.reduceModels()
    pfbuildModel.organizeParents()
    pfbuildModel.buildBus()

    pfOptions = PowerFlowOptions(pfbuildModel, pfLoadData)
    pfOptions.checkForOptions()

    writeFiles = PowerFlowWriteFiles(pfLoadData, pfbuildModel,dir=dir, confOpts=pfOptions.confOpts)
    writeFiles.writeFiles()

    pass

