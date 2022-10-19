import RPi.GPIO as GPIO
import time
from time import sleep
from matplotlib import pyplot

leds = [24, 25, 8, 7, 12, 16, 20, 21]
troyka = 17

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17
leds = [24, 25, 8, 7, 12, 16, 20, 21]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(troyka, GPIO.OUT)
GPIO.setup(comp, GPIO.IN) 
GPIO.setup(leds, GPIO.OUT)


def decimal2binary(value):
    return [int(x) for x in bin(value)[2:].zfill(8)] #Перевод числа в двоичную систему



def adc(): 
    a = [0]*8
    for i in range(8):
        a[i] = 1
        GPIO.output(dac,a)
        sleep(0.05)
        compvalue = GPIO.input(comp)
        if compvalue == 0:
            a[i] = 0

    return 128 * a[0] + 64 * a[1] + 32 * a[2] + 16 * a[3] + 8 * a[4] + 4 * a[5] + 2 * a[6] + a[7] 

try:
    measured_value = []
    value = 0
    measurements = 0
    GPIO.output(troyka, 1)
    time_start = time.time() #начало эксперимента

#зарядка конденсатора

    while value < 0.97*256:
        value = adc()
        measured_value.append(value) 
        measurements += 1 #кол-во измерений
        GPIO.output(leds, decimal2binary(value))
        sleep(0.005)
        print(measured_value)

    GPIO.output(troyka, 0)

#разрядка конденсатора

    while value > 256*0.02:
        value = adc()
        measured_value.append(value)
        measurements += 1
        GPIO.output(leds, decimal2binary(value))
        sleep(0.005)
        print(measured_value)

    final_time = time.time() - time_start #время эксперимента
    #перевод значений в строки
    measured_data_str = [str(item) for item in measured_value]

    with open ("data.txt", "w") as outfile:
        outfile.write("\n".join(measured_data_str))
    with open ("setting.txt", "w") as file:
        file.write(str(final_time))
        # file.write(final_time/measurements)
    print('общая продолжительность эксперимента{}, период одного измерения {}, средняя частота дискретизации {}, шаг квантования {}'.format(final_time, final_time/measurements, 1/final_time/measurements))             



#построение графика

    pyplot.plot(measured_value)
    pyplot.show

finally:

    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)                    
    GPIO.cleanup()  


