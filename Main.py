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
    def move(side):                     # drive function start
        if side == 'l':  # l
            motor_right.duty(68)
            motor_left.duty(0)
            sleep(0.1)
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
        if side == 'r':  # r
            motor_right.duty(0)
            motor_left.duty(68)
            sleep(0.1)
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
        if side == "L":
            motor_left.set_backwards()
            motor_right.duty(60)
            motor_left.duty(60)
            sleep(0.25)
            motor_left.set_forwards()
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
        if side == "R":
            motor_right.set_backwards()
            motor_right.duty(60)
            motor_left.duty(60)
            sleep(0.1)
            motor_right.set_forwards()
            motor_right.duty(0)
            motor_left.duty(0)
            sleep(0.01)
                                                 # drive function end
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
    if distL < 150 and distR < 150:            #Hallway function start
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
        sleep(0.02)                          # Hallway function end
    else:                                    # Line following function start
        if w0 > 2800:     # Calibrated values for what each sensor interprets as a black line
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
            move("l")  # make a small left turn
        else:
            if ls:
                move("L")  # make a sharp left turn 

            elif ls and rs:
                move("L")
                move("L")
                move("L")   # Make sure to turn left
            elif rs:
                if not cs:
                    move("R")  # make a sharp right turn
                else:
                    move("l")  # make a small left turn (only makes the sharp right turn when middle sensor doesnt see line)
            else:
                move("r")  # make a small right turn
        sleep(0.04)
        
                # pseudo code for potential idea if needed
                # line in postion 0 centre until a R or L sensor detects
                # position is updated to -1 or 1
                # this remains until another sensor spots the line and updates the position
                # position data is used to update control over sensor data
                # maybe reset whenever 0 is reached somehow and rely on sensor data for pos0 and pos data for -1/1

