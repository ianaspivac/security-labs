import json
from winreg import *
from searchOption import saveOptions


def getRegExist(path):
    try:
        aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, path)
        return True
    except:
        return False
    finally:
        CloseKey(aKey)


def getRegValue(path, customItem):
    try:
        aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        aKey = OpenKey(aReg, path)
        valReg = QueryValueEx(aKey, customItem['item'])
        return valReg[0]
    except:
        return -1
    finally:
        CloseKey(aKey)


def verifyAudit(listKeywords, string):
    resultsValid = []
    resultsInvalid = []
    customItemsVerify = []
    customItems = json.loads(saveOptions(listKeywords, string))
    for key, customItem in customItems.items():
        if customItem[0]['type'] == 'REGISTRY_SETTING':
            path = customItem[0]['reg_key']
            item = customItem[0]['reg_item']
            value = customItem[0]['value_data']
            nullNotAllow = 'CAN_NOT_BE_NULL' == customItem[0]['reg_option']
            customItemsVerify.append(
                {'name': key, 'type': 'REGISTRY_SETTING', 'path': path, 'item': item, 'value': value,
                 'nullNotAllow': nullNotAllow})
        if customItem[0]['type'] == 'REG_CHECK':
            path = customItem[0]['value_data']
            exist = not ('MUST_NOT_EXIST' == customItem[0]['reg_option'])
            customItemsVerify.append({'name': key, 'type': 'REG_CHECK', 'path': path, 'exist': exist})
    for customItem in customItemsVerify:
        path = customItem['path'][5:]
        if customItem['type'] == 'REG_CHECK':
            if customItem['exist'] == getRegExist(path):
                resultsValid.append(customItem['name'] + " is valid.")
            elif customItem['exist']:
                resultsInvalid.append(customItem['name'] + " is invalid, the key should exist.")
            else:
                resultsInvalid.append(customItem['name'] + " is invalid, the key should NOT exist.")
        elif customItem['type'] == 'REGISTRY_SETTING':
            regVal = getRegValue(path, customItem)
            if regVal == -1:
                if customItem['nullNotAllow']:
                    resultsInvalid.append(customItem['name'] + " must have non null value.")
                else:
                    resultsValid.append(customItem['name'] + " is valid.")
            elif regVal == int(customItem['value']):
                resultsValid.append(customItem['name'] + " is valid.")
            else:
                resultsInvalid.append(customItem['name'] + " is invalid, value has to be " + customItem['value'] + ".")
    return '\n'.join(resultsValid), '\n'.join(resultsInvalid), len(resultsValid), len(resultsInvalid)
