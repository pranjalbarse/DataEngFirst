import sys
import rapidjson as json
import optional_faker as _
import uuid
import random
from dotenv import load_dotenv
from faker import Faker
from datetime import date, datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256

# Load Public Key for Encryption
with open("rsa_key.pub", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

load_dotenv()
fake = Faker()
resorts = ["Vail", "Beaver Creek", "Breckenridge", "Keystone", "Crested Butte", "Park City"]

def encrypt_message(message):
    """Encrypts a message using the RSA public key"""
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=SHA256()),
            algorithm=SHA256(),
            label=None
        )
    )
    return encrypted.hex() # Convert bytes to hex for safe transfer

def print_lift_ticket():
    state = fake.state_abbr()
    lift_ticket = {
        'txid': str(uuid.uuid4()),
        'rfid': hex(random.getrandbits(96)),
        'resort': fake.random_element(elements=resorts),
        'purchase_time': datetime.now(timezone.utc).isoformat(),
        'expiration_time': date(2023, 6, 1).isoformat(),
        'days': fake.random_int(min=1, max=7),
        'name': fake.name()
    }
    
    json_data = json.dumps(lift_ticket,ensure_ascii=False)
    encrypted_data = encrypt_message(json_data) # Encrypt before output
    print(encrypted_data) # Print encrypted output

if __name__ == "__main__":
    args = sys.argv[1:]
    total_count = int(args[0])
    for _ in range(total_count):
        print_lift_ticket()
    print('')