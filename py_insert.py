import json
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load the private key
try:
    with open("rsa_key_fixed.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None  # Change if your key has a password
        )
    logging.info("Private key loaded successfully.")
except Exception as e:
    logging.error(f"Error loading private key: {e}")
    exit(1)

# Function to decrypt data
def decrypt_data(encrypted_data):
    try:
        decrypted_data = private_key.decrypt(
            encrypted_data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return decrypted_data.decode("utf-8")
    except Exception as e:
        logging.error(f"Error decrypting data: {e}")
        return None

# Read input data from stdin
try:
    input_data = json.loads(input())
    if "encrypted_message" in input_data:
        decrypted_message = decrypt_data(bytes.fromhex(input_data["encrypted_message"]))
        if decrypted_message:
            logging.info(f"Decrypted message: {decrypted_message}")
        else:
            logging.error("Failed to decrypt message.")
    else:
        logging.error("No encrypted message found in input data.")
except Exception as e:
    logging.error(f"Error processing input data: {e}")