from gpiozero import DigitalInputDevice
import time

def mute_on_shake():
    input = DigitalInputDevice(4)
    last_shake = time.time()

    while True:
        if input.value:
            if time.time() - last_shake > 3:
                print("Mute!")
