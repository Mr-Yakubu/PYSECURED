from flask import Flask, render_template, request, redirect, url_for, flash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to decrypt the ciphertext
def decrypt_message(key, ciphertext):
    iv = ciphertext[:16]  # Extract initialization vector from ciphertext
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB(iv))
    decryptor = cipher.decryptor()
    decrypted_text = decryptor.update(ciphertext[16:]) + decryptor.finalize()
    return decrypted_text.decode()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    sms_status = None

    key = request.form['key'].strip()
    text = request.form['text']
    phone_number = request.form['phone_number']

    # Validate key length for AES (16, 24, or 32 bytes)
    if len(key) not in [16, 24, 32]:
        return render_template('index.html', sms_status="Invalid key length. Key must be 16, 24, or 32 bytes for AES.", ciphertext=None)

    # Encrypt the text using AES
    iv = os.urandom(16)  # Initialization vector for AES
    cipher = Cipher(algorithms.AES(key.encode()), modes.CFB(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_text = padder.update(text.encode()) + padder.finalize()
    ciphertext = iv + encryptor.update(padded_text) + encryptor.finalize()

    flash('Thank you for using PYSECURED!')
    return redirect(url_for('decrypt', ciphertext=ciphertext.hex(), phone_number=phone_number))

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        decryption_key = request.form['decryption_key']
        ciphertext_hex = request.form['ciphertext']

        # Convert ciphertext from hex back to bytes
        ciphertext = bytes.fromhex(ciphertext_hex)

        # Decrypt the text using the decryption key
        decrypted_message = decrypt_message(decryption_key, ciphertext)

        return render_template('decrypt.html', decrypted_message=decrypted_message)
    
    # If no decryption attempt yet, show the ciphertext and form
    ciphertext_hex = request.args.get('ciphertext', None)
    phone_number = request.args.get('phone_number', None)

    return render_template('decrypt.html', ciphertext=ciphertext_hex, phone_number=phone_number)

if __name__ == '__main__':
    app.run(debug=True)
