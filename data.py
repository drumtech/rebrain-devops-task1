import requests
import psutil
import os
import socket
import datetime
import logging
import time

logging.basicConfig(filename=f'{time.strftime("%d%m%Y")}.log', format='%(asctime)s %(levelname)s %(message)s', datefmt='%b %d %H:%M:%S', level=logging.INFO)
logging.info(f'Programm was started')
name = socket.gethostname()
some = os.environ['HOME']

try:
    outside_api = requests.get('https://api.my-ip.io/ip')
    outside_api.raise_for_status()
    ip = outside_api.text
    inside_api = requests.get('http://127.0.0.1:8000/admin/')
    inside_api.raise_for_status()
    list_ip = []
    for i in requests.get('http://127.0.0.1:8000/api/servers/').json():
        list_ip.append(i['ip_address'])
    if ip in list_ip:
        logging.info(f'This node is already on our server')
    else:
        requests.post('http://127.0.0.1:8000/api/servers/add', data={"ip_address": ip, "description": some, "name": name, "server_is_active": 'true'})
        logging.info(f'Server registration was successfully')
except requests.exceptions.ConnectionError:
    logging.error(f'Our api-server is unavailable, touch your DevOps')
    print('Our api-server is unavailable, touch your DevOps')
    exit()
except requests.HTTPError:
    logging.error(f'The resource which give your outside IP address is unavailable, maybe you should use vpn')
    print('The resource which give your outside IP address is unavailable, maybe you should use vpn')
    exit()
except requests.exceptions.RequestException as err:
    logging.error(str(err))
    print('Some troubles with our network, see it in log file')
    exit()


def byte_to_mbyte(a):
    return round(((a / 1024) / 1024), 2)


mem_tot = byte_to_mbyte(psutil.virtual_memory().total)
mem_use = byte_to_mbyte(psutil.virtual_memory().used)
mem_per = round(((mem_tot - (byte_to_mbyte(psutil.virtual_memory().available))) / mem_tot * 100), 2)


disk = []
for el1 in psutil.disk_partitions():
    tmp_dict = {}
    tmp_dict['disk'] = el1.device
    tmp_dict['mountpoint'] = el1.mountpoint
    tmp_dict['file_system_type'] = el1.fstype
    tmp_dict['total'] = byte_to_mbyte(psutil.disk_usage(el1.mountpoint).total)
    tmp_dict['used'] = byte_to_mbyte(psutil.disk_usage(el1.mountpoint).used)
    disk.append(tmp_dict)


net_1 = []
for el1 in sorted(psutil.net_if_stats().items()):
    tmp_dict = {}
    if el1[1].isup == True:
        tmp_dict[el1[0]] = 'up'
    else:
        tmp_dict[el1[0]] = 'down'
    tmp_dict['mtu'] = el1[1].mtu
    net_1.append(tmp_dict)


net_2 = []
for el1 in sorted(psutil.net_if_addrs().items()):
    tmp_dict = {}
    tmp_dict['IP_address'] = el1[1][0].address
    net_2.append(tmp_dict)


net = []
for el1, el2 in zip(net_2, net_1):
    el2.update(el1)
    net.append(el2)


speca = {'host_information': {'username': os.getlogin() , 'sysname': os.uname().sysname, 'hostname': os.uname().nodename, 'boot_time': datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%H:%M:%S %d-%m-%Y")},
          'network': net,
          'disk': disk,
          'memory': {'memory_total': mem_tot, 'memory_used': mem_use, 'memory_percent': mem_per},
          'cpu': {'cpu_cores': psutil.cpu_count(logical=False), 'cpu_physical_cores': psutil.cpu_count(), 'cpu_freqency': psutil.cpu_freq().max},
          'load_average': {'1 min': psutil.getloadavg()[0], '5 min': psutil.getloadavg()[1], '15 min': psutil.getloadavg()[2]}
          }


if psutil.sensors_battery() != None:
    laptop_only = {'battery_charge_percentage': psutil.sensors_battery().percent,
                    'AC_power': psutil.sensors_battery().power_plugged}
    speca.update(laptop_only)


def check_add_info(url):
    k = requests.get(url).json()
    data = {"host_information": speca['host_information'], "network": speca['network'], "disk": speca['disk'], "memory": speca['memory'], 'cpu': speca['cpu'], 'load_average': speca['load_average'], 'battery_charge_percentage': speca['battery_charge_percentage'], 'AC_power': speca['AC_power']}
    if len(k) == 0:
        requests.post(f'{url}add', json=data)
        logging.info(f'Received data about this device --> {speca}')
    list_hostname = []
    for el in k:
        list_hostname.append(el['host_information']['hostname'])
        if el['host_information']['hostname'] == name:
            pk = el['id']
            requests.put(f'http://127.0.0.1:8000/api/additional_information/{pk}', json=data)
            logging.info(f'Received data about this device were updated and now it is --> {speca}')
    if el['host_information']['hostname'] != name and name not in list_hostname:
        requests.post('http://127.0.0.1:8000/api/additional_information/add', json=data)
        logging.info(f'Received data about this device --> {speca}')

def check_server_availability(url):
    try:
        url_get = requests.get(url)
        url_get.raise_for_status()
        logging.info(f'Resource {url} is ready')
    except requests.exceptions.RequestException as err:
        logging.error(str(err))
        print(f'Some troubles with {url}')
        exit()

try:
    while True:
        check_server_availability('http://127.0.0.1:8000/api/additional_information/')
        check_server_availability('https://api.my-ip.io/ip')
        check_add_info('http://127.0.0.1:8000/api/additional_information/')
        time.sleep(60)
except KeyboardInterrupt:
    logging.info('\n######################################################The program was interrupted by user!#########################################################################')
