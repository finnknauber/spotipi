import RPi.GPIO as GPIO
import time

def play_tone(frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2.0
    cycles = int(duration / period)

    while cycles > 0:
        GPIO.output(18, GPIO.HIGH)
        time.sleep(half_period)
        GPIO.output(18, GPIO.LOW)
        time.sleep(half_period)
        cycles -= 1


def play_startup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(2000, 0.2)
    time.sleep(0.125)
    play_tone(2500, 0.3)
    time.sleep(0.2)
    play_tone(3000, 0.3)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(2000, 0.2)
    time.sleep(0.125)
    play_tone(2500, 0.3)
    time.sleep(0.2)
    play_tone(2000, 0.3)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_success():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(1900, 0.25)
    time.sleep(0.02)
    play_tone(2500, 0.25)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_error():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(350, 0.1)
    time.sleep(0.1)
    play_tone(350, 0.4)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_song():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(7500, 0.05)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_wroteSong():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    play_tone(3000, 0.25)
    time.sleep(0.3)
    play_tone(2250, 0.1)
    time.sleep(0.125)
    play_tone(2250, 0.1)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

