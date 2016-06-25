import importlib
packages=['requests','termcolor']
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

def container_operations(url,action,id):

    if action == 'rm':
        endpoint = '/containers/{}'.format(id)
        rest_point = url + endpoint

        r = requests.delete(rest_point)

        print termcolor.colored('Deleted container {}'.format(id), 'red')
    else:
        endpoint = '/containers/{}/{}'.format(id,action)
        rest_point = url + endpoint

        r = requests.post(rest_point)

        status = 'started' if action=='start' else 'stopped'
        print termcolor.colored('{} container {}'.format(status,id), 'cyan')

def get_info(url,id):

    endpoint = '/containers/{}/json'.format(id)
    rest_point = url + endpoint

    r = requests.get(rest_point)

    data = [r.json()['Name'].replace('/',''),r.json()['State']['Status'],list(r.json()['Config']['ExposedPorts'].keys()),r.json()['Config']['Image']]

    return data

def do_operations(conf):

    container_operations(conf['url'],conf['action'],conf['id'])