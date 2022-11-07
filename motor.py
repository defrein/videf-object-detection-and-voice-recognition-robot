import RPi.GPIO as GPIO
import time

# set pin GPIO
ena = 17
enb = 25
in1 = 27
in2 = 22
in3 = 23
in4 = 24
# temp1 = 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(ena, GPIO.OUT)
GPIO.setup(enb, GPIO.OUT)

GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)
p1 = GPIO.PWM(ena, 1000)
p2 = GPIO.PWM(enb, 1000)


p1.start(25)
p2.start(25)

# change speed function from 0 to 100% speed

def changeSpeed(pwm):
    p1.ChangeDutyCycle(pwm)
    p2.ChangeDutyCycle(pwm)


# move robot function
def motorStop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def motorRight(speed):
    changeSpeed(speed)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)


def motorLeft(speed):
    changeSpeed(speed)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)


def motorForward(speed):
    changeSpeed(speed)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)


def motorBackward(speed):
    changeSpeed(speed)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
