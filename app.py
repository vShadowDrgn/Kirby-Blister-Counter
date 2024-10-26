from threading import Thread
from flask import Flask, render_template, request, redirect, url_for, jsonify
from database_manager import Dao # type: ignore
#from hardware import ir_loop # type: ignore

app = Flask(__name__)
database = Dao("database.db")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/statistik')
def statistik():
    return render_template("statistik.html")

@app.route('/increase_counter')
def increase_counter():
    database.increase_counter()
    return jsonify({"success": True, "message": "Erfolgreich gezählt"})

if __name__ == "__main__":
    #t = Thread(target=ir_loop, args=(database,))
    #t.start()
    app.run(host="0.0.0.0", debug=True) #, use_reloader=False)
