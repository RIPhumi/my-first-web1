from flask import Flask, request, render_template

app = Flask(__name__)
ip_list = []
PASSWORD = "9554216787"

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip = request.remote_addr
    return ip

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password")
    if password == PASSWORD:
        ip = get_client_ip()
        if ip not in ip_list:
            ip_list.append(ip)
        return render_template("dashboard.html", ips=ip_list)
    else:
        return "Incorrect password", 403

if __name__ == "__main__":
    app.run(debug=False)

