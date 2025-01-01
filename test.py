from tkinter import *
import sqlite3
from tkinter.messagebox import *
from datetime import date
def create_tables():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect("bus_management.db")
    cursor = connection.cursor()

    try:
        # Create 'bus' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus (
            bus_id VARCHAR(5) NOT NULL PRIMARY KEY,
            bus_type VARCHAR(10),
            capacity INT,
            fair INT,
            op_id VARCHAR(5) NOT NULL,
            route_id VARCHAR(5) NOT NULL,
            FOREIGN KEY(op_id) REFERENCES operator(opr_id),
            FOREIGN KEY(route_id) REFERENCES route(r_id)
        )
        ''')

        # Create 'operator' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS operator (
            opr_id VARCHAR(5) PRIMARY KEY,
            name VARCHAR(20),
            address VARCHAR(50),
            phone CHAR(10),
            email VARCHAR(30)
        )
        ''')

        # Create 'running' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS running (
            b_id VARCHAR(5),
            run_date DATE,
            seat_avail INT,
            FOREIGN KEY(b_id) REFERENCES bus(bus_id)
        )
        ''')

        # Create 'route' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS route (
            r_id VARCHAR(5) NOT NULL PRIMARY KEY,
            s_name VARCHAR(20),
            s_id VARCHAR(5),
            e_name VARCHAR(20),
            e_id VARCHAR(5)
        )
        ''')

        # Create 'booking_history' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_history (
            name VARCHAR(20),
            gender CHAR(1),
            no_of_seat INT,
            phone CHAR(10),
            age INT,
            booking_ref VARCHAR(10) NOT NULL PRIMARY KEY,
            booking_date DATE,
            travel_date DATE,
            bid VARCHAR(5),
            FOREIGN KEY(bid) REFERENCES bus(bus_id)
        )
        ''')

        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Commit the changes and close the connection
        connection.commit()
        connection.close()

