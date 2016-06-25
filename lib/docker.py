import subprocess
import pip
import importlib
import json
import containers
packages=['requests','termcolor','time','texttable']
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


def build(conf):

    # request endpoint and url
    url = conf['url']
    endpoint = '/build?t=' + conf['image_name']
    rest_point = url + endpoint

    print termcolor.colored('Building image "{}" from directory "{}"... \n\t(This might take a while)'.format(conf['image_name'],conf['directory']), 'blue')

    # file to post in request
    tar = 'tar cvf application.tar -C {} .'.format(conf['directory'])
    subprocess.Popen(tar.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)

    time.sleep(1)
    # request data
    headers = {"Content-Type": "application/x-tar"}
    data = open('application.tar', 'rb').read()

    r = requests.post(rest_point, data=data, headers=headers)

    #print type(r.status_code())
    if r.status_code == 200:
        print termcolor.colored('Image built successfully!', 'green')

    create_containers(conf)



def create_containers(conf):

    print termcolor.colored('Creating "{}" containers from image "{}"... '.format(conf['num_instances'],conf['image_name']), 'blue')

    # request endpoint and url
    url = conf['url']
    endpoint = '/containers/create'
    rest_point = url + endpoint

    headers = {"Content-Type": "application/json"}
    with open(conf['container_spec']) as data_file:
        data = json.load(data_file)

    data['Image'] = conf['image_name']

    print termcolor.colored('Created {} containers!'.format(conf['num_instances']), 'green')

    ids =[]
    container_data = []
    container_data.append(['ID','Name','Status','Ports','Image'])

    for i in range(1, int(conf['num_instances'])+1):

        r = requests.post(rest_point, headers=headers, data=json.dumps(data))

        containers.container_operations(url,'start',r.json()['Id'])
        time.sleep(0.5)

        container_data.append(containers.get_info(url,r.json()['Id']))

    t = texttable.Texttable()
    t.add_rows(container_data)
    print t.draw()


def list(conf):
    pass

def cleanup(conf):
    pass

def cleanup_prompt():
    pass

def get_images(conf):
    pass

def get_containers(conf):
    pass
