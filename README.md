# Common info about application
This application is for simple monitoring your devices like: **servers**, *laptop*, **home _PC_**, but not for ~~smartphone~~

## More details
Our application has two part - server part and clien part.

###### ***Server part***

It is a simple API server based on django[^1], it take base information and additional information from your devices with helps from client part

*Based information which it processes:*
1. ID
2. Outside IP address
3. Description
4. Hostname
5. Is server active?(True/False)

*Additional information which it processes:*

| Parameter                         | Includes                                                         |
| --------------------------------- | ---------------------------------------------------------------- |
| ID                                | ID in database                                                   |
| Host information                  | Username, sysname, hostname, boot time                           |
| Environment                       | A lot of information it depends of you :yum:                     |
| Network (all of yours interfaces) | Name of interface, MTU, private IP address                       |
| Memory                            | Memory total volume, memory used volume, percent of memory       |
| Disk drivers (all of yours)       | Device, mountpoint, file system type, total volume, used volume  |
| CPU                               | Count of CPU cores, count of threads, CPU freqency(max value)    |
| Load average                      | 1 min, 5 min, 15 min                                             |


###### ***Client part***

It is just a python [script](data.py), which i've tested while only on Linux based OS, for use it you need [python](https://www.python.org/downloads/)... I think 3.8 version and upper 

*Information which send our [script](data.py)*

**Once every 60 seconds it sends data to the server**
~~If you look up you'll see everything it's sending :smile:~~

* Checks for base info
  - Available of [public server](https://api.my-ip.io/ip)
  - Available of [private server](http://127.0.0.1:8000/api/servers/)
  - The presence of such a record

* Checks for additional info
  - Available of [public server](https://api.my-ip.io/ip) before of sending data
  - Available of [private server](http://127.0.0.1:8000/api/additional_information/) before of sending data

> ~~And some checks for [script](data.py) works like this~~

```
def check_server_availability(url):
     try:
         url_get = requests.get(url)
         url_get.raise_for_status()
         logging.info(f'Resource {url} is ready')
     except requests.exceptions.RequestException as err:
         logging.error(str(err))
         print(f'Some troubles with {url}')
         exit()
```

## Task Lists
- [x] Exit from programm if catch exceptions
- [ ] Transfer server part to public
- [ ] Maybe someone else checks
- [ ] Test on Windows OS systems
- [ ] Test on Mac OS systems
- [x] Make coffee and relax
![Keep calm and learn Linux](https://cdn.pixabay.com/photo/2013/07/13/13/34/linux-161108_1280.png)
[^1]: And of course it is my final project from mini practices about Python by [Rebrain](https://rebrainme.com/) :kissing_heart:
