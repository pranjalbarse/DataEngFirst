import json
import random
import uuid
import logging
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from datetime import datetime
from faker import Faker
import sys

# Set up logging
logging.basicConfig(level=logging.INFO)

# Load public key for encryption
try:
    with open("rsa_public.pem", "rb") as public_key_file:
        public_key = serialization.load_pem_public_key(public_key_file.read())
    logging.info("Public key loaded successfully.")
except Exception as e:
    logging.error(f"Error loading public key: {e}")
    exit(1)

fake = Faker()

# Sample resorts for generating data
resorts = [
    "Vail", "Beaver Creek", "Breckenridge", "Keystone", "Crested Butte", 
    "Park City", "Heavenly", "Northstar", "Kirkwood", "Whistler Blackcomb"
]

def get_optional_value(generator_func):
    """Returns either a generated value or None randomly."""
    return generator_func() if random.choice([True, False]) else None

# Encrypt data using the public key
def encrypt_message(message):
    try:
        encrypted_message = public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message.hex()
    except Exception as e:
        logging.error(f"Error encrypting message: {e}")
        return None

# Generate a lift ticket (sample data)
def print_lift_ticket():
    state = fake.state_abbr()
    lift_ticket = {
        'txid': str(uuid.uuid4()),
        'rfid': hex(random.getrandbits(96)),
        'resort': fake.random_element(elements=resorts),
        'purchase_time': datetime.now().isoformat(),
        'expiration_time': datetime(2023, 6, 1).isoformat(),
        'days': random.randint(1, 7),
        'name': fake.name(),
        'address': get_optional_value(lambda: {
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': state,
            'postalcode': fake.zipcode_in_state(state)
        }),
        'phone': get_optional_value(fake.phone_number),
        'email': get_optional_value(fake.email),
        'emergency_contact': get_optional_value(lambda: {'name': fake.name(), 'phone': fake.phone_number()}),
    }

    # Convert dictionary to JSON and encrypt it
    json_data = json.dumps(lift_ticket, ensure_ascii=False)
    encrypted_data = encrypt_message(json_data)

    if encrypted_data:
        # Print the encrypted message as JSON
        print(json.dumps({"encrypted_message": encrypted_data}))
    else:
        logging.error("Failed to encrypt data.")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        try:
            total_count = int(args[0])
            for _ in range(total_count):
                print_lift_ticket()
        except ValueError:
            logging.error("Error: Invalid argument. Please provide an integer.")