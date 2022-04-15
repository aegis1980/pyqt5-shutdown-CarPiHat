#!/usr/bin/python
'''
PyQt5 app that overlays *everything* to give a countdown on shutdown and
a button to delay it. 

author: Jon Robinson (c)2022
licence: MIT 
'''
import sys
from subprocess import call

import RPi.GPIO as GPIO # import our GPIO module

from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QGridLayout, QLabel

# if set to true, wont actually shutdown, will close.
# this is the default unless you pass 'live' as an arg when you run.
DEBUG = True 

IGN_PIN = 12		# our 12V switched pin is BCM12
EN_POWER_PIN = 25	# our latch pin is BCM25

ON_SCREEN_COUNTDOWN = 10  # 10 secs. 
SNOOZE_TIME_MINS = 1 #1 mins in ms
SNOOZE_TIME_MS = int((5/60 if DEBUG else SNOOZE_TIME_MINS)* 60 * 1000)

COUNTDOWN_STYLING ="""
    QLabel {
        color : black;
        font : 24px;
    }
"""

SNOOZE_BTN_STYLING ="""
    QPushButton {
        background-color: #2B5DD1;
        color: #FFFFFF;
        border-style: outset;
        padding: 3px;
        font: 24px;
        border-width: 5px;
        border-radius: 10px;
        border-color: #2752B8;
    }
    QPushButton:hover {
        background-color: #4a75d9;
    }
    QPushButton:pressed {
        background-color: #1e56d9;
        border-style: inset;
    }
"""

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(IGN_PIN, GPIO.IN) # set our 12V switched pin as an input
GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH) # set our latch as an output
GPIO.output(EN_POWER_PIN, 1) # latch our power. We are now in charge of switching power off

class Comms(QObject):
    '''
    Help class to deal with threading between GPIO and qt_timers.
    Using Qt signals
    '''

    ignitionChangeSignal = pyqtSignal()

    def ignitionChange(self,channel):
        self.ignitionChangeSignal.emit()


class ShutDownApp(QWidget):

    def __init__(self):
        super().__init__()

        self.uiComms = Comms()
        self.uiComms.ignitionChangeSignal.connect(self.ignitionChange)

        GPIO.add_event_detect(IGN_PIN, GPIO.BOTH, callback=self.uiComms.ignitionChange, bouncetime=200)

        self.screenCountdown = ON_SCREEN_COUNTDOWN
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)

        self.snoozeTimer=QTimer()
        self.snoozeTimer.timeout.connect(self.startCountdownTimer)
        self.countDownTimer=QTimer()
        self.countDownTimer.timeout.connect(self.updateCountdown)
        self.countdownLbl=QLabel('',self)
        self.countdownLbl.setStyleSheet(COUNTDOWN_STYLING)

        self.snoozeBtn=QPushButton(f'Snooze for {SNOOZE_TIME_MINS} mins')
        self.snoozeBtn.clicked.connect(self.snooze)
        self.snoozeBtn.setStyleSheet(SNOOZE_BTN_STYLING)

        layout=QGridLayout()
        layout.addWidget(self.countdownLbl,0,0,1,2)
        layout.addWidget(self.snoozeBtn,1,0)

        self.setLayout(layout)

        
    def show(self):
        super().show()
        self.center()

    def center(self):
        """
        Centres popup on the screen
        """
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def updateCountdown(self):
        self.screenCountdown -= 1
        self.countdownLbl.setText(f'{self.screenCountdown}s to shutdown')
        if self.screenCountdown <= 0:
            self.shutDown()

    def snooze(self):
        if DEBUG:
            print(f"Snoozing for {SNOOZE_TIME_MINS} mins")
        self.hide()
        self.resetCountdownTimer()
        self.startSnoozeTimer()
        

    def resetCountdownTimer(self):
        self.countDownTimer.stop()
        self.screenCountdown= ON_SCREEN_COUNTDOWN
        self.countdownLbl.setText(f'{self.screenCountdown}s to shutdown')

    def startSnoozeTimer(self):
        self.snoozeTimer.start(SNOOZE_TIME_MS)

    def startCountdownTimer(self):
        self.countdownLbl.setText(f'{self.screenCountdown}s to shutdown')
        self.show()
        self.countDownTimer.start(900) # update timer onscreen every < 1 second 

    def ignitionChange(self):
        high = GPIO.input(IGN_PIN) # high is rising

        if DEBUG:
            print(f"ignition change. High: {high}")

        if high:
            # resets everything
            self.snoozeTimer.stop()
            self.resetCountdownTimer()
            self.hide()
        else: # low
            self.snooze()

    def shutDown(self):
        if DEBUG:
            print("System was told to shutdown. But we are in DEBUG mode, so we exited")
            sys.exit()

        print("Shutting Down")
        call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down

if __name__ == '__main__':
    if sys.argv and 'live' in sys.argv:
        DEBUG = False # default is 'not live' which does not shut down Pi. Need to pass 'live' as arg at start
    app = QApplication(sys.argv)
    my_app = ShutDownApp()
    sys.exit(app.exec_())


