import os
import re
import subprocess

class ManageServices():
    """ManageServices all EPE's geoservices to ArcGIS server"""

    UTIL_SVCS = 'util'
    GEN_SVCS = 'gen'
    SYS_SVCS = 'sys'
    DELETE_SERVICE = 'delete'
    STATUS_SERVICE = 'status'
    STOP_SERVICE = 'stop'
    START_SERVICE = 'start'
    LIST_SERVICES = '-l'
    VALID_OPERATIONS = [DELETE_SERVICE, STATUS_SERVICE,
                        STOP_SERVICE, START_SERVICE]


    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.serviceList = {}
        self.genServices = {}
        self.utilServices = []
        self.sysServices = []

        # create site from server
        self.site = "http://%s:6080" % server

        # ArcGIS supplies command line tools to manage services
        self.manageServicePy = os.path.join(os.getenv("AGSSERVER"),"tools", "admin", "manageservice.py")
        self.manageServicePy = '"%s"' % self.manageServicePy
        self.manageService = "python  " + self.manageServicePy
        self.baseCmd = "%s -s %s -u %s -p %s" % (self.manageService, self.site, self.user, password)

        # lets load up the services
        self.getServices()


    def service(self, serviceName, operation):
        """ Main method for making a call with operation type """
        op = None
        cmd = "%s -n %s -o %s" % (self.baseCmd, serviceName, operation)

        if self.serviceExists(serviceName):
            if operation in self.VALID_OPERATIONS:
                op = os.popen(cmd, ).read()
                print (open)
            else:
                print ("ERR: Invalid operation: %s" % operation)

        self.getServices()
        return op


    def stopService(self, serviceName):
        return self.service(serviceName, self.STOP_SERVICE)


    def startService(self, serviceName):
        return self.service(serviceName, self.START_SERVICE)


    def statusService(self, serviceName):
        return self.service(serviceName, self.STATUS_SERVICE)


    def deleteService(self, serviceName):
        return self.service(serviceName, self.DELETE_SERVICE)


    def serviceExists(self, serviceName):
        ret = serviceName in self.serviceList.keys()
        if not ret:
            print ("ERR: Service %s not found" % serviceName)
        return ret


    def deleteAllGPServices(self):
        for svc in self.serviceList:
            if (self.serviceList[svc]['type'] == 'GPServer' and
                 self.serviceList[svc]['status'] == 'STARTED' and
                 self.serviceList[svc]['cat'] == 'gen'):

                self.deleteService(svc)


    def deleteAllMapServices(self):
        for svc in self.serviceList:
            if (self.serviceList[svc]['type'] == 'MapServer' and
                 self.serviceList[svc]['status'] == 'STARTED' and
                 self.serviceList[svc]['cat'] == 'gen'):

                self.deleteService(svc)


    def deleteAllServices(self):
        self.deleteAllMapServices()
        self.deleteAllGPServices()


    # def listServices(self, pythonExec, fpManageService, username, passwd, server):
    def getServices(self):
        """ Returns all client services (Map and Geoprocessor).
            Will not return ArcGIS services
        """
        cmd = "%s %s" % (self.baseCmd, self.LIST_SERVICES)
        # proc = subprocess.Popen(cmd, shell=True,
        #                         stdin=subprocess.PIPE,
        #                         stdout=subprocess.PIPE)
        proc = os.popen(cmd).read()
        for x in proc.split("\n"):
            if (len(x.strip()) > 0):
                k,v = x.split("|")
                # if not (k.startswith('Utilities') or k.startswith('System') or k.startswith('Sample')):
                #     key = re.sub(r'.\w*$', "", k.strip())
                #     value = v.strip()
                #     self.serviceList[key] = value

                cat = 'gen'
                k = k.strip()
                if (k.startswith('Utilities')):
                    cat = 'util'
                    k = re.sub(r'Utilities/', "", k.strip())
                elif (k.startswith('System')):
                    cat = 'sys'
                    k = re.sub(r'System/', "", k.strip())

                svcAndType = k.split(".")

                # do not put in System or Utilities.  Can comment
                # out later if needed
                if (cat == 'util' or cat == 'sys' or k.startswith('Sample')):
                    self.serviceList # do not add
                else:
                    self.serviceList[svcAndType[0]] = {'cat': cat,
                                                   'type': svcAndType[1],
                                                   'status': v.strip()}

        return proc

    def printServices(self):
        """ prints the current services """
        for k,v in self.serviceList.iteritems():
            print ("%s - %s" % (k,v))
        print("\n\n")

if __name__ == '__main__':

    # ms = ManageServices("epedev002-ll", "siteadmin", "epeconsulting")
    # ms = ManageServices("epedev005-ll", "siteadmin", "epeconsulting")
    # ms = ManageServices("gssrvrel", "siteadmin", "epeconsulting")
    # ms = ManageServices("gssrvdev", "siteadmin", "epeconsulting")
    # ms = ManageServices("epedev001-desk", "siteadmin", "epeconsulting")
    ms = ManageServices("hotec-be", "siteadmin", "epeconsulting")

    # ms.deleteAllGPServices()
    # ms.deleteAllMapServices()
    # ms.deleteAllServices()
    # ms.deleteService('intPowerflowAnalysis')
    # ms.printServices()
    # s = ms.getServices()
    # s.printServices()
    print ("Finished!")
