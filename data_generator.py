import sys
import rapidjson as json
import uuid
import random

from dotenv import load_dotenv
from faker import Faker
from datetime import date, datetime, timezone

load_dotenv()
fake = Faker()

resorts = [
    "Vail", "Beaver Creek", "Breckenridge", "Keystone", "Crested Butte", "Park City", "Heavenly", "Northstar",
    "Kirkwood", "Whistler Blackcomb", "Perisher", "Falls Creek", "Hotham", "Stowe", "Mount Snow", "Okemo",
    "Hunter Mountain", "Mount Sunapee", "Attitash", "Wildcat", "Crotched", "Stevens Pass", "Liberty", "Roundtop", 
    "Whitetail", "Jack Frost", "Big Boulder", "Alpine Valley", "Boston Mills", "Brandywine", "Mad River",
    "Hidden Valley", "Snow Creek", "Wilmot", "Afton Alps", "Mt. Brighton", "Paoli Peaks"
]

def get_optional_value(generator_func):
    """Returns either a generated value or None randomly."""
    return generator_func() if random.choice([True, False]) else None

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

    d = json.dumps(lift_ticket) + '\n'
    sys.stdout.write(d)

if __name__ == "__main__":
    args = sys.argv[1:]
    total_count = int(args[0])
    for _ in range(total_count):
        print_lift_ticket()
    print('')

---------- Forwarded message ---------
From: Pranjal Barse <pranjalbarse2003@gmail.com>
Date: Sat, 22 Feb, 2025, 12:43 am
Subject: Re: python
To: Pranjal Barse <pranjal.barse@saama.com>


import sys
import rapidjson as json
import uuid
import random

from dotenv import load_dotenv
from faker import Faker
from datetime import date, datetime, timezone

load_dotenv()
fake = Faker()

resorts = [
    "Vail", "Beaver Creek", "Breckenridge", "Keystone", "Crested Butte", "Park City", "Heavenly", "Northstar",
    "Kirkwood", "Whistler Blackcomb", "Perisher", "Falls Creek", "Hotham", "Stowe", "Mount Snow", "Okemo",
    "Hunter Mountain", "Mount Sunapee", "Attitash", "Wildcat", "Crotched", "Stevens Pass", "Liberty", "Roundtop",
    "Whitetail", "Jack Frost", "Big Boulder", "Alpine Valley", "Boston Mills", "Brandywine", "Mad River",
    "Hidden Valley", "Snow Creek", "Wilmot", "Afton Alps", "Mt. Brighton", "Paoli Peaks"
]

def get_optional_value(generator_func):
    """Returns either a generated value or None randomly."""
    return generator_func() if random.choice([True, False]) else None

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

    d = json.dumps(lift_ticket) + '\n'
    sys.stdout.write(d)

if __name__ == "__main__":
    args = sys.argv[1:]
    total_count = int(args[0])
    for _ in range(total_count):
        print_lift_ticket()
    print('')