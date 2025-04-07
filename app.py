from flask import Flask, request, render_template_string, redirect
import os
from datetime import datetime

app = Flask(__name__)

# Set your password here
PASSWORD = "9554216787"

# HTML template for password form
password_form = """
<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h2>Enter Password</h2>
    <form method="POST">
        <input type="password" name="password" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

# HTML template for success page
success_page = """
<!DOCTYPE html>
<html>
<head><title>Welcome</title></head>
<body>
    <h2>Access Granted</h2>
    <p>Your IP has been logged. Thank you!</p>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password")
        if password == PASSWORD:
            # Get real client IP, accounting for proxy headers
            ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(",")[0].strip()

            # Log IP with timestamp
            with open("ips.txt", "a") as f:
                f.write(f"{datetime.now()} - {ip}\n")

            return render_template_string(success_page)
        else:
            return "Incorrect password", 403
    return render_template_string(password_form)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
