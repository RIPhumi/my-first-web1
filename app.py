from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Password to access the IP log
PASSWORD = "9554216787"

# File to store IPs
VISITOR_LOG = "visitor_ips.txt"

def log_ip(ip_address):
    # Avoid logging duplicates
    if not os.path.exists(VISITOR_LOG):
        with open(VISITOR_LOG, "w") as f:
            f.write("")
    with open(VISITOR_LOG, "r") as f:
        logged_ips = f.read().splitlines()
    if ip_address not in logged_ips:
        with open(VISITOR_LOG, "a") as f:
            f.write(ip_address + "\n")

@app.route("/", methods=["GET"])
def index():
    ip = request.remote_addr
    log_ip(ip)
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    entered_password = request.form.get("password")
    if entered_password == PASSWORD:
        with open(VISITOR_LOG, "r") as f:
            ip_list = f.read().splitlines()
        return render_template("dashboard.html", ips=ip_list)
    else:
        return render_template("index.html", error="Incorrect password!")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
