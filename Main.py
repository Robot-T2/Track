# import required files for code

from motor import Motor
from machine import Pin, ADC
from time import sleep

# Initialize motors

motor_right = Motor("right", 9, 8, 6)
motor_left = Motor("left", 11, 10, 7)
motor_left.set_forwards()
motor_right.set_forwards()


# Distances from the centroid of the robot to the centre of each sensor in mm
x0 = -20
x1 = 0
x2 = 20

# Initialise pins for analog line sensors
adc_A0 = ADC(Pin(26))
adc_A1 = ADC(Pin(27))
adc_A2 = ADC(Pin(28))
dire = 0
while True:
    extra = 0
    # Storing sensor data in w0, w1, w2
    w0 = adc_A0.read_u16()  # R
    w1 = adc_A1.read_u16()  # C
    w2 = adc_A2.read_u16()  # L

    numerator = w0 * x0 + w1 * x1 + w2 * x2
    denominator = w0 + w1 + w2
    extra = 0

    line_dist = (numerator / denominator) - 0.05  # Centre Calibration
    if w2 > 9000:  # left sensor sees line
        speed_L = 0
        speed_R = 80
        extra = 0.045
        dire = "R"
    elif w0 < 9000 and w1 < 10000 and w2 < 9000:  # no sensors see line
        if dire == "L":   # Method to turn back towards the line that was lost
            speed_L = 75
            speed_R = 0
        elif dire == "R":
            speed_L = 0
            speed_R = 75
        else:
            speed_L = 60
            speed_R = 44
    elif w0 > 9000 > w2:   # right sensor sees line and left sensor does not
        speed_L = 75
        speed_R = 0
        extra = 0.04
        dire = "L"  # dont think about it lol idk why it just works
    else:
        Kp = 0.009  # Proportional constant value
        steer_value = Kp * line_dist
        if steer_value > 0:
            speed_L = int(0)  # Adjust as needed
            speed_R = int(60 + steer_value * 50)  # Adjust as needed
        else:
            speed_L = int(60 - steer_value * 50)  # Adjust as needed
            speed_R = int(0)  # Adjust as needed
        if w1 > 10000:  # Centre sensor sees line
            dire = 0

    motor_right.duty(speed_R)
    motor_left.duty(speed_L)
    sleep(0.07 + extra)
    motor_right.duty(0)
    motor_left.duty(0)
    sleep(0.19)

