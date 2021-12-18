from winreg import *

systemsOptions = {}


def setRegValue(path, key, value):
    try:
        aKey = OpenKey(HKEY_LOCAL_MACHINE, path, 0,  KEY_ALL_ACCESS)
        print(path,key,value)
        SetValueEx(aKey, key, 0, REG_DWORD, value)
    except:
        return
    finally:
        CloseKey(aKey)

def enforceRules(dictSystemsOptions):
    for key, value in dictSystemsOptions.items():
        if len(value) == 3:
            setRegValue(value[0], key, value[2])

def rollback():
    for key, value in systemsOptions.items():
        if len(value) == 3:
            setRegValue(value[0], key, value[1])

def saveSystemsOptions(keys):
    global systemsOptions
    systemsOptions = keys
    enforceRules(systemsOptions)
