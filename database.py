# import sqlite3
# import tkinter as tk
# from tkinter import messagebox

# def initialize_db():
#     conn = sqlite3.connect("bus_reservation.db")
#     cursor = conn.cursor()

#     # Create buses table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS buses (
#             bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             bus_number TEXT NOT NULL,
#             source TEXT NOT NULL,
#             destination TEXT NOT NULL,
#             capacity INTEGER NOT NULL,
#             available_seats INTEGER NOT NULL
#         )
#     ''')

#     # Create reservations table
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS reservations (
#             reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
#             bus_id INTEGER NOT NULL,
#             passenger_name TEXT NOT NULL,
#             seats_booked INTEGER NOT NULL,
#             FOREIGN KEY (bus_id) REFERENCES buses (bus_id)
#         )
#     ''')

#     conn.commit()
#     conn.close()

# def add_bus_gui():
#     def add_bus():
#         bus_number = bus_number_entry.get()
#         source = source_entry.get()
#         destination = destination_entry.get()
#         try:
#             capacity = int(capacity_entry.get())
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Capacity must be a number")
#             return

#         conn = sqlite3.connect("bus_reservation.db")
#         cursor = conn.cursor()
#         cursor.execute('''
#             INSERT INTO buses (bus_number, source, destination, capacity, available_seats)
#             VALUES (?, ?, ?, ?, ?)
#         ''', (bus_number, source, destination, capacity, capacity))
#         conn.commit()
#         conn.close()

#         messagebox.showinfo("Success", "Bus added successfully!")
#         add_bus_window.destroy()

#     add_bus_window = tk.Toplevel()
#     add_bus_window.title("Add Bus")

#     tk.Label(add_bus_window, text="Bus Number:").grid(row=0, column=0)
#     bus_number_entry = tk.Entry(add_bus_window)
#     bus_number_entry.grid(row=0, column=1)

#     tk.Label(add_bus_window, text="Source:").grid(row=1, column=0)
#     source_entry = tk.Entry(add_bus_window)
#     source_entry.grid(row=1, column=1)

#     tk.Label(add_bus_window, text="Destination:").grid(row=2, column=0)
#     destination_entry = tk.Entry(add_bus_window)
#     destination_entry.grid(row=2, column=1)

#     tk.Label(add_bus_window, text="Capacity:").grid(row=3, column=0)
#     capacity_entry = tk.Entry(add_bus_window)
#     capacity_entry.grid(row=3, column=1)

#     tk.Button(add_bus_window, text="Add Bus", command=add_bus).grid(row=4, column=0, columnspan=2)

# def view_buses_gui():
#     conn = sqlite3.connect("bus_reservation.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM buses")
#     buses = cursor.fetchall()
#     conn.close()

#     view_window = tk.Toplevel()
#     view_window.title("Available Buses")

#     if not buses:
#         tk.Label(view_window, text="No buses available.").pack()
#     else:
#         for bus in buses:
#             bus_info = f"ID: {bus[0]}, Number: {bus[1]}, Source: {bus[2]}, Destination: {bus[3]}, Capacity: {bus[4]}, Available Seats: {bus[5]}"
#             tk.Label(view_window, text=bus_info).pack()

# def book_ticket_gui():
#     def book_ticket():
#         try:
#             bus_id = int(bus_id_entry.get())
#             seats_to_book = int(seats_entry.get())
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Bus ID and Seats must be numbers")
#             return

#         passenger_name = name_entry.get()
#         conn = sqlite3.connect("bus_reservation.db")
#         cursor = conn.cursor()

#         cursor.execute("SELECT available_seats FROM buses WHERE bus_id = ?", (bus_id,))
#         result = cursor.fetchone()

#         if result and result[0] >= seats_to_book:
#             cursor.execute('''
#                 INSERT INTO reservations (bus_id, passenger_name, seats_booked)
#                 VALUES (?, ?, ?)
#             ''', (bus_id, passenger_name, seats_to_book))
#             cursor.execute('''
#                 UPDATE buses SET available_seats = available_seats - ? WHERE bus_id = ?
#             ''', (seats_to_book, bus_id))
#             conn.commit()
#             messagebox.showinfo("Success", "Booking successful!")
#             book_ticket_window.destroy()
#         else:
#             messagebox.showerror("Error", "Not enough seats available.")

#         conn.close()

#     book_ticket_window = tk.Toplevel()
#     book_ticket_window.title("Book Ticket")

#     tk.Label(book_ticket_window, text="Bus ID:").grid(row=0, column=0)
#     bus_id_entry = tk.Entry(book_ticket_window)
#     bus_id_entry.grid(row=0, column=1)

#     tk.Label(book_ticket_window, text="Passenger Name:").grid(row=1, column=0)
#     name_entry = tk.Entry(book_ticket_window)
#     name_entry.grid(row=1, column=1)

#     tk.Label(book_ticket_window, text="Seats to Book:").grid(row=2, column=0)
#     seats_entry = tk.Entry(book_ticket_window)
#     seats_entry.grid(row=2, column=1)

#     tk.Button(book_ticket_window, text="Book", command=book_ticket).grid(row=3, column=0, columnspan=2)

# def cancel_reservation_gui():
#     def cancel_reservation():
#         try:
#             reservation_id = int(reservation_id_entry.get())
#         except ValueError:
#             messagebox.showerror("Invalid Input", "Reservation ID must be a number")
#             return

#         conn = sqlite3.connect("bus_reservation.db")
#         cursor = conn.cursor()
#         cursor.execute("SELECT bus_id, seats_booked FROM reservations WHERE reservation_id = ?", (reservation_id,))
#         result = cursor.fetchone()

#         if result:
#             bus_id, seats_booked = result
#             cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id,))
#             cursor.execute("UPDATE buses SET available_seats = available_seats + ? WHERE bus_id = ?", (seats_booked, bus_id))
#             conn.commit()
#             messagebox.showinfo("Success", "Reservation canceled successfully!")
#             cancel_reservation_window.destroy()
#         else:
#             messagebox.showerror("Error", "Reservation not found.")

#         conn.close()

#     cancel_reservation_window = tk.Toplevel()
#     cancel_reservation_window.title("Cancel Reservation")

#     tk.Label(cancel_reservation_window, text="Reservation ID:").grid(row=0, column=0)
#     reservation_id_entry = tk.Entry(cancel_reservation_window)
#     reservation_id_entry.grid(row=0, column=1)

#     tk.Button(cancel_reservation_window, text="Cancel", command=cancel_reservation).grid(row=1, column=0, columnspan=2)

# def main():
#     initialize_db()

#     root = tk.Tk()
#     root.title("Bus Reservation System")

#     tk.Label(root, text="Bus Reservation System", font=("Arial", 16)).pack(pady=10)

#     tk.Button(root, text="Add Bus", command=add_bus_gui).pack(pady=5)
#     tk.Button(root, text="View Buses", command=view_buses_gui).pack(pady=5)
#     tk.Button(root, text="Book Ticket", command=book_ticket_gui).pack(pady=5)
#     tk.Button(root, text="Cancel Reservation", command=cancel_reservation_gui).pack(pady=5)

#     root.mainloop()

# if __name__ == "__main__":
#     main()
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage

def initialize_db():
    conn = sqlite3.connect("bus_reservation.db")
    cursor = conn.cursor()

    # Enable foreign key checks in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create operator table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operator (
            opr_id TEXT PRIMARY KEY,
            name TEXT,
            address TEXT,
            phone TEXT CHECK(length(phone) = 10),
            email TEXT
        )
    ''')

    # Create route table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS route (
            r_id TEXT PRIMARY KEY,
            s_name TEXT,
            s_id TEXT,
            e_name TEXT,
            e_id TEXT
        )
    ''')

    # Create bus table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus (
            bus_id TEXT PRIMARY KEY,
            bus_type TEXT,
            capacity INTEGER,
            fair INTEGER,
            op_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            FOREIGN KEY (op_id) REFERENCES operator (opr_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (route_id) REFERENCES route (r_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    # Create running table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS running (
            b_id TEXT,
            run_date DATE,
            seat_avail INTEGER,
            PRIMARY KEY (b_id, run_date),
            FOREIGN KEY (b_id) REFERENCES bus (bus_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    # Create booking_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_history (
            name TEXT,
            gender TEXT CHECK(gender IN ('M', 'F', 'O')),
            no_of_seat INTEGER,
            phone TEXT CHECK(length(phone) = 10),
            age INTEGER,
            booking_ref TEXT PRIMARY KEY,
            booking_date DATE,
            travel_date DATE,
            bid TEXT,
            FOREIGN KEY (bid) REFERENCES bus (bus_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def check_booking_gui():
    # Placeholder for "Check Booking" functionality
    messagebox.showinfo("Info", "Check Booking feature coming soon!")

def find_bus_gui():
    # Placeholder for "Find Bus" functionality
    messagebox.showinfo("Info", "Find Bus feature coming soon!")

def admin_gui():
    # Create a new window for the Admin Panel
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("400x400")  # Set the size of the admin window

    # Add buttons to the Admin Panel
    tk.Button(admin_window, text="New Operator", font=("Arial", 14), command=new_operator_gui).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(admin_window, text="New Bus", font=("Arial", 14), command=new_bus_gui).place(relx=0.5, rely=0.45, anchor='center')
    tk.Button(admin_window, text="New Route", font=("Arial", 14), command=new_route_gui).place(relx=0.5, rely=0.6, anchor='center')
    tk.Button(admin_window, text="New Run", font=("Arial", 14), command=new_run_gui).place(relx=0.5, rely=0.75, anchor='center')

def new_operator_gui():
    # Placeholder for "New Operator" functionality
    messagebox.showinfo("Info", "New Operator feature coming soon!")
def new_operator_gui():
    # Create a new window for managing operators
    operator_window = tk.Toplevel()
    operator_window.title("Manage Operators")
    operator_window.geometry("500x450")  # Set the size of the operator window

    # Labels and Entry widgets for operator details
    tk.Label(operator_window, text="Operator ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Address:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Phone:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Email:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Entry widgets for user input
    opr_id_entry = tk.Entry(operator_window, font=("Arial", 12))
    name_entry = tk.Entry(operator_window, font=("Arial", 12))
    address_entry = tk.Entry(operator_window, font=("Arial", 12))
    phone_entry = tk.Entry(operator_window, font=("Arial", 12))
    email_entry = tk.Entry(operator_window, font=("Arial", 12))

    opr_id_entry.grid(row=0, column=1, padx=10, pady=10)
    name_entry.grid(row=1, column=1, padx=10, pady=10)
    address_entry.grid(row=2, column=1, padx=10, pady=10)
    phone_entry.grid(row=3, column=1, padx=10, pady=10)
    email_entry.grid(row=4, column=1, padx=10, pady=10)

    # Function to add a new operator
    def add_operator():
        opr_id = opr_id_entry.get().strip()
        name = name_entry.get().strip()
        address = address_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not (opr_id and name and address and phone and email):
            messagebox.showerror("Error", "All fields are required!")
            return

        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Insert data into operator table
            cursor.execute('''
                INSERT INTO operator (opr_id, name, address, phone, email)
                VALUES (?, ?, ?, ?, ?)
            ''', (opr_id, name, address, phone, email))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Operator added successfully!")
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Operator ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to edit an existing operator
    def edit_operator():
        opr_id = opr_id_entry.get().strip()
        name = name_entry.get().strip()
        address = address_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not (opr_id and name and address and phone and email):
            messagebox.showerror("Error", "All fields are required!")
            return

        if len(phone) != 10 or not phone.isdigit():
            messagebox.showerror("Error", "Phone number must be 10 digits!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Update data in operator table
            cursor.execute('''
                UPDATE operator
                SET name = ?, address = ?, phone = ?, email = ?
                WHERE opr_id = ?
            ''', (name, address, phone, email, opr_id))

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "No operator found with the given ID!")
            else:
                messagebox.showinfo("Success", "Operator updated successfully!")

            conn.commit()
            conn.close()
            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to clear all entry fields
    def clear_entries():
        opr_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    # Function to show all operators in a new window
    def show_all_operators():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM operator")
        operators = cursor.fetchall()
        conn.close()

        # Create a new window to display operators
        show_window = tk.Toplevel()
        show_window.title("All Operators")
        show_window.geometry("600x400")

        # Create a scrollable text area
        text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

        # Add operator details to the text area
        if operators:
            for operator in operators:
                text_area.insert(tk.END, f"Operator ID: {operator[0]}\n")
                text_area.insert(tk.END, f"Name: {operator[1]}\n")
                text_area.insert(tk.END, f"Address: {operator[2]}\n")
                text_area.insert(tk.END, f"Phone: {operator[3]}\n")
                text_area.insert(tk.END, f"Email: {operator[4]}\n")
                text_area.insert(tk.END, "-" * 40 + "\n")
        else:
            text_area.insert(tk.END, "No operators found.")

    # Add buttons for Add, Edit, and Show All Operators
    tk.Button(operator_window, text="Add Operator", font=("Arial", 12), command=add_operator).grid(row=5, column=0, pady=20)
    tk.Button(operator_window, text="Edit Operator", font=("Arial", 12), command=edit_operator).grid(row=5, column=1, pady=20)
    tk.Button(operator_window, text="Show All Operators", font=("Arial", 12), command=show_all_operators).grid(row=6, column=0, columnspan=2, pady=10)

def new_bus_gui():
    # Create a new window for managing buses
    bus_window = tk.Toplevel()
    bus_window.title("Manage Buses")
    bus_window.geometry("800x600")  # Increased size for better layout

    # Labels and Entry widgets for bus details
    tk.Label(bus_window, text="Bus ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Bus Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Capacity:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Operator ID:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Route ID:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Entry widgets for user input
    bus_id_entry = tk.Entry(bus_window, font=("Arial", 12))
    bus_type_entry = tk.Entry(bus_window, font=("Arial", 12))
    capacity_entry = tk.Entry(bus_window, font=("Arial", 12))

    # Dropdowns for foreign keys
    operator_var = tk.StringVar(bus_window)
    route_var = tk.StringVar(bus_window)

    bus_id_entry.grid(row=0, column=1, padx=10, pady=10)
    bus_type_entry.grid(row=1, column=1, padx=10, pady=10)
    capacity_entry.grid(row=2, column=1, padx=10, pady=10)

    operator_menu = tk.OptionMenu(bus_window, operator_var, "")
    operator_menu.grid(row=3, column=1, padx=10, pady=10)

    route_menu = tk.OptionMenu(bus_window, route_var, "")
    route_menu.grid(row=4, column=1, padx=10, pady=10)

    # Function to populate dropdowns with data from operator and route tables
    def populate_dropdowns():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        # Fetch operator IDs and names
        cursor.execute("SELECT opr_id, name FROM operator")
        operators = cursor.fetchall()
        if operators:
            operator_menu['menu'].delete(0, 'end')
            for opr_id, name in operators:
                operator_menu['menu'].add_command(label=f"{opr_id} - {name}", command=lambda value=f"{opr_id}": operator_var.set(value))
        else:
            operator_var.set("No Operators Available")
            operator_menu['menu'].add_command(label="No Operators Available")

        # Fetch route IDs and details
        cursor.execute("SELECT r_id, s_name, e_name FROM route")
        routes = cursor.fetchall()
        if routes:
            route_menu['menu'].delete(0, 'end')
            for r_id, s_name, e_name in routes:
                route_menu['menu'].add_command(label=f"{r_id} - {s_name} to {e_name}", command=lambda value=f"{r_id}": route_var.set(value))
        else:
            route_var.set("No Routes Available")
            route_menu['menu'].add_command(label="No Routes Available")

        conn.close()

    populate_dropdowns()

    # Function to add a new bus
    def add_bus():
        bus_id = bus_id_entry.get().strip()
        bus_type = bus_type_entry.get().strip()
        capacity = capacity_entry.get().strip()
        op_id = operator_var.get().strip()
        route_id = route_var.get().strip()

        if not (bus_id and bus_type and capacity and op_id and route_id):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            capacity = int(capacity)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a numeric value!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Insert data into bus table
            cursor.execute('''
                INSERT INTO bus (bus_id, bus_type, capacity, op_id, route_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (bus_id, bus_type, capacity, op_id.split(" ")[0], route_id.split(" ")[0]))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Bus added successfully!")
            clear_entries()
            populate_dropdowns()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bus ID already exists or invalid Operator/Route ID!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to clear all entry fields
    def clear_entries():
        bus_id_entry.delete(0, tk.END)
        bus_type_entry.delete(0, tk.END)
        capacity_entry.delete(0, tk.END)
        operator_var.set("")
        route_var.set("")

    # Add buttons for Add and Clear
    tk.Button(bus_window, text="Add Bus", font=("Arial", 12), command=add_bus).grid(row=5, column=0, pady=20)
    tk.Button(bus_window, text="Clear", font=("Arial", 12), command=clear_entries).grid(row=5, column=1, pady=20)

    # Function to show all buses
    def show_all_buses():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        # Join bus table with operator and route tables
        cursor.execute('''
            SELECT b.bus_id, b.bus_type, b.capacity, o.name AS operator_name, r.s_name || " to " || r.e_name AS route_details
            FROM bus b
            JOIN operator o ON b.op_id = o.opr_id
            JOIN route r ON b.route_id = r.r_id
        ''')
        buses = cursor.fetchall()
        conn.close()

        # Create a new window to display all buses
        show_window = tk.Toplevel()
        show_window.title("All Buses")
        show_window.geometry("800x500")

        # Create a scrollable text area
        text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

        # Add bus details to the text area
        if buses:
            for bus in buses:
                text_area.insert(tk.END, f"Bus ID: {bus[0]}\n")
                text_area.insert(tk.END, f"Bus Type: {bus[1]}\n")
                text_area.insert(tk.END, f"Capacity: {bus[2]}\n")
                text_area.insert(tk.END, f"Operator: {bus[3]}\n")
                text_area.insert(tk.END, f"Route: {bus[4]}\n")
                text_area.insert(tk.END, "-" * 50 + "\n")
        else:
            text_area.insert(tk.END, "No buses found.")

    # Add a button to show all buses
    tk.Button(bus_window, text="Show All Buses", font=("Arial", 12), command=show_all_buses).grid(row=6, column=0, columnspan=2, pady=10)

def new_route_gui():
    # Placeholder for "New Route" functionality
    messagebox.showinfo("Info", "New Route feature coming soon!")

def new_run_gui():
    # Placeholder for "New Run" functionality
    messagebox.showinfo("Info", "New Run feature coming soon!")

def main():
    initialize_db()

    root = tk.Tk()
    root.title("Bus Reservation System")
    root.geometry("600x500")  # Set the size of the window

    # Add an image to the home page
    image = PhotoImage(file="C:\\Users\\ratho\\OneDrive\\Desktop\\bus booking\\Bus-Booking\\Bus_for_project.png")
    image_label = tk.Label(root, image=image)
    image_label.place(relx=0.5, rely=0.2, anchor='center')  # Center the image at 20% of the window height

    # Add buttons for Check Booking, Find Bus, and Admin
    tk.Button(root, text="Check Booking", font=("Arial", 14), command=check_booking_gui).place(relx=0.5, rely=0.5, anchor='center')
    tk.Button(root, text="Find Bus", font=("Arial", 14), command=find_bus_gui).place(relx=0.5, rely=0.6, anchor='center')
    tk.Button(root, text="Admin", font=("Arial", 14), command=admin_gui).place(relx=0.5, rely=0.7, anchor='center')

    root.mainloop()

if __name__ == "__main__":
    main()

