from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
PASSWORD = "9554216787"
IPS_FILE = "ips.txt"

def get_client_ip():
    if "X-Forwarded-For" in request.headers:
        return request.headers["X-Forwarded-For"].split(',')[0].strip()
    return request.remote_addr

def log_ip(ip):
    with open(IPS_FILE, "a") as f:
        f.write(ip + "\n")

def read_logged_ips():
    try:
        with open(IPS_FILE, "r") as f:
            return list(set(line.strip() for line in f if line.strip()))
    except FileNotFoundError:
        return []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password")
    if password == PASSWORD:
        ip = get_client_ip()
        log_ip(ip)
        ips = read_logged_ips()
        return render_template("dashboard.html", ips=ips)
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)


