from gpiozero import Button
import threading
import time

class FilamentMotionSensorTimeoutDetection(threading.Thread):
    used_pin = -1
    max_not_moving_time = -1
    keepRunning = True

    # Initialize FilamentMotionSensor
    def __init__(self, threadID, threadName, pUsedPin, pMaxNotMovingTime, pLogger, pData, pCallback=None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = threadName
        self.callback = pCallback
        self._logger = pLogger
        self._data = pData

        self.used_pin = pUsedPin
        self.max_not_moving_time = pMaxNotMovingTime
        self._data.last_motion_detected = time.time()
        self.keepRunning = True
        
        btn = Button(self.used_pin)
        btn.when_activated = motion
        btn.when_deactivated = motion
        # GPIO.add_event_detect(self.used_pin, GPIO.BOTH, callback=self.motion)

    # Override run method of threading
    def run(self):
        while self.keepRunning:
            timespan = (time.time() - self._data.last_motion_detected)

            if (timespan > self.max_not_moving_time):
                if(self.callback != None):
                    self.callback()

            time.sleep(0.250)

       # GPIO.remove_event_detect(self.used_pin) # not sure if there is a need to replace it

    # Eventhandler for GPIO filament sensor signal
    # The new state of the GPIO pin is read and determinated.
    # It is checked if motion is detected and printed to the console.
    def motion(self):
        self._data.last_motion_detected = time.time()
        self.callback(True)
        self._logger.debug("Motion detected at " + str(self._data.last_motion_detected))