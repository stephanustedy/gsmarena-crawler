__author__ = 'Natan Elia'

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'util')))

import Util;

def createIndexMap():
    indexMap = []
    indexMap.append('name_24')
    indexMap.append('description')
    indexMap.append('release_date')
    indexMap.append('general_brand')
    indexMap.append('general_release-date')
    indexMap.append('general_network')
    indexMap.append('general_style')
    indexMap.append('general_colors')
    indexMap.append('size_length')
    indexMap.append('size_width')
    indexMap.append('size_thickness')
    indexMap.append('size_weight')
    indexMap.append('display_type')
    indexMap.append('display_size')
    indexMap.append('display_colors')
    indexMap.append('memory_internal')
    indexMap.append('memory_external')
    indexMap.append('data_gprs')
    indexMap.append('data_edge')
    indexMap.append('data_3g')
    indexMap.append('data_wifi')
    indexMap.append('data_bluetooth')
    indexMap.append('camera_main')
    indexMap.append('camera_front')
    indexMap.append('features_operating-system')
    indexMap.append('features_cpu')
    indexMap.append('features_messaging')
    indexMap.append('features_radio')
    indexMap.append('features_browser')
    indexMap.append('features_games')
    indexMap.append('features_gps')
    indexMap.append('features_java')
    indexMap.append('features_tv')
    indexMap.append('identifier')
    indexMap.append('picture')
    indexMap.append('action')
    return indexMap

def getGeneralNetwork(networkData):
    twog = Util.returnEmptyIfNone(networkData, '2G bands') if (Util.returnEmptyIfNone(networkData, '2G bands') != '') else ''
    threeg = Util.returnEmptyIfNone(networkData, '3G bands') + '\n' if (Util.returnEmptyIfNone(networkData, '3G bands') != '') else ''
    fourg = Util.returnEmptyIfNone(networkData, '4G bands') + '\n' if (Util.returnEmptyIfNone(networkData, '4G bands') != '') else ''
    return fourg + threeg + twog

def getYes(data):
    return 'v' if (data != '' and data != 'No' and data != 'N/A') else ''

def processPhoneJSON(mainMap, dataMap):
    phoneMap = {}

    phoneMap['name_24'] = Util.returnEmptyIfNone(mainMap, 'device_name')
    description = Util.returnEmptyIfNone(mainMap, 'canonical_name')
    phoneMap['description'] = description if type(description) == str else Util.returnEmptyIfNone(description, 'text')
    phoneMap['release_date'] = Util.getCurrentDate()
    phoneMap['general_brand'] = Util.returnEmptyIfNone(mainMap, 'device_name').split(' ')[0]
    phoneMap['general_release-date'] = Util.returnEmptyIfNone(dataMap, 'Launch', 'Announced')
    phoneMap['general_network'] = getGeneralNetwork(dataMap['Network'])
    phoneMap['general_style'] = ''
    phoneMap['general_colors'] = Util.returnEmptyIfNone(dataMap, 'Misc', 'Colors')

    (height, width, thickness) = Util.getSize(Util.returnEmptyIfNone(dataMap, 'Body', 'Dimensions'))
    phoneMap['size_length'] = height
    phoneMap['size_width'] = width
    phoneMap['size_thickness'] = thickness
    phoneMap['size_weight'] = Util.removeInsideParentheses(Util.returnEmptyIfNone(dataMap, 'Body', 'Weight'))

    displayType = Util.returnEmptyIfNone(dataMap, 'Display', 'Type')
    if ', ' in displayType:
        displayTypeSplit = displayType.split(', ')
        phoneMap['display_type'] = displayTypeSplit[0]
        phoneMap['display_colors'] = displayTypeSplit[1]
    else:
        phoneMap['display_type'] = displayType
        phoneMap['display_colors'] = ''

    displayResolution = Util.returnEmptyIfNone(dataMap, 'Display', 'Resolution')
    displayResolution = Util.removeInsideParentheses(displayResolution)
    displaySize = Util.returnEmptyIfNone(dataMap, 'Display', 'Size')
    phoneMap['display_size'] = displayResolution + ', ' + displaySize
    phoneMap['memory_internal'] = Util.returnEmptyIfNone(dataMap, 'Memory', 'Internal')
    phoneMap['memory_external'] = '' if (Util.returnEmptyIfNone(dataMap, 'Memory', 'Card slot') == 'No') else Util.returnEmptyIfNone(dataMap, 'Memory', 'Card slot')
    phoneMap['data_gprs'] = getYes(Util.returnEmptyIfNone(dataMap, 'Network', 'GPRS'))
    phoneMap['data_edge'] = getYes(Util.returnEmptyIfNone(dataMap, 'Network', 'EDGE'))
    phoneMap['data_3g'] = getYes(Util.returnEmptyIfNone(dataMap, 'Network', '3G bands'))
    phoneMap['data_wifi'] = getYes(Util.returnEmptyIfNone(dataMap, 'Comms', 'WLAN'))
    phoneMap['data_bluetooth'] = getYes(Util.returnEmptyIfNone(dataMap, 'Comms', 'Bluetooth'))
    phoneMap['camera_main'] = Util.returnEmptyIfNone(dataMap, 'Camera', 'Primary').replace('\u00d1\u2026','x')
    phoneMap['camera_front'] = getYes(Util.returnEmptyIfNone(dataMap, 'Camera', 'Secondary'))
    phoneMap['features_operating-system'] = Util.returnEmptyIfNone(dataMap, 'Platform', 'OS')
    phoneMap['features_cpu'] = Util.returnEmptyIfNone(dataMap, 'Platform', 'CPU')
    phoneMap['features_messaging'] = Util.returnEmptyIfNone(dataMap, 'Features', 'Messaging')
    phoneMap['features_radio'] = getYes(Util.returnEmptyIfNone(dataMap, 'Comms', 'Radio'))
    phoneMap['features_browser'] = getYes(Util.returnEmptyIfNone(dataMap, 'Features', 'Browser'))
    phoneMap['features_games'] = getYes(Util.returnEmptyIfNone(dataMap, 'Features', 'Games'))
    phoneMap['features_gps'] = getYes(Util.returnEmptyIfNone(dataMap, 'Comms', 'GPS'))
    phoneMap['features_java'] = getYes(Util.returnEmptyIfNone(dataMap, 'Features', 'Java'))
    phoneMap['features_tv'] = getYes(Util.returnEmptyIfNone(dataMap, 'Features', 'TV'))
    phoneMap['identifier'] = ''
    phoneMap['picture'] = ''
    phoneMap['action'] = ''

    return phoneMap


def mapToCSV(jsons, indexMap, filename):
    f = open(filename, 'w')
    f.write('"' + '","'.join(indexMap) + '"\n')
    for (jsonData) in jsons:
        phoneMap = processPhoneJSON(jsonData['main'], jsonData['data'])
        f.write(Util.mapToCSVLine(indexMap, phoneMap) + '\n')
    f.close()
