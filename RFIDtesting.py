from mfrc522 import ExtendedMFRC522
import RPi.GPIO as GPIO
import time


def writeTag(text):
    if text:
        print("Place tag on reader")
        reader = ExtendedMFRC522(sections=10)
        try:
            reader.write(text)
        finally:
            GPIO.cleanup()
        print("Written")


def readTag():
    reader = ExtendedMFRC522()
    try:
        while True:
            id, text = reader.read_no_block()
            if id:
                print("Read text:", text)
                GPIO.cleanup()
                return
    finally:
        print("cleaning up reader")
        GPIO.cleanup()


if __name__ == "__main__":
    print("Writing text: 'This is a test' to tag")
    writeTag("This is a test")
    time.sleep(3)
    print("Reading text from tag")
    readTag()
    print("Finished")

