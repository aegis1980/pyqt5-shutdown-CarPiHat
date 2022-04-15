# Shutdown app for (OpenAuto Pro +) CarPiHat

**Work in progress. Don't blame me if you raun down your battery**

This is dialog overlay for intended for delayed shutdown of in-car system using RPi and CarPiHat. 

I have OpenAuto Pro  running, but this Qt app is entirely independent of OpenAuto Pro. 

Refer to CarPiHat wiki for more info on this PCB's latched powerdown function. A Python script in included in CarPiHat wiki which safely shuts down RPi 10 seconds are ignition (IGN) has gone LOW (typ 12V).


## Some set up
1. Install PyQt5 from bash:
```
sudo apt-get update
sudo apt-get install python3-pyqt5
```
2. In the CarPiHat wiki the python script is set running from `rc.local`, prior to RPi Ui (and OpenAuto Pro starting). Different here - we want to run the script after UI has started. Add the following at the end of 
```

```


3. There is some setup of pins too (refer to CarPiHat wiki for more info). Add the following to "/boot/config.txt"
```
dtoverlay=gpio-poweroff,gpiopin=25,active_low
```


## Configuration

* You can change the snooze time and on screen countdown time at the top of the script. The defaults are 2 minutes and 10 seconds respectively.
* Included is some css-type styling for the 