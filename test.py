
# import sqlite3

# def delete_all_records():
#     try:
#         conn = sqlite3.connect("bus_reservation.db")
#         cursor = conn.cursor()

#         # Enable foreign key constraints
#         cursor.execute("PRAGMA foreign_keys = ON;")

#         # Delete from child tables first to prevent foreign key issues
#         cursor.execute("DELETE FROM booking;")
#         cursor.execute("DELETE FROM running;")
#         cursor.execute("DELETE FROM bus;")
#         cursor.execute("DELETE FROM route;")
#         cursor.execute("DELETE FROM operator;")

#         conn.commit()
#         conn.close()

#         print("✅ All records deleted successfully!")

#     except Exception as e:
#         print(f"❌ An error occurred: {e}")

# # Run the function
# delete_all_records()
from logging import root

import sqlite3

def show_all_records():
    try:
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        # List of tables to fetch data from
        tables = ["operator", "route", "bus", "running", "booking"]

        for table in tables:
            print(f"\n🔹 Records from {table}:")
            cursor.execute(f"SELECT * FROM {table};")
            records = cursor.fetchall()
            
            if records:
                for row in records:
                    print(row)
            else:
                print("No records found.")

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the function
show_all_records()

