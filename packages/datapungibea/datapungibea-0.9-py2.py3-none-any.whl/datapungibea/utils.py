'''
datapungibea.utils
~~~~~~~~~~~~~~~~~~

This module provides utility functions that are used 
within datapungibea and by the users when they want 
to update internal configs.
'''

import json
import pkg_resources

def getConnectionParameters(connectionParameters = {}, userSettings = {}):  
    '''
      :param userSettings: (optional) dictionary of  ``'ApiKeysPath': a path to json with API Keys`` and  ``'ApiKeyLabel': label (key) of JSON entry containing the key``
      If userSettings is an empty dictionary (default option), method will try to load it from saved userSettings.  

      output, a dictionary with user key and datasource url
    '''

    if not connectionParameters == {}:
        return(connectionParameters)

    if userSettings == {}:
        userSettings = getUserSettings()

    try:
        with open(userSettings['ApiKeysPath']) as jsonFile:
             connectionParameters = (json.load(jsonFile))[userSettings['ApiKeyLabel']]
        return(connectionParameters)
    except:
        print('Could not find dictionary key ' + userSettings['ApiKeyLabel'] + ' in \n '+ userSettings['ApiKeysPath'])
        return   

def getResourcePath(relativePath, resource_package = __name__):
    '''
     Given relative, get its full path
     eg: relative path: /config/userSettings.json
     will return
     datapungibea path + relative path
     note: can replace resource_package with package name:
     eg: 'datapungibea'
    '''
    fullPath = pkg_resources.resource_filename(resource_package, relativePath)
    return(fullPath)

def getUserSettings(userSettings = {}):
    '''
        loads the userSettings file.
    '''
    if not userSettings == {}:
        return(userSettings)

    userSettingsPath = getResourcePath('/config/userSettings.json','datapungibea') #TODO: remove package name.
    try:
        with open(userSettingsPath) as jsonFile:
             userSettings = json.load(jsonFile)
        return(userSettings)
    except:
        print('.utils.py: Could not open the userSettings: \n ./config/userSettings.json \n returning empty dictionary')
        return({})


def setUserSettings(newPath):  #TODO: check if still valid
    '''
       sets the api key path in the package config file. 
       eg:
       import datapungibea as dpb
       dpb.utils.setUserSettings('myPath')
    '''
    userSettingsPath = getResourcePath('/config/userSettings.json')
    try:
        with open(userSettingsPath) as jsonFile:
             config = json.load(jsonFile)
    except:
        print('Could not open the configuration file: \n datapungi/config/userSettings.json')
        pass
    
    config['ApiKeysPath'] = newPath

    try:
        with open(userSettingsPath,'w') as jsonFile:
            json.dump(config,jsonFile)
        print('Path to the API Keys updated! New Path: \n' + config['ApiKeysPath'])
    except:
        print('Could not save the configuration to file: \n datapungibea/config/userSettings.json \n Path API Key not updated')
        pass

def setTestFolder(newTestsPath):
    userSettingsPath = getResourcePath('/config/userSettings.json')
    try:
        with open(userSettingsPath) as jsonFile:
             config = json.load(jsonFile)
    except:
        print('Could not open the configuration file: \n datapungi/config/userSettings.json')
        pass
    
    config['TestsOutputPath'] = newTestsPath

    try:
        with open(userSettingsPath,'w') as jsonFile:
            json.dump(config,jsonFile)
        print('Path to the Tests Output Folder updated! New Path: \n' + config['TestsOutputPath'])
    except:
        print('Could not save the configuration to file: \n datapungibea/config/userSettings.json \n Path to the Tests Output not updated')
        pass            

if __name__ == '__main__':
    setTestFolder('U:/Tests')