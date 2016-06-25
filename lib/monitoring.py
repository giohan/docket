import docker
import containers
import importlib
import math
packages=['requests','texttable']
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)



def metrics(conf):

    metric_data = []
    container_ids = docker.get_containers(conf)
    metric_data.append(["Name","CPU %","Mem Usage / Limit","Net I / O"])

    for id in container_ids:
        stats = get_stats(conf['url'],id)

        mem = convertSize(int(stats['memory_stats']['usage'])) + ' / ' + convertSize(int(stats['memory_stats']['limit']))
        net = convertSize(int(stats['networks']['eth0']['rx_bytes'])) + ' / ' + convertSize(int(stats['networks']['eth0']['tx_bytes']))
        cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
        system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
        cpu_utilization = str((cpu_delta / system_delta) * float(len(stats['cpu_stats']['cpu_usage']['percpu_usage'])))

        metric_data.append([id,"{} %".format(cpu_utilization),mem,net])

    t = texttable.Texttable()
    t.add_rows(metric_data)
    print t.draw()


def realtime(conf):
    pass



def do_monitor(conf):

    if not conf['auto_update']:
        metrics(conf)
    else:
        realtime(conf)


def get_stats(url,id):

    endpoint = '/containers/{}/stats?stream=false'.format(id)
    rest_point = url + endpoint

    r = requests.get(rest_point)

    return r.json()


def convertSize(size):
   if (size == 0):
       return '0B'
   size_name = ("B","KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1000,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])

