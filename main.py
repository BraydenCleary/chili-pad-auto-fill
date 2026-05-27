# Chili reservoir auto-fill -- ESP32 + MicroPython
# On power-up: check the level and pump if needed, then sleep 24 hours, repeat.

from machine import Pin
import time

# ---- CONFIG ----
RELAY_PIN  = 22
SENSOR_PIN = 23

RELAY_ON  = 1
RELAY_OFF = 0

SENSOR_WET = 1    # wet = 1, confirmed from testing
MAX_RUN_S  = 30   # flood failsafe -- never pump longer than this
# ----------------

relay  = Pin(RELAY_PIN, Pin.OUT)
sensor = Pin(SENSOR_PIN, Pin.IN, Pin.PULL_DOWN)

relay.value(RELAY_OFF)


def is_wet():
    return sensor.value() == SENSOR_WET


def fill():
    if is_wet():
        print("Level OK -- no fill needed")
        return
    print("Low water -> running pump")
    relay.value(RELAY_ON)
    start = time.ticks_ms()
    try:
        while True:
            if is_wet():
                print("Reached level -> stopping")
                break
            if time.ticks_diff(time.ticks_ms(), start) > MAX_RUN_S * 1000:
                print("TIMEOUT -> stopping (check water source / sensor)")
                break
            time.sleep(0.1)
    finally:
        relay.value(RELAY_OFF)


while True:
    print("Checking water level...")
    fill()
    print("Done. Sleeping 24 hours.")
    time.sleep(24 * 60 * 60)  # 24 hours in seconds


