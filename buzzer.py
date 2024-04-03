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

#   // play error sound
#   tone(buzzer, 350, 100);
#   delay(200);
#   tone(buzzer, 350, 400);
#   delay(500);

#   // play notification sound
#   tone(buzzer, 3000, 250);
#   delay(300);
#   tone(buzzer, 2250, 100);
#   delay(125);
#   tone(buzzer, 2250, 100);

#   // play cancel sound
#   tone(buzzer, 500, 250);
#   delay(300);
#   tone(buzzer, 300, 150);

def play_success():
    play_tone(2000, 0.25)
    time.sleep(0.3)
    play_tone(2200, 0.15)
    GPIO.output(18, GPIO.LOW)
    GPIO.cleanup()

# when starting up
    # playsetup
    # playstartup

# when connecting to wifi
    # playsuccess
    # playerror

# when writing to tag or reading
    # playsong
    # wrotesong

play_success()

