from mfrc522 import ExtendedMFRC522
import RPi.GPIO as GPIO
import urllib.parse


def writeTag(text):
    text = urllib.parse.quote(text)
    print(text)
    if text:
        print("Place thingy on majig")
        reader = ExtendedMFRC522(sections=10)

        try:
            reader.write(text)
        finally:
            GPIO.cleanup()
        print("Written")