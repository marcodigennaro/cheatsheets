MONGODB cheatsheet
==================

# make sure to use conda mongodb

$: which mongod 
> /home/mdi0316/miniconda3/envs/kubas/bin/mongod

$: mongod --version
> db version v4.0.3
> git version: 7ea530946fa7880364d88c8d8b6026bbc9ffa48c
> OpenSSL version: OpenSSL 1.1.1q  5 Jul 2022
> allocator: tcmalloc
> modules: none
> build environment:
>     distarch: x86_64
>     target_arch: x86_64

# check running processes 
ps -edaf | grep mongo 


######################
### ON WORKSTATION ###
######################

# Starting and configuring the database

0) Set in /etc/mongod.conf

>> # Where to store the data.
>> dbpath=/home/mdi0316/mongodb
>> 
>> #where to log
>> logpath=/home/mdi0316/mongodb/mongodb.log
>> 
>> bind_ip = 127.0.0.1,10.100.192.47
>> port = 27017
>> 
>> auth = true

1) Starting mongod without any admin/password:
mongod --port 27018 --dbpath ~/fireworks_data/db/ 

2) Connect to the database:
mongo  --port 27018

3) Setup admin user and password in the mongo shell:
use admin
db.createUser({ user:"mdi0316", pwd:"rhew3621KRHE", roles:[ {role:"root", db:"admin"}, 
                                                            {role:"dbOwner", db:"admin"}
                                                      ]})
#authsource : 'admin' in my_launchpad.yaml 

4) create kubas db and initiate with something 
use kubas
mydict = { "name": "Marco", "age": "36" }
db.test.insert(mydict)

5) stop db in 1) and 2)

6) Starting mongod as a daemon (fork)
mongod --port 27018 --dbpath ~/fireworks_data/db/ --logpath ~/fireworks_data/log/fireworks.log --fork --bind_ip_all --auth

7) Now, admin can connect using:
mongo --port 27018 -u "mdi0316" -p 'rhew3621KRHE' --authenticationDatabase "admin"

#
#7) In the same mongo shell
## create user and password for the database:
##use kubas
##db.createUser( { user : 'mdi0316', pwd : 'rhew3621KRHE', roles: [ {role:"dbOwner", db:"kubas"}, {role:"readWrite",db:"kubas"} ] } )
##db.grantRolesToUser( 'mdi0316' , ['readWrite'] )

##################
### ON CLUSTER ###
##################

8) Connect from another server (AT cluster) - default port 
mongo --port 27018 -u "mdi0316" -p 'rhew3621KRHE' --authenticationDatabase "admin" --host 10.100.192.47

8.0) if not on opened port - activate tunnel on terminal 1
ssh -N -L 27018:localhost:27018 mdi0316@10.100.192.47

9) for slurm submissions - open the tunnel nodeXYZ -> masternode. Outside of the network 10.100.192.1 could not work
ssh -N -L 27018:localhost:27018 mdi0316@bezavrdat-master01
