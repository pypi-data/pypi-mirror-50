import importlib
import os
import shutil
import traceback
import logging

from withinPath import withinPath

def copyFiles(files, destinationDir):
    for file in files:
        if os.path.isdir(file):
            dest = os.path.join(destinationDir, file)
            shutil.copyfile(file, dest)
        else:
            finalDir = os.path.join(destinationDir, os.path.dirname(file))
            dest = os.path.join(destinationDir, file)
            os.makedirs(finalDir, exist_ok = True)
            shutil.copy2(file, dest)

defaultRootPath = os.getcwd()

class CacheManager():
    def __init__(self, rootPath, sourcePath, toCacheFiles):
        self.rootPath = defaultRootPath
        self.sourcePath = sourcePath

        self.cachePath = os.path.join(self.rootPath, 'cache')
        self.cached = os.path.isdir(self.cachePath)
        self.files = toCacheFiles

    # for now on we are going to be working from the experiment forder in the outputs... may be it needs a new name.
    # Every experiment need to be fully contained within the cache folder and everythin in the network is loaded relative to cache folder as root so no chance should be needed from the original script
    # 
    def moduleLoader(self, reload = False):
        with withinPath(toDir = self.cachePath, fromDir = self.rootPath):
            module = importlib.import_module('network')
            if reload:
                module = importlib.reload(module)

        return module

    def destroyCache(self):
        try:
            shutil.rmtree('cache')
            self.cached = False
        except Exception as e:
            logging.error(traceback.format_exc())

    def fillCache(self):
        print('---------------')
        print(self.sourcePath, '\n' , self.rootPath, '\n' , self.cachePath, '\n' , self.files)
        with withinPath(toDir = self.sourcePath, fromDir =  self.rootPath):
            copyFiles(self.files, self.cachePath)
            self.cached = True

    def createCache(self):
        if self.cached == True:
            self.destroyCache()
            self.cached = False
        elif self.cached == None:
            raise ValueError('cache state undefined')
        self.fillCache()