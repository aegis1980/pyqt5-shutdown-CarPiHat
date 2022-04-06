from re import S
import RPi.GPIO as GPIO # import our GPIO module
import time
from subprocess import call

from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QGridLayout, QLabel
import sys


IGN_PIN = 12		# our 12V switched pin is BCM12
EN_POWER_PIN = 25	# our latch pin is BCM25

IGN_LOW_TIME = 10 * 1900 # time (ms) before a shutdown is initiated after power loss
FIVE_MINUTES = 5 *3600 * 1000 #five mins in ms

GPIO.setup(IGN_PIN, GPIO.IN) # set our 12V switched pin as an input
GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH) # set our latch as an output
GPIO.output(EN_POWER_PIN, 1) # latch our power. We are now in charge of switching power off

class MyApp(QWidget):

    def __init__(self):
        super().__init__()


        GPIO.add_event_detect(IGN_PIN, GPIO.FALLING, callback=self.ignitionToLow, bouncetime=200)
        GPIO.add_event_detect(IGN_PIN, GPIO.RISING, callback=self.ignitionToHigh, bouncetime=200)
        

        self.setWindowTitle('QTimer example')
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.X11BypassWindowManagerHint)

        self.mainTimer=QTimer()
        self.mainTimer.timeout.connect(self.shutDown)
        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)
        self.label=QLabel('Label')
        self.startBtn=QPushButton('Turn off now')
        self.addFive=QPushButton('Add 5mins')

        layout=QGridLayout()
        layout.addWidget(self.label,0,0,1,2)
        layout.addWidget(self.startBtn,1,0)
        layout.addWidget(self.endBtn,1,1)

        self.startBtn.clicked.connect(self.startTimer)
        self.addFive.clicked.connect(self.addFive)


        self.setLayout(layout)

        
    def show(self):
        super().show()
        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def showTime(self):
        time=QDateTime.currentDateTime()
        timeDisplay=time.toString('yyyy-MM-dd hh:mm:ss dddd')
        self.label.setText(timeDisplay)
    
    def startTimer(self):
        self.timer.start(1000)
        self.startBtn.setEnabled(False)
        self.endBtn.setEnabled(True)

    def addFive(self):
        self.startMainTimer(FIVE_MINUTES)
        

    def mainTimer(self, t = IGN_LOW_TIME ):
        self.mainTimer.stop()
        self.mainTimer.start(IGN_LOW_TIME)

    def ignitionToLow(self):
        self.mainTimer.start(IGN_LOW_TIME*1000)
        self.timerStartTime = time.time()
        
        pass

    def ignitionToHigh(self):
        self.mainTimer.stop()
        self.timer.stop()
        self.hide()

    def shutDown(self):
        print("Shutting Down")
        call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down


app = QApplication(sys.argv)
my_app = MyApp()
app.exec_()



ignLowCounter = 0

while 1:
	if GPIO.input(IGN_PIN) != 1: 				# if our 12V switched is not disabled
		time.sleep(1)							# wait a second
		ignLowCounter += 1						# increment our counter
		if ignLowCounter > IGN_LOW_TIME:		# if it has been switched off for >10s
			print("Shutting Down")
			call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down
	else:
		ignLowCounter = 0 						# reset our counter, 12V switched is HIGH again

