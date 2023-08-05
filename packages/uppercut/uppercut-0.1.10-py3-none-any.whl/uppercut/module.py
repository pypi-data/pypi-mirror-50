""" tools to configure modules used in an uppercut system """
from redis import Redis
import constants
import json
import environment
import signal
import time
from sharedvars import SharedVarStore, SystemVarStore
redishost = environment.getVar(constants.EnvVars.MOD_REG_SERVER,"localhost")
    
class Module(object):
    def terminate(self,signum,frame):
        self._isUp = False
    
    def __init__(self,name,interval):
        signal.signal(signal.SIGINT,self.terminate)
        signal.signal(signal.SIGTERM,self.terminate)
        self.VarStore = SharedVarStore(name)
        self._sysVarStore = SystemVarStore()
        self._name = name
        self._interval = interval
        self._isUp = False
        self._register()

    def _register(self):
        _redis = Redis(host=redishost)
        modInfo = {'name':self._name}
        self._sysVarStore.push(constants.Keys.MOD_LIST,modInfo)
        print('pushed mod info')

    def start(self):
        self._isUp = True
        while self._isUp:
            self.mainLoop()
            time.sleep(self._interval)

if __name__=="__main__":
    class test_mod(Module):
        def mainLoop(self):
            print(self)
    myMod = test_mod('test_mod', 1)
    myMod.start()
