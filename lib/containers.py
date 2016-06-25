import importlib
try:
    importlib.import_module('requests')
except ImportError:
    import pip
    pip.main(['install', 'requests'])
finally:
    globals()['requests'] = importlib.import_module('requests')

def container_operations(url,action,id):

    # request endpoint and url
    endpoint = '/containers/{}/{}'.format(id,action)
    rest_point = url + endpoint

    r = requests.post(rest_point)

def get_info(url,id):

    endpoint = '/containers/{}/json'.format(id)
    rest_point = url + endpoint

    r = requests.get(rest_point)

    data = [r.json()['Id'],r.json()['Name'].replace('/',''),r.json()['State']['Status'],list(r.json()['Config']['ExposedPorts'].keys()),r.json()['Config']['Image']]

    return data
