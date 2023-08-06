import atexit
import signal
import sys
import time


def handle():
    time.sleep(2)
    print("exit now")

atexit.register(handle)
signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(1))

if __name__ == "__main__":
    for i in range(100000000):
        print(i)
        time.sleep(1)
