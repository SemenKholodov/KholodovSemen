import RPi.GPIO as GPIO
from time import sleep

def decimal2binary(value):
    return [int(x) for x in bin(value)[2:].zfill(8)]


def voltage(value):
    v = (3.3 / 255) * value
    return "{:.2f}".format(v)

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(comp, GPIO.IN)


def adc():
    for value in range(256):
        GPIO.output(dac,decimal2binary(value))
        sleep(0.0005)
        if GPIO.input(comp) == 0:
            return value
            
     
    # signal = decimal2binary(value)
    # GPIO.output(dac, signal)
    # return signal

try:
    while True:
        voltage = (adc()/256)*3.3
        sleep(0.05) 
        print(f'Bits: {adc()}, Input voltage {round(voltage, 3)}')

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)                    
    GPIO.cleanup()

