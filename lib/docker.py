import subprocess
import pip
import importlib
packages=['requests','termcolor','time']
for package in packages:
    try:
        importlib.import_module(package)
        print 'Imported {}'.format(package)
    except ImportError:
        import pip
        pip.main(['install', package])
        print 'Installed {}'.format(package)
    finally:
        globals()[package] = importlib.import_module(package)


def build(conf):

    # request endpoint and url
    url = conf['url']
    endpoint = '/build?t=' + conf['image_name']
    rest_point = url + endpoint

    print termcolor.colored('\tBuilding image "{}" from directory "{}"... \n\t\tThis might take a second'.format(conf['image_name'],conf['directory']), 'green')

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
        print termcolor.colored('\tImage built successfully!', 'green')

def create_containers(conf):
    pass

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
