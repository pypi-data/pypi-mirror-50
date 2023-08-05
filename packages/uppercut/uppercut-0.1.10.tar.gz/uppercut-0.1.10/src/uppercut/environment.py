import os

def getVar(name,default=None,tp = str):
    """
    Convenience function to get env variable or default value is the var doesn't exist
    """
    return os.environ.get(name,default)
