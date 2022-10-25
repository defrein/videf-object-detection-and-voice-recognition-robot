# IMPORT ALL LIBRARIES

# ignore warning from gpiozero
import warnings
warnings.simplefilter('ignore')

# - for voice recognition
import speech_recognition as sr
import playsound
from gtts import gTTS
import random
import os
import mute_alsa

# - for object(color) detection
from color_interval import *
import cv2
import imutils
from imutils.video import WebcamVideoStream

# - for processing
from _thread import *

# - for drive robot
import time
from motor import *

# - for button and led
import time
from button_led_sensor import *




# FUNCTIONS


def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True


def record_audio(ask=False):
    on_led(ledYellow, 1)
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        if ask:
            speak(ask)
        audio = r.listen(source, phrase_time_limit=5)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio, language="id-ID")
        except sr.UnknownValueError:
            on_led(ledRed, 1)
        except sr.RequestError:
            speak('Maaf, layanan tidak tersedia saat ini')
        return voice_data.lower()


def speak(audio_string):
    tts = gTTS(text=audio_string, lang='id')
    r = random.randint(1, 1000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    # print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if there_exists(["cari bola", "tari bola", "lari bola", "dari bola"]):
        on_led(ledGreen, 1)
        color_text = voice_data[10:len(voice_data)]
        return color_text
    elif there_exists(["bola"]):
        on_led(ledGreen, 1)
        color_text = voice_data[5:len(voice_data)]
        return color_text
    else:
        on_led(ledRed, 1)
        color_text = ''
        return color_text


def drive():
    global cx, cy, flag, lock, found, count, notfound, threadStop
    while not threadStop:
        if flag == 1 and lock:
            if cx > 400 and cy > 180 and cy < 300:
                motorRight(30)
                time.sleep(0.015)
            elif cx < 240 and cy > 180 and cy < 300:
                motorLeft(30)
                time.sleep(0.015)
            elif cy > 300:
                speed = (cy * 100 / 240) - 100
                motorBackward(int(speed))
                time.sleep(0.015)
            elif cy < 180:
                speed = (cy * 100 / (-240)) + 100
                motorForward(int(speed))
                time.sleep(0.015)
            else:
                motorStop()
                found = True
                threadStop = True
                # jarak = calculateDistance()
                # print("jarak: ", jarak)
                # if jarak < 30:
                #     motorStop()
                #     found = True
        else:
            while flag == 0 and count <= 2000:
                motorLeft(30)
                count = count + 0.001
                if count >= 2000 and found == False:
                    motorStop()
                    notfound = True
                    threadStop = True


def resetState():
    global threadStop, found, notfound,lower_color, upper_color, color_text, flag, lock, device
    motorStop()
    threadStop = True
    found = False
    notfound = False
    lower_color = None
    upper_color = None
    color_text = ''
    flag = 0
    lock = False
    device.stop()
    device = None
    # GPIO.cleanup()


# initialize for voice recognition
r = sr.Recognizer()
voice_data = ''
color_text = ''
# global found, notfound
speak("Videf")
time.sleep(1)
while True:
    found = False
    notfound = False
    lower = None
    upper = None
    if button.is_pressed:
        voice_data = record_audio()
        color_text = respond(voice_data)
        # print(voice_data)
        if len(color_text) > 0:
            lower, upper = whichColor(color_text)
            # print(lower)
            # print(upper)
            global cx, cy, flag, lock, threadStop
            threadStop = False
            lock = False
            flag = 0
            if lower is not None and upper is not None:
                lower_color = lower
                upper_color = upper
                device = WebcamVideoStream(src=0).start()
                start_new_thread(drive, ())
                count = 0
                while True:
                    frame = device.read()
                    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
                    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

                    mask = cv2.inRange(hsv, lower_color, upper_color)
                    mask = cv2.erode(mask, None, iterations=2)
                    mask = cv2.dilate(mask, None, iterations=2)

                    cnts = cv2.findContours(
                        mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    if len(cnts) > 0:
                        c = max(cnts, key=cv2.contourArea)
                        ((x, y), radius) = cv2.minEnclosingCircle(c)
                        x, y, w, h = cv2.boundingRect(c)
                        M = cv2.moments(c)
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        center = (cx, cy)

                        if radius > 10:
                            flag = 1
                            lock = True

                    else:
                        flag = 0

                    # if flag == 1:
                    #     lock = True

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        threadStop = True
                        GPIO.cleanup()
                        break

                    if found:
                        speak("Saya menemukan bola " + color_text)
                        resetState()
                        break

                    if notfound and flag == 0:
                        speak("Saya tidak menemukan bola " + color_text)
                        resetState()
                        break
            else:
                on_led(ledRed, 1)
        else:
            on_led(ledRed, 1)
