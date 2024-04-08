from gpiozero import DigitalInputDevice
import time
import os

def mute_on_shake():
    input = DigitalInputDevice(4)
    last_shake = time.time()

    while True:
        if input.value:
            if time.time() - last_shake > 3:
                last_shake = time.time()
                print("Mute!")
                os.system("amixer -D pulse sset Master mute")
