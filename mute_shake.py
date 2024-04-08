# import time
import os

# input = DigitalInputDevice(4)
# last_shake = time.time()
# muted = False

# while True:
#     if input.value:
#         if time.time() - last_shake > 3:
#             last_shake = time.time()
#             print("Mute!")

os.system("amixer set Master toggle")
