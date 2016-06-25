import docker
import containers
import importlib
try:
    importlib.import_module('requests')
except ImportError:
    import pip
    pip.main(['install', 'requests'])
finally:
    globals()['requests'] = importlib.import_module('requests')



def metrics(conf):

    metrics = []
    container_ids = docker.get_containers(conf)

    for id in container_ids:
        stats = get_stats(conf['url'],id)
        print stats

    print container_ids



def realtime(conf):
    pass



def do_monitor(conf):

    if not conf['auto_update']:
        metrics(conf)



def get_stats(url,id):

    # request endpoint and url
    endpoint = '/containers/{}/stats?stream=false'.format(id)
    rest_point = url + endpoint

    r = requests.get(rest_point)

    return r.json()

