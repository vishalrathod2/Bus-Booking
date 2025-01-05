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
    # Create a new window for managing routes
    route_window = tk.Toplevel()
    route_window.title("Manage Routes")
    route_window.geometry("800x600")  # Set the size of the window

    # Labels and Entry widgets for route details
    tk.Label(route_window, text="Route ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="Start Location Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="Start Location ID:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="End Location Name:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="End Location ID:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

    # Entry widgets for user input
    route_id_entry = tk.Entry(route_window, font=("Arial", 12))
    start_name_entry = tk.Entry(route_window, font=("Arial", 12))
    start_id_entry = tk.Entry(route_window, font=("Arial", 12))
    end_name_entry = tk.Entry(route_window, font=("Arial", 12))
    end_id_entry = tk.Entry(route_window, font=("Arial", 12))

    # Place Entry widgets in the grid
    route_id_entry.grid(row=0, column=1, padx=10, pady=10)
    start_name_entry.grid(row=1, column=1, padx=10, pady=10)
    start_id_entry.grid(row=2, column=1, padx=10, pady=10)
    end_name_entry.grid(row=3, column=1, padx=10, pady=10)
    end_id_entry.grid(row=4, column=1, padx=10, pady=10)

    # Function to add a new route
    def add_route():
        r_id = route_id_entry.get().strip()
        s_name = start_name_entry.get().strip()
        s_id = start_id_entry.get().strip()
        e_name = end_name_entry.get().strip()
        e_id = end_id_entry.get().strip()

        if not (r_id and s_name and s_id and e_name and e_id):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Insert data into the route table
            cursor.execute('''
                INSERT INTO route (r_id, s_name, s_id, e_name, e_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (r_id, s_name, s_id, e_name, e_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Route added successfully!")
            clear_entries()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Route ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to edit an existing route
    def edit_route():
        r_id = route_id_entry.get().strip()
        s_name = start_name_entry.get().strip()
        s_id = start_id_entry.get().strip()
        e_name = end_name_entry.get().strip()
        e_id = end_id_entry.get().strip()

        if not (r_id and s_name and s_id and e_name and e_id):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Update the existing route
            cursor.execute('''
                UPDATE route
                SET s_name = ?, s_id = ?, e_name = ?, e_id = ?
                WHERE r_id = ?
            ''', (s_name, s_id, e_name, e_id, r_id))

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Route ID not found!")
            else:
                messagebox.showinfo("Success", "Route updated successfully!")

            conn.commit()
            conn.close()

            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to clear all entry fields
    def clear_entries():
        route_id_entry.delete(0, tk.END)
        start_name_entry.delete(0, tk.END)
        start_id_entry.delete(0, tk.END)
        end_name_entry.delete(0, tk.END)
        end_id_entry.delete(0, tk.END)

    # Function to show all routes
    def show_all_routes():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        # Fetch all routes from the route table
        cursor.execute('''
            SELECT r_id, s_name, s_id, e_name, e_id FROM route
        ''')
        routes = cursor.fetchall()
        conn.close()

        # Create a new window to display all routes
        show_window = tk.Toplevel()
        show_window.title("All Routes")
        show_window.geometry("800x500")

        # Create a scrollable text area
        text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

        # Add route details to the text area
        if routes:
            for route in routes:
                text_area.insert(tk.END, f"Route ID: {route[0]}\n")
                text_area.insert(tk.END, f"Start Location Name: {route[1]}\n")
                text_area.insert(tk.END, f"Start Location ID: {route[2]}\n")
                text_area.insert(tk.END, f"End Location Name: {route[3]}\n")
                text_area.insert(tk.END, f"End Location ID: {route[4]}\n")
                text_area.insert(tk.END, "-" * 50 + "\n")
        else:
            text_area.insert(tk.END, "No routes found.")

    # Add buttons for Add, Edit, and Show All Routes
    tk.Button(route_window, text="Add Route", font=("Arial", 12), command=add_route).grid(row=5, column=0, pady=20)
    tk.Button(route_window, text="Edit Route", font=("Arial", 12), command=edit_route).grid(row=5, column=1, pady=20)
    tk.Button(route_window, text="Clear", font=("Arial", 12), command=clear_entries).grid(row=6, column=0, pady=20)
    tk.Button(route_window, text="Show All Routes", font=("Arial", 12), command=show_all_routes).grid(row=6, column=1, pady=20)

def new_run_gui():
    # Create a new window for managing running buses
    run_window = tk.Toplevel()
    run_window.title("Manage Running Buses")
    run_window.geometry("800x600")  # Set the size of the window

    # Labels and Entry widgets for running details
    tk.Label(run_window, text="Bus ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(run_window, text="Run Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(run_window, text="Seats Available:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')

    # Entry widgets for user input
    bus_id_entry = tk.Entry(run_window, font=("Arial", 12))
    run_date_entry = tk.Entry(run_window, font=("Arial", 12))
    seat_avail_entry = tk.Entry(run_window, font=("Arial", 12))

    # Place Entry widgets in the grid
    bus_id_entry.grid(row=0, column=1, padx=10, pady=10)
    run_date_entry.grid(row=1, column=1, padx=10, pady=10)
    seat_avail_entry.grid(row=2, column=1, padx=10, pady=10)

    # Function to add a new running bus
    def add_running():
        b_id = bus_id_entry.get().strip()
        run_date = run_date_entry.get().strip()
        seat_avail = seat_avail_entry.get().strip()

        if not (b_id and run_date and seat_avail):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            seat_avail = int(seat_avail)  # Ensure seat availability is a valid integer
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Insert data into the running table
            cursor.execute(''' 
                INSERT INTO running (b_id, run_date, seat_avail)
                VALUES (?, ?, ?)
            ''', (b_id, run_date, seat_avail))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Running bus added successfully!")
            clear_entries() # type: ignore
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bus ID or Run Date already exists, or invalid Bus ID!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to edit an existing running bus
    def edit_running():
        b_id = bus_id_entry.get().strip()
        run_date = run_date_entry.get().strip()
        seat_avail = seat_avail_entry.get().strip()

        if not (b_id and run_date and seat_avail):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            seat_avail = int(seat_avail)  # Ensure seat availability is a valid integer
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Update the existing running bus
            cursor.execute('''
                UPDATE running
                SET seat_avail = ?
                WHERE b_id = ? AND run_date = ?
            ''', (seat_avail, b_id, run_date))

            if cursor.rowcount == 0:
                messagebox.showerror("Error", "Bus ID or Run Date not found!")
            else:
                messagebox.showinfo("Success", "Running bus updated successfully!")

            conn.commit()
            conn.close()

            clear_entries() # type: ignore
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Function to show all running buses
    def show_all_running():
        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Fetch all running buses from the running table
            cursor.execute('''
                SELECT r.b_id, b.bus_type, r.run_date, r.seat_avail
                FROM running r
                JOIN bus b ON r.b_id = b.bus_id
            ''')
            running_buses = cursor.fetchall()
            conn.close()

            # Create a new window to display all running buses
            show_window = tk.Toplevel()
            show_window.title("All Running Buses")
            show_window.geometry("800x500")

            # Create a scrollable text area
            text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
            text_area.pack(expand=True, fill=tk.BOTH)

            # Add running bus details to the text area
            if running_buses:
                for bus in running_buses:
                    text_area.insert(tk.END, f"Bus ID: {bus[0]}\n")
                    text_area.insert(tk.END, f"Bus Type: {bus[1]}\n")
                    text_area.insert(tk.END, f"Run Date: {bus[2]}\n")
                    text_area.insert(tk.END, f"Seats Available: {bus[3]}\n")
                    text_area.insert(tk.END, "-" * 50 + "\n")
            else:
                text_area.insert(tk.END, "No running buses found.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Add buttons for managing running buses
    tk.Button(run_window, text="Add Running Bus", font=("Arial", 12), command=add_running).grid(row=3, column=0, pady=20)
    tk.Button(run_window, text="Edit Running Bus", font=("Arial", 12), command=edit_running).grid(row=4, column=0, pady=20)
    tk.Button(run_window, text="Show All Running Buses", font=("Arial", 12), command=show_all_running).grid(row=5, column=0, pady=20)


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

