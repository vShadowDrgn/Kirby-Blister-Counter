import time
import RPi.GPIO as GPIO # type: ignore
from threading import Lock

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(8, 50)
pwm.start(0)

servo_lock = Lock()

def set_angle(angle):
    with servo_lock:
        print(f"Servo {angle}°")
        duty = 2 + (angle / 18)  # 2 corresponds to 0 degrees, 12 corresponds to 180 degrees
        pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        pwm.ChangeDutyCycle(0)

def ir_loop(database):
    last_input = GPIO.input(10)
    while True:
        inpt = GPIO.input(10)

        if inpt == 0:  # Sensor ist getriggert
            if last_input == 1:  # Wenn der Sensor im letzten Schleifendurchlauf auf 1 war, hat sich der Zustand also verändert (von aus zu an).
                database.increase_counter() # Zähler erhöhen
                set_angle(120) # Klappe öffnen
        elif inpt == 1 and last_input == 0:  # Wenn der Sensor jetzt auf 1 ist und vorher auf 0 war, hat sich der Zustand ebenfalls verändert (von an zu aus)
            set_angle(35) # Klappe schließen

        last_input = inpt # Variable für letzten Input updaten
        time.sleep(0.01)