import docker
import appdirs
import os
import win32.servicemanager as servicemanager
import win32api
import win32serviceutil
import win32service
import win32event
import multiprocessing
import struct
from sys import modules
from socketserver import TCPServer, StreamRequestHandler

from win32serviceutil import ServiceFramework


APPNAME = 'ancypwn'
APPAUTHOR = 'Anciety'


TEMP_DIR = appdirs.user_cache_dir(APPNAME, APPAUTHOR)

EXIST_FLAG = os.path.join(TEMP_DIR, 'ancypwn.id')
DAEMON_PID = os.path.join(TEMP_DIR, 'ancypwn.daemon.pid')


class AlreadyRuningException(Exception):
    pass


class NotRunningException(Exception):
    pass


def plugin_module_import(name):
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        prompt = 'plugin {} not found, please install it first.\n'.format(name)
        prompt += 'try follwing:\n\tpip3 install {}'.format(name)
        raise PluginNotFoundError(prompt)


class NotificationHandler(StreamRequestHandler):
    def handle(self):
        length = struct.unpack('<I', bytes_content)[0]
        json_content = self.request.recv(length)
        content = json.loads(json_content)
        terminal = content['terminal']
        command = '''ancypwn attach
{}'''.format(content['exec'])
        realname = 'ancypwn_terminal_{}'.format(terminal)
        mod = plugin_module_import(realname)
        mod.run(command)


class ServerProcess(multiprocessing.Process):

    def __init__(self, port, *args, **kwargs):
        super(ServerProcess, self).__init__(*args, **kwargs)
        self.port = port

    def run(self):
        self.server = TCPServer(('', self.port), NotificationHandler)
        self.server.serve_forever()


class TerminalService(ServiceFramework):
    """
    The service waiting for incoming messages and start terminal when required
    """

    _svc_name = 'AncypwnTerminalService'
    _svc_display_name = 'Ancypwn Terminal Service'
    _svc_description = 'Ancypwn supporting terminal service, to support new terminal wake up'
    
    def __init__(self, port):
        super().__init__(self, [self._svc_name])
        self.wait_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.wait_event)

    def SvcDoRun(self):
        self.timeout = 120000
        self.tcp_server = ServerProcess(port)
        self.tcp_server.start()

        while True:
            res = win32event.WaitForSingleObject(self.wait_event, self.timeout)
            if res == win32event.WAIT_OBJECT_0:
                self.tcp_server.terminate()
                break


installed = False
def _start_service():
    """starts service of waiting for opening new terminals
    """
    win32serviceutil.StartService(TerminalService._svc_name, machine=platform.node())

def _end_service():
    """ends the terminal service
    """
    win32serviceutil.StopService(TerminalService._svc_name, machine=platform.node())


def _figure_volumes(directory):
    """figures out the volumes to be binded

    Example:
        D:\\x -> /mnt/d/x
    """
    directory = os.path.expanduser(directory)
    directory = directory.replace(":\\", '\\')
    directory = directory.replace('\\', '/')
    return '/mnt/{}'.format(directory[0].lower()) + directory[1:]


def _attach_interactive(url, name):
    cmd = 'powershell.exe -Command "docker -H {} -it {} bash"'.format(url, name)
    os.system(cmd)


def _run_container(url, image_name, volumes, privileged):
    """does run the container
    """
    client = docker.DockerClient(base_url=url)
    container = client.containers
    running = container.run(
            image_name,
            '/bin/bash',
            cap_add=['SYS_ADMIN', 'SYS_PTRACE'],
            detach=True,
            tty=True,
            volumes=volumes,
            privileged=privileged,
            network_mode='host',
            remove=True,
            )

    with open(EXIST_FLAG, 'w') as flag:
        flag.write(running.name)

    _attach_interactive(url, running.name)


def _read_container_name():
    if not os.path.exists(EXIST_FLAG):
        raise NotRunningException('Ancypwn is not running yet')

    container_name = None
    with open(EXIST_FLAG, 'r') as f:
        container_name = f.read()
    if not container_name:
        os.remove(EXIST_FLAG)
        raise Exception('incorrect status')
    return container_name


def run(config=None, directory=None, image_name=None, priv=None):
    directory = os.path.abspath(directory) 
    if not os.path.exists(directory):
        raise IOError('direcotry to bind not exist')

    if os.path.exists(EXIST_FLAG):
        raise AlreadyRuningException('ancypwn is already running, you should either end it or attach to it')


    _start_service()
    volumes = _figure_volumes(directory)
    try:
        _run_container(config['backend']['url'], image_name, volumes, priv)
    except Exception as e:
        _end_service()
        raise e


def attach(config):
    container_name = _read_container_name()
    conts = container.list(filters={'name': container_name})
    if len(conts) != 1:
        raise Exception('multiple images of name {} found, unable to execute'.format(image_name))

    _attach_interactive(url, conts[0].name)


def end(config):
    container = _read_container_name()
    conts = container.list(filters={'name': container_name})
    if len(conts) < 1:
        os.remove(EXIST_FLAG)
        raise NotRunningException('not running')

    conts[0].stop()
    os.remove(EXIST_FLAG)
    _end_service()


