import json
import os
import time
import RPi.GPIO as GPIO
from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, jsonify

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pwm = GPIO.PWM(8, 50)

pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)  # 2 corresponds to 0 degrees, 12 corresponds to 180 degrees
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Give time for the servo to reach the position
    pwm.ChangeDutyCycle(0)  # Stop sending signal to the servo

set_angle(35)

counter = 0
app = Flask(__name__)

def increase_counter():
    global counter
    counter += 1

def ir_loop():
    global counter
    while True:
        inpt = GPIO.input(10)
        if inpt == 0:
            increase_counter()
            set_angle(120)
            time.sleep(1)
            set_angle(35)
        time.sleep(0.01)

@app.route('/')
def index():
    return f"Es wurden bereits {counter} Blister eingeworfen. Das sind {counter * 5} Punkte"


if __name__ == "__main__":
    t = Thread(target=ir_loop)
    t.start()
    app.run(host="0.0.0.0", debug=True)
