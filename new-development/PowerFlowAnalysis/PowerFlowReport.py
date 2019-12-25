import os
import json
import math

import arcpy

# from addaUtils import intOrNone, floatOrNone
from DBStructs import DB_STRUCT


class PowerFlowOptions():


    def __init__(self, allBr, sortedKeys):
        self.reportTemplate = self.getNamedReportTemplate()
        self.allBr = allBr
        self.sortedKeys = sortedKeys


    def compileReport(self):
        self.report= {'title': self.reportTemplate['title'], 'rows': []}
        rs= self.report['rows']
        for k in self.sortedKeys:
            if k in self.allBr: rs.append(self.reportRow(self.allBr[k]))


    def reportRow(self, v):
        return {c['label']: self.calcQuant(v, c['field']) for c in self.reportTemplate['columns']}


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
