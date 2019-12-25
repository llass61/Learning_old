import logging
from suds.client import Client

from SudsResponseConverter import basic_sobject_to_dict

#logging.basicConfig(level=logging.DEBUG)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


class EPEConnection(object):

    def __init__(self, url, wsdl=None, timeout=15):
        self.url = url
        self.wsdl = wsdl
        self.client = None
        self.timeout = timeout

    def connect(self):
        if (wsdl):
            self.client = Client(wsdl, timeout=self.timeout)
            self.client.wsdl.services[0].setlocation(url)
        else:
            self.client = Client(url, timeout=self.timeout)

    def getClient(self):
        return self.client



def printFleetIds(fleetData):

    if fleetData:
        fleetList = (fleetData['SynoviaApi'])['Fleets']
        for f in fleetList:
            for ff in f:
                if ff != 'Fleet':
                    for fff in ff:
                        print ("Fleet: " + fff._ID)


def printVehicleIds(vehicleData):
    if vehicleData:
        vehicleList = (vehicleData['SynoviaApi'])['Vehicles']
        for f in vehicleList:
            for ff in f:
                if ff != 'Vehicle':
                    for fff in ff:
                        print ("Fleet:  " + fff._FleetID + ";  Vehicle: " + fff._VehicleID)


def printLastUpdatedVehicles(lastUpdData):
    if lastUpdData:
        vehicleUpdList = (lastUpdData['SynoviaApi'])['VehiclesLastPositions']
        for f in vehicleUpdList:
            for ff in f:
                if ff != 'VehicleLastPosition':
                    for fff in ff:
                        print ("Fleet:  " + fff._FleetID + ";  Vehicle: " + fff._VehicleID)


def fixUglyData(data, a, b):
    retLst = []
    if data:
        list = (data['SynoviaApi'])[a]
        for f in list:
            for ff in f:
                if ff != b:
                    for fff in ff:
                        retLst.append(fff)

    return retLst


wsdl = r'file:///C:\Users\llassetter\Grid-I\int\SynoviaApi.svc.xml'
#wsdl = r'https://apiqa.synovia.com/SynoviaApi.svc?wsdl'
url = r'https://api.synovia.com/SynoviaApi.svc'
conn = EPEConnection(url, wsdl)


#client = Client(wsdl, timeout=15)
#client.wsdl.services[0].setlocation(url)
conn.connect()
client = conn.getClient()

args=['C3603B16-6401-4530-93FA-4924C7150BC1','','']
#args=['FDD85CE8-5571-4643-B071-3117CBB8073D']

# fleets
fleets = getattr(client.service, 's0002')
fleetData = fleets(*args)

# Vehicles
vehicles = getattr(client.service, 's0003')
vehicleData = vehicles(*args)

fleetIds = ['96FF87C9-D8D2-432F-B6A8-1584D3082CDE','97FD3B87-82B9-42C2-BE84-25E0C67F3170','79DA4F09-6267-430D-8A52-F2FCB3FA1BC9']
#args[2] = ','.join(fleetIds)
lastUpdated = getattr(client.service, 's0116')
lastUpdData = lastUpdated(*args)

fleetList = fixUglyData(fleetData, 'Fleets', 'Fleet')
actFleetIds = [af._ID for af in fleetList]

vehUpdList = fixUglyData(lastUpdData, 'VehiclesLastPositions', 'VehicleLastPosition')
vehList = fixUglyData(vehicleData, 'Vehicles', 'Vehicle')
actVehIds = [v._VehicleID for v in vehList if v._FleetID in actFleetIds]

filteredUpdPositions = [last for last in lastUpdData if last._VehicleID in actVehIds]

#activeVehiclesIDs = [v._VehicleID for v in vehList if v.]
fleetDict = basic_sobject_to_dict(fleetData)

printFleetIds(fleetData)
printVehicleIds(vehicleData)
printLastUpdatedVehicles(lastUpdData)
pass