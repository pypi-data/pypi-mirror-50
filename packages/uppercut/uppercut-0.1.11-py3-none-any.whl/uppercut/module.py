""" tools to configure modules used in an uppercut system """
from redis import Redis
import uppercut.constants as constants
import json
import uppercut.environment as environment
import signal
import time
from uppercut.sharedvars import SharedVarStore, SystemVarStore
redishost = environment.getVar(constants.EnvVars.SHARED_VAR_HOST,"localhost")
    
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
            temp = time.time()%60
            self.VarStore.set('temperature',temp)
            print(self)
    myMod = test_mod('test_mod', 1)
    myMod.start()
