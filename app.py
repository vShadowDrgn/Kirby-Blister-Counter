from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database_manager import Dao # type: ignore
from hardware import ir_loop # type: ignore

counter = 0
app = Flask(__name__)
database = Dao("database.db")

def increase_counter():
    global counter
    counter += 1

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/statistik')
def statistik():
    return render_template("statistik.html")

if __name__ == "__main__":
    t = Thread(target=ir_loop, args=(database,))
    t.start()
    app.run(host="0.0.0.0", debug=False, use_reloader=False)
