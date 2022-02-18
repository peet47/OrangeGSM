## Orange GSM
![alt text](https://github.com/peet47/OrangeGSM/blob/main/images/img1.png?raw=true)
Just a small funny project during the holidays.

## App setup

In app.py you have to adjust thw following two values:
```
con_phonenumber = "YOUR_MOBILE_NUMBER"
SIM800L = SIM800L("YOUR_SERIAL_PORT") like "/dev/ttyAMA0"
```

All new sms are added to the database every 60 seconds.

The Python requirements are in requirements.txt

`pip3 install -r requirements.txt`

Y ou can start the app with `python3 app.py`

# Disable serial console
We will start by disabling serial console to enable communication between the pi and sim800l via serial0 .

Open the terminal on your pi and run sudo rasp-config Select Interfaces → Serial Select No to the 1st prompt and Yes for the 2nd.

## OR

# PI SIM800  Board

Free up your serial ports

First we need to edit the /boot/config.txt file

`sudo nano /boot/config.txt`

Add the following lines

```
dtoverlay=pi3-miniuart-bt
enable_uart=1
force_turbo=1
```

Now we need to edit the /boot/cmdline.txt file

sudo nano /boot/cmdline.txt

Remove all references of "console=", for example, if the line reads:

`dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`

Change it to:

`dwc_otg.lpm_enable=0 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait`

Next, we need to edit the /lib/systemd/system/hciuart.service file:

`sudo nano /lib/systemd/system/hciuart.service`

Comment out the After= line (by adding the # symbol at the begining of the line) and add the following on a new line

`After = dev-ttyS0.device`

Comment out the ExecStart= line (by adding the # symbol at the begining of the line) and add the following on a new line

`ExecStart = /usr/lib/hciattach /dev/ttyS0 bcm43xx 460800 noflow -`

 

Update your RPi

Make sure your raspberry pi is fully up to date by running these commands:

```
sudo apt-get update
sudo apt-get upgrade
sudo rpi-update
sudo reboot
```


Credtis:
for the HTML5 template html5up.net | @ajlkn
for the way better implemention of the gsm modul as I did. https://github.com/jakhax/raspberry-pi-sim800l-gsm-module