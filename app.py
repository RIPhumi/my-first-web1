
from flask import Flask, request, render_template, redirect
import os

app = Flask(__name__)
PASSWORD = "9554216787"  # Change this to your secret password
ip_log_file = "ips.txt"

@app.route("/")
def index():
    ip = request.remote_addr
    with open(ip_log_file, "a") as f:
        f.write(f"{ip}\n")
    return render_template("index.html")

@app.route("/auth", methods=["POST"])
def auth():
    password = request.form.get("password")
    if password == PASSWORD:
        with open(ip_log_file, "r") as f:
            ips = f.readlines()
        return render_template("result.html", ips=[ip.strip() for ip in ips])
    else:
        return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
