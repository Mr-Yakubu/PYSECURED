from flask import Flask, render_template, request, redirect, url_for
from twilio.rest import Client
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
import base64

account_sid = ACec15f65a92e4a485d1b0282af63cbd38
auth_token = 410330a186e728be35e59b1f9b90611a
client = Client(account_sid, auth_token)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        algorithm = request.form['algorithm']
        key = request.form['key'].encode()
        text = request.form['text'].encode()

    otp = key.decode()  # Use the key as OTP for simplicity
    send_sms(receiver_phone_number, f'Your OTP is: {otp}')
        
        if algorithm == 'AES':
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
        elif algorithm == 'DES':
            cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
        
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(text) + encryptor.finalize()
        
        decryptor = cipher.decryptor()
        decrypted_text = decryptor.update(ciphertext) + decryptor.finalize()
        
        return render_template('index.html', ciphertext=base64.b64encode(ciphertext).decode(), decrypted_text=decrypted_text.decode())
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
