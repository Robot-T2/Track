# import required packages
from motor import Motor
from machine import Pin, ADC
from time import sleep
from ultrasonic import Sonic

# initialise left, right and front facing ultrasonic sensors
ultrasonic_sensorL = Sonic(4, 5)
ultrasonic_sensorR = Sonic(12, 13)
ultrasonic_sensorF = Sonic(3, 2)

# initialise left and right motors and set direction to forwards
motor_right = Motor("right", 9, 8, 6)
motor_left = Motor("left", 11, 10, 7)
motor_right.set_forwards()
motor_left.set_forwards()

# initialise 3 analogue IR sensors
adc_A0 = ADC(Pin(26))
adc_A1 = ADC(Pin(27))
adc_A2 = ADC(Pin(28))


# helper functions

# function to read and return line sensor data
def read_line_sensors():
    readings = [adc_A0.read_u16(), adc_A1.read_u16(), adc_A2.read_u16()]
    for _ in range(5):
        readings[0] += adc_A0.read_u16()
        readings[1] += adc_A1.read_u16()
        readings[2] += adc_A2.read_u16()
        sleep(0.01)
    return [r / 6 for r in readings]


# function to read and return ultrasonic sensor data
def read_ultrasonic_sensors():
    distL = int(ultrasonic_sensorL.distance_mm())
    distR = int(ultrasonic_sensorR.distance_mm())
    distF = int(ultrasonic_sensorF.distance_mm())
    return distL, distR, distF


# move function to achieve the wiggle utilised inside line following method
def move(side):
    if side == 'l':  # Small left turn
        motor_right.duty(68)
        motor_left.duty(0)
    elif side == 'r':  # Small right turn
        motor_right.duty(0)
        motor_left.duty(68)
    elif side == "L":  # Sharp left turn
        motor_left.set_backwards()
        motor_right.duty(60)
        motor_left.duty(60)
        sleep(0.15)
    elif side == "R":  # Sharp right turn
        motor_right.set_backwards()
        motor_right.duty(60)
        motor_left.duty(60)
        sleep(0.05)
    sleep(0.1)
    motor_left.set_forwards()
    motor_right.set_forwards()
    motor_right.duty(0)
    motor_left.duty(0)
    sleep(0.07)


# main line following method
def follow_line(w0, w1, w2):
    rs = w0 > 2800
    cs = w1 > 10000
    ls = w2 > 2800
    if ls:
        move("L")
    elif cs:
        move("l")
    elif rs:
        if not cs:
            move("R")
        else:
            move("l")
    else:
        move("r")


# wall following method
def follow_wall(distanceL, distanceR):
    if distanceR < distanceL:
        motor_left.duty(30)
        motor_right.duty(60)
    elif distanceR > distanceL:
        motor_left.duty(60)
        motor_right.duty(30)
    else:
        motor_left.duty(55)
        motor_right.duty(55)
    sleep(0.1)
    motor_left.duty(0)
    motor_right.duty(0)
    sleep(0.05)


# stop vehicle - to be called when vehicle is valid for parking
def stop_vehicle():
    motor_left.duty(0)
    motor_right.duty(0)
    sleep(2)                        # additional time added here


# Main loop
while True:
    # read all sensors
    w0, w1, w2 = read_line_sensors()
    distL, distR, distF = read_ultrasonic_sensors()

    # main logic
    # if walls detected on L, R, F - vehicle parks
    # if walls detected on only L, R - vehicle follows walls
    # if walls detected on only 1 side or not detected - vehicle follows line

    if distF < 100:
        stop_vehicle()
    elif distL < 150 and distR < 150:
        follow_wall(distL, distR)
    else:
        follow_line(w0, w1, w2)

    # update time
    sleep(0.04)
