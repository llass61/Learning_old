import arcpy
import os
import datetime


class Connection():

    def __init__(self):

        self.directRun = True
        self.dir = os.environ.get('GS_BACKEND', '..')
        self.server = os.environ.get('GS_SERVER')
        self.sde = os.environ.get('GS_SDE')  # sde file name
        # self.dbPfx = os.environ.get('GS_PFX', 'hotec.sde.')
        # self.sde = 'eneri'
        if not self.sde.endswith('.sde'):
            self.sde = self.sde + '.sde'

    def getSde(self):
        return self.sde

    def getSdeFullPath(self):
        return os.path.join(self.dir, self.sde)

    def getDir(self):
        return self.dir

    def getServer(self):
        return self.server


