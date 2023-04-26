SHELL commands
=============

#is firewall active?
sudo ufw status

#is mongod running?
lsof -i | grep mongod

#is port XYZ open?
lsof -nP | grep XYZ


#open tunnel
ssh -N -L 27072:localhost:27072 mdi0316@10.100.192.47

# create folders to mount for cluster connection
mkdir /storage

sudo mkdir /storage

sudo mount 10.100.192.1:/storage /storage

sudo apt install nfs-common 

sudo mount 10.100.192.1:/storage /storage

#cat these 3 lines into /etc/fstab 

#10.100.192.1:/storage /storage nfs rw,relatime,vers=3 0 0

#10.100.192.1:/home    /cluster_homes nfs rw,relatime,vers=3 0 0

#10.100.192.1:/data    /data nfs rw,relatime,vers=3 0 0


#nohup 

#ignores the HUP signal and therefore does not stop when the user logs out.


#check if library is installed

ldconfig -p | grep libjpeg


#check open ports (eg samba)

telnet 10.100.192.47 139

telnet 10.100.192.47 445


/etc/apt/sources.list #contains list of sources for apt-get install/update

