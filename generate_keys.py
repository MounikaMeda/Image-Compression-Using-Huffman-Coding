#!/usr/bin/env python3
"""
RSA Key Pair Generator for Secure Image Compressor
This script generates the required private and public keys for digital signatures.
"""

import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keys(keys_folder="keys", key_size=2048):
    """
    Generate RSA private and public key pair for digital signatures.
    
    Args:
        keys_folder (str): Folder to save the keys
        key_size (int): RSA key size in bits (2048 or 4096 recommended)
    """
    
    # Create keys folder if it doesn't exist
    os.makedirs(keys_folder, exist_ok=True)
    
    print(f"🔐 Generating {key_size}-bit RSA key pair...")
    
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    
    # Get public key from private key
    public_key = private_key.public_key()
    
    # Serialize private key to PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Serialize public key to PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save private key
    private_key_path = os.path.join(keys_folder, "private_key.pem")
    with open(private_key_path, "wb") as f:
        f.write(private_pem)
    
    # Save public key
    public_key_path = os.path.join(keys_folder, "public_key.pem")
    with open(public_key_path, "wb") as f:
        f.write(public_pem)
    
    print(f"✅ Private key saved to: {private_key_path}")
    print(f"✅ Public key saved to: {public_key_path}")
    
    # Set file permissions (Unix-like systems only)
    try:
        os.chmod(private_key_path, 0o600)  # Read/write for owner only
        os.chmod(public_key_path, 0o644)   # Read for all, write for owner
        print("🔒 File permissions set securely")
    except AttributeError:
        print("⚠️  File permissions not set (Windows system)")
    
    return private_key_path, public_key_path

def verify_keys(keys_folder="keys"):
    """
    Verify that the generated keys are valid and can be loaded.
    """
    
    private_key_path = os.path.join(keys_folder, "private_key.pem")
    public_key_path = os.path.join(keys_folder, "public_key.pem")
    
    try:
        # Test loading private key
        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        
        # Test loading public key
        with open(public_key_path, "rb") as f:
            public_key = serialization.load_pem_public_key(f.read())
        
        print("✅ Key verification successful!")
        print(f"🔑 Private key size: {private_key.key_size} bits")
        print(f"🔑 Public key size: {public_key.key_size} bits")
        
        return True
        
    except Exception as e:
        print(f"❌ Key verification failed: {e}")
        return False

def main():
    """
    Main function to generate and verify RSA keys.
    """
    
    print("=" * 50)
    print("🔐 RSA Key Generator for Secure Image Compressor")
    print("=" * 50)
    
    # Check if keys already exist
    if os.path.exists("keys/private_key.pem") and os.path.exists("keys/public_key.pem"):
        response = input("Keys already exist. Regenerate? (y/N): ").lower()
        if response != 'y':
            print("Skipping key generation.")
            verify_keys()
            return
    
    try:
        # Generate keys
        private_path, public_path = generate_rsa_keys()
        
        print("\n" + "=" * 30)
        print("🔍 Verifying generated keys...")
        print("=" * 30)
        
        # Verify keys
        if verify_keys():
            print("\n✅ RSA key pair generated successfully!")
            print("Your Flask app can now use digital signatures.")
        else:
            print("\n❌ Key generation failed. Please try again.")
            
    except Exception as e:
        print(f"\n❌ Error generating keys: {e}")
        print("Please ensure you have the 'cryptography' package installed:")
        print("pip install cryptography")

if __name__ == "__main__":
    main()