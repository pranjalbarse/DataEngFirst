import json
import logging
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Encrypt the message using RSA
def encrypt_message(message, public_key):
    try:
        encrypted_message = public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message.hex()
    except Exception as e:
        logger.error(f"Error encrypting message: {e}")
        return None

# Load public key
def load_public_key():
    try:
        with open("rsa_public.pem", "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
        logger.info("Public key loaded successfully.")
        return public_key
    except Exception as e:
        logger.error(f"Error loading public key: {e}")
        return None

# Generate and encrypt the data
def generate_data():
    # Sample data (replace with your actual data generation logic)
    lift_ticket = {
        "txid": "eaa511e4-15e7-40fe-a580-d778e6f64478",
        "rfid": "0x76a4bddb7f9a55baf9bd1135",
        "resort": "Heavenly Resort",
        "purchase_time": "2025-02-21T20:34:15.293899",
        "expiration_time": "2023-06-01T00:00:00",
        "days": 1,
        "name": "Jeffery Rogers",
        "address": {"street_address": "4987 Briggs Tunnel", "city": "Port Robin", "state": "RI", "postalcode": "02833"},
        "phone": "287.696.7175",
        "email": "winterskenneth@example.net",
        "emergency_contact": None
    }

    # Convert data to JSON string
    json_data = json.dumps(lift_ticket, ensure_ascii=False)
    public_key = load_public_key()

    if public_key:
        encrypted_message = encrypt_message(json_data, public_key)
        if encrypted_message:
            # Return the encrypted message as a JSON object
            return json.dumps({"encrypted_message": encrypted_message})
        else:
            logger.error("Failed to encrypt data.")
            return None
    return None

if __name__ == "__main__":
    encrypted_data = generate_data()
    if encrypted_data:
        print(encrypted_data) # This will output the encrypted message