# import required files for code

from motor import Motor
from machine import Pin, ADC
from time import sleep
from ultrasonic import sonic

# Initialize motors

motor_right = Motor("right", 9, 8, 6)
motor_left = Motor("left", 11, 10, 7)
motor_left.set_forwards()
motor_right.set_forwards()

# Pin locations for the three ultrasonic sensors
TRIG = 3
ECHO = 2
ultrasonic_sensor_front = sonic(TRIG, ECHO)
ultrasonic_sensor_right = sonic(12, 13)
ultrasonic_sensor_left = sonic(4, 5)

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

    # Read the Ultrasonic sensor values
    dist_F = ultrasonic_sensor_front.distance_mm()
    dist_R = ultrasonic_sensor_right.distance_mm()
    dist_L = ultrasonic_sensor_left.distance_mm()

    numerator = w0 * x0 + w1 * x1 + w2 * x2
    denominator = w0 + w1 + w2
    extra = 0
    line_dist = (numerator / denominator) - 0.05  # Centre Calibration
    if 0 < dist_F < 70:
        # stop function begin
        motor_right.duty(0)
        motor_left.duty(0)
        sleep(2)
        # stop function end

    elif 0 < dist_L < 180 and 0 < dist_R < 180 and w0 < 2800 and w1 < 10000 and w2 < 2800:
        # wall following begin
        Kp = 0.01  # Proportional constant value
        wall_error = min(dist_L - dist_R, 40)
        steer = Kp * wall_error
        if steer > 0:
            speed_L = int(0)  # Adjust as needed
            speed_R = int(60 + steer)  # Adjust as needed
        else:
            speed_L = int(60 - steer)  # Adjust as needed
            speed_R = int(0)  # Adjust as needed
        motor_right.duty(speed_R)
        motor_left.duty(speed_L)
        sleep(0.03)
        motor_right.duty(0)
        motor_left.duty(0)
        sleep(0.003)
        # wall following end
    else:
        # line following begin
        if w2 > 2800:  # left sensor sees line
            speed_L = 0
            speed_R = 80
            extra = 0.02
            dire = "R"
        elif w0 < 2800 and w1 < 10000 and w2 < 2800:  # no sensors see line
            if dire == "L":  # Method to turn back towards the line that was lost
                speed_L = 75
                speed_R = 0
            elif dire == "R":
                speed_L = 0
                speed_R = 75
            else:
                speed_L = 57
                speed_R = 48
        elif w0 > 3000 and w2 < 2800:  # right sensor sees line and left sensor does not
            speed_L = 75
            speed_R = 0
            extra = 0.015
            dire = "L"
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
        # line following end
        motor_right.duty(speed_R)
        motor_left.duty(speed_L)
        sleep(0.06 + extra)
        motor_right.duty(0)
        motor_left.duty(0)
        sleep(0.07)
