import sys
from subprocess import call

import RPi.GPIO as GPIO # import our GPIO module

from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QGridLayout, QLabel


DEBUG = True #if set to true, wont actually shutdown, will close.

IGN_PIN = 12		# our 12V switched pin is BCM12
EN_POWER_PIN = 25	# our latch pin is BCM25

IGN_LOW_TIME = 10  # time (s) before a shutdown is initiated after power loss
FIVE_MINUTES = 5 *3600 * 1000 #five mins in ms

GPIO.setup(IGN_PIN, GPIO.IN) # set our 12V switched pin as an input
GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH) # set our latch as an output
GPIO.output(EN_POWER_PIN, 1) # latch our power. We are now in charge of switching power off

class ShutDownApp(QWidget):

    def __init__(self):
        super().__init__()


        GPIO.add_event_detect(IGN_PIN, GPIO.FALLING, callback=self.ignitionToLow, bouncetime=200)
        GPIO.add_event_detect(IGN_PIN, GPIO.RISING, callback=self.ignitionToHigh, bouncetime=200)
        
        self.finalCountdown= IGN_LOW_TIME
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)

        self.mainTimer=QTimer()
        self.mainTimer.timeout.connect(self.startCountdownTimer)
        self.countDownTimer=QTimer()
        self.countDownTimer.timeout.connect(self.updateCountdown)
        self.label=QLabel('')
        self.addFiveBtn=QPushButton('Gimme 5 mins')

        layout=QGridLayout()
        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.addFiveBtn,1,0)

        self.addFiveBtn.clicked.connect(self.addFive)

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
        self.finalCountdown -= 1
        self.label.setText(f'{self.finalCountdown}s to shutdown')
        if self.finalCountdown == 0:
            self.shutDown()

    def addFive(self):
        self.resetCountdownTimer()
        self.startMainTimer(t = FIVE_MINUTES)
        

    def resetCountdownTimer(self):
        self.countDownTimer.stop()
        self.finalCountdown= IGN_LOW_TIME

    def startMainTimer(self, t = IGN_LOW_TIME ):
        self.mainTimer.start(IGN_LOW_TIME)

    def ignitionToLow(self):
        self.startMainTimer()
        self.resetCountdownTimer()

    def ignitionToHigh(self):
        """
        resets everything
        """ 
        self.mainTimer.stop()
        self.resetCountdownTimer()

        self.hide()

    def shutDown(self):
        if DEBUG:
            print("System was told to shutdown. But we are in DEBUG mode, so we exited")
            sys.exit()

        print("Shutting Down")
        call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down


app = QApplication(sys.argv)
my_app = ShutDownApp()
app.exec_()


