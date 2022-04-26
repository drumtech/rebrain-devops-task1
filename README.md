#Common info about application
This application is for simple monitoring your devices like: **servers**, *laptop*, **home _PC_**, but not for ~~smartphone~~

## More details
Our application has two part - server part and clien part.

######***Server part***

It is a simple API server based on django[^1], it can take base information and additional information from your devices with helps from client part

*Based information which it processes:*
1. ID
2. Outside IP address
3. Description
4. Hostname
5. Is server active?(True/False)

*Additional information which it processes:*
1. ID
2. Host information
   - Username
   - Sysname
   - Hostname
   - Boot time
3. Environment(a lot of information it depends of you :yum:)
4. Network (all of yours interfaces)
   - Name of interface
   - MTU
   - Inside IP address
5. Memory
   - Memory total volume
   - Memory used volume
   - Percent of memory 
6. Disk drivers (all of yours):
   - Device
   - Mountpoint
   - File system type
   - Total volume
   - Used volume
7. CPU
   - Count of cpu cores
   - Count of threads
   - CPU freqency(max value)
8. Load average
   - 1 min
   - 5 min
   - 15 min

######***Client part***

It is just a python script, which i've tested while only on Linux based OS, for use it you need python... I think 3.8 version and upper

*Information which sand our script*

**Once every 60 seconds it sends data to the server**
~~If you look up you'll see everything it's sending :smile:~~

* Checks for base info
  - Available of [outside server](https://api.my-ip.io/ip)
  - Available of [inside server](http://127.0.0.1:8000/api/servers/)
  - The presence of such a record

* Checks for additional info
  - Available of [outside server](https://api.my-ip.io/ip) before of sending data
  - Available of [inside server](http://127.0.0.1:8000/api/additional_information/) before of sending data

* > And some checks for script works 






[^1] And of course it is my final project from mini practices about Python by Rebrain :kissing_heart:
