import threading
import time

import RPi.GPIO as GPIO #WirePI

# How many time the state of the PIR stays ON even if the PIR reports no more
# motion
AFTER_MOTION_DURATION = 60

# See https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
GPIO_MODE = GPIO.BOARD # GPIO.BCM

OFF = False
ON = True
PIR_STATE_TO_STR = { ON: 'ON', OFF: 'OFF', None: 'Unknown' }

class PIRState:
    def __init__(self, GPIO_pir):
        """ Get the state of the PIR.

        The GPIO_pir is the GPIO number of the board connected to the PIR Motion sensor
        """
        self.state = None
        self.last_time = time.time()
        self.execute = True
        self.GPIO_pir = GPIO_pir

        #GPIO Pin Setup
        GPIO.setmode(GPIO_MODE)
        GPIO.setup(GPIO_pir, GPIO.IN)

        self.thread = threading.Thread(target=self.run, args=())
        self.thread.daemon = True
        self.thread.start()

    def run(self):
        while self.execute:
            pir = GPIO.input(self.GPIO_pir) == 1

            if pir == ON:
                self.last_time = time.time()

            if self.state == ON and pir == OFF and \
               time.time() - self.last_time < AFTER_MOTION_DURATION:
                continue

            self.state = pir

            # Check every 0.2s after new states
            time.sleep(0.2) 

    def get_pir(self):
        return self.state

    def get_str_pir(self):
        return PIR_STATE_TO_STR[self.state]

    def finish(self):
        self.execute = False
        self.thread.join()
        GPIO.cleanup()

# Tests
if __name__ == '__main__':

    a = PIRState(32) 
    sec = time.time()
    
    # Monitor the states during 1 hour
    while time.time() - sec < 60 * 60 :
        print(a.get_str_pir())
        time.sleep(1)
    
    a.finish()

