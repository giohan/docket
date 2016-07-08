import subprocess
import pip
import importlib
import json
import containers
import monitoring
packages=['requests','termcolor','time','texttable']
for package in packages:
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

#####
# This is where the magic happens. Builds an image based on given parameters and calls create_containers
#####
def build(conf):

    #####
    # If we want to create container from existing image, skip image creation.
    #####
    if conf['container_only']:
        create_containers(conf)
        print termcolor.colored('Fetching metrics... ', 'cyan')
        monitoring.metrics(conf)
        return

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

    print termcolor.colored('Fetching metrics... ', 'cyan')
    monitoring.metrics(conf)


#####
# Creates a number of containers based on user input
#####
def create_containers(conf):

    print termcolor.colored('Creating "{}" new containers from image "{}"... '.format(conf['num_instances'],conf['image_name']), 'blue')

    # request endpoint and url
    url = conf['url']
    endpoint = '/containers/create'
    rest_point = url + endpoint

    headers = {"Content-Type": "application/json"}
    with open(conf['container_spec']) as data_file:
        data = json.load(data_file)

    # If the 'Image' attribute is not provided in the container.spec, use the command line 'image_name' argument's value.
    # If the user gives name via command line, then this overrides the one in container.spec
    if (conf['image_name'] != 'docket/app') or ('Image' not in data) or (data['Image'] == ''):
        data['Image'] = conf['image_name']

    print termcolor.colored('Created {} new containers!'.format(conf['num_instances']), 'green')

    # This is the list to be printed post creation
    container_data = []
    container_data.append(["Name","Status","IP","Ports","Image"])

    for i in range(1, int(conf['num_instances'])+1):

        r = requests.post(rest_point, headers=headers, data=json.dumps(data))

        containers.container_operations(url,'start',r.json()['Id'])
        time.sleep(0.5)

        container_data.append(containers.get_info(url,r.json()['Id']))

    t = texttable.Texttable()
    t.add_rows(container_data)
    print t.draw()


#####
# Prints a list of containers and their configuration and status
#####
def list(conf):

    ids = get_containers(conf)

    container_data = []
    container_data.append(["Name","Status","IP","Ports","Image"])
    for id in ids:
        container_data.append(containers.get_info(conf['url'],id))

    t = texttable.Texttable()
    t.add_rows(container_data)
    print t.draw()


#####
# Returns container names. Only running by default
#####
def get_containers(conf):

    url = conf['url']
    endpoint = '/containers/json'

    if 'all' in conf and conf['all']:
        endpoint = endpoint + '?all=1'
    rest_point = url + endpoint

    r = requests.get(rest_point)

    ids = []
    for cont in r.json():
        ids.append(cont['Names'][0].replace('/',''))

    return ids