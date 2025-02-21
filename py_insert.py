import os
import sys
import logging
import json
import snowflake.connector
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization

# Load environment variables
load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.WARN)
snowflake.connector.paramstyle = 'qmark'

def load_private_key():
    """Load and deserialize the private key from environment variables."""
    try:
        private_key_str = os.getenv("PRIVATE_KEY", "").replace("\\n", "\n").strip()
        if not private_key_str:
            raise ValueError("PRIVATE_KEY environment variable is empty or not set.")

        private_key_bytes = private_key_str.encode("utf-8")

        private_key = serialization.load_pem_private_key(
            private_key_bytes,
            password=None  # Ensure no password is needed
        )

        return private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    except Exception as e:
        logging.error(f"Error loading private key: {e}")
        sys.exit(1)

def connect_snow():
    """Establish a connection to Snowflake using the private key."""
    private_key = load_private_key()

    try:
        return snowflake.connector.connect(
            account=os.getenv("SNOWFLAKE_ACCOUNT"),
            user=os.getenv("SNOWFLAKE_USER"),
            private_key=private_key,
            role="INGEST",
            database="INGEST",
            schema="INGEST",
            warehouse="INGEST",
            session_parameters={'QUERY_TAG': 'py-insert'},
        )
    except Exception as e:
        logging.error(f"Snowflake connection error: {e}")
        sys.exit(1)

def save_to_snowflake(snow, message):
    """Insert a record into Snowflake from a JSON message."""
    try:
        record = json.loads(message)
        logging.debug("Inserting record into database")

        row = (
            record.get('txid'),
            record.get('rfid'),
            record.get('resort'),
            record.get('purchase_time'),
            record.get('expiration_time'),
            record.get('days'),
            record.get('name'),
            json.dumps(record.get('address', {})),
            record.get('phone'),
            record.get('email'),
            json.dumps(record.get('emergency_contact', {}))
        )

        query = """
        INSERT INTO LIFT_TICKETS_PY_INSERT
        ("TXID", "RFID", "RESORT", "PURCHASE_TIME", "EXPIRATION_TIME", "DAYS", "NAME", "ADDRESS", "PHONE", "EMAIL", "EMERGENCY_CONTACT")
        SELECT ?, ?, ?, ?, ?, ?, ?, PARSE_JSON(?), ?, ?, PARSE_JSON(?)
        """

        with snow.cursor() as cur:
            cur.execute(query, row)

        logging.debug(f"Inserted ticket: {record}")

    except Exception as e:
        logging.error(f"Error inserting record: {e}")

if __name__ == "__main__":
    with connect_snow() as snow:
        for message in sys.stdin:
            if message.strip():  # Ignore empty lines
                save_to_snowflake(snow, message)
        logging.info("Ingestion complete")

