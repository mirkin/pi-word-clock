
## Table of contents

- [About](#about)
- [MAC Put OS onto SD card](#mac-pu-os-onto-sd-card)
- [MAC Setup](#mac-setup)
- [See Pi Files in Mac Finder](#see-pi-files-in-mac-finder)
- [See Pi Files on PC (Samba)](#see-pi-files-in-windows-explorer)
- [Static IP Setup](#static-ip-setup)
- [Git setup](#git-setup)
- [Wifi Setup ](#wifi-setup )
- [Remove Wolfram](#remove-wolfram)
- [I2C Setup](#i2c-setup)
- [User Management](#user-management)
- [Setup VNC](#setup-vnc)
- [Setup .local domain](#setup-local-domain)
- [Disk Usage](#disk-usage)
- [Pimoroni Unicorn Hat](#pimoroni-unicorn-hat)
- [Run at Startup](#run-at-startup)
- [Create symbolic link](#symbolic-link)
- [Make file executable](#make-python-file-executable)

##About
We have so many Raspberry Pi computers in our household, so we set up a collection of useful information so we can share our knowledge and quicky set up new systems.

##MAC Put OS onto SD card 
=======================

Insert SD card  

```bash
diskutil list

/dev/disk0
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *251.0 GB   disk0
   1:                        EFI EFI                     209.7 MB   disk0s1
   2:                  Apple_HFS Macintosh HD            250.1 GB   disk0s2
   3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3
/dev/disk1
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *4.0 GB     disk1
   1:                 DOS_FAT_32 NO NAME                 4.0 GB     disk1s1
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *39.8 MB    disk2
   1:                  Apple_HFS Garmin Express          39.8 MB    disk2s1
```

Mine is the 4.0 GB and my .img on my system is /Volumes/H/xfer/usefull-apps/RasPi/2014-09-09-wheezy-raspbian.img

```bash
diskutil unmountDisk /dev/disk1
Unmount of all volumes on disk1 was successful


sudo dd bs=1m if=/Volumes/H/xfer/usefull-apps/RasPi/2014-09-09-wheezy-raspbian.img of=/dev/disk1

```

Then wait for a long time CTRL+t will show progress
Took about half an hr. Then plug in the Pi and off you go.

##MAC Setup
=========

I'm going headless so no monitor, keyboard, or mouse. Plugged into network and checked the
DHCP client table in my router to find it's IP which was 192.168.1.107 in my case.

Open a shell and 

```bash
ssh pi@192.168.1.23

The authenticity of host '192.168.1.107 (192.168.1.107)' can't be established.
RSA key fingerprint is 65:3f:76:ff:1d:5c:02:5f:bb:54:ed:35:d8:b8:5a:f8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.107' (RSA) to the list of known hosts.
pi@192.168.1.107's password:
Linux raspberrypi 3.12.28+ #709 PREEMPT Mon Sep 8 15:28:00 BST 2014 armv6l

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.

NOTICE: the software on this Raspberry Pi has not been fully configured. Please run 'sudo raspi-config'
```
If you want to be up to date

```bash
sudo apt-get update
```

Now configure for the first time

```bash
sudo raspi-config
```

Expand file system to use the full SD
Under advanced set hostname and enable I2C finish and reboot.

##Static IP Setup

Now I want to set a static IP address so change the /etc/network/interfaces 

```bash
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

Using nano because no vim yet 
ip I want is 192.168.1.32 and my gateway is 192.168.1.1 my DHCP starts
at 192.168.1.100 so no chance it will lease anything under 100 so 32 is safe.

```bash
auto lo

iface lo inet loopback
#iface eth0 inet dhcp
iface eth0 inet static
address 192.168.1.32
netmask 225.225.225.0
network 192.168.1.0
broadcast 192.168.1.255
gateway 192.168.1.1

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
```

```bash
sudo reboot
```

Can now ssh to 192.168.1.32

##See Pi Files in Mac Finder

I want to be able to browse and edit files on my Mac so
```bash
sudo apt-get install netatalk
```
Now I can log in at pi and use finder and all my favourite editing tools.


##See Pi files in Windows Explorer

Browse and edit files on the PC.

Install Samba

```bash
sudo apt-get install samba samba-common-bin
```

Then edit /etc/samba/smb.conf

```bash
wins support = yes
[pihome]
   comment= Pi Home
   path=/home/pi
   browseable=Yes
   writeable=Yes
   only guest=no
   create mask=0777
   directory mask=0777
   public=no
```

Set up your user and restart the service

```bash
sudo smbpasswd -a pi
sudo service samba restart
sudo 
```

##Git setup
```bash
git config --global user.email "alex@example.com"
git config --global user.name "My name"
```

##Wifi Setup 

Edit /etc/network/interfaces 

```bash
#interfaces to bring up automatically when ifup is run with -a
auto lo eth0 wlan0

#command such as ifup --allow=hotplug eth0 wlan0 will bring up only if listed below
allow-hotplug eth0
allow-hotplug wlan0

#127.0.0.1
iface lo inet loopback

#iface eth0 inet dhcp

#wired lan gets static ip 192.168.1.32
iface eth0 inet static
   address 192.168.1.32
   gateway 192.168.1.1
   netmask 255.255.255.0
   #network 192.168.1.0
   #broadcast 192.168.1.255

#wireless
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface walvin inet static
   address 192.168.1.33
   gateway 192.168.1.1
   netmask 255.255.255.0
   #network 192.168.1.0
   #broadcast 192.168.1.255

iface default inet dhcp
```

Edit /etc/wpa_supplicant/wpa_supplicant.conf
You can set multiple wireless networks and have different id_str for each
to reference in /etc/network/interfaces 
``bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
   ssid="mywirelessssid"
   psk="mypassword"
   key_mgmt=WPA-PSK
   id_str="walvin"
}
```

##Remove Wolfram

Free up disk space by removing almost 500meg of Wolfram
```bash
sudo apt-get purge wolfram-engine
```

##I2C Setup
Get tools and python libs
```bash
sudo apt-get install i2c-tools
sudo apt-get install python-smbus
```

Add i2c-dev to /etc/modules
```bash
# /etc/modules: kernel modules to load at boot time.
#
# This file contains the names of kernel modules that should be loaded
# at boot time, one per line. Lines beginning with "#" are ignored.
# Parameters can be specified after the module name.

snd-bcm2835
i2c-dev
```
If you have this file, it may need editing
```bash
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```
Then comment out (add # to the start) or remove
```bash
#blacklist i2c-bcm2708
```

Then check with sudo i2cdetect -y 1 (Newer models) or sudo i2cdetect -y 0 depending on your model

```bash
sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- 71 -- -- -- -- -- --
```

Any problems, you may need to reboot
```bash
sudo reboot
```

##User Management
Add/Remove a user I'll add and remove alex, the -r is to delete the home folder of alex
```bash
sudo adduser alex
sudo userdel -r alex
```
The user will not be able to sudo, if you want them to be able to then
```bash
sudo visudo
```
and add an entry for them
```bash
#
# This file MUST be edited with the 'visudo' command as root.
#
# Please consider adding local content in /etc/sudoers.d/ instead of
# directly modifying this file.
#
# See the man page for details on how to write a sudoers file.
#
Defaults        env_reset
Defaults        mail_badpass
Defaults        secure_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

# Host alias specification

# User alias specification

# Cmnd alias specification

# User privilege specification
root    ALL=(ALL:ALL) ALL

# Allow members of group sudo to execute any command
%sudo   ALL=(ALL:ALL) ALL

# See sudoers(5) for more information on "#include" directives:

#includedir /etc/sudoers.d
pi ALL=(ALL) NOPASSWD: ALL
alex ALL=(ALL) NOPASSWD: ALL
```

Change your password or another person's
```bash
passwd
sudo passwd alex
```
##Setup VNC 
```bash
sudo apt-get install tightvncserver
```
Wait for install, and press Y enter if it asks for confirmation.
```bash
vncserver :1

You will require a password to access your desktops.

Password:
```
Follow instructions, and then to start it up
```bash
vncserver :0 -geometry 1920x1080 -depth 24
```

##Setup .local domain
Useful if you get a dynamic IP from your DHCP or even if you have a static IP and forget it. netatalk will already have set this up but here is how to do it anyway.
```bash
sudo apt-get install avahi-daemon
```

##Disk Usage
Useful to know what is taking up space if you only use a small 4Gig SD.

```bash
sudo du -sh /*
sudo du -sh /dirname/*
```
The h option shows info in “Human Readable Format“ bytes,k,meg,gig instead of disk blocks. The s option will stop it reporting on subdirectories 

##OpenCV Python
```bash
sudo apt-get install python-opencv
```

If you want to use the camera
```bash
sudo modprobe bcm2835-v4l2
```

##X11 Windows on Mac
Download X11 for Mac open shell and type xhost +
Tick both boxes on Mac preferences under security
SSH user_of_pi@ip_of_pi -X (I didn't need the -X option)
export DISPLAY='ip_of_mac:0.0'

##Pimoroni Unicorn Hat
Only uses 3 pins GPIO 18, +5V and Ground. To match up with the unicorn hat and pi B+ is used jump wires between pins 2(5V),9(Ground),12(GPIO18) to the same on the Hat. So that is the 1st and 6th on one side and 5th on the other.

Software
https://github.com/pimoroni/UnicornHat
\curl -sS get.pimoroni.com/unicornhat | bash

Or

(Python 3)
sudo apt-get install python3-pip python3-dev
sudo pip-3.2 install unicornhat
(Python 2)
sudo apt-get install python-pip python-dev
sudo pip install unicornhat

##Run at startup
Put file in /etc/init.d (for example start-eyes and make sure it's executable chmod +x start-eyes)
sudo update-rc.d start-eyes defaults

You can follow a pattern to make these startup daemons a little cleaner and allow start and stop
here is an example for a python script that makes LED Eyes light up. 

```bash
#!/bin/bash
#/etc/init.d/led-eyes
### BEGIN INIT INFO
# Provides: led-eyes
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: to start led matrix eyes
# Description:       to start led matrix eyes
### END INIT INFO

# Using the lsb functions to perform the operations.
. /lib/lsb/init-functions
# Process name ( For display )
name=`basename $0`
echo "Name -> $name"
pid_file="/var/run/$name.pid"

case "$1" in
    start)
        log_daemon_msg "Starting LED Eyes"
        start-stop-daemon --start --background --pidfile $pid_file --make-pidfile --exec /home/pi/dev/pi-word-clock/python/Eyes.py
        ;;
    stop)
        log_daemon_msg "Stopping LED Eyes"
        start-stop-daemon --stop --pidfile $pid_file
        ;;
    *)
        echo "usage start-eyes start:stop"
        exit 1
        ;;
esac
exit 0
```

If you want to start/stop this deamon from the shell use a symbolic link so it can be found on the PATH
```bash
sudo ln -s /etc/init.d/start-eyes /usr/bin/start-eyes
```

##Symoblic Link

```bash
ln -s target source
```

target is the existing link, source is the new symoblic link

##Make Python File Executable
sudo chmod +x filename.py


##VIM

hjkl to move cursor, ESC normal mode, i insert, A append :q! quit don't save, :wq save and quit
u undo, ctrl r redo, U undo entire line, p inserts text just deleted after cursor, r replace char with next
char to be typed, c change so ce then type will change end of a word c$ change to end of line
ctrl g - line number and col etc.

:! followed by any shell command to execute a command

% will find matchin parentheses

Navigating
gg start, G end, lineNumber then G go to line
crtl b page up ctry f page down

Search
/phrase
search again n opposite dir N
?phrase searches backward

Replace
:s/old/new
:s/old/new/g all on line
:%s/old/new/g whole file
:%s/old/new/gc whole file but with prompts

Copy Paste
v for visual mode, move cursor y to yank (copy) p to paste

Delete
x del char or 8x delete 8
dw delete from cursor to start of next word or d8w
de delete frtom cursor to end of current word e8w
d$ delete from cursor to end of line
dd delete line 8dd delete 8 lines

Motion - move to (AS Above can add number before to repeat X times)
w,e,$(end of line),0(start of line)

