from flask import Flask, render_template, request, send_file
import os
from compression.huffman import compress, decompress
from compression.encryption import encrypt_data, decrypt_data
from compression.signature import sign_data, verify_signature
import pickle
import traceback
import hashlib
from PIL import Image
import io

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
        try:
            img_data = image.read()

            compressed_data, codes = compress(img_data)
            data_hash = hashlib.sha256(compressed_data).hexdigest()
            signature = sign_data(compressed_data, os.path.join(KEYS_FOLDER, "private_key.pem"))

            package = {
                'compressed_data': compressed_data,
                'codes': codes,
                'signature': signature,
                'data_hash': data_hash
            }

            pickled_package = pickle.dumps(package)
            encrypted_package = encrypt_data(pickled_package, password)

            out_path = os.path.join(UPLOAD_FOLDER, "compressed.huffimg")
            with open(out_path, "wb") as f:
                f.write(encrypted_package)

            return send_file(out_path, as_attachment=True)
        except Exception as e:
            return render_template("error.html", title="Compression Error", message=str(e))

    return render_template("error.html", title="Input Error", message="Missing image or password.")

@app.route('/decompress', methods=['POST'])
def decompress_route():
    file = request.files['file']
    password = request.form['password']

    if file and password:
        try:
            encrypted_data = file.read()

            try:
                decrypted_data = decrypt_data(encrypted_data, password)
            except Exception as decrypt_error:
                return render_template("error.html", title="Decryption Failed", message="""
                    Possible reasons:
                    <ul>
                        <li>✗ Wrong password</li>
                        <li>✗ File was tampered or corrupted</li>
                        <li>✗ Not a valid encrypted file</li>
                    </ul>
                """)

            try:
                package = pickle.loads(decrypted_data)
                compressed_data = package['compressed_data']
                codes = package['codes']
                signature = package['signature']
                stored_hash = package['data_hash']
            except Exception:
                return render_template("error.html", title="Invalid Format", message="This file is not a valid compressed image package.")

            current_hash = hashlib.sha256(compressed_data).hexdigest()
            if current_hash != stored_hash:
                return render_template("error.html", title="Integrity Check Failed", message="SHA-256 hash mismatch detected. File may be tampered or corrupted.")

            if not verify_signature(compressed_data, signature, os.path.join(KEYS_FOLDER, "public_key.pem")):
                return render_template("error.html", title="Signature Verification Failed", message="Invalid digital signature. The file may not be from the original sender.")

            decompressed_data = decompress(compressed_data, codes)

            img = Image.open(io.BytesIO(decompressed_data))
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            output = io.BytesIO()
            img.save(output, format='JPEG', quality=60, optimize=True)

            out_path = os.path.join(UPLOAD_FOLDER, "compressed_output.jpg")
            with open(out_path, "wb") as f:
                f.write(output.getvalue())

            return send_file(out_path, as_attachment=True)

        except Exception as e:
            return render_template("error.html", title="Processing Error", message=str(e))

    return render_template("error.html", title="Input Error", message="Missing file or password.")

@app.route('/decompress_only', methods=['POST'])
def decompress_only_route():
    file = request.files['file']
    password = request.form['password']

    if file and password:
        try:
            encrypted_data = file.read()

            try:
                decrypted_data = decrypt_data(encrypted_data, password)
            except Exception as decrypt_error:
                return render_template("error.html", title="Decryption Failed", message="""
                    Possible reasons:
                    <ul>
                        <li>✗ Wrong password</li>
                        <li>✗ File was tampered or corrupted</li>
                        <li>✗ Not a valid encrypted file</li>
                    </ul>
                """)

            try:
                package = pickle.loads(decrypted_data)
                compressed_data = package['compressed_data']
                codes = package['codes']
                # Note: We skip signature and hash verification in this route
            except Exception:
                return render_template("error.html", title="Invalid Format", message="This file is not a valid compressed image package.")

            # Decompress the data to get original raw image bytes
            decompressed_data = decompress(compressed_data, codes)

            # Detect file extension from original data
            img = Image.open(io.BytesIO(decompressed_data))
            original_format = img.format or 'PNG'
            
            format_extensions = {
                'JPEG': 'jpg',
                'PNG': 'png', 
                'BMP': 'bmp',
                'TIFF': 'tiff',
                'GIF': 'gif',
                'WEBP': 'webp'
            }
            file_ext = format_extensions.get(original_format, 'png')
            
            # Save the raw decompressed data directly (exact original bytes)
            out_path = os.path.join(UPLOAD_FOLDER, f"original_restored.{file_ext}")
            with open(out_path, "wb") as f:
                f.write(decompressed_data)

            return send_file(out_path, as_attachment=True)

        except Exception as e:
            return render_template("error.html", title="Processing Error", message=str(e))

    return render_template("error.html", title="Input Error", message="Missing file or password.")

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)