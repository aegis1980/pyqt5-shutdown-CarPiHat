# Shutdown app for (OpenAuto Pro +) CarPiHat

**Work in progress. Don't blame me if you run down your car battery**

This is dialog overlay for delayed shutdown of in-car system using RPi and CarPiHat. 
* When ignition goes off, it'll for **2 minutes** (by default), then;
* Popup a dialog onscreen with a second-by-second countdown from **20 seconds** (by default)
* If user does not press the snooze button, RPi will nicely shut down on zero. Hitting **snooze** will dismiss the dialog for another 2 minutes (by default).

I have OpenAuto Pro running, but this Qt app is entirely independent of OpenAuto Pro. 

![Snapshot of dialog over OAP](/snapshot.png)

Refer to [CarPiHat wiki](https://github.com/gecko242/CarPiHat/wiki/Quick-Start-Guide#:~:text=SCL%3A%20BCM3-,Safe%20Shutdown%20Example,-%3A) for more info on the CarPiHat's latched powerdown function. A simple Python script in included in CarPiHat wiki which safely shuts down RPi 10 seconds after ignition (IGN) has gone LOW.


## Set up
### 1. Clone this repo
Easiest to clone out in `/home/pi`
```
git clone https://github.com/aegis1980/pyqt5_shutdown_CarPiHat.git
```
### 2. Install PyQt5
I found this to be easiest using `apt-get`, rather than using `pip3`.
```
sudo apt-get update
sudo apt-get install python3-pyqt5
```
### 3. Start script on startup
In the CarPiHat wiki the python script is set running from `rc.local`, prior to RPi Ui (and OpenAuto Pro starting). 

Different here - we want to run the script after UI has started. Add the following at the end of `/etc/xdg/lxsession/LXDE-pi/autostart`:

```
python3 /home/pi/pyqt5_shutdownapp_CarPiHat/qt_shutdown.py live &
```
**NOTE:** If you don't pass `live` argument the deault is not go into [debug mode](#debug-mode). 

To edit autostart:
```
sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
```


### 4. GPIO setup
There is some setup of pins too (refer to CarPiHat wiki for more info). Add the following to `/boot/config.txt`
```
dtoverlay=gpio-poweroff,gpiopin=25,active_low
```
To edit `config.txt`:
```
sudo nano /boot/config.txt
```

## Configuration

* You can change the snooze time (`SNOOZE_TIME_MINS` in **minutes**) and the on screen countdown time (`ON_SCREEN_COUNTDOWN` in **seconds**) at the top of the script. The defaults are 2 minutes and 10 seconds respectively.
* Included is some css-type styling for the snooze button and countdown. Not that experienced with Qt - guess you can make it look however you please. 
* Default UI sizing is for the official RPi touchscreen, which is (only) 800x480 (`UI_SCALE=1`). Use `UI_SCALE` to scale up for higher resolutions (e.g. Full HD, 1980x1080: `UI_SCALE=2.5`). Default is x2.5 (for full HD)

## Debug mode

Running without `live` argument runs in debug mode:
* Does not shut-down pi when countdown runs out. Just closes app.
* Snooze time set to 5 seconds
* Logging.