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

#####
# Starts, stops or removes a container based on 'action' parameter
#####
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
        color = 'cyan' if action=='start' else 'yellow'
        print termcolor.colored('{} container {}'.format(status,id), color)


#####
# Gets configuration info and status of a given container
#####
def get_info(url,id):

    endpoint = '/containers/{}/json'.format(id)
    rest_point = url + endpoint

    r = requests.get(rest_point)

    ports = r.json()['NetworkSettings']['Ports']
    portlist = []
    if r.json()['State']['Status'] == 'running':
        for k,v in ports.iteritems():
            portlist.append('{}: {}'.format(k.split('/')[0],v[0]['HostPort']))

    data = [r.json()['Name'].replace('/',''),r.json()['State']['Status'],r.json()['NetworkSettings']['IPAddress'],'\n'.join(portlist),r.json()['Config']['Image']]

    return data

def do_operations(conf):

    container_operations(conf['url'],conf['action'],conf['id'])