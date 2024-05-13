from motor import Motor
from machine import Pin, ADC
from time import sleep
from ultrasonic import Sonic

ultrasonic_sensorL = Sonic(4, 5)
ultrasonic_sensorR = Sonic(12, 13)

motor_right = Motor("right", 9, 8, 6)
motor_left = Motor("left", 11, 10, 7)
motor_left.set_forwards()
motor_right.set_forwards()

# Initialise pins for analog line sensors
adc_A0 = ADC(Pin(26))
adc_A1 = ADC(Pin(27))
adc_A2 = ADC(Pin(28))
val = 1
while True:
    def move(side):
        if side == 1:  # l
            motor_right.duty(68)
            motor_left.duty(0)
            sleep(0.1)
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
        if side == -1:  # r
            motor_right.duty(0)
            motor_left.duty(68)
            sleep(0.1)
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
        if side == "L":
            motor_left.set_backwards()
            motor_right.duty(68)
            motor_left.duty(68)
            sleep(0.25)
            motor_left.set_forwards()
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)

        if side == "R":
            motor_right.set_backwards()
            motor_right.duty(68)
            motor_left.duty(68)
            sleep(0.25)
            motor_right.set_forwards()
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)


    # Storing sensor data in w0, w1, w2
    w0 = adc_A0.read_u16()
    w1 = adc_A1.read_u16()
    w2 = adc_A2.read_u16()
    for i in range(5):
        w0 += adc_A0.read_u16()
        w1 += adc_A1.read_u16()
        w2 += adc_A2.read_u16()
        sleep(0.01)
    w0 = w0 / 6
    w1 = w1 / 6
    w2 = w2 / 6
    ultrasonic_sensorL = Sonic(4, 5)
    ultrasonic_sensorR = Sonic(12, 13)
    distL = int(ultrasonic_sensorL.distance_mm())
    distR = int(ultrasonic_sensorR.distance_mm())
    print(distL)
    print(distR)
    if distL < 150 and distR < 150:
        if distR < distL:
            motor_left.duty(55)
            motor_right.duty(70)
            sleep(0.15)
            motor_left.duty(0)
            motor_right.duty(0)
            sleep(0.01)
        elif distR > distL:
            motor_left.duty(70)
            motor_right.duty(55)
            sleep(0.15)
            motor_left.duty(0)
            motor_right.duty(0)
            sleep(0.01)
        else:
            motor_left.duty(60)
            motor_right.duty(60)
        sleep(0.02)
    else:
        if w0 > 2800:
            rs = True
        else:
            rs = False
        if w1 > 10000:
            cs = True
        else:
            cs = False
        if w2 > 2800:
            ls = True
        else:
            ls = False

        if cs:
            move(val)
        else:
            if rs:
                val = -1
                move("R")

            elif ls:
                val = 1
                move("L")

            else:
                move(val * -1)

                # pseudo code
                # line in postion 0 centre until a R or L sensor detects
                # position is updated to -1 or 1
                # this remains until another sensor spots the line and updates the position
                # position data is used to update control over sensor data
                # maybe reset whenever 0 is reached somehow and rely on sensor data for pos0 and pos data for -1/1
