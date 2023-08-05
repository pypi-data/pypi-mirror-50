"""some standard constants used with an uppercut system"""
class EnvVars(object):
    """commonly used env variable names"""
    SHARED_VAR_HOST = "SHARED_VAR_HOST" # the env var used to store the host name of the service that manages variables shared between modules.
    # some friendlier constant names.
    SharedVariableServer = SHARED_VAR_HOST
    ModuleRegistrationServer = SHARED_VAR_HOST

class Keys(object):
    """commonly used key names"""
    UPPERCUT_SYS = "UPPERCUT_SYS" 
    MOD_LIST = "MOD_LIST"
