import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


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


def play_success():
    play_tone(1900, 0.25)
    time.sleep(0.02)
    play_tone(2500, 0.25)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

def play_error():
    play_tone(350, 0.1)
    time.sleep(0.1)
    play_tone(350, 0.4)

def play_cancel():
    play_tone(500, 0.25)
    time.sleep(0.3)
    play_tone(300, 0.15)

def play_notification():
    play_tone(3000, 0.25)
    time.sleep(0.3)
    play_tone(2250, 0.1)
    time.sleep(0.125)
    play_tone(2250, 0.1)


# when starting up
    # playsetup
    # playstartup

# when connecting to wifi
    # playsuccess
    # playerror

# when writing to tag or reading
    # playsong
    # wrotesong

play_cancel()

