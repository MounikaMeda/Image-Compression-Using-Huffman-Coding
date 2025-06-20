from flask import Flask, render_template, request, send_file, redirect
import os
from compression.huffman import compress, decompress
from compression.encryption import encrypt_data, decrypt_data
from compression.signature import sign_data, verify_signature
import pickle
import traceback

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
KEYS_FOLDER = "keys"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress', methods=['POST'])
def compress_route():
    image = request.files['image']
    password = request.form['password']

    if image and password:
        img_data = image.read()

        # Huffman compression
        compressed_data, codes = compress(img_data)

        # Signature before encryption
        signature = sign_data(compressed_data, os.path.join(KEYS_FOLDER, "private_key.pem"))

        # Pack everything using pickle
        package = {
            'compressed_data': compressed_data,
            'codes': codes,
            'signature': signature
        }

        pickled_package = pickle.dumps(package)

        # Encrypt it
        encrypted_package = encrypt_data(pickled_package, password)

        # Save encrypted file
        out_path = os.path.join(UPLOAD_FOLDER, "compressed.huffimg")
        with open(out_path, "wb") as f:
            f.write(encrypted_package)

        return send_file(out_path, as_attachment=True)

    return "❌ Missing file or password."

@app.route('/decompress', methods=['POST'])
def decompress_route():
    file = request.files['file']
    password = request.form['password']

    if file and password:
        try:
            encrypted_data = file.read()

            # Decrypt
            decrypted_data = decrypt_data(encrypted_data, password)

            # Load from pickle
            package = pickle.loads(decrypted_data)
            compressed_data = package['compressed_data']
            codes = package['codes']
            signature = package['signature']

            # Verify signature
            if not verify_signature(compressed_data, signature, os.path.join(KEYS_FOLDER, "public_key.pem")):
                return "❌ Signature verification failed!"

            # Decompress
            decompressed_data = decompress(compressed_data, codes)

            # Save result
            out_path = os.path.join(UPLOAD_FOLDER, "decompressed.png")
            with open(out_path, "wb") as f:
                f.write(decompressed_data)

            return send_file(out_path, as_attachment=True)

        except Exception as e:
            return f"❌ Error: {str(e)}<br><pre>{traceback.format_exc()}</pre>"

    return "❌ Missing file or password."
    
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
