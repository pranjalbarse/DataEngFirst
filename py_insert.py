import sys
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

# Decrypt the message using RSA
def decrypt_data(encrypted_message, private_key):
    try:
        decrypted_message = private_key.decrypt(
            bytes.fromhex(encrypted_message),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return decrypted_message.decode('utf-8')
    except Exception as e:
        logger.error(f"Error decrypting message: {e}")
        return None

# Load private key
def load_private_key():
    try:
        with open("rsa_key_fixed.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        logger.info("Private key loaded successfully.")
        return private_key
    except Exception as e:
        logger.error(f"Error loading private key: {e}")
        return None

# Insert data into the database (stub for actual insert)
def insert_data_into_db(decrypted_message):
    # You can insert your decrypted data into your Snowflake database here
    logger.info(f"Data to be inserted: {decrypted_message}")
    # Example: db_connection.execute("INSERT INTO table_name (columns) VALUES (values)")
    logger.info("Data inserted successfully into the database")

if __name__ == "__main__":
    # Read the input data
    input_data = sys.stdin.read()
    logger.info(f"Received input data: {input_data}")

    try:
        data = json.loads(input_data)
        encrypted_message = data.get("encrypted_message", None)

        if encrypted_message:
            private_key = load_private_key()
            if private_key:
                decrypted_message = decrypt_data(encrypted_message, private_key)
                if decrypted_message:
                    logger.info(f"Decrypted message: {decrypted_message}")
                    insert_data_into_db(decrypted_message)
                else:
                    logger.error("Decryption failed.")
            else:
                logger.error("Private key not loaded.")
        else:
            logger.error("No encrypted message found in input data.")
    except Exception as e:
        logger.error(f"Error processing input data: {e}")
conn.commit()
print("Transaction commited")