from redis import Redis
import json
import constants 
import environment

def encode(val):
    return json.dumps(val)

def decode(val):
    return json.loads(val.decode('utf-8'))

_redisInstance = None
def GetRedisInstance(redisHost=None):
    global _redisInstance
    if _redisInstance is None:
        redisHost = redisHost or environment.getVar(constants.EnvVars.SHARED_VAR_SERVER,'localhost')
        _redisInstance = Redis(host=redisHost)
    return _redisInstance

class SharedVarStore(Redis):
    """This class abstracts the reading and setting of shared variables between modules.
    This specific implementation uses Redis"""
    def __init__(self,moduleName,redisHost=None):
        
        self._client = GetRedisInstance(redisHost)
        self._modName = moduleName

    def getKey(self,varName):
        """generate the key name used to store the var in Redis"""
        return '{}/{}'.format(self._modName,varName)

    def get(self,varName,defaultValue=None):
        """ Get the value of a shared variable.

        @param: varName The name of the variable that you need to access.
        @param: defaultValue The default value to return if the variable doesn't exist yet.
        """
        v = self._client.get(self.getKey(varName))
        if v is None: return defaultValue
        return decode(v)

    def set(self,varName,value):
        """ Set the value of a shared variable.

        @param: varName The name of the variable to set.
        @param: value The new value of the variable.
        """
        self._client.set(self.getKey(varName),encode(value))

    def push(self,listName,value):
        k = self.getKey(listName)
        v = encode(value)
        self._client.lpush(k,v)
        self._client.lpush
    
def SystemVarStore():
    return SharedVarStore(constants.Keys.UPPERCUT_SYS)