# Shutdown app for (OpenAuto Pro +) CarPiHat

**Work in progress. Don't blame me if you raun down your battery**

This is dialog overlay for delayed shutdown of in-car system using RPi and CarPiHat. I have OpenAuto Pro running, but this Qt app is entirely independent of OAP. 

Refer to docs for CarPiHet for more info on this PCB's latched powerdown function. [simple_shutdown.py](simple_shutdown.py) is the script provided in the CarPiHat wiki which safely shuts down RPi 10 seconds are ignition (IGN) has gone LOW (typ 12V).


## Some set up
1. Install PyQt5 from bash:
```
sudo apt-get update
sudo apt-get install python3-pyqt5
```
2. There is some setup of pins and stuff to do - refer to CarPiHat wiki (here)
3. In wiki the python script is set running from `rc.local`, prior to RPi Ui (and OAP starting). Different here - want to run the script after UI has started:

[todo]

## Configuration
[todo]