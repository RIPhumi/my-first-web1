from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

# Set your password here
PASSWORD = "9554216787"

# HTML form for username and password
login_form = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Enter your details</h2>
    <form method="POST">
        <label>Username:</label>
        <input type="text" name="username" required><br><br>
        <label>Password:</label>
        <input type="password" name="password" required><br><br>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# Success page showing the user's IP
success_page = """
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>
    <h2>Access Granted</h2>
    <p>Your IP <strong>{{ ip }}</strong> has been logged as <strong>{{ user }}</strong>. Thank you!</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if password == PASSWORD:
            # Get visitor's IP
            ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(",")[0].strip()

            # Save IP and username to file
            with open("ips.txt", "a") as f:
                f.write(f"{datetime.now()} - {ip} - {username}\n")

            return render_template_string(success_page, ip=ip, user=username)
        else:
            return "Incorrect password", 403
    return render_template_string(login_form)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
