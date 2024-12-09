from flask import Flask
from flask import render_template
from flask import request
import db_interface as db_manager

#QR Code Additional Imports
from flask import redirect, url_for, session
import pyotp
import pyqrcode
import os
import base64
from io import BytesIO

app = Flask(__name__)

is_logged_in = False

#Add a secret key
app.secret_key = 'AYHJGHIULP'

@app.route("/", methods=["POST", "GET"])
def index_page():
    global is_logged_in
    if request.method == "POST":
        if request.form["password"].isdigit():
            password = int(request.form["password"])
            email = request.form["email"]
            is_logged_in = db_manager.check_login(email, password)
            if is_logged_in:
                user_secret = pyotp.random_base32()
                session['username'] = email  # Save username in session
                session['secret'] = user_secret  # Save user secret in session
                return redirect(url_for("enable_2fa")) #direct to the 2FA route
            else:
                return render_template("index.html")
        app.logger.critical(f"{email} is logged in ? {is_logged_in}")
    return render_template("index.html", is_logged_in=is_logged_in), 200

#Displays and handles the 2FA

@app.route('/enable_2fa.html', methods=['GET', 'POST'])
def enable_2fa():
    global is_logged_in
    if 'username' not in session:
        return render_template("index.html")
    
    username = session['username']
    user_secret = session['secret']  # Retrieve user secret from session - Session Management
    
    # Generate QR code for the user's secret key
    totp = pyotp.TOTP(user_secret)
    otp_uri = totp.provisioning_uri(name=username, issuer_name="YourAppName")
    qr_code = pyqrcode.create(otp_uri)
    stream = BytesIO()
    qr_code.png(stream, scale=5)
    qr_code_b64 = base64.b64encode(stream.getvalue()).decode('utf-8')

    if request.method == 'POST':
        otp_input = request.form['otp']
        if totp.verify(otp_input):
            return render_template("index.html", is_logged_in=is_logged_in), 200
            #return redirect(url_for('home'))  # Redirect to home if OTP is valid
        else:
            #return "Invalid OTP. Please try again.", 401
            is_logged_in = False
            return redirect(url_for('index_page'))  # Redirect to home if OTP is valid

    return render_template("enable_2fa.html", qr_code=qr_code_b64)

if __name__ == "__main__":
    app.run(debug=True)
