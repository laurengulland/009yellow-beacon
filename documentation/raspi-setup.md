# Raspberry Pi Setup

## Installations
### Software and Packages
This is a running list of things that we've installed. Will be updated as is called for.
```bash
$ sudo apt-get update
$ pip install pyserial
```

### Wifi
Connect to MIT GUEST wifi. There is no password.

You can do this via the GUI or by modifying `/etc/network/interfaces`. However, we didn't do this, so you're on your own for that one (it's super googleable though).

### Setting up SSH
In order to have the option to use the raspi headless (without a monitor/keyboard), we need to configure it to be accessible over SSH.
`$ sudo raspi-config`
First set a password: Navigate to `Change User Password` and hit enter, and follow the password change procedure. You will use this whenever you SSH into the Pi.
Next, select `Advanced Options`, then navigate to `SSH` and enable it.
It's up to you whether you also want to modify `Boot Options` to require your password on startup, but I recommend it.

## Connecting to the Raspberry Pi over SSH
### Finding the IP Address

This is the tricky part. Haven't found a good way to do this headless (without a monitor/keyboard) yet, but hopefully that will happen soon. (Although for the mockup demo we'll have a monitor and keyboard for it anyway, so maybe it won't.)

With a monitor/keyboard, open the terminal and run `$ hostname -I` -- this will give you the IP address. The Pi should automatically connect to MIT GUEST on boot, but if it hasn't found wifi by the time you run this, you should check that out.

### SSH from Linux/OSX

1. Connect to MIT GUEST
2. In your terminal: `$ ssh pi@IPADDRESS`
3. Type password when prompted
4. Use terminal like normal!

### SSH from Windows
See related Adafruit tutorial [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-6-using-ssh/ssh-under-windows).

1. Download and install PuTTY from [here](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html).
2. Connect to MIT GUEST.
3. Run PuTTY.
4. In the PuTTY window (see image below), type the IP Address you're attempting to connect to, and leave all other default settings the same. (See image)
5. Click Yes on the popup (it's asking to save the ssh key, which as long as you're connecting to the right thing is fine - See image below).
6. Enter username and password when prompted.
7. Use linux shell as normal!

First PuTTY window: (step 4)

![Initial PuTTY Window](https://cdn-learn.adafruit.com/assets/assets/000/003/156/original/learn_raspberry_pi_putty_config.png?1396792467)

PuTTY Warning: (step 5)

![PuTTY Warning PopUp](https://cdn-learn.adafruit.com/assets/assets/000/003/157/original/learn_raspberry_pi_putty_warning.png?1396792485)

Example connected PuTTY Window: (step 7)

![Example Connected PuTTY Window](https://cdn-learn.adafruit.com/assets/assets/000/003/158/large1024/learn_raspberry_pi_putty_connected.png?1396792500)
