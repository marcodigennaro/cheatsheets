Change password from master01

1) Connect:
   ssh -i ~/.ssh/id_ed25519 mdi0316@10.100.192.1

2) Change password:
   smbpasswd

Mount from WS:
1) sudo -i
2) mount -t cifs -o user=mdi0316,vers=1.0 //10.100.192.1/data /data
