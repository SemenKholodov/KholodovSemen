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
    number = 0
    for value in range (0, 8):
        if number>= 0:
            GPIO.output(dac, decimal2binary(number))
        else:
            GPIO.output(dac, decimal2binary(0))   
            return 0
        sleep(0.0005)
        if GPIO.input(comp) == 0:
            number -= 2**(7-value)
        else:
            number += 2**(7-value)  

    return number                                          
            
     
    # signal = decimal2binary(value)
    # GPIO.output(dac, signal)
    # return signal

try:
    while True:
        voltage = (adc()/256)*3.3
        sleep(0.0) 
        print(f'Bits: {adc()}, Input voltage {round(voltage, 3)}')

finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)                    
    GPIO.cleanup()

