import sqlite3
import tkinter as tk
from tkinter import messagebox 
from tkinter import PhotoImage
from tkinter import ttk
from tkcalendar import DateEntry
def initialize_db():
    conn = sqlite3.connect("bus_reservation.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operator (
            opr_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            address TEXT,
            phone TEXT CHECK(length(phone) = 10),
            email TEXT UNIQUE
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS route (
            r_id TEXT PRIMARY KEY,
            s_name TEXT NOT NULL,
            s_id TEXT NOT NULL,
            e_name TEXT NOT NULL,
            e_id TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bus (
            bus_id TEXT PRIMARY KEY,
            bus_type TEXT NOT NULL,
            capacity INTEGER NOT NULL CHECK(capacity > 0),
            op_id TEXT NOT NULL,
            route_id TEXT NOT NULL,
            FOREIGN KEY (op_id) REFERENCES operator (opr_id) ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (route_id) REFERENCES route (r_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS running (
            b_id TEXT NOT NULL,
            run_date DATE NOT NULL,
            seat_avail INTEGER NOT NULL CHECK(seat_avail >= 0),
            PRIMARY KEY (b_id, run_date),
            FOREIGN KEY (b_id) REFERENCES bus (bus_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
           
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            b_id TEXT NOT NULL,
            run_date DATE NOT NULL,
            user_name TEXT NOT NULL,
            contact TEXT NOT NULL CHECK(length(contact) = 10),
            seat_number INTEGER NOT NULL CHECK(seat_number > 0),
            UNIQUE (b_id, run_date, seat_number),  -- Ensure each seat is booked only once per bus run
            UNIQUE (b_id, run_date, user_name, contact),  -- Ensure one user cannot book multiple times per run
            FOREIGN KEY (b_id) REFERENCES bus (bus_id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')
   
    conn.commit()
    conn.close()
def check_booking_gui():
    # Main window for checking bookings
    root = tk.Tk()
    root.title("Check Booking")
    root.geometry("400x300")

    tk.Label(root, text="Check Booking", font=("Arial", 20, "bold")).pack(pady=10)

    tk.Label(root, text="Enter Contact Number:", font=("Arial", 12)).pack(pady=5)
    contact_entry = tk.Entry(root, font=("Arial", 12), width=30)
    contact_entry.pack(pady=5)

    def check_booking():
        contact = contact_entry.get().strip()
        if not contact:
            messagebox.showerror("Error", "Contact number is required!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            # Query to check bookings by contact
            cursor.execute("""
            SELECT 
                b.booking_id, b.b_id, b.run_date, b.user_name, b.seat_number, bus.bus_type 
            FROM 
                booking b
            JOIN 
                bus ON b.b_id = bus.bus_id
            WHERE 
                b.contact = ?;
            """, (contact,))
            bookings = cursor.fetchall()
            conn.close()

            if bookings:
                display_bookings(bookings)
            else:
                messagebox.showinfo("No Bookings Found", "No bookings found for this contact number.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_bookings(bookings):
        booking_window = tk.Toplevel(root)
        booking_window.title("Booking Details")
        booking_window.geometry("600x300")

        tk.Label(booking_window, text="Your Bookings", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("Booking ID", "Bus ID", "Run Date", "User Name", "Seat Number", "Bus Type")
        tree = ttk.Treeview(booking_window, columns=columns, show="headings", height=10)
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for booking in bookings:
            tree.insert("", tk.END, values=booking)

        tk.Button(booking_window, text="Close", font=("Arial", 12), command=booking_window.destroy).pack(pady=10)

    tk.Button(root, text="Check Booking", font=("Arial", 14, "bold"), command=check_booking, bg="blue", fg="white").pack(pady=20)

    root.mainloop()
def find_bus_page():
    # Main window
    root = tk.Tk()
    root.title("Find Bus")
    root.geometry("800x500")

    tk.Label(root, text="Find Bus", font=("Arial", 20, "bold")).pack(pady=10)

    input_frame = tk.Frame(root)
    input_frame.pack(pady=20)

    tk.Label(input_frame, text="Source Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(input_frame, text="Destination Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
    tk.Label(input_frame, text="Travel Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="w")

    source_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    destination_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)
    travel_date_entry = tk.Entry(input_frame, font=("Arial", 12), width=30)

    source_entry.grid(row=0, column=1, padx=10, pady=5)
    destination_entry.grid(row=1, column=1, padx=10, pady=5)
    travel_date_entry.grid(row=2, column=1, padx=10, pady=5)

    def search_buses():
        source = source_entry.get().strip()
        destination = destination_entry.get().strip()
        travel_date = travel_date_entry.get().strip()

        if not source or not destination or not travel_date:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            query = '''
                SELECT 
                    b.bus_id, b.bus_type, b.capacity, r.run_date, r.seat_avail
                FROM 
                    bus b
                JOIN 
                    route rt ON b.route_id = rt.r_id
                JOIN 
                    running r ON b.bus_id = r.b_id
                WHERE 
                    rt.s_name = ? AND rt.e_name = ? AND r.run_date = ?
            '''
            cursor.execute(query, (source, destination, travel_date))
            buses = cursor.fetchall()
            conn.close()

            if buses:
                display_buses(buses, travel_date)
            else:
                messagebox.showinfo("No Buses Found", "No buses available for the selected route and date.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def display_buses(buses, travel_date):
        bus_window = tk.Toplevel(root)
        bus_window.title("Available Buses")
        bus_window.geometry("800x400")

        columns = ("Bus ID", "Bus Type", "Capacity", "Run Date", "Seats Available")
        tree = ttk.Treeview(bus_window, columns=columns, show="headings", height=20)
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for bus in buses:
            tree.insert("", tk.END, values=bus)

        def book_ticket():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showerror("Error", "Please select a bus to book a seat!")
                return

            bus_details = tree.item(selected_item, "values")
            if not bus_details:
                messagebox.showerror("Error", "Unable to retrieve bus details!")
                return

            open_booking_form(bus_details, travel_date)

        tk.Button(bus_window, text="Book Ticket", font=("Arial", 12), command=book_ticket).pack(pady=10)

    def open_booking_form(bus_details, travel_date):
        bus_id, bus_type, capacity, run_date, seats_available = bus_details
        capacity = int (capacity)

        booking_window = tk.Toplevel()
        booking_window.title("Book Ticket")
        booking_window.geometry("600x500")

        tk.Label(booking_window, text="Book Ticket", font=("Arial", 20, "bold")).pack(pady=10)
        tk.Label(booking_window, text=f"Bus ID: {bus_id}", font=("Arial", 12)).pack(pady=5)
        tk.Label(booking_window, text=f"Seats Available: {seats_available}", font=("Arial", 12)).pack(pady=5)

        # Create a frame for seat selection
        seat_frame = tk.Frame(booking_window)
        seat_frame.pack(pady=10)

        def get_booked_seats():
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()
            cursor.execute('''SELECT seat_number FROM booking WHERE b_id = ? AND run_date = ?''', (bus_id, travel_date))
            booked_seats ={seat[0] for seat in cursor.fetchall()}
            conn.close()
            return booked_seats

        # Get the booked seats
        booked_seats = get_booked_seats()

        # Create buttons for each seat
        cols = 5
        rows = (capacity // cols) + (1 if capacity % cols != 0 else 0)
        seat_buttons = {}
        for r in range(rows):
            for c in range(cols):
                seat_num = (r * cols) + (c + 1)
                if seat_num > capacity:  # Stop if we exceed the available seats
                  break
                is_booked = seat_num in booked_seats
                seat_button = tk.Button(
                  seat_frame,
                  text=f"{seat_num}",
                  font=("Arial", 10),
                  width=5,
                  bg="red" if is_booked else "green",
                  fg="white",
                  state="disabled" if is_booked else "normal",
                  command=lambda num=seat_num: confirm_booking(bus_id, travel_date, num)
                 )
                seat_button.grid(row=r, column=c, padx=5, pady=5)  # Arrange in grid layout
                seat_buttons[seat_num ] = seat_button  # Store the button in the list
                seat_num += 1
        tk.Label(booking_window, text="User Name:", font=("Arial", 12)).pack(pady=5)
        user_name_entry = tk.Entry(booking_window, font=("Arial", 12))
        user_name_entry.pack(pady=5)

        tk.Label(booking_window, text="Contact:", font=("Arial", 12)).pack(pady=5)
        contact_entry = tk.Entry(booking_window, font=("Arial", 12))
        contact_entry.pack(pady=5)

        # Function to confirm booking
        def confirm_booking(bus_id, travel_date, seat_number):
            user_name = user_name_entry.get().strip()
            contact = contact_entry.get().strip()

            if not user_name or not contact:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                conn = sqlite3.connect("bus_reservation.db")
                cursor = conn.cursor()

                # Check if the user has already booked a seat
                # cursor.execute('''SELECT * FROM booking WHERE b_id = ? AND run_date = ? AND seat_number = ?''',
                #                (bus_id, travel_date, seat_number))
                # existing_booking = cursor.fetchone()

                cursor.execute('''SELECT * FROM booking WHERE b_id = ? AND run_date = ? AND seat_number = ?''', 
                               (bus_id, travel_date, seat_number))
                existing_booking = cursor.fetchone()

                if existing_booking:
                    messagebox.showerror("Error", f"Seat {seat_number} is already booked!")
                    conn.close()
                    return

                # Insert the booking
                cursor.execute('''INSERT INTO booking (b_id, run_date, user_name, contact, seat_number)
                            VALUES (?, ?, ?, ?, ?)''', (bus_id, travel_date, user_name, contact, seat_number))
                # Update the seat availability
                cursor.execute('''UPDATE running SET seat_avail = seat_avail - 1 WHERE b_id = ? AND run_date = ?''',
                           (bus_id, travel_date))

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"Booking confirmed for Seat {seat_number}.")
                booking_window.destroy()

                # Disable the booked seat button
                seat_buttons[seat_number - 1].config(state="disabled",bg="red")
                booking_window.destroy()

  
            except Exception as e:
                messagebox.showerror

       # tk.Button(booking_window, text="Confirm Booking", font=("Arial", 12), command=confirm_booking).pack(pady=20)
            
    tk.Button(root, text="Search Buses", font=("Arial", 14, "bold"), command=search_buses, bg="blue", fg="white").pack(pady=20)

    root.mainloop()
         
def admin_gui():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("400x400")  

    # Button styles with background and foreground colors
    tk.Button(admin_window, text="New Operator", font=("Arial", 14), bg="#4CAF50", fg="white", command=new_operator_gui).place(relx=0.5, rely=0.3, anchor='center')
    tk.Button(admin_window, text="New Bus", font=("Arial", 14), bg="#2196F3", fg="white", command=new_bus_gui).place(relx=0.5, rely=0.45, anchor='center')
    tk.Button(admin_window, text="New Route", font=("Arial", 14), bg="#FF9800", fg="white", command=new_route_gui).place(relx=0.5, rely=0.6, anchor='center')
    tk.Button(admin_window, text="New Run", font=("Arial", 14), bg="#FF5722", fg="white", command=new_run_gui).place(relx=0.5, rely=0.75, anchor='center')

    admin_window.mainloop()

def new_operator_gui():
    operator_window = tk.Toplevel()
    operator_window.title("Manage Operators")
    operator_window.geometry("500x450") 

    tk.Label(operator_window, text="Operator ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Address:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Phone:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(operator_window, text="Email:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

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

    def clear_entries():
        opr_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    def show_all_operators():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM operator")
        operators = cursor.fetchall()
        conn.close()

        show_window = tk.Toplevel()
        show_window.title("All Operators")
        show_window.geometry("600x400")

        text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

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

    tk.Button(operator_window, text="Add Operator", font=("Arial", 12), command=add_operator).grid(row=5, column=0, pady=20)
    tk.Button(operator_window, text="Edit Operator", font=("Arial", 12), command=edit_operator).grid(row=5, column=1, pady=20)
    tk.Button(operator_window, text="Show All Operators", font=("Arial", 12), command=show_all_operators).grid(row=6, column=0, columnspan=2, pady=10)

def new_bus_gui():
    bus_window = tk.Toplevel()
    bus_window.title("Manage Buses")
    bus_window.geometry("800x600") 

    tk.Label(bus_window, text="Bus ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Bus Type:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Capacity:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Operator ID:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(bus_window, text="Route ID:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

    bus_id_entry = tk.Entry(bus_window, font=("Arial", 12))
    bus_type_entry = tk.Entry(bus_window, font=("Arial", 12))
    capacity_entry = tk.Entry(bus_window, font=("Arial", 12))

    operator_var = tk.StringVar(bus_window)
    route_var = tk.StringVar(bus_window)

    bus_id_entry.grid(row=0, column=1, padx=10, pady=10)
    bus_type_entry.grid(row=1, column=1, padx=10, pady=10)
    capacity_entry.grid(row=2, column=1, padx=10, pady=10)

    operator_menu = tk.OptionMenu(bus_window, operator_var, "")
    operator_menu.grid(row=3, column=1, padx=10, pady=10)

    route_menu = tk.OptionMenu(bus_window, route_var, "")
    route_menu.grid(row=4, column=1, padx=10, pady=10)

    def populate_dropdowns():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute("SELECT opr_id, name FROM operator")
        operators = cursor.fetchall()
        if operators:
            operator_menu['menu'].delete(0, 'end')
            for opr_id, name in operators:
                operator_menu['menu'].add_command(label=f"{opr_id} - {name}", command=lambda value=f"{opr_id}": operator_var.set(value))
        else:
            operator_var.set("No Operators Available")
            operator_menu['menu'].add_command(label="No Operators Available")

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

            cursor.execute('''
            INSERT INTO bus (bus_id, bus_type, capacity, op_id, route_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (bus_id, bus_type, capacity, op_id.split(" ")[0], route_id.split(" ")[0]))
            from datetime import datetime, timedelta
            today = datetime.today()
            for i in range(7):  # Next 7 days
              run_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
              cursor.execute('''
                INSERT INTO running (b_id, run_date, seat_avail)
                VALUES (?, ?, ?)
            ''', (bus_id, run_date, capacity))



            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Bus added successfully!")
            clear_entries()
            populate_dropdowns()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bus ID already exists or invalid Operator/Route ID!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    def clear_entries():
        bus_id_entry.delete(0, tk.END)
        bus_type_entry.delete(0, tk.END)
        capacity_entry.delete(0, tk.END)
        operator_var.set("")
        route_var.set("")
    tk.Button(bus_window, text="Add Bus", font=("Arial", 12), command=add_bus).grid(row=5, column=0, pady=20)
    tk.Button(bus_window, text="Clear", font=("Arial", 12), command=clear_entries).grid(row=5, column=1, pady=20)

    def show_all_buses():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT b.bus_id, b.bus_type, b.capacity, o.name AS operator_name, r.s_name || " to " || r.e_name AS route_details
            FROM bus b
            JOIN operator o ON b.op_id = o.opr_id
            JOIN route r ON b.route_id = r.r_id
        ''')
        buses = cursor.fetchall()
        conn.close()

        show_window = tk.Toplevel()
        show_window.title("All Buses")
        show_window.geometry("800x500")

        text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
        text_area.pack(expand=True, fill=tk.BOTH)

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

    tk.Button(bus_window, text="Show All Buses", font=("Arial", 12), command=show_all_buses).grid(row=6, column=0, columnspan=2, pady=10)

def new_route_gui():
    route_window = tk.Toplevel()
    route_window.title("Manage Routes")
    route_window.geometry("800x600")

    tk.Label(route_window, text="Route ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="Start Location Name:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="Start Location ID:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="End Location Name:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10, sticky='w')
    tk.Label(route_window, text="End Location ID:", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=10, sticky='w')

    route_id_entry = tk.Entry(route_window, font=("Arial", 12))
    start_name_entry = tk.Entry(route_window, font=("Arial", 12))
    start_id_entry = tk.Entry(route_window, font=("Arial", 12))
    end_name_entry = tk.Entry(route_window, font=("Arial", 12))
    end_id_entry = tk.Entry(route_window, font=("Arial", 12))

    route_id_entry.grid(row=0, column=1, padx=10, pady=10)
    start_name_entry.grid(row=1, column=1, padx=10, pady=10)
    start_id_entry.grid(row=2, column=1, padx=10, pady=10)
    end_name_entry.grid(row=3, column=1, padx=10, pady=10)
    end_id_entry.grid(row=4, column=1, padx=10, pady=10)

    def add_route():
        r_id = route_id_entry.get().strip()
        s_name = start_name_entry.get().strip()
        s_id = start_id_entry.get().strip()
        e_name = end_name_entry.get().strip()
        e_id = end_id_entry.get().strip()

        if not (r_id and s_name and s_id and e_name and e_id):
            messagebox.showerror("Error", "All fields are required!")
            return

        if s_id == e_id:
            messagebox.showerror("Error", "Start Location ID and End Location ID cannot be the same!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

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

    def edit_route():
        r_id = route_id_entry.get().strip()
        s_name = start_name_entry.get().strip()
        s_id = start_id_entry.get().strip()
        e_name = end_name_entry.get().strip()
        e_id = end_id_entry.get().strip()

        if not (r_id and s_name and s_id and e_name and e_id):
            messagebox.showerror("Error", "All fields are required!")
            return

        if s_id == e_id:
            messagebox.showerror("Error", "Start Location ID and End Location ID cannot be the same!")
            return

        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            cursor.execute("SELECT 1 FROM route WHERE r_id = ?", (r_id,))
            if cursor.fetchone() is None:
                messagebox.showerror("Error", "Route ID not found!")
                return

            cursor.execute('''
                UPDATE route
                SET s_name = ?, s_id = ?, e_name = ?, e_id = ?
                WHERE r_id = ?
            ''', (s_name, s_id, e_name, e_id, r_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Route updated successfully!")
            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_entries():
        route_id_entry.delete(0, tk.END)
        start_name_entry.delete(0, tk.END)
        start_id_entry.delete(0, tk.END)
        end_name_entry.delete(0, tk.END)
        end_id_entry.delete(0, tk.END)

    def show_all_routes():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute('''
            SELECT r_id, s_name, s_id, e_name, e_id FROM route
        ''')
        routes = cursor.fetchall()
        conn.close()

        show_window = tk.Toplevel()
        show_window.title("All Routes")
        show_window.geometry("800x400")

        columns = ("Route ID", "Start Name", "Start ID", "End Name", "End ID")
        tree = ttk.Treeview(show_window, columns=columns, show="headings", height=20)
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for route in routes:
            tree.insert("", tk.END, values=route)

        if not routes:
            messagebox.showinfo("No Routes Found", "There are no routes in the database.")

        tk.Button(show_window, text="Close", command=show_window.destroy).pack(pady=10)

    tk.Button(route_window, text="Add Route", font=("Arial", 12), command=add_route).grid(row=5, column=0, pady=20)
    tk.Button(route_window, text="Edit Route", font=("Arial", 12), command=edit_route).grid(row=5, column=1, pady=20)
    tk.Button(route_window, text="Clear", font=("Arial", 12), command=clear_entries).grid(row=6, column=0, pady=20)
    tk.Button(route_window, text="Show All Routes", font=("Arial", 12), command=show_all_routes).grid(row=6, column=1, pady=20)

def new_run_gui():
    run_window = tk.Toplevel()
    run_window.title("Manage Running Buses")
    run_window.geometry("800x600")  

    tk.Label(run_window, text="Bus ID:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
    tk.Label(run_window, text="Run Date (YYYY-MM-DD):", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky='w')
    tk.Label(run_window, text="Seats Available:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky='w')

    bus_id_entry = tk.Entry(run_window, font=("Arial", 12))
    run_date_entry = tk.Entry(run_window, font=("Arial", 12))
    seat_avail_entry = tk.Entry(run_window, font=("Arial", 12))

    bus_id_entry.grid(row=0, column=1, padx=10, pady=10)
    run_date_entry.grid(row=1, column=1, padx=10, pady=10)
    seat_avail_entry.grid(row=2, column=1, padx=10, pady=10)

    def add_running():
        b_id = bus_id_entry.get().strip()
        run_date = run_date_entry.get().strip()
        seat_avail = seat_avail_entry.get().strip()

        if not (b_id and run_date and seat_avail):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            seat_avail = int(seat_avail) 
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            cursor.execute(''' 
                INSERT INTO running (b_id, run_date, seat_avail)
                VALUES (?, ?, ?)
            ''', (b_id, run_date, seat_avail))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Running bus added successfully!")
            clear_entries() 
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Bus ID or Run Date already exists, or invalid Bus ID!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def edit_running():
        b_id = bus_id_entry.get().strip()
        run_date = run_date_entry.get().strip()
        seat_avail = seat_avail_entry.get().strip()

        if not (b_id and run_date and seat_avail):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            seat_avail = int(seat_avail)  
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM running WHERE b_id = ? AND run_date = ?', (b_id, run_date))
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE running
                    SET seat_avail = ?
                    WHERE b_id = ? AND run_date = ?
                ''', (seat_avail, b_id, run_date))
                messagebox.showinfo("Success", "Running bus updated successfully!")
            else:
                messagebox.showerror("Error", "Bus ID or Run Date not found!")

            conn.commit()
            conn.close()

            clear_entries()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def clear_entries():
        bus_id_entry.delete(0, tk.END)
        run_date_entry.delete(0, tk.END)
        seat_avail_entry.delete(0, tk.END)

    def show_all_running():
        try:
            conn = sqlite3.connect("bus_reservation.db")
            cursor = conn.cursor()

            cursor.execute('''
                SELECT r.b_id, b.bus_type, r.run_date, r.seat_avail
                FROM running r
                JOIN bus b ON r.b_id = b.bus_id
            ''')
            running_buses = cursor.fetchall()
            conn.close()

            show_window = tk.Toplevel()
            show_window.title("All Running Buses")
            show_window.geometry("800x500")
            text_area = tk.Text(show_window, font=("Arial", 12), wrap=tk.WORD)
            text_area.pack(expand=True, fill=tk.BOTH)
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

    tk.Button(run_window, text="Add Running Bus", font=("Arial", 12), command=add_running).grid(row=3, column=0, pady=20)
    tk.Button(run_window, text="Edit Running Bus", font=("Arial", 12), command=edit_running).grid(row=4, column=0, pady=20)
    tk.Button(run_window, text="Show All Running Buses", font=("Arial", 12), command=show_all_running).grid(row=5, column=0, pady=20)

# Main application
def main():
    initialize_db()

    root = tk.Tk()
    root.title("Bus Reservation System")

    # Set the window to full screen
    root.attributes("-fullscreen", True)

    # You can also handle the escape key to exit full-screen mode
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    # Set background color for the root window
    root.configure(bg="#F0F0F0")  # Light grey background for the window

    image = PhotoImage(file="Bus_for_project.png")
    image_label = tk.Label(root, image=image, bg="#F0F0F0")  # Background color for label
    image_label.place(relx=0.5, rely=0.2, anchor='center')  # Image centered at the top

    # Customize button colors
    tk.Button(root, text="Check Booking", font=("Arial", 14), bg="#4CAF50", fg="white", command=check_booking_gui).place(relx=0.33, rely=0.5, anchor='center')
    tk.Button(root, text="Find Bus", font=("Arial", 14), bg="#2196F3", fg="white", command=find_bus_page).place(relx=0.5, rely=0.5, anchor='center')
    tk.Button(root, text="Admin", font=("Arial", 14), bg="#FF9800", fg="white", command=admin_gui).place(relx=0.67, rely=0.5, anchor='center')

    # Exit button, centered below the other buttons
    tk.Button(root, text="Exit", font=("Arial", 14), bg="#F44336", fg="white", command=root.quit).place(relx=0.5, rely=0.7, anchor='center')

    root.mainloop()
if __name__ == "__main__":
    main()