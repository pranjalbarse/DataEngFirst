import sys
import json
import uuid
import random
from dotenv import load_dotenv
from faker import Faker
from datetime import date, datetime, timezone
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256

# Load environment variables (if needed)
load_dotenv()

# Initialize Faker for generating fake data
fake = Faker()

# Resort list for random selection
resorts = [
    "Vail", "Beaver Creek", "Breckenridge", "Keystone", "Crested Butte", "Park City", "Heavenly", "Northstar",
    "Kirkwood", "Whistler Blackcomb", "Perisher", "Falls Creek", "Hotham", "Stowe", "Mount Snow", "Okemo",
    "Hunter Mountain", "Mount Sunapee", "Attitash", "Wildcat", "Crotched", "Stevens Pass", "Liberty", "Roundtop", 
    "Whitetail", "Jack Frost", "Big Boulder", "Alpine Valley", "Boston Mills", "Brandywine", "Mad River",
    "Hidden Valley", "Snow Creek", "Wilmot", "Afton Alps", "Mt. Brighton", "Paoli Peaks"
]

# Function to get optional value (to randomize some data)
def get_optional_value(generator_func):
    return generator_func() if random.choice([True, False]) else None

# Function to encrypt the data
def encrypt_message(message):
    try:
        with open("rsa_key_fixed.pem", "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )
        encrypted_data = private_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=SHA256()),
                algorithm=SHA256(),
                label=None
            )
        )
        return encrypted_data.hex() # Return encrypted data as hex
    except Exception as e:
        sys.stderr.write(f"Error encrypting message: {e}\n")
        return None

# Function to print the lift ticket and encrypt it
def print_lift_ticket():
    state = fake.state_abbr()
    lift_ticket = {
        'txid': str(uuid.uuid4()),
        'rfid': hex(random.getrandbits(96)),
        'resort': fake.random_element(elements=resorts),
        'purchase_time': datetime.now(timezone.utc).isoformat(),
        'expiration_time': date(2023, 6, 1).isoformat(),
        'days': fake.random_int(min=1, max=7),
        'name': fake.name(),
        'address': get_optional_value(lambda: {
            'street_address': fake.street_address(),
            'city': fake.city(),
            'state': state,
            'postalcode': fake.postcode_in_state(state)
        }),
        'phone': get_optional_value(fake.phone_number),
        'email': get_optional_value(fake.email),
        'emergency_contact': get_optional_value(lambda: {'name': fake.name(), 'phone': fake.phone_number()}),
    }

    # Convert lift ticket data to JSON
    json_data = json.dumps(lift_ticket, ensure_ascii=False)

    # Encrypt the JSON data
    encrypted_data = encrypt_message(json_data)

    if encrypted_data:
        # Wrap the encrypted data in a dictionary and print it
        output_data = {
            "encrypted_message": encrypted_data
        }
        # Print the JSON with the encrypted message
        print(json.dumps(output_data))

# Main function to handle command-line arguments and generate tickets
if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        try:
            total_count = int(args[0])
            for _ in range(total_count):
                print_lift_ticket()
        except ValueError:
            sys.stderr.write("Error: Invalid argument. Please provide an integer.\n")
    else:
        sys.stderr.write("Error: Please provide the number of records to generate.\n")