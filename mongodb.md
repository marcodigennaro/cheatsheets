MONGODB cheatsheet
==================
### check running processes
```
ps -edaf | grep mongosh

#or #sudo lsof -i | grep mongosh

#or #sudo lsof -iTCP -sTCP:LISTEN -n -P | grep mongosh
```

### kill previous instances

```
sudo kill 12054
```

### make sure to use conda mongodb

$: which mongod
```
 /home/uname/miniconda3/envs/kubas/bin/mongod
```

$: mongod --version
```
> db version v4.0.3
> git version: 7ea530946fa7880364d88c8d8b6026bbc9ffa48c
> OpenSSL version: OpenSSL 1.1.1q  5 Jul 2022
> allocator: tcmalloc
> modules: none
> build environment:
>     distarch: x86_64
>     target_arch: x86_64
```

### make sure mongodb folder exists and is empty
```
rm -r /home/mdi0316/.mongodb/jfremote
mkdir /home/mdi0316/.mongodb/jfremote
mkdir /home/mdi0316/.mongodb/jfremote/db
mkdir /home/mdi0316/.mongodb/jfremote/log
```

ON WORKSTATION
--------------

### Starting and configuring the database

0) Set in /etc/mongod.conf

```
>> # Where to store the data.
>> storage:
>> dbPath=/home/uname/mongodb
>>
>> #where to log
>> systemLog:
>>   path=/home/uname/mongodb/mongodb.log
>>
>> net:
>>   bind_ip = 127.0.0.1,10.100.192.47
>>   port = 27017
>>
>> security:
>>   authorization: enabled
```

```
user = "mdi0316"
pwd = "dhxe-3736-%+=!-WHHF"
port = 27017
dbpath = /home/mdi0316/.mongodb/kubas/db
dblog = /home/mdi0316/.mongodb/kubas/log/mnh.log
```

1) Starting mongod without any admin/password:
```
mongod --port $port --dbpath $dbpath
```

2) Connect to the database:
```
mongosh --port $port
```

3) Setup admin user and password in the mongosh shell:
```
use admin
db.createUser({
    user:"mdi0316",
    pwd:"psw1",
    roles:[ {role:"root", db:"admin"},
            {role:"dbOwner", db:"admin"}]
    })
```

```
db.grantRolesToUser(
    "mdi0316",
    [  { role: "dbOwner", db: "kubas" } ,
       { role: "dbOwner", db: "pgel" } ]
    )
```

4) create kubas db and initiate with something
```
use exemple
my_dict = { "name": "Marco", "age": "36" }
db.ex_collection.insertOne(my_dict)
db.ex_collection.findOne()

>> {
>>    "_id" : ObjectId("64919e6aa09061a14012da20"),
>>     "name" : "Marco",
>>     "age" : "36"
>> }
```

5) stop db in 1) and 2)

6) Starting mongod as a daemon (fork)

```
mongod --port $port --dbpath $dbpath --logpath $logpath --fork --bind_ip_all --auth
```

7) Now, admin can connect using:

```
mongosh --port 27018 -u "mdi0316" -p "GEJR-shfb-6252-*():" --authenticationDatabase "admin"
```

ON CLUSTER
----------

8.0) Connect from another server (AT cluster) - default port

```
$ mongosh --port 27018 -u "uname" -p 'pswd' --authenticationDatabase "admin" --host 10.100.192.47
```

8.1) if not on opened port - activate tunnel on terminal 1

```
$ ssh -N -L 27018:localhost:27018 uname@10.100.192.47
```

9) for slurm submissions - open the tunnel nodeXYZ -> masternode. Outside of the network 10.100.192.1 could not work
```
$ ssh -N -L 27018:localhost:27018 uname@bezavrdat-master01
```
