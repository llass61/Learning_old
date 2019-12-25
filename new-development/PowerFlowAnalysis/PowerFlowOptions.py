import os
import json
import math

import arcpy

from addaUtils import floatOrNone, intOrNone

# from addaUtils import intOrNone, floatOrNone
from DBStructs import DB_STRUCT


class PowerFlowOptions():

    CONF_OPTS_DEF = ['; constantz', 'windmill']
    LOSS_ADJ_PARAMS = {'objective': 'P', 'method': 'T',
                       'tol': 1E-6, 'max_iter': 1000, 'init': 1.0}
    LOSS_ADJ_KEYS = ['objective', 'method', 'tol', 'max_iter', 'init']

    OPTS_MAP = ['loadScaling', 'genScaling', 'adjustForLosses']
    FAULT_CALC_SETTINGS_DEF = {'def_r': 1e-6, 'def_x': 0.0, 'oh_r': 1e-6,
                               'oh_x': 0.0, 'ug_r': 1e-6, 'ug_x': 0.0}

    FAULT_FLOW_SETTINGS_DEF = {'def_r': 1e-6, 'def_x': 0.0, 'oh_r': 1e-6, 'oh_x': 0.0,
                               'ug_r': 1e-6, 'ug_x': 0.0, 'def_con': 'Y', 'fault_points': []}

    CAP_OPT_SETTINGS = {'max_bank_size': 70.0, 'min_bank_size': 0.0, 'min_dist': 3500.0,
                     'corrective_factor': 0.7, 'add_single_ph': 0, 'indep_switching': 0}

    CAP_OPT_KEY = 'withcap'

    NEMA_KVA_HP = {'A': 1.6, 'B': 3.3, 'C': 3.8, 'D': 4.3, 'E': 4.7, 'F': 5.3,
                   'G': 5.9, 'H': 6.7, 'J': 7.5, 'K': 8.5, 'L': 9.5, 'M': 10.6,
                   'N': 11.8, 'P': 13.2, 'R': 15.0, 'S': 17.99, 'T': 19.99, 'U': 22.39, 'V': 25}

    MOTOR_KVA_HP_DEF = 2.0
    MOTOR_LOCKED_ROTOR_PF_DEF = 0.3
    MOTOR_V_DEF = 120
    MOTOR_CON_DEF = 0
    # defKvaHp, defLockedRotorPf, defMotorV, defMotCon = 2.0, 0.3, 120, 0

    def __init__(self, pfBuildModel, pfLoadData, opts=None, confOpts=CONF_OPTS_DEF,
                 adjForLosses=None,
                 faultCalcSettings=FAULT_CALC_SETTINGS_DEF,
                 faultFlowSettings=FAULT_FLOW_SETTINGS_DEF):

        self.opts = opts
        self.confOpts = confOpts
        self.adjustForLosses = adjForLosses
        self.lossAdjustmentParameters = PowerFlowOptions.LOSS_ADJ_PARAMS
        self.lossAdjustmentKeys = PowerFlowOptions.LOSS_ADJ_KEYS
        self.net = pfBuildModel.net
        self.toBus = pfBuildModel.toBus
        self.allBr = pfBuildModel.allBr
        self.busV = pfBuildModel.busV

        self.loadFeatureClass = pfLoadData.loadFeatureClass
        self.loadTable = pfLoadData.loadTable
        self.circuitsWhereClause = pfLoadData.circuitsWhereClause

        self.faultCalcSettings = faultCalcSettings
        self.faultFlowSettings = faultFlowSettings

        self.capOptSettings = self.CAP_OPT_SETTINGS
        self.reportTemplate = self.getNamedReportTemplate()


    def checkForOptions(self):

        if not (self.opts is None or self.opts == ''):

            try:
                opts = json.loads(self.opts)

                # carry through some of the options
                for k in self.OPTS_MAP:
                    if k in self.opts: setattr(self, k, opts[k])

                self.adjForLoses(opts)
                self.scenario(opts)
                self.faultCalc(opts)
                self.faultFlow(opts)
                self.motorStart(opts)
                self.capacitorOpt(opts)
                self.report(opts)

            except:
                arcpy.AddError("Invalid options string.")





    def adjForLoses(self, opts):
        if self.adjustForLosses is not None:
            self.lossAdjustmentParameters.update(
                opts.get('adjustForLosses', {}))
            arcpy.AddMessage('Feeder load adjustemtns for losses enabled; parameters: %s' % str(
                self.lossAdjustmentParameters))
            self.confOpts.append('adjustfeederloads '+' '.join(
                [str(self.lossAdjustmentParameters[k]) for k in self.lossAdjustmentKeys]))
            #self.confOpts.append('adjustfeederloads '+ ('S' if self.adjustForLosses == 'S' else 'P')+' '+('P' if self.adjustForLossesPerPhase == True else 'T'))

    def scenario(self, opts):
        if 'si' in opts:
            try:  # Scenario,Bus,Phases,Connection,ra,xa,rb,xb,rc,xc,rg,xg
                zs = opts['si']
                shunt = {'Bus': self.toBus.get(zs.get('secname')), 'Connection': intOrNone(
                    zs.get('con')), 'Phases': intOrNone(zs.get('phases'))}
                for k in ['ra', 'xa', 'rb', 'xb', 'rc', 'xc', 'rg', 'xg']:
                    shunt[k] = floatOrNone(zs.get(k))
                if all(map(lambda k: shunt[k] is not None, ['Bus', 'Connection', 'Phases'])):
                    sc = 'si@'+zs['secname']+'-'+str(shunt['Bus'])
                    shunt['Scenario'] = sc
                    self.net['shunt'][sc] = shunt
                    self.net['scenario'][sc] = {'Scenario': sc}
            except:
                arcpy.AddMessage("Invalid shunt impedance spec.")

    def faultCalc(self, opts):
         if 'fault_calc' in opts:
            fco = opts['fault_calc']
            if fco is None:
                fco = {}
            self.faultCalcSettings.update(fco)
            self.confOpts.append(
                'faultimpedances %(def_r)f %(oh_r)f %(ug_r)f' % self.faultCalcSettings)
            arcpy.AddMessage("Fault calculations enabled.")

    def faultFlow(self, opts):
        if 'fault_flow' in opts:
            ffo = opts['fault_flow']
            if ffo is None:
                ffo = {}
            self.faultFlowSettings.update(ffo)
            if self.addFaults() > 0:
                sc = 'fault_flow'
                self.net['scenario'][sc] = {'Scenario': sc}
            else:
                arcpy.AddMessage("No fault points found.")

            #self.confOpts.append('faultimpedances %(def_r)f %(oh_r)f %(ug_r)f'%self.faultCalcSettings)
            arcpy.AddMessage("Fault flow enabled.")

    def motorStart(self, opts):
        if 'motor_start' in opts:
            ms = opts['motor_start']
            arcpy.AddMessage("Motor start analysis enabled.")
            if self.addMotors() > 0:
                sc = 'motor_start'
                self.net['scenario'][sc] = {'Scenario': sc}
            else:
                arcpy.AddMessage("No valid motors found.")

    def capacitorOpt(self, opts):
        # capacitorplacement 70.0 0.0 3500.0 0.7 0
        if 'cap_opt' in opts:
            co = opts['cap_opt']
            if co is None:
                co = {}
            self.CAP_OPT_SETTINGS.update(co)
            arcpy.AddMessage("Capacitor optimization enabled.")
            #params= [('max_bank_size', 70.0), ('min_bank_size', 0.0), ('min_dist', 3500.0), ('corrective_factor', 0.7), ('add_single_ph', 0),]
            #pstr= 'capacitorplacement '
            #for p in params:
            #    v= str(co[p[0]] if co.has_key(p[0]) else p[1])
            #    pstr+="%s "%v
            #    printMsg(self.directRun, "Cap Opt param %s set to %s."%(p[0], v))
            #self.confOpts.append(pstr)
            self.confOpts.append(
                'capacitorplacement %(max_bank_size)f %(min_bank_size)f %(min_dist)f %(corrective_factor)f %(add_single_ph)d %(indep_switching)d' % self.capOptSettings)
            # also add the scenario self.CAP_OPT_KEY = "withcap"
            sc = self.CAP_OPT_KEY
            self.net['scenario'][sc] = {'Scenario': sc}

    def report(self, opts):
        if 'report' in opts:
            rf = opts['report']
            if 'named_template' in rf:
                arcpy.AddMessage("Named template selected.")
                self.reportTemplate = self.getNamedReportTemplate(rf['named_template'])
            elif 'template' in rf:
                arcpy.AddMessage("Template provided.")
                self.reportTemplate = rf['template']
            else:
                arcpy.AddMessage("No template provided, using default template.")
                self.reportTemplate = self.getNamedReportTemplate()

    def transCon(self, c):
        return 1 if c == 'D' else 0

    def addFaults(self):
        fc = 0
        for fp in self.faultFlowSettings['fault_points']:
            sr = {'rg': self.faultFlowSettings['def_r'],
                  'xg': self.faultFlowSettings['def_x'],
                  'con': self.faultFlowSettings['def_con'],
                  'ra': 0, 'rb': 0, 'rc': 0, 'xa': 0, 'xb': 0, 'xc': 0}

            if isinstance(fp, str) or isinstance(fp, unicode):
                fpid = fp
            elif isinstance(fp, dict):
                fpid = fp['secname']
                sr.update(fp)
            else:
                continue

            e, bus = self.allBr.get(fpid), self.toBus.get(fpid)
            if e is None or bus is None:
                continue
            arcpy.AddMessage("Fault added at %s." % fpid)

            sr['Connection'] = self.transCon(sr['con'])
            #{'def_r': 0.0, 'def_x': 0.0, 'oh_r': 0.0, 'oh_x': 0.0, 'ug_r': 0.0, 'ug_x': 0.0, 'fault_points': []}
            shunt = {'Bus': bus, 'Scenario': 'fault_flow',
                     'Phases': self.transPhase(e['phasecode'])}
            shunt.update(sr)
            self.net['shunt'][fpid] = shunt
            fc += 1
        return fc

    def addMotors(self):
        motors = self.loadFeatureClass(
            DB_STRUCT.GRID_EQUIP_FC, wherClause="%s and otype='motor'" % self.circuitsWhereClause)
        mms = self.loadTable(DB_STRUCT.MOD_MOTOR_TBL, None, None, True)
        # defKvaHp, defLockedRotorPf, defMotorV, defMotCon = 2.0, 0.3, 120, 0  # 0 : Y, 1: D
        mc = 0
        for m, v in motors.items():
            if not (v.get('status') and v['status'].index('1') >= 0):
                continue
            mm = mms.get(v.get('equipref'))
            bus = self.toBus.get(v.get('parentsec'))
            busV = self.busV.get(v.get('parentsec'))
            if not (mm and bus and busV):
                continue

            # if there is a load record in the option, we adjust the current magnitude by the full load current
            method = 'new'
            pars = json.loads(v['pars']) if v['pars'] is not None else None
            lr = self.net['load'].get(pars.get('load'))
            lmr = self.net['model_load'].get(lr.get('equipref'))
            ratio = floatOrNone(pars.get('ratio'))

            if lr and lr['parentsec'] != v['parentsec']:
                arcpy.AddMessage("Warning, motor (%s) and its associated load (%s) not on the same parent." % (
                    v['secname'], lr['secname']))
            if lr and not self.phaseSubset(v['phasecode'], lr['phasecode']):
                arcpy.AddMessage("Warning, motor (%s) and its associated load (%s) do not have conforming phase codes." % (
                    v['secname'], lr['secname']))

            flc = sum([(lmr['kw_'+p] * (1 if p.upper() in lr['phasecode'] else 0))
                       for p in list('abc')])/lmr['pf']/busV*ratio if lmr and lr and ratio else 0
            flcc = (flc*lmr['pf'] - 1j * flc*math.sin(math.copysign(1,
                                                                    lmr['pf']) * math.acos(math.fabs(lmr['pf'])))) if lmr else 0

            kva_hp = mm.get('lr_kva_hp') or self.NEMA_KVA_HP.get(
                mm.get('nema_code')) or self.MOTOR_KVA_HP_DEF
            pf = mm.get('lr_pf') or  self.MOTOR_LOCKED_ROTOR_PF_DEF
            inrushcm = mm['hp'] * kva_hp * (mm.get('sr_ratio') or 1.0) / busV

            if method == 'new':
                stc = (inrushcm * (pf - 1j * math.sin(math.acos(pf))) -
                       flcc) / len(v['phasecode'])
                z = busV * 1000 / stc
                arcpy.AddMessage("Equivalent impedance for motor %s: %0.3f +j %0.3f, |z|= %0.3f" %
                                 (v['secname'], z.real, z.imag, abs(z)))
            else:
                nv = len(v['phasecode']) * (busV * 1000 *
                                            (pf + 1j * math.sin(math.acos(pf))))
                znl = nv / inrushcm
                z = nv / (inrushcm - flc)
                arcpy.AddMessage("Equivalent impedance for motor %s: %0.3f, %0.3f (factoring FL)" % (
                    v['secname'], abs(znl), abs(z)))

            r, x = z.real, z.imag
            r += (mm['sr_r'] if mm['sr_r'] else 0)
            x += (mm['sr_x'] if mm['sr_x'] else 0)
            arcpy.AddMessage(
                "Effective equiv impedance for motor %s: %0.3f +j %0.3f" % (v['secname'], r, x))

            shunt = {'Bus': bus, 'Connection':  self.MOTOR_CON_DEF, 'Scenario': 'motor_start',
                     'Phases': self.transPhase(v['phasecode']), 'rg': 0, 'xg': 0,
                     'ra': r, 'rb': r, 'rc': r, 'xa': x, 'xb': x, 'xc': x}
            self.net['shunt'][m] = shunt
            mc += 1
        return mc

    def transPhase(self, ph):
        p = ph.lower()
        phase = 0
        pc = 'abcn'  # can be improved by a loop over p not pc
        for i in range(4):
            if pc[i] in p:
                phase += 2**i
        return phase

    def phaseSubset(self, pc, pp):
        if pc is None or pc == '':
            return False
        for p in pc:
            if p not in pp:
                return False
        return True


    def getNamedReportTemplate(self, name=None):
        if name is None:
            template = {'title': 'Report Title',
                        'columns': [
                            {'label': 'id', 'field': 'secname', },
                            {'label': 'parent', 'field': 'parentsec', },
                            {'label': 'Circuit', 'field': 'circuit', },
                            {'label': 'equipment', 'field': 'equipref', },
                            {'label': 'phase', 'field': 'phasecode', },
                            {'label': 'Element Type', 'field': 'otype', },
                            {'label': 'nominal voltage', 'field': 'nom_v', },
                            {'label': 'rating', 'field': 'c_rating', },
                            {'label': 'Length', 'field': 'length', },
                            {'label': 'Number of Loads (direct)',
                             'field': 'n_di_load', },
                            {'label': 'Number of Loads (downstream)',
                             'field': 'n_ds_load', },
                            {'label': 'kW Loads (downstream)',
                             'field': 's_load_kw', },
                            {'label': 'kVAR Loads (downstream)',
                             'field': 's_load_kvar', },
                            {'label': 'Number of Caps (direct)',
                             'field': 'n_di_cap', },
                            {'label': 'Number of Caps (downstream)',
                             'field': 'n_ds_cap', },
                            {'label': 'kVAR Caps (downstream)',
                             'field': 's_cap_kvar', },
                        ]}

            template['columns'] += [{'label': "Vdrop 120 %s" % (p),
                                     'field': "vd120_m_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "Vdrop Balanced 120",
                                     'field': "vd120_m_l"}]
            template['columns'] += [{'label': "Voltage (base 120) %s" % (p),
                                     'field': "v120_m_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "Voltage Balanced (base 120)",
                                     'field': "v120_m_l"}]
            template['columns'] += [{'label': "Loading %% %s" % (p),
                                     'field': "loading_m_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "Through kW %s" % (p),
                                     'field': "p_kw_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "Through kVAR %s" % (p),
                                     'field': "q_kvar_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "PF %s" % (p),
                                     'field': "pf_m_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "V 120 %s" % (p),
                                     'field': "v120_m_%s" % (p)} for p in 'abc']
            template['columns'] += [{'label': "Balanced Voltage %s" % (i),
                                     'field': "v%s_l" % (i)} for i in ['r', 'i']]
            template['columns'] += [{'label': "%s%s_%s" % (q, i, p),
                                     'field': "%s%s_%s" % (q, i, p)} for q in ['v', 'c', 'l', 'fi',
                                                                               'fc', 's_', 'vpu_',
                                                                               'loading_', 'v120_'] for i in 'ri' for p in 'abc']
            template['columns'] += [{'label': "fi%s%s" % (t, i),
                                     'field': "fi%s%s" % (t, i)} for t in ['0', '1'] for i in ['r', 'i']]

        else:
            # obtain named template
            pass
        return template


if __name__ == '__main__':

    # opts = '{"loadScaling": 1.0, "genScaling": 1.0, "adjustForLosses": {} }'
    # objective: "P" or "R"  method:  "T" or "P"
    opts = '{"loadScaling": 1.0, "genScaling": 1.0, "adjustForLosses": {"objective": "P", "method": "T", "tol": 0.00000100, "max_iter": 1000, "init": 1} }'

    # PowerFlowOptions()
