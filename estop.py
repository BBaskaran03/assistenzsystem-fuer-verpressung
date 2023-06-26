import sys
import time

import keyboard


def ensure_safty():
    keyboard.is_pressed("a"), keyboard.is_pressed("d"), keyboard.is_pressed("k")

    print("ESTOP active in 3 seconds ...")
    time.sleep(3)
    print("ESTOP active now ...")

    while True:
        # time.sleep(0.5)

        keyboard.is_pressed("a"), keyboard.is_pressed("d"), keyboard.is_pressed("k")

        # your code here
        if keyboard.is_pressed("a") == False:
            print("Key interrupt detected", "a")
            # sys.exit()
            raise Exception("ESTOP Triggered")

        if keyboard.is_pressed("d") == False:
            print("Key interrupt detected", "d")
            # sys.exit()
            raise Exception("ESTOP Triggered")

        if keyboard.is_pressed("k"):
            print("Key interrupt detected", "k")
            # sys.exit()
            raise Exception("ESTOP Triggered")


if __name__ == "__main__":
    time.sleep(2)
    ensure_safty()
