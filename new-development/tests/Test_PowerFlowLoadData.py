import unittest
# from datetime import datetime
# from datetime import timedelta
# import numpy

# import PowerFlowAnalysis.PowerFlowLoadData
from PowerFlowAnalysis import *

# loads customer interval power file
class Test_loadIntervalLoadFile(unittest.TestCase):

    # def setUp(self):
    #     self.fileName = r'tests/data/sql.txt'
        # self.startTs = datetime.now()
        # self.endTs = self.startTs + timedelta(days=1)


    def testCreatePowerFlowLoadDataClass(self):
        # db = PowerFlowAnalysis.
        pfLoadData = None #PowerFlowLoadData(None, '.*', 'TT2', 'GS1')
        self.assertIsNotNone(pfLoadData, "Error creating PowerFlowLoadData object")


    # def testNoInputFile(self):
    #     # args = {'fileName': None, 'notGP': True, 'startTs': self.startTs, 'endTs': self.endTs}
    #     dd = ManageIntervalLoadProfile()
    #     retVal = dd.loadIntervalLoadFile()
    #     self.assertFalse(retVal, "Filename is None - should return False: %s" % retVal)


    # def testInvalidInputFile(self):
    #     # args = {'fileName': './none', 'notGP': True, 'startTs': self.startTs, 'endTs': self.endTs}
    #     dd = ManageIntervalLoadProfile()
    #     retVal = dd.loadIntervalLoadFile()
    #     self.assertFalse(retVal, "Filename is Invalid - should return False: %s" % retVal)


    # def testGoodInputFile(self):
    #     # args = {'fileName': self.fileName, 'notGP': True, 'startTs': self.startTs, 'endTs': self.endTs}
    #     dd = ManageIntervalLoadProfile()
    #     retVal = dd.loadIntervalLoadFile()
    #     self.assertTrue(retVal, "Unable to find : %s" % self.fileName)


# filters string timestamps
# class Test_filterByTimestamp(unittest.TestCase):

#     def setUp(self):
#         self.fileName = r'./data/sql.txt'
#         self.startTs = datetime.now()
#         self.endTs = self.startTs + timedelta(days=1)
#         self.beforeStart = self.startTs - timedelta(seconds=1)
#         self.afterEnd = self.endTs + timedelta(seconds=1)
#         self.startTsSf = self.startTs.strftime("%I:%M%p %m/%d/%Y")
#         args = {'fileName': self.fileName, 'notGP': True, 'startTs': self.startTs, 'endTs': self.endTs}
#         self.dd = ManageIntervalLoadProfile()
#         self.dd.loadIntervalLoadFile(args)


#     def testSameAsStart(self):
#         retVal = self.dd.filterByTimestamp(self.startTs)
#         self.assertTrue(retVal, "startTs should be good: %s" % self.startTs)


#     def testSameAsEnd(self):
#         retVal = self.dd.filterByTimestamp(self.endTs)
#         self.assertTrue(retVal, "EndTs should be good: %s" % self.endTs)


#     def testBeforeStart(self):
#         retVal = self.dd.filterByTimestamp(self.beforeStart)
#         self.assertFalse(retVal, "beforeStart < startTs - should return False: %s" % self.beforeStart)


#     def testAfterEnd(self):
#         retVal = self.dd.filterByTimestamp(self.afterEnd)
#         self.assertFalse(retVal, "afterEnd > endTs - should return False: %s" % self.afterEnd)


# class Test_calcLoadsByPhase(unittest.TestCase):

#     def setUp(self):
#         self.dd = ManageIntervalLoadProfile()


#     def testGoodPhaseA(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = kwh / 4
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'A')
#         self.assertTrue(kwVals[0] == kw, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == 0, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == 0, "kw_c is incorrect")


#     def testGoodPhaseAB(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4) / 2
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'AB')
#         self.assertTrue(kwVals[0] == kw, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == kw, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == 0, "kw_c is incorrect")


#     def testGoodPhaseABC(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4) / 3
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'ABC')
#         self.assertTrue(kwVals[0] == kw, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == kw, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == kw, "kw_c is incorrect")


#     def testGoodPhaseAC(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4) / 2
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'AC')
#         self.assertTrue(kwVals[0] == kw, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == 0.0, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == kw, "kw_c is incorrect")


#     def testGoodPhaseB(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4)
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'B')
#         self.assertTrue(kwVals[0] == 0.0, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == kw, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == 0.0, "kw_c is incorrect")


#     def testGoodPhaseBC(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4) / 2
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'BC')
#         self.assertTrue(kwVals[0] == 0.0, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == kw, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == kw, "kw_c is incorrect")


#     def testGoodPhaseC(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4)
#         kwVals = self.dd.calcLoadsByPhase(kwh, 'C')
#         self.assertTrue(kwVals[0] == 0.0, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == 0.0, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == kw, "kw_c is incorrect")


#     def testEmptyPhase(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4)
#         kwVals = self.dd.calcLoadsByPhase(kwh, '')
#         self.assertTrue(kwVals[0] == 0.0, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == 0.0, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == 0.0, "kw_c is incorrect")


#     def testNullPhase(self):
#         self.dd.timestep = 15
#         kwh = .3333
#         kw = (kwh / 4)
#         kwVals = self.dd.calcLoadsByPhase(kwh, '')
#         self.assertTrue(kwVals[0] == 0.0, "kw_a is incorrect")
#         self.assertTrue(kwVals[1] == 0.0, "kw_b is incorrect")
#         self.assertTrue(kwVals[2] == 0.0, "kw_c is incorrect")


if __name__ == '__main__':
    # pfLd = PowerFlowLoadData(None, None, None, None)
    print("HI")
