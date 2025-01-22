from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database_manager import Dao # type: ignore
import os

if "RASPBERRY_PI" in os.environ:
    from hardware import ir_loop # type: ignore

app = Flask(__name__)
database = Dao("database.db")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/statistik')
def statistik():
    return render_template("statistik.html")

@app.route('/reset_counter', methods=['POST'])
def reset_counter():
    database.reset_counter()
    return jsonify({"success": True, "message": "Erfolgreich geleert"})

@app.route('/increase_counter', methods=['POST'])
def increase_counter():
    database.increase_counter()
    return jsonify({"success": True, "message": "Erfolgreich gezählt"})

@app.route('/decrease_counter', methods=['POST'])
def decrease_counter():
    database.decrease_counter()
    return jsonify({"success": True, "message": "Erfolgreich abgezogen"})

@app.route('/get_counter', methods=['GET'])
def get_counter():
    total_count = database.get_total_count()
    current_count = database.get_current_count()
    return jsonify({"success": True, "message": "Hier sind deine Werte", "total_count": total_count, "current_count": current_count})

@app.route('/get_statistics', methods=['GET'])
def get_statistics():
    year=request.args.get("year", type=str)
    month=request.args.get("month", type=str)
    yearly_statistics = database.get_yearly_statistics(year)
    print(yearly_statistics)
    monthly_statistics = database.get_monthly_statistics(year, month)
    return jsonify({"success": True, "yearly_statistics": yearly_statistics, "monthly_statistics": monthly_statistics})

if __name__ == "__main__":
    if "RASPBERRY_PI" in os.environ :
        t = Thread(target=ir_loop, args=(database,))
        t.start()
        app.run(host="0.0.0.0", debug=False , use_reloader=False)
    else:
        app.run(host="0.0.0.0", debug=True)
