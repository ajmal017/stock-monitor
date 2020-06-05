from flask import Flask, render_template, jsonify
import time

app = Flask("__main__")


@app.route("/")
def my_index():
    return render_template("index.html", token="Hello from Flask")


@app.route("/time")
def get_time():
    return jsonify({"time": time.time()})


app.run(debug=True)
