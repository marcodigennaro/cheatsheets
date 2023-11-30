#| 0) On WS:
#| check if vnc server is running, get port (below= -rfbport 5903) and server port (below -kill :3)
$ ps -ef | grep vnc
> mdi0316    22480       1  3 11:13 ?        00:00:58 /opt/TurboVNC/bin/Xvnc :3 -desktop TurboVNC: tme022:3 (mdi0316) -auth /home/mdi0316/.Xauthority -geometry 1240x900 -depth 24 -rfbauth /home/mdi0316/.vnc/passwd -x509cert /home/mdi0316/.vnc/x509_cert.pem -x509key /home/mdi0316/.vnc/x509_private.pem -rfbport 5903 -fp /usr/share/fonts/X11/misc,/usr/share/fonts/X11/Type1 -deferupdate 1 -dridir /usr/lib/x86_64-linux-gnu/dri -registrydir /usr/lib/xorg
> mdi0316    22490       1  0 11:13 ?        00:00:00 sh -c (/opt/TurboVNC/bin/xstartup.turbovnc; /opt/TurboVNC/bin/vncserver -kill :3) >> '/home/mdi0316/.vnc/tme022:3.log' 2>&1 &


#| 1) On WS: kill the previous instance if necessasry
$ /opt/TurboVNC/bin/vncserver -kill :3

#| 2) On WS: start new vncserver
$ vncserver

#| 3) On WS: start chnge password
vncpasswd
gdvv-343 #
vsww-372 #view-only

#| 4) On MBP: start tunnel
$ ssh mdi0316@10.100.192.47 -L 5903:localhost:5903


#| 5) On MBP can connect throug TurboVNC:

Go > Connect to server
     add connection
     vnc://10.100.192.100:3

#| 6) On WS desktop, run command (glxgears or ovito) with and withouth vglrun  (frames per seconds)
