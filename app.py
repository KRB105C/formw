from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask_cors import CORS  # Tambahkan CORS
import logging
import datetime
import os

app = Flask(__name__)
CORS(app)  # Aktifkan CORS untuk semua rute

# Konfigurasi email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Ambil dari ENV
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Ambil dari ENV
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

EMAIL_TUJUAN = os.getenv('EMAIL_TUJUAN')  # Email penerima (ENV)

mail = Mail(app)

# Konfigurasi log
logging.basicConfig(
    filename="email_api.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

@app.route('/')
def home():
    return "🚀 Flask API is running with Gunicorn!"

@app.route('/submit-form', methods=['POST'])
def submit_form():
    request_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client_ip = request.remote_addr
    data = request.get_json()

    if not data:
        return jsonify({"error": "Data tidak ditemukan", "status": "failed"}), 400

    email_body = "\n".join([f"{key}: {value}" for key, value in data.items()])

    try:
        msg = Message("Form Submission", recipients=[EMAIL_TUJUAN])
        msg.body = email_body
        mail.send(msg)

        return jsonify({
            "message": f"✅ Email terkirim ke {EMAIL_TUJUAN}",
            "data_sent": data,
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e), "status": "failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
