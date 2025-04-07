from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)
password = "9554216787"

# HTML content
HTML = '''
<!DOCTYPE html>
<html>
<head>
  <title>Protected Page</title>
</head>
<body>
  {% if error %}<p style="color:red;">{{ error }}</p>{% endif %}
  {% if not authenticated %}
    <form method="post">
      <label>Password:</label>
      <input type="password" name="password">
      <input type="submit" value="Enter">
    </form>
  {% else %}
    <h1>Welcome!</h1>
    <p>Your IP has been logged.</p>
    <h2>Logged IPs:</h2>
    <pre>{{ logs }}</pre>
  {% endif %}
</body>
</html>
'''

def get_real_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0]
    else:
        ip = request.remote_addr
    return ip

@app.before_request
def log_ip():
    ip = get_real_ip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('ips.txt', 'a') as f:
        f.write(f'{now} - {ip} (visited)\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    authenticated = False

    if request.method == 'POST':
        if request.form.get('password') == password:
            authenticated = True
        else:
            error = "Incorrect password."

    logs = ""
    try:
        with open('ips.txt', 'r') as f:
            logs = f.read()
    except FileNotFoundError:
        logs = "No visitors yet."

    return render_template_string(HTML, error=error, authenticated=authenticated, logs=logs)

if __name__ == '__main__':
    app.run(debug=True)
