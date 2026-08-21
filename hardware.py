import time
from threading import Lock

from gpiozero import Device, PWMOutputDevice, DigitalInputDevice
from gpiozero.pins.lgpio import LGPIOFactory

# Physical pin 8 = BCM GPIO14
# Physical pin 10 = BCM GPIO15

Device.pin_factory = LGPIOFactory(chip=0)
servo = PWMOutputDevice(14, frequency=50, initial_value=0)
sensor = DigitalInputDevice(15, pull_up=False)

servo_lock = Lock()

def set_angle(angle):
    with servo_lock:
        print(f"Servo {angle}°")
        duty_percent = 2 + (angle / 18)
        servo.value = duty_percent / 100
        time.sleep(0.5)
        servo.value = 0

def ir_loop(database):
    last_input = sensor.value

    while True:
        inpt = sensor.value

        if inpt == 0:
            if last_input == 1:
                database.increase_counter()
                set_angle(120)

        elif inpt == 1 and last_input == 0:
            set_angle(35)

        last_input = inpt
        time.sleep(0.01)
