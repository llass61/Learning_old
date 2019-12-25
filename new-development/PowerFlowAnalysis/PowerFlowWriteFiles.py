import os
import shutil
import copy
import arcpy
import math
import json

from collections import defaultdict

from Connection import Connection
from addaUtils import floatOrNone
from DBStructs import DB_STRUCT


class PowerFlowWriteFiles():
    FROM_SKEL = [DB_STRUCT.MOD_TRANS_CONN_TBL, DB_STRUCT.MOD_LOAD_TBL, #DB_STRUCT.MOD_UG_TBL, #DB_STRUCT.MOD_TRANS_TBL, #DB_STRUCT.MOD_CONSTR_TBL,
                #DB_STRUCT.WIND_MOD_COND, DB_STRUCT.WIND_MOD_UG, #DB_STRUCT.WIND_MOD_CONSTR,
                ] #DB_STRUCT.WIND_MOD_TRANS, DB_STRUCT.WIND_MOD_REG] # DB_STRUCT.MOD_COND_TBL, ,

    SKIP_MODEL_RECS= [DB_STRUCT.MOD_TRANS_TBL, DB_STRUCT.MOD_COND_TBL, DB_STRUCT.MOD_UG_TBL, DB_STRUCT.MOD_CONSTR_TBL] # DB_STRUCT.WIND_MOD_COND, ,

    SOURCE_IMPEDANCE_DEF = {'r0': 0, 'x0': 0, 'r1': 0, 'x1': 1e-4}

    FILE_NAMES = {
        DB_STRUCT.GRID_POW_LINE_FC: 'linedata.csv',
        DB_STRUCT.GRID_EQUIP_TRANS: 'transdata.csv',
        DB_STRUCT.GRID_EQUIP_SRC: 'sourcedata.csv',
        DB_STRUCT.GRID_EQUIP_CAP: 'capdata.csv',
        DB_STRUCT.GRID_LOADS_FC: 'loaddata.csv',
        DB_STRUCT.GRID_EQUIP_GEN: 'vcdata.csv',
        DB_STRUCT.CIRCUIT: 'circuits.csv',
        DB_STRUCT.SHUNT: 'shunt.csv',
        DB_STRUCT.SCENARIO: 'scen.csv',
        DB_STRUCT.MOD_COND_TBL: 'basecatalogs.csv',
        DB_STRUCT.MOD_UG_TBL: 'ugcatalogs.csv',
        DB_STRUCT.MOD_CONSTR_TBL: 'constructioncatalog.csv',
        DB_STRUCT.MOD_TRANS_TBL: 'transformercatalog.csv',
        DB_STRUCT.MOD_TRANS_CONN_TBL: 'tfmrconn.csv',
        DB_STRUCT.MOD_LOAD_TBL: 'loadmodels.csv',
        DB_STRUCT.WIND_MOD_COND: 'OH.csv',
        DB_STRUCT.WIND_MOD_UG: 'UG.csv',
        DB_STRUCT.WIND_MOD_CONSTR: 'wm_const.csv',
        DB_STRUCT.WIND_MOD_TRANS: 'TR.csv',
        DB_STRUCT.WIND_MOD_REG: 'REG.csv'
    }

    KEYWORD_MAP = {
        'linefile': DB_STRUCT.GRID_POW_LINE_FC,
        'transformerfile': DB_STRUCT.GRID_EQUIP_TRANS,
        'loadfile': DB_STRUCT.GRID_LOADS_FC,
        'sourcefile': DB_STRUCT.GRID_EQUIP_SRC,
        'circuitfile': DB_STRUCT.CIRCUIT,
        'scenariofile': DB_STRUCT.SCENARIO,
        'shuntfile': DB_STRUCT.SHUNT,
        'capfile': DB_STRUCT.GRID_EQUIP_CAP,
        'voltagecontrolfile': DB_STRUCT.GRID_EQUIP_GEN,
        'transformercatalogfile': DB_STRUCT.MOD_TRANS_TBL,
        'transformerconnectionfile': DB_STRUCT.MOD_TRANS_CONN_TBL,
        'ugcatalogfile': DB_STRUCT.MOD_UG_TBL,
        'loadmodelfile': DB_STRUCT.MOD_LOAD_TBL,
        'conductorfile': DB_STRUCT.MOD_COND_TBL,
        'constructionfile': DB_STRUCT.MOD_CONSTR_TBL,
        'windmillconductorfile': DB_STRUCT.WIND_MOD_COND,
        'windmillugcatalogfile': DB_STRUCT.WIND_MOD_UG,
        'windmillconstructionfile': DB_STRUCT.WIND_MOD_CONSTR,
        'windmilltransformerfile': DB_STRUCT.WIND_MOD_TRANS,
        'windmillregulatorfile': DB_STRUCT.WIND_MOD_REG
    }

    MODEL_FILE_HEADERS = {
            DB_STRUCT.GRID_POW_LINE_FC: """Name,FromBus,ToBus,Phases,Volts,CCt,Length,Cond,Neut,Construction""",
            DB_STRUCT.GRID_EQUIP_TRANS: """Name,FromBus,ToBus,from phase,from base volts,sec phases,sec volts,cct,transformer,Init tap,tapstatus,regvolt""",
            DB_STRUCT.GRID_EQUIP_SRC: """Name,Bus,Phases,Volt,Angle,r1,x1,r0,x0""",
            DB_STRUCT.GRID_EQUIP_CAP: """Name,Bus,Phases,Controlmode,regbus,voltset,kvarblock,numblocks,initstat,capname""",
            DB_STRUCT.GRID_LOADS_FC: """Name,Bus,Phases,Conn,kwa,pfa,kwb,pfb,kwc,pfc,LoadModel""",
            DB_STRUCT.GRID_EQUIP_GEN: "Name,Bus,Phases,kwa,kvaramax,kvaramin,vmaxa,vmina,kwb,kvarbmax,kvarbmin,vmaxb,vminb,kwc,kvarcmax,kvarcmin,vmaxc,vminc",
            DB_STRUCT.CIRCUIT: """Bus,CircuitId""",
            DB_STRUCT.SCENARIO: """Scenario""",
            DB_STRUCT.SHUNT: """Scenario,Bus,Phases,Connection,ra,xa,rb,xb,rc,xc,rg,xg""",
            DB_STRUCT.MOD_COND_TBL: """catalog_key,Type,GMR,RDC,RATING,DIAMETER""",
            DB_STRUCT.MOD_UG_TBL: """UGName,PHASE_CONDUCTOR_ID,NEUTRAL_CONDUCTOR_ID,DIELECTRIC,RATING,OUTSIDEDIAMETER,DIAMETEROVERSCREEN,DIAMETEROVERINSUL,NONEUTRALSTRANDS,FULLNEUT,JACKETTHICKNESS,SHIELDTHICKNESS""",
            DB_STRUCT.MOD_CONSTR_TBL: """id,x1,y1,x2,y2,x3,y3,x4,y4""",
            DB_STRUCT.MOD_TRANS_TBL: """Type,VectorGroup,Rating,r,x,coreloss,magpf,pri ground,sec ground,pri ground r,pri ground x,sec ground r,sec ground x,maxtap,mintap,basttap,tapbus""",
            #DB_STRUCT.MOD_TRANS_CONN_TBL: None,
            DB_STRUCT.MOD_LOAD_TBL: """Loadname,% res,resp,resq,% Comm,commp,commq,% Indust,indp,indq""",
            DB_STRUCT.WIND_MOD_COND: """id,material,rating,rdc25,rdc50,gmr,pref_neut_desc,diam,cat,pref_neut""",
            DB_STRUCT.WIND_MOD_UG: """id,type,rating,phase_cond_r,gmr,ccn_r,n_strand_n,od_insul,od_inc_n,d_const_un,d_un,gmr_n,d_cond,dist_cn,cat""",
            DB_STRUCT.WIND_MOD_CONSTR: """id,oh_1_gmdp,oh_v_gmdp,oh_3_gmdp,oh_1_gmdpn,oh_v_gmdpn,oh_3_gmdpn,ug_gmcp,height_ground,height_unit,dist_od,dist_unit,spacing,v_rating,assume_full_transportation,pos_1_ph,pos_first_ph,pos_second_ph,vert_h_pos_a,vert_h_pos_b,vert_h_pos_c,vert_h_pos_n,hor_d_pos_a,hor_d_pos_b,hor_d_pos_c,hor_d_pos_n,cat""",
            DB_STRUCT.WIND_MOD_TRANS: """id,ampacity,condType,pi_a,pi_b,pi_c,xr_a,xr_b,xr_c,single_kva_a,single_kva_b,single_kva_c,r_gp,r_gs,r_g,x_gp,x_gs,x_g,k_fac,nll_a,nll_b,nll_c,cat""",
            DB_STRUCT.WIND_MOD_REG: """id,ampacity,ct_rating,boost,buck,step_size,bandwidth,cat"""
    }

    MODEL_FILE_LINES = {
            DB_STRUCT.GRID_POW_LINE_FC: """%(secname)s,%(FromBus)d,%(ToBus)d,%(Phases)d,%(Volts).3f,%(CCt)s,%(Length)f,%(Cond)s,%(Neut)s,%(Construction)s""",
            'prot': """%(secname)s,%(FromBus)d,%(ToBus)d,%(Phases)d,%(Volts).3f,%(CCt)s,%(Length)f,%(Cond)s,%(Neut)s,%(Construction)s""",
            'switch': """%(secname)s,%(FromBus)d,%(ToBus)d,%(Phases)d,%(Volts).3f,%(CCt)s,%(Length)f,%(Cond)s,%(Neut)s,%(Construction)s""",
            DB_STRUCT.GRID_EQUIP_TRANS: """%(secname)s,%(FromBus)d,%(ToBus)d,%(fphase)d,%(fbasevolts).3f,%(secphases)d,%(secvolts).3f,%(CCt)s,%(transformer)s,%(Init tap)d,%(tapstatus)d,%(regvolt)f""",
            'reg': """%(secname)s,%(FromBus)d,%(ToBus)d,%(fphase)d,%(fbasevolts).3f,%(secphases)d,%(secvolts).3f,%(CCt)s,%(transformer)s,%(Init tap)d,%(tapstatus)d,%(regvolt)f""",
            DB_STRUCT.GRID_EQUIP_SRC: """%(secname)s,%(Bus)d,%(Phases)d,%(Volt)f,%(Angle)f,%(r1)f,%(x1)f,%(r0)f,%(x0)f""",
            DB_STRUCT.GRID_EQUIP_CAP: """%(secname)s,%(Bus)d,%(Phases)d,%(Controlmode)d,%(regbus)d,%(voltset)f,%(kvarblock)f,%(numblocks)d,%(initstat)d,%(capname)s""",
            DB_STRUCT.GRID_LOADS_FC: """%(secname)s,%(Bus)d,%(Phases)d,%(Conn)d,%(kwa)f,%(pfa)f,%(kwb)f,%(pfb)f,%(kwc)f,%(pfc)f,%(LoadModel)s""",
            DB_STRUCT.GRID_EQUIP_GEN: """%(secname)s,%(Bus)d,%(Phases)d,%(kwa)f,%(kvarmaxa)f,%(kvarmina)f,%(vmaxa)f,%(vmina)f,%(kwb)f,%(kvarmaxb)f,%(kvarminb)f,%(vmaxb)f,%(vminb)f,%(kwc)f,%(kvarmaxc)f,%(kvarminc)f,%(vmaxc)f,%(vminc)f""",
            DB_STRUCT.CIRCUIT: """%(Bus)d,%(CircuitId)s""",
            DB_STRUCT.SCENARIO: """%(Scenario)s""",
            DB_STRUCT.SHUNT: """%(Scenario)s,%(Bus)d,%(Phases)d,%(Connection)d,%(ra)f,%(xa)f,%(rb)f,%(xb)f,%(rc)f,%(xc)f,%(rg)f,%(xg)f""",
            DB_STRUCT.MOD_COND_TBL: """%(id)s,%(type)s,%(gmr)f,%(rdc)f,%(rating)f,%(diam)f""",
            DB_STRUCT.MOD_UG_TBL: """%(id)s,%(cond_id)s,%(cond_id)s,%(di)s,%(rating)f,%(out_diam)f,%(diam_over_screen)f,%(diam_over_insul)f,%(nn_strands)d,%(full_neut)d,%(jacket_thickness)f,%(jacket_thickness)f""",
            DB_STRUCT.MOD_CONSTR_TBL: """%(id)s,%(x1)f,%(y1)f,%(x2)f,%(y2)f,%(x3)f,%(y3)f,%(x4)f,%(y4)f""",
            DB_STRUCT.MOD_TRANS_TBL: """%(Type)s,%(VectorGroup)s,%(Rating)f,%(r)f,%(x)f,%(coreloss)f,%(magpf)f,%(pri ground)f,%(sec ground)f,%(pri ground r)f,%(pri ground x)f,%(sec ground r)f,%(sec ground x)f,%(maxtap)f,%(mintap)f,%(basttap)f,%(tapbus)f""",
            #DB_STRUCT.MOD_TRANS_CONN_TBL: None,
            DB_STRUCT.MOD_LOAD_TBL: """%(Loadname)s,%(% res)f,%(resp)f,%(resq)f,%(% Comm)f,%(commp)f,%(commq)f,%(% Indust)f,%(indp)f,%(indq)f""",
            DB_STRUCT.WIND_MOD_COND: """%(id)s,%(material)s,%(rating)f,%(rdc25)f,%(rdc50)f,%(gmr)f,%(pref_neut_desc)s,%(diam)f,%(cat)s,%(pref_neut)s""",
            DB_STRUCT.WIND_MOD_UG: """%(id)s,%(type)s,%(rating)f,%(phase_cond_r)f,%(gmr)f,%(ccn_r)f,%(n_strand_n)d,%(od_insul)f,%(od_inc_n)f,%(d_const_un)f,%(d_un)f,%(gmr_n)f,%(d_cond)f,%(dist_cn)f,%(cat)s""",
            DB_STRUCT.WIND_MOD_CONSTR: """%(id)s,%(oh_1_gmdp)f,%(oh_v_gmdp)f,%(oh_3_gmdp)f,%(oh_1_gmdpn)f,%(oh_v_gmdpn)f,%(oh_3_gmdpn)f,%(ug_gmcp)f,%(height_ground)f,%(height_unit)s,%(dist_od)f,%(dist_unit)s,%(spacing)s,%(v_rating)f,%(assume_full_transportation)d,%(pos_1_ph)s,%(pos_first_ph)s,%(pos_second_ph)s,%(vert_h_pos_a)f,%(vert_h_pos_b)f,%(vert_h_pos_c)f,%(vert_h_pos_n)f,%(hor_d_pos_a)f,%(hor_d_pos_b)f,%(hor_d_pos_c)f,%(hor_d_pos_n)f,%(cat)s""",
            DB_STRUCT.WIND_MOD_TRANS: """%(id)s,%(ampacity)f,%(condType)s,%(pi_a)f,%(pi_b)f,%(pi_c)f,%(xr_a)f,%(xr_b)f,%(xr_c)f,%(single_kva_a)f,%(single_kva_b)f,%(single_kva_c)f,%(r_gp)f,%(r_gs)f,%(r_g)f,%(x_gp)f,%(x_gs)f,%(x_g)f,%(k_fac)f,%(nll_a)f,%(nll_b)f,%(nll_c)f,%(cat)s""",
            DB_STRUCT.WIND_MOD_REG: """%(id)s,%(ampacity)f,%(ct_rating)f,%(boost)f,%(buck)f,%(step_size)f,%(bandwidth)f,%(cat)s"""
    }

    MODEL_LINKS= { # denotes for each element, what field(s) should be checked against what (group of) models.
        DB_STRUCT.GRID_EQUIP_CAP: [('equipref', DB_STRUCT.MOD_CAP_TBL)],
        DB_STRUCT.GRID_EQUIP_TRANS: [('equipref', DB_STRUCT.MOD_TRANS_TBL)],
        DB_STRUCT.GRID_EQUIP_PROT: [('equipref', DB_STRUCT.MOD_PROT_TBL)],
        DB_STRUCT.GRID_EQUIP_GEN: [('equipref', DB_STRUCT.MOD_GEN_TBL)],
        DB_STRUCT.GRID_EQUIP_REG: [('equipref', DB_STRUCT.MOD_REG_TBL)],
        DB_STRUCT.GRID_EQUIP_SRC: [('equipref', DB_STRUCT.MOD_SRC_TBL)],
        DB_STRUCT.GRID_POW_LINE_FC: [('conductor', [DB_STRUCT.MOD_COND_TBL, DB_STRUCT.MOD_UG_TBL]),
                                     ('nuetral', [DB_STRUCT.MOD_COND_TBL, DB_STRUCT.MOD_UG_TBL, None]),
                                     ('construction', DB_STRUCT.MOD_CONSTR_TBL)]
        # conductor field should either exist in the conds or ugs
        }

    EQ_2_FILE = {DB_STRUCT.GRID_POW_LINE_FC: [DB_STRUCT.GRID_POW_LINE_FC, DB_STRUCT.GRID_EQUIP_PROT, DB_STRUCT.GRID_EQUIP_SWITCH],
                 DB_STRUCT.GRID_EQUIP_TRANS: [DB_STRUCT.GRID_EQUIP_TRANS, DB_STRUCT.GRID_EQUIP_REG],
                 DB_STRUCT.WIND_MOD_COND: [DB_STRUCT.MOD_COND_TBL],
                 DB_STRUCT.WIND_MOD_UG: [DB_STRUCT.MOD_UG_TBL],
                 DB_STRUCT.WIND_MOD_CONSTR: [DB_STRUCT.MOD_CONSTR_TBL],
                 DB_STRUCT.WIND_MOD_TRANS: [DB_STRUCT.MOD_TRANS_TBL],
                 DB_STRUCT.WIND_MOD_REG: [DB_STRUCT.MOD_REG_TBL]
    }

    def __init__(self,
                 pfLoadData,
                 pfBuildModel,
                 dir=None,
                 configFile=None,
                 confOpts={},
                 skipRecs=SKIP_MODEL_RECS,
                 fromSkel=FROM_SKEL,
                 defaultSourceImpedances=SOURCE_IMPEDANCE_DEF,
                 defaultConstruction='SystemCnstDefault',
                 protConstruction='SystemCnstDefault',
                 protConductor=None,
                 switchConstruction='SystemCnstDefault',
                 switchConductor=None,
                 loadScaling=1.0,
                 genScaling=1.0,
                 systemTemperature=35,
                 skeletonDir=None):

        self.conn = Connection()

        self.net = pfLoadData.net
        self.fromBus = pfBuildModel.fromBus
        self.toBus = pfBuildModel.toBus
        self.busV = pfBuildModel.busV

        self.dir = dir if dir != None else os.path.join(self.conn.getDir(), 'pfe')

        self.configFile = configFile
        if self.configFile is None:
            self.configFile = os.path.join(self.dir, 'pfcattest.ini')

        self.confOpts = confOpts

        self.skeletonDir = skeletonDir
        if self.skeletonDir is None:
            self.skeletonDir = os.path.join(self.conn.getDir(), 'pfe')

        self.fromSkel = fromSkel
        self.skipRecs = skipRecs
        self.defaultSourceImpedances = defaultSourceImpedances

        self.defaultConstruction = pfBuildModel.defaultConstruction
        self.protConstruction = pfBuildModel.protConstruction
        self.protConductor = pfBuildModel.protConductor
        self.switchConstruction = pfBuildModel.switchConstruction
        self.switchConductor = pfBuildModel.switchConductor

        self.loadScaling = loadScaling
        self.genScaling = genScaling
        self.systemTemperature= systemTemperature # in C (used for Rdc adjustments)


    def writeConfigFile(self):
        if 'conf' not in self.fromSkel:

            with open(os.path.join(self.dir, self.configFile), 'w') as f:
                for k, v in PowerFlowWriteFiles.KEYWORD_MAP.items():
                    if self.FILE_NAMES[v] is not None:
                        f.write("""%s %s\n""" % (k, self.FILE_NAMES[v]))
                for o in self.confOpts:
                    f.write("""%s\n""" % o)
        else:
            self.getFileFromSkeleton(self.configFile)

    def getFileFromSkeleton(self, fn):
        sf = os.path.join(self.skeletonDir, fn)
        if os.path.isfile(sf):
            try:
                shutil.copyfile(sf, os.path.join(self.dir, fn))
            except:
                arcpy.AddMessage("Error getting file %s from the skeleton dir" % sf)
        else:
            arcpy.AddMessage("Error: File %s does not exist in skeleton dir." % sf)


    def writeModelFile(self, m):
        if self.FILE_NAMES[m] is not None:
            # copy files from skel dir if in fromSkel
            if m in self.fromSkel: self.getFileFromSkeleton(self.FILE_NAMES[m])
            else:
                with open(os.path.join(self.dir, self.FILE_NAMES[m]), 'w') as f:
                    if self.MODEL_FILE_HEADERS[m] is not None: f.write(self.MODEL_FILE_HEADERS[m]+'\n')
                    if m not in self.skipRecs:
                        kl= self.EQ_2_FILE[m] if m in self.EQ_2_FILE else [m]
                        for mi in kl:
                            # print "Model item %s"%mi
                            for b, l in self.net[mi].items():
                                if mi in [DB_STRUCT.CIRCUIT, DB_STRUCT.SHUNT, DB_STRUCT.SCENARIO] or mi[:6]== 'model_' or b in self.fromBus: # only consider connected elements
                                    e= self.getElement(mi, b, l, m)
                                    if e is None:
                                        arcpy.AddWarning("Disabled element ignored. Item id: %s"%b)
                                    else:
                                        try:
                                            f.write(self.MODEL_FILE_LINES[m] % e + '\n')
                                        except BaseException as e:
                                            print("Model %s in model file %s, item %s: %s, element: %s"%(mi, m, b, str(l), str(e)))
                                            if mi=='lines' and l is not None and 'length' in l and l['length'] is None:
                                                arcpy.AddMessage("Error: Power line with no geometry. Item id: %s, parentsec id: %s."%(b, str(l and l.get('parentsec'))))
                                            arcpy.AddError("Error in model. Item id: %s, parentsec id: %s. Error %s"%(b, str(l and l.get('parentsec')), str(e)))
                                else:
                                    arcpy.AddMessage("Asset %s is not connected and hence ignored."%b)
                    #else:
                    #    arcpy.AddMessage("Skipping records for file %s." % m)

        else:
            print("Model %s does not need a file."%m)

    def getElement(self, m, b, l, mf):
        element = defaultdict(None)
        if m == DB_STRUCT.GRID_EQUIP_SRC:
            self.validateElement(m, b, l)
            sourceData = self.net['model_source'].get(l['equipref'])
            element.update({'secname': l['secname'], 'Bus': self.toBus[b], 'Phases': self.transPhase(l['phasecode'] + 'N'), 'Volt': sourceData['ratio'], 'Angle': 0.0, })
            eps = 1e-4
            if sourceData:
                zb = ((sourceData['vsource']*math.sqrt(3)*sourceData['ratio'])**2)/sourceData['rating'] # Z base is calculated based on L-L kV
                zb = ((sourceData['vsource']*math.sqrt(3))**2)/sourceData['rating'] # Z base is calculated based on L-L kV
                element['r1'] = (sourceData.get('pos_r', 0.0) or 0.0)/ zb
                element['r0'] = (sourceData.get('zero_r', 0.0) or 0.0)/ zb
                element['x1'] = (sourceData.get('pos_x', self.defaultSourceImpedances['x1']) or 0.0) / zb
                element['x0'] = (sourceData.get('zero_x', 0.0) or 0.0) / zb
                for svk in ['pos_r', 'zero_r', 'pos_x', 'zero_x']:
                    if sourceData.get(svk) is None: arcpy.AddWarning('Warning source impedance %s is none. Replaced with default value.'%svk)
                if sourceData.get('pos_x') == 0:
                    arcpy.AddMessage("Warning: Zero X1 detected for source %s (eqr: %s), replaced with %f"%(l['secname'], l['equipref'], self.defaultSourceImpedances['x1']))
            else:
                arcpy.AddMessage("Warning: No source data for source %s (eqr: %s), replaced X1 with %f (R0, R1, X0 set to 0)"%(l['secname'], l['equipref'], self.defaultSourceImpedances['x1']))
                element.update(self.defaultSourceImpedances)

            #element['x1'] = (sourceData['pos_l'] * 2 * math.pi * self.freq if sourceData else eps) / zb
            #element['x0'] = (sourceData['zero_l'] * 2 * math.pi * self.freq if sourceData else eps) / zb
        elif m == DB_STRUCT.GRID_POW_LINE_FC:
            self.validateElement(m, b, l)
            #eqp= self.net['model_line'][l['equipref']]
            if l['phasecode'] is None:
                arcpy.AddMessage('Error: Line %s doe not have a phasecode and hence ignored.'%l['secname'])
            else:
                const= l['construction'] if l['construction'] is not None and l['construction']!='' else self.defaultConstruction
                element.update({'secname': l['secname'], 'FromBus': self.fromBus[b], 'ToBus': self.toBus[b], 'Volts': self.busV[b], 'CCt': l[DB_STRUCT.CIRCUIT],
                        'Phases': self.transPhase(l['phasecode'] + 'N'), 'Length': l['imp_len'] if l['imp_len'] is not None else l['length'],
                        'Cond': l['conductor'], 'Neut': l['neutral'] if l['neutral'] else l['conductor'], 'Construction': const, })
        elif m == DB_STRUCT.GRID_EQUIP_PROT:
            self.validateElement(m, b, l)
            element.update({'secname': l['secname'], 'FromBus': self.fromBus[b], 'ToBus': self.toBus[b], 'Volts': self.busV[b], 'CCt': l[DB_STRUCT.CIRCUIT],
                    'Phases': self.transPhase(l['phasecode'] + 'N'), 'Length': 0.001,
                    'Cond': self.protConductor, 'Neut': self.protConductor, 'Construction': self.protConstruction, })
        elif m == DB_STRUCT.GRID_EQUIP_SWITCH:
            self.validateElement(m, b, l)
            element.update({'secname': l['secname'], 'FromBus': self.fromBus[b], 'ToBus': self.toBus[b], 'Volts': self.busV[b], 'CCt': l[DB_STRUCT.CIRCUIT],
                    'Phases': self.transPhase(l['phasecode'] + 'N'), 'Length': 0.001,
                    'Cond': self.switchConductor, 'Neut': self.switchConductor, 'Construction': self.switchConstruction, })
        elif m == DB_STRUCT.GRID_LOADS_FC:
            self.validateElement(m, b, l)
            loadData = self.net[DB_STRUCT.MOD_LOAD_TBL].get(l['equipref'])
            element.update({'secname': l['secname'], 'Bus': self.fromBus[b], 'Phases': self.transPhase(l['phasecode'] + 'N'), 'Conn': 0, 'LoadModel': 'residential'})
            for p in ['a', 'b', 'c']:
                element['kw' + p] = loadData['kw_' + p] * self.loadScaling if (loadData and p.upper() in l['phasecode']) else 0.0
                element['pf' + p] = loadData['pf'] if (loadData and p.upper() in l['phasecode']) else 1.0
        elif m == DB_STRUCT.GRID_EQUIP_GEN:
            self.validateElement(m, b, l)
            genDataMaster = self.net['model_gen'].get(l['equipref'])
            genData = self.net['model_genp'].get(l['equipref'])
            element.update({'secname': l['secname'], 'Bus': self.fromBus[b], 'Phases': self.transPhase(l['phasecode'] + 'N')})
            for p in ['a', 'b', 'c']:
                for q in ['kw', 'kvarmin', 'kvarmax', 'vmin', 'vmax']:
                    element[q + p] = genData[q + p] * self.genScaling if (genData and p.upper() in l['phasecode']) else 0.0

        elif m == DB_STRUCT.GRID_EQUIP_TRANS:
            self.validateElement(m, b, l)
            pars= json.loads(l['pars']) if l['pars'] is not None else {}
            vOut= floatOrNone(pars.get('vOut')) # for transformers, vOut is absolute
            vIn= floatOrNone(pars.get('vInput'))
            vOutNom= floatOrNone(pars.get('vOutNom'))
            # sec_v= round(vOut, 2)
            eq= self.net[DB_STRUCT.MOD_TRANS_TBL].get(l['equipref'])
            ratio= 1.0
            if (vOutNom is None or vIn is None or vIn ==0):
                arcpy.AddMessage('Transformer specific ratio data not found, using library data.')
                if eq is not None and 'ratio' in eq:
                    ratio = eq['ratio']
                else:
                    arcpy.AddWarning('Transformer model ratio not present, 1.0 is assumed.')
            else:
                ratio= vOutNom/vIn
            sec_v= self.busV[b] * ratio if vOutNom is None else vOutNom

            l['ratio']= ratio # always nominal ratio
            l['secv']= sec_v # nominal outV
            l['regv']= vOut/sec_v if vOut is not None else 1.0 # operational pu

            if 'wdgCode' in pars:
                wc= pars['wdgCode'].split('-')
                pph= self.transPhase(l['phasecode'] + ('N' if wc[0] == 'Y' else ''))
                sph= self.transPhase(l['phasecode'] + ('N' if wc[1] == 'Y' else ''))
            else:
                pph= self.transPhase(l['phasecode'] + 'N')
                sph= self.transPhase(l['phasecode'] + 'N')

            element.update({'secname': l['secname'], 'FromBus': self.fromBus[b], 'ToBus': self.toBus[b], 'fbasevolts': self.busV[b], 'secvolts': l['secv'],
                    'CCt': l[DB_STRUCT.CIRCUIT], 'fphase': pph, 'secphases': sph, 'transformer': l['equipref'],
                   'Init tap': 1,'tapstatus': 0, 'regvolt':  l['regv']})
            # tapstatus 0: fixd, 1: regulated

        elif m == DB_STRUCT.GRID_EQUIP_REG:
            self.validateElement(m, b, l)
            pars= json.loads(l['pars']) if l['pars'] is not None else {}
            vOut= floatOrNone(pars.get('vOut')) # for reg, vOut is in pu
            # sec_v= round(vOut, 2)
            eq= self.net[DB_STRUCT.MOD_REG_TBL].get(l['equipref'])
            sec_v= self.busV[b] if eq is None else eq['out_volts']
            pu = (1.0 if eq is None else sec_v/self.busV[b]) if vOut is None else vOut

            l['ratio']= 1.0  # always nominal ratio
            l['secv']= self.busV[b] # nominal outV
            l['regv']= pu # operational pu

            element.update({'secname': l['secname'], 'FromBus': self.fromBus[b], 'ToBus': self.toBus[b], 'fbasevolts': self.busV[b], 'secvolts': l['secv'],
                        'CCt': l[DB_STRUCT.CIRCUIT], 'fphase': self.transPhase(l['phasecode'] + 'N'), 'secphases': self.transPhase(l['phasecode'] + 'N'),
                        'transformer': l['equipref'], 'Init tap': 1, 'tapstatus': 1, 'regvolt':  l['regv'] })

        elif m == DB_STRUCT.GRID_EQUIP_CAP:
            if l['status']=='111':
                self.validateElement(m, b, l)
                kvar = self.net['model_cap'][l['equipref']]['kvar_a']
                element.update({'secname': l['secname'], 'Bus': self.fromBus[b], 'Phases': self.transPhase(l['phasecode']),
                            'Controlmode': 0, 'regbus': self.fromBus[b], 'voltset': 1.0, 'kvarblock': kvar, 'numblocks': 1, 'initstat': 1, 'capname': b,})
            else:
                element= None
        elif m == DB_STRUCT.CIRCUIT:
                element.update({'Bus': l['bus'], 'CircuitId': l[DB_STRUCT.CIRCUIT], })
        elif m in [DB_STRUCT.SHUNT, DB_STRUCT.SCENARIO]:
                element.update(l)
        elif m == DB_STRUCT.MOD_LOAD_TBL:
            pass
        elif m == DB_STRUCT.MOD_COND_TBL:
           element.update(l)
           a= (l['rdc50']-l['rdc25'])/(25*l['rdc25'])
           element.update({'rdc': l['rdc25']*(1+a*(self.systemTemperature-25)), 'type': '0', }) # full blown Rdc adjustment
           # linear Rdc adjustment
           #b= 0.4
           #element.update({'rdc': l['rdc50']*b+l['rdc25']*(1-b), 'type': '0', }) # (l['rdc50']+l['rdc25'])/2
           if mf== DB_STRUCT.WIND_MOD_COND:
               element.update({'cat': element.get('category'), 'pref_neut_desc': 'NA', 'pref_neut': 'NA'})

        elif m == DB_STRUCT.MOD_UG_TBL:
           element.update(l)
           if mf== DB_STRUCT.WIND_MOD_UG:
               element.update({'type': element.get('ug_type')})

        elif m == DB_STRUCT.MOD_CONSTR_TBL: # distances are in feet
            # id,x1,y1,x2,y2,x3,y3,x4,y4
            element.update(l)
            #if False:
            #    pass
            #elif all([(l[k] is not None) for k in ['height_ground', 'height_unit', 'oh_1_gmdp', 'oh_v_gmdp', 'oh_3_gmdp', 'oh_1_gmdpn', 'oh_v_gmdpn', 'oh_3_gmdpn']]):
            #    h= l['height_ground']
            #    if l['height_unit'] == 'in': h= h/12
            #    element.update({'x1': -l['oh_1_gmdp'],'y1': h+0.0,'x2': 0.0,'y2': h+l['oh_1_gmdp'],'x3': l['oh_1_gmdp'],'y3': h+0.0,'x4': 0.0,'y4': h+0.0})
            if True or mf == DB_STRUCT.WIND_MOD_CONSTR:
                element.update(
                    {'x1': l['hor_d_pos_a'], 'y1': l['vert_h_pos_a'], 'x2': l['hor_d_pos_b'], 'y2': l['vert_h_pos_b'], 'x3': l['hor_d_pos_c'],
                     'y3': l['vert_h_pos_c'], 'x4': l['hor_d_pos_n'], 'y4': l['vert_h_pos_n']})
        elif m == DB_STRUCT.MOD_TRANS_TBL:
            element.update(l)
            if mf == DB_STRUCT.WIND_MOD_TRANS:
                element.update({'id': element.get('equipref'), 'condType': element.get('connection'), })
                element.update({'single_%s'%k: element.get(k) for k in ['kva_a', 'kva_b', 'kva_c']})
            element.update({k: 0.0 for k, v in element.items() if v is None})
        elif m == DB_STRUCT.MOD_REG_TBL:
            element.update(l)
            if mf == DB_STRUCT.WIND_MOD_REG:
                element.update({'id': element.get('equipref'), 'ct_rating': element.get('rating'), 'cat': 'reg'})
        #elif m == DB_STRUCT.MOD_TRANS_CONN_TBL:
        #    pass

        return element

    def validateElement(self, m, b, l):
        if l is None:
            arcpy.AddError("Error in model, no record. Model: %s, Item id: %s."%(m, b))
        elif not 'phasecode' in l or l['phasecode'] is None:
            print("Model %s, item %s: %s"%(m, b, str(l)))
            arcpy.AddError("Error in model, no phasecode. Model: %s, Item id: %s."%(m, b))
        else:
            if not self.validateElementModel(m, b, l):
                arcpy.AddError("Error in model, invalid equipment model. Model: %s, Item id: %s."%(m, b))

    def validateElementModel(self, m, b, l):
        if m is None: return False
        if m in self.MODEL_LINKS:
        # build the model validation dict on the fly as needed
            if not hasattr(self, 'modelValidationDict'): self.modelValidationDict= {}
            if not m in self.modelValidationDict:
                mv= {}
                for ml in self.MODEL_LINKS[m]:
                    # assemble all the model table keys and check if None is allowed
                    mks= set([ml[1]] if type(ml[1])== str else ml[1])
                    # assemble the model keys
                    ks= set.union(*[set(self.net[mn].keys() if mn in self.net else []) for mn in mks])
                    mv[ml[0]]= {'mks': mks, 'ks': ks}
                self.modelValidationDict[m]= mv
            else: mv= self.modelValidationDict[m]

            # validate the model using the validation dict
            for ml in self.MODEL_LINKS[m]:
                if ml[0] in l:
                    # assemble all the model table keys and check if None is allowed
                    if l[ml[0]] is None and None not in mv[ml[0]]['mks']: return False
                    # check if the value of the model field (ml[0]) exists exists in the model keys
                    # note: if the field does not exist, then it is passed
                    elif l[ml[0]] not in mv[ml[0]]['ks']: return False
        return True

    def transPhase(self, ph):
        p = ph.lower()
        phase = 0
        pc= 'abcn' # can be improved by a loop over p not pc
        for i in range(4):
            if pc[i] in p: phase += 2**i
        return phase


    def writeFiles(self):
        self.writeConfigFile()
        for m in self.FILE_NAMES.keys(): self.writeModelFile(m)


if __name__ == '__main__':

    dir = r'C:\Users\llassetter\hotec'
    engDir = r'C:\epe\gs_backend\pfe'
    cfg = 'pfcattest.ini'

    # pfFiles = PowerFlowWriteFiles(dir=dir)

    # pfFiles = PowerFlowWriteFiles(
    #              configFile=cfg,
    #              dir=dir,
    #              confOpts={},
    #              skeletonDir=engDir)

    # pfFiles.writeConfigFile()

    pass
