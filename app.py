from itertools import count
from flask import Flask, request
from flask.helpers import flash, url_for
from flask.templating import render_template
import re
import pyotp
import urllib.request
import urllib.parse
import requests
from werkzeug.utils import redirect
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

totp = pyotp.TOTP("base32secret3232", interval=180)

app.config["SECRET_KEY"] = "APP_SECRET_KEY"



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/number")
def number():
    return render_template("number.html")

@app.route("/number", methods=["POST"])
def number_form():
    number = request.form.get("number")
    pattern = re.match(r"[6-9][0-9]{9}", number)

    if pattern:
        flash("The Number is Valid", "success")
        number = str(number)
        otp_gen = totp.now()
        name = str(request.form.get("name"))
        # send otp to number
        otp_message = f"Your OTP for AADHAR verification is {otp_gen}"
        msg = f"{name} Aadhar Verification OTP is {otp_gen}"
        resp =  sendSMS(number, msg)
        flash("Enter the otp sent to your valid Mobile Number")
        return redirect(url_for("otp"))
    else:
        flash(f"The Number is Not Valid", "danger")
        return redirect(url_for("number"))
def sendSMS(number, message):
    url = "https://www.fast2sms.com/dev/bulk"
    params={
        "authorization":"SO3dt7mZ89h4vbkIiuPoDlfAe6VWHMagq10Uy5GENpXwLYzj2KrUVWjCcAPGqkJn72uaxDY0Ob1HLgep",
        "sender_id":"SMSINI",
        "message":message,
        "language":"english",
        "route":"p",
        "numbers":number
    }
    rs = requests.get(url, params=params)
    return rs
    

@app.route("/otp")
def otp():
    return render_template("otp.html")


@app.route("/otp", methods=['POST'])
def otp_form():
    otp_rec = int(request.form.get("otp"))
    otp_ver = totp.verify(otp_rec)
    if otp_ver:
        flash("OTP is Valid", "success")
        return render_template("consent1.html")
    else:
        flash(f"OTP is not Valid", "danger")
        return redirect(url_for("otp"))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload_file():
    return '''
    <!doctype html>
    <title>Upload Proof File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''
@app.route('/upload', methods=['POST'])
def upload():

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Uploaded new File</h1>
        '''

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')




		

