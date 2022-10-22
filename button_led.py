# from signal import pause
from gpiozero import LED, Button
import time

button = Button(12)
ledGreen = LED(13)
ledYellow = LED(26)
ledRed = LED(19)


def on_led(ledColor, on_time):
    ledColor.on()
    time.sleep(on_time)
    ledColor.off()
