from flask import Flask, request, redirect, render_template_string, session
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

PASSWORD = "9554216787"
IPS_FILE = "ips.txt"

username_template = '''
<!doctype html>
<title>Enter Username</title>
<h2>Enter your username</h2>
<form method="POST">
  <input type="text" name="username" required>
  <input type="submit" value="Next">
</form>
'''

password_template = '''
<!doctype html>
<title>Vault Login</title>
<h2>Vault Authentication Required</h2>
<form method="POST">
  <input type="password" name="password" required>
  <input type="submit" value="Enter">
</form>
'''

logged_in_template = '''
<!doctype html>
<title>Welcome</title>
<h2>Access Granted</h2>
<p>Your IP has been logged!</p>
<pre>{{ ips }}</pre>
'''

def get_client_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

def log_ip(ip, username):
    existing = {}
    if os.path.exists(IPS_FILE):
        with open(IPS_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    existing[parts[0]] = parts[1]

    if ip not in existing:
        existing[ip] = username
        with open(IPS_FILE, 'a') as f:
            f.write(f"{ip} - {username}\n")

def read_ips():
    if os.path.exists(IPS_FILE):
        with open(IPS_FILE, 'r') as f:
            return f.read()
    return "No IPs logged yet."

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect('/')
        return render_template_string(username_template)

    if 'authenticated' not in session:
        if request.method == 'POST':
            password = request.form['password']
            if password == PASSWORD:
                session['authenticated'] = True
                ip = get_client_ip()
                log_ip(ip, session['username'])
                return redirect('/')
        return render_template_string(password_template)

    return render_template_string(logged_in_template, ips=read_ips())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
