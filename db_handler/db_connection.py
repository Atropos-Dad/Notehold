import sqlite3
from sqlite3 import Error
import os

DB_FILE = "database.db"
SCHEMA_FILE = "schema.sql"

class SingletonDBConnection:
    _instance = None
    connection = None  # Class-level attribute initialization

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SingletonDBConnection, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        if self.connection is None:  # Only initialize if not already connected
            self.connection = self._create_connection(DB_FILE)
            if self.connection:
                self.connection.row_factory = sqlite3.Row  # Enable row factory for named columns

    def _create_connection(self, db_file):
        try:
            db_exists = os.path.exists(db_file)
            conn = sqlite3.connect(db_file, check_same_thread=False)
            print(f"Connection to SQLite DB successful: {db_file}")
            if not db_exists:
                self._initialize_database(conn)
            return conn
        except Error as e:
            print(f"Error: '{e}' occurred while connecting to SQLite DB")
            return None

    def _initialize_database(self, conn):
        print("Initializing database")
        try:
            with open(SCHEMA_FILE, 'r') as schema_file:
                conn.executescript(schema_file.read())
                conn.commit()
            print(f"Database initialized with schema from {SCHEMA_FILE}")
        except Error as e:
            print(f"Error: '{e}' occurred while initializing the database")
        except FileNotFoundError:
            print(f"Schema file {SCHEMA_FILE} not found")

    def get_connection(self):
        if self.connection is None:
            self._initialize()
        return self.connection

    def cleanup(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def __del__(self):
        self.cleanup()

# Usage example:
# db = SingletonDBConnection()
# connection = db.get_connection()
