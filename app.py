from flask import Flask, request, redirect, url_for, render_template_string
import os

app = Flask(__name__)

USERNAME_FILE = 'ips.txt'
PASSWORD = '9554216787'

# Simple HTML templates
username_form = '''
    <h2>Enter your username:</h2>
    <form method="POST">
        <input type="text" name="username" required>
        <input type="submit" value="Next">
    </form>
'''

password_form = '''
    <h2>Vault Authentication Required</h2>
    <p>Your IP has been logged.</p>
    <form method="POST">
        <input type="password" name="password" required>
        <input type="submit" value="Unlock">
    </form>
'''

success_page = '''
    <h2>Welcome, Access Granted!</h2>
    <p>Logged Visitors:</p>
    <pre>{{ logs }}</pre>
'''

# Helper to get real IP
def get_real_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr

# Helper to read user-IP mappings
def read_ips():
    if not os.path.exists(USERNAME_FILE):
        return {}
    with open(USERNAME_FILE, 'r') as f:
        lines = f.readlines()
        return dict(line.strip().split(' - ', 1) for line in lines if ' - ' in line)

# Helper to write user-IP mappings
def write_ips(data):
    with open(USERNAME_FILE, 'w') as f:
        for ip, user in data.items():
            f.write(f"{ip} - {user}\n")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            ip = get_real_ip()
            data = read_ips()
            if ip not in data:
                data[ip] = username
                write_ips(data)
            # Store username in session-like behavior using query string
            return redirect(url_for('vault', user=username))
    return render_template_string(username_form)

@app.route('/vault', methods=['GET', 'POST'])
def vault():
    ip = get_real_ip()
    username = request.args.get('user', 'Unknown')

    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            logs = open(USERNAME_FILE).read() if os.path.exists(USERNAME_FILE) else "No logs yet."
            return render_template_string(success_page, logs=logs)
        return "Incorrect password.", 403

    return render_template_string(password_form)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
