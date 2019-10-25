import RPi.GPIO as GPIO

class LampTrigger:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
    
    def getStatus(self):
        return GPIO.input(self.pin)

    def getStringResponse(self):    
        return 'GPIO {} status: {}'.format(str(self.pin), 'high' if self.getStatus() else 'low')
    
    def on(self):
        GPIO.output(self.pin, False)
    
    def off(self):
        GPIO.output(self.pin, True)
    
    def toggle(self):
        GPIO.output(self.pin, not self.getStatus())