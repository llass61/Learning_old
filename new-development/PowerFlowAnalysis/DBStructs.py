
class DB_STRUCT:

    GRID_LOADS_FC = 'grid_loads'
    GRID_POW_LINE_FC = 'grid_powerlines'
    GRID_EQUIP_FC = 'grid_equipment'

    # break up equipment into types
    GRID_EQUIP_SRC = 'grid_equip_src'
    GRID_EQUIP_TRANS = 'grid_equip_trans'
    GRID_EQUIP_SWITCH = 'grid_equip_switch'
    GRID_EQUIP_REG = 'grid_equip_reg'
    GRID_EQUIP_PROT = 'grid_equip_prot'
    GRID_EQUIP_CAP = 'grid_equip_cap'
    GRID_EQUIP_GEN = 'grid_equip_gen'

    MOD_CAP_TBL = 'model_cap'
    MOD_CIRC_TBL = 'model_circuit'
    MOD_COND_TBL = 'model_conductor'
    MOD_CONSTR_TBL = 'model_construction'
    MOD_GEN_PROF_TBL = 'model_gen_profile'
    MOD_GEN_TBL = 'model_generator'
    MOD_LOAD_TBL = 'model_loads'
    MOD_MOTOR_TBL = 'model_motor'
    MOD_PROT_TBL = 'model_protection'
    MOD_REG_TBL = 'model_regulator'
    MOD_SRC_TBL = 'model_source'
    MOD_SWITCH_TBL = 'model_switch'
    MOD_TRANS_TBL = 'model_transformer'
    MOD_UG_TBL = 'model_ug'
    MOD_WIRE_TBL = 'model_wire'
    MOD_TRANS_CONN_TBL = 'model_trans_conn'

    CIRCUIT = 'circuit'
    SHUNT = 'shunt'
    SCENARIO = 'scenario'

    WIND_MOD_COND = 'windmill_model_cond'
    WIND_MOD_UG = 'windmill_model_ug'
    WIND_MOD_CONSTR = 'windmill_model_const'
    WIND_MOD_TRANS = 'windmill_model_tran'
    WIND_MOD_REG = 'windmill_model_reg'

    INT_MOD_LOAD_TBL = 'int_model_load'

    BRANCH_ELEMENTS = [GRID_EQUIP_SRC, GRID_POW_LINE_FC,
                       GRID_EQUIP_TRANS, GRID_EQUIP_SWITCH,
                       GRID_EQUIP_REG, GRID_EQUIP_PROT]

    TOP_ELEMENTS = [GRID_EQUIP_GEN, GRID_LOADS_FC, GRID_EQUIP_CAP]

    # DB_NETWORK = {'line': GRID_POW_LINE_FC,
    #               'load': GRID_LOADS_FC, 'equipment': GRID_EQUIP_FC}

    DB_MODEL = {
        'load': MOD_LOAD_TBL, 'trans': MOD_TRANS_TBL, 'cap': MOD_CAP_TBL, 'prot': MOD_PROT_TBL,
                'reg': MOD_REG_TBL, 'switch': MOD_SWITCH_TBL, 'source': MOD_SRC_TBL,
                'wire': MOD_WIRE_TBL, 'circuit': MOD_CIRC_TBL, 'ug': MOD_UG_TBL,
                'conductor': MOD_COND_TBL, 'construction': MOD_CONSTR_TBL, 'motor': MOD_MOTOR_TBL,
                'gen': MOD_GEN_TBL, 'genp': MOD_GEN_PROF_TBL,
    }

    MODELS_TO_CHECK = {
        GRID_EQUIP_SRC: [('equipref', [MOD_SRC_TBL])],

        GRID_POW_LINE_FC: [('conductor', [MOD_COND_TBL, MOD_UG_TBL]),
                            ('neutral', [MOD_COND_TBL, MOD_UG_TBL]),
                            ('construction', [MOD_CONSTR_TBL])],

        GRID_EQUIP_GEN: [('equipref', [MOD_GEN_TBL])],
        GRID_EQUIP_PROT: [('equipref', [MOD_PROT_TBL])],
        GRID_EQUIP_REG: [('equipref', [MOD_REG_TBL])],
        GRID_EQUIP_CAP: [('equipref', [MOD_CAP_TBL])],
        GRID_EQUIP_TRANS: [('equipref', [MOD_TRANS_TBL])],
        # GRID_LOADS_FC: [('equipref', [MOD_LOAD_TBL])],
    }

    CASE_RESULTS = {'study': 'res_study', 'pf': 'res_pf'}


if __name__ == '__main__':
    print(DB_STRUCT.MODELS_TO_CHECK)
