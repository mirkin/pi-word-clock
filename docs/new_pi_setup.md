
MAC Put OS onto SD card 
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

MAC Setup
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

Now configure

```bash
sudo raspi-config
```

Expand file system to use the full SD
Under advanced set hostname and enable I2C finish and reboot.

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




