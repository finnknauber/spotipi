from gpiozero import DigitalInputDevice
import time

def mute_on_shake():
    input = DigitalInputDevice(4)
    last_shake = time.time()
    print("Mute on shake")

    while True:
        if input.value:
            print("Mute!")
            if time.time() - last_shake > 3:
                pass
