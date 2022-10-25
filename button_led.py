# from signal import pause
from gpiozero import LED, Button, DistanceSensor
import time

button = Button(12)
ledGreen = LED(13)
ledYellow = LED(26)
ledRed = LED(19)
sensor = DistanceSensor(echo=21, trigger=20)


def on_led(ledColor, on_time):
    ledColor.on()
    time.sleep(on_time)
    ledColor.off()

def calculateDistance():
    objectDis = sensor.distance * 100
    return objectDis

