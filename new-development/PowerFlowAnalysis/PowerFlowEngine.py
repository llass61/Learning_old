import os
import datetime
import time
import subprocess

import arcpy

from addaUtils import timeMessage
from Connection import Connection


class PowerFlowEngine():

    PF_LOGFILE_NM = 'pfe.log'
    PF_ENG_DIR = 'pfe'
    PF_CONFIG_FILENAME = 'pfcattest.ini'

    def __init__(self, dir=None, engineDir=None, configFile=PowerFlowEngine.PF_CONFIG_FILENAME):

        self.conn = Connection()

        self.dir = dir if dir != None else self.conn.getDir()

        self.engineDir = engineDir
        if self.engineDir is None:
            self.engineDir = os.path.join(self.conn.getDir(), self.PF_ENG_DIR)

        self.configFile = configFile

        self.engineCommand = r"""java -jar "%s\pfe.jar" %s""" % (
            self.engineDir, self.configFile)

        self.logfile = os.path.join(self.dir, self.PF_LOGFILE_NM)

        pass

    def run(self):
        # build command
        # run engine and collect output -> should we run in parallel?
        od = os.getcwd()
        os.chdir(self.dir)
        startTime = time.time()
        with open(self.logfile, 'w') as logFile:
            cmd = self.engineCommand % {
                'configFile': self.configFile,
                'enginDir': self.engineDir
            }
            logFile.write('Starting Engine at %s\n' %
                          str(datetime.datetime.now()))
            logFile.write('Working directory: %s\n' % os.getcwd())
            logFile.write('Engine command line: %s\n' % cmd)
            p = subprocess.Popen(cmd,
                                 shell=True,
                                 stdout=logFile,
                                 stderr=logFile)

        toc = time.time()
        with open(os.path.join(self.dir, self.logfile), 'r') as logFile:
            while p.poll() is None:
                l = logFile.readline()
                while l:
                    if l.find('Start YBus Build') >= 0:
                        toc = timeMessage(
                            toc, 'Engine: Reading pf data files', None)
                    if l.find('YBus Factorization') >= 0:
                        toc = timeMessage(
                            toc, 'Engine: YBus Factorize Complete')
                    if l.find('Power Flow Converged') >= 0:
                        print(l[:-1])
                        toc = timeMessage(toc, 'Engine: Power flow')
                    l = logFile.readline()
                lPos = logFile.tell()
                time.sleep(0.1)
                logFile.seek(lPos)
        toc = timeMessage(toc, 'Engine: Writing pf files')
        print("Total Engine Time (min):" + "%.2f" %
              ((time.time() - startTime) / 60))
        res = p.returncode
        if res == 0:
            arcpy.AddMessage("Power flow finished successfully!")
        else:
            arcpy.AddError(
                "Power flow engine failed! See log file for errors.")

        os.chdir(od)
        return res

if __name__ == '__main__':

    dir = r'C:\Users\llassetter\hotec'
    engDir = r'C:\epe\gs_backend\pfe'
    cfg = 'pfcattest.ini'

    pfe = PowerFlowEngine(dir, engDir, cfg)
    # pfe = PowerFlowEngine()

    pfe.run()

    pass
