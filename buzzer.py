import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)


def play_tone(frequency, duration):
    period = 1.0 / frequency
    half_period = period / 2.0
    cycles = int(duration / period)
    
    for _ in range(cycles):
        GPIO.output(18, GPIO.HIGH)
        time.sleep(half_period)
        GPIO.output(18, GPIO.LOW)
        time.sleep(half_period)


play_tone(500, 500)
time.sleep(1)
play_tone(1000, 500)
GPIO.output(18, GPIO.LOW)
GPIO.cleanup()

