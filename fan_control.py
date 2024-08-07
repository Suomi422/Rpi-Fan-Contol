import os
import time
import logging

from enum import Enum
import RPi.GPIO as GPIO


logging.basicConfig(filename='/var/log/fan_control.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

THERMAL_FILE = "/sys/class/thermal/thermal_zone0/temp"
PWM_PIN = 18  # GPIO pin 18 (physical pin 12)
SHOULD_RUN_AT_SERVICE_STOP = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, 1000)  # 1kHz frequency (Noctua NF-A4x10 5V PWM)
pwm.start(50)


class FanSpeed(Enum):
    OFF = 0
    QUARTER = 25
    HALF = 50
    FULL = 100


TEMPERATURE_SORT = {
    45: FanSpeed.OFF,
    50: FanSpeed.QUARTER,
    55: FanSpeed.HALF,
    60: FanSpeed.FULL,
}


def get_cpu_temp():
    try:
        with open(THERMAL_FILE, 'r') as file:
            temp_str = file.read().strip()
            temp_c = int(temp_str) / 1000.0
            return temp_c
    except FileNotFoundError:
        logging.error(f"Temperature file not found: {THERMAL_FILE}")
        return None
    except Exception as e:
        logging.error(f"Error reading temperature: {e}")
        return None


def get_fan_speed(temperature):
    sorted_thresholds = sorted(TEMPERATURE_SORT.keys(), reverse=True)
    for threshold in sorted_thresholds:
        if temperature < threshold:
            continue
        return TEMPERATURE_SORT[threshold]

    return TEMPERATURE_SORT[sorted_thresholds[-1]]


def main():
    try:
        while True:
            temp = get_cpu_temp()
            if temp is None:
                time.sleep(5)
                continue

            fan_speed = get_fan_speed(temp)
            logging.info(f"Temperature: {temp:.1f}°C, Fan Speed: {fan_speed.name}")

            pwm.ChangeDutyCycle(fan_speed.value)
            if fan_speed == FanSpeed.OFF:
                time.sleep(5)
            else:
                time.sleep(20)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        pwm.ChangeDutyCycle(FanSpeed.OFF.value)
        time.sleep(1)
        pwm.stop()
        if SHOULD_RUN_AT_SERVICE_STOP == True:
            GPIO.cleanup()
        logging.error("Stopping service")


if __name__ == "__main__":
    main()
