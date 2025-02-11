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
        bus_window.geometry("800x500")

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
    tk.Button(root, text="Search Buses", font=("Arial", 14, "bold"), command=search_buses, bg="blue", fg="white").pack(pady=20)

    root.mainloop()
         
def admin_gui():
    admin_window = tk.Toplevel()
    admin_window.title("Admin Panel")
    admin_window.geometry("1550x900")

    
    tk.Label(admin_window, text="Admin Panel", font=("Arial", 20, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(pady=10, fill="x")
    image = PhotoImage(file="Bus_for_project.png")
    tk.Label(admin_window, image=image).place(relx=0.5, rely=0.2, anchor='center')

    tk.Button(admin_window, text="New Operator", font=("Arial", 14), bg="#4CAF50", fg="white", command=new_operator_gui).place(relx=0.2, rely=0.5, anchor='center')
    tk.Button(admin_window, text="New Bus", font=("Arial", 14), bg="#2196F3", fg="white", command=new_bus_gui).place(relx=0.4, rely=0.5, anchor='center')
    tk.Button(admin_window, text="New Route", font=("Arial", 14), bg="#FF9800", fg="white", command=new_route_gui).place(relx=0.6, rely=0.5, anchor='center')
    tk.Button(admin_window, text="New Run", font=("Arial", 14), bg="#FF5722", fg="white", command=new_run_gui).place(relx=0.8, rely=0.5, anchor='center')

    admin_window.mainloop()

def new_operator_gui():
    operator_window = tk.Toplevel()
    operator_window.title("Manage Operators")
    operator_window.geometry("600x500")
    operator_window.configure(bg="#f0f0f0")  # Light background

    # ======= Heading Label =======
    tk.Label(operator_window, text="Manage Operators", font=("Arial", 16, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(fill="x")

    # ======= Main Form Frame =======
    form_frame = tk.Frame(operator_window, bg="#f0f0f0")
    form_frame.pack(pady=20, padx=20)

    # ======= Labels & Entries =======
    tk.Label(form_frame, text="Operator ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    opr_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    opr_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Address:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    address_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    address_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Phone:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    phone_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    email_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    email_entry.grid(row=4, column=1, padx=10, pady=5)

    # ======= Add Operator Logic =======
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

    # ======= Edit Operator Logic =======
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
                UPDATE operator SET name=?, address=?, phone=?, email=? WHERE opr_id=?
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

    # ======= Clear Entries =======
    def clear_entries():
        opr_id_entry.delete(0, tk.END)
        name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    # ======= Show All Operators (Treeview) =======
    def show_all_operators():
        show_window = tk.Toplevel()
        show_window.title("All Operators")
        show_window.geometry("900x600")
        show_window.configure(bg="#f0f0f0")

        # Table Frame
        frame = tk.Frame(show_window, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, expand=True, fill="both")

        # Treeview Table
        columns = ("Operator ID", "Name", "Address", "Phone", "Email")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        # Column Headings
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=140, anchor="center")

        # Scrollbar
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

        # Fetch data
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM operator")
        operators = cursor.fetchall()
        conn.close()

        # Insert data into Treeview
        for operator in operators:
            tree.insert("", "end", values=operator)

        # Close Button
        tk.Button(show_window, text="Close", font=("Arial", 12), bg="#FF5733", fg="white", command=show_window.destroy).pack(pady=10)

    # ======= Buttons (Styled) =======
    button_frame = tk.Frame(operator_window, bg="#f0f0f0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Operator", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
              command=add_operator, width=12, relief="raised", bd=2).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(button_frame, text="Edit Operator", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
              command=edit_operator, width=12, relief="raised", bd=2).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(button_frame, text="Show All", font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
              command=show_all_operators, width=12, relief="raised", bd=2).grid(row=0, column=2, padx=10, pady=10)

    # Close Button
    tk.Button(button_frame, text="Close", font=("Arial", 12, "bold"), bg="#FF5733", fg="white",
              command=operator_window.destroy, width=12, relief="raised", bd=2).grid(row=1, column=1, padx=10, pady=10)

def new_bus_gui():
    bus_window = tk.Toplevel()
    bus_window.title("Manage Buses")
    bus_window.geometry("450x500") 
    tk.Label(bus_window, text="Add New Bus", font=("Arial", 16, "bold"), fg="white", bg="#333333", padx=20, pady=10).grid(row=0, column=0, columnspan=2, sticky="ew")

    form_frame = tk.Frame(bus_window, bg="#f0f0f0")
    form_frame.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky="ew")    

    tk.Label(form_frame, text="Bus ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    bus_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    bus_id_entry.grid(row=0, column=1, padx=10, pady=5)
    tk.Label(form_frame, text="Bus Type:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    bus_type_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    bus_type_entry.grid(row=1, column=1, padx=10, pady=5)    
    tk.Label(form_frame, text="Capacity:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    capacity_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    capacity_entry.grid(row=2, column=1, padx=10, pady=5)   
    tk.Label(form_frame, text="Operator ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    operator_var = tk.StringVar()
    operator_menu = ttk.Combobox(form_frame, textvariable=operator_var, font=("Arial", 12), width=23, state="readonly")
    operator_menu.grid(row=3, column=1, padx=10, pady=5)
    tk.Label(form_frame, text="Route ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    route_var = tk.StringVar()
    route_menu = ttk.Combobox(form_frame, textvariable=route_var, font=("Arial", 12), width=23, state="readonly")
    route_menu.grid(row=4, column=1, padx=10, pady=5)

    def populate_dropdowns():
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()

        cursor.execute("SELECT opr_id, name FROM operator")
        operators = cursor.fetchall()
        operator_menu["values"] = [f"{op[0]} - {op[1]}" for op in operators]
        cursor.execute("SELECT r_id, s_name, e_name FROM route")
        routes = cursor.fetchall()
        route_menu["values"] = [f"{r[0]} - {r[1]} to {r[2]}" for r in routes]

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
            bus_window.destroy()
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

    button_frame = tk.Frame(bus_window, bg="#f0f0f0")
    button_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(button_frame, text="Add Bus", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", 
              command=add_bus, width=12, relief="raised", bd=2).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="Clear", font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
              command=clear_entries, width=12, relief="raised", bd=2).grid(row=0, column=1, padx=10, pady=10)
    tk.Button(button_frame, text="Close", font=("Arial", 12, "bold"), bg="#FF5733", fg="white",
              command=bus_window.destroy, width=12, relief="raised", bd=2).grid(row=0, column=2, padx=10, pady=10)

    def show_all_buses():
        show_window = tk.Toplevel()
        show_window.title("All Buses")
        show_window.geometry("800x525")
        show_window.configure(bg="#f0f0f0")

        tk.Label(show_window, text="Bus Details", font=("Arial", 16, "bold"), fg="white", bg="#333333", padx=20, pady=10).grid(row=0, column=0, columnspan=2, sticky="ew")

        frame = tk.Frame(show_window, bg="#f0f0f0")
        frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        columns = ("Bus ID", "Bus Type", "Capacity", "Operator", "Route")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        tree.heading("Bus ID", text="Bus ID", anchor="center")
        tree.heading("Bus Type", text="Bus Type", anchor="center")
        tree.heading("Capacity", text="Capacity", anchor="center")
        tree.heading("Operator", text="Operator", anchor="center")
        tree.heading("Route", text="Route", anchor="center")

        tree.column("Bus ID", width=100, anchor="center")
        tree.column("Bus Type", width=150, anchor="center")
        tree.column("Capacity", width=80, anchor="center")
        tree.column("Operator", width=200, anchor="center")
        tree.column("Route", width=250, anchor="center")

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12), rowheight=25, background="#f9f9f9", foreground="black")
        style.configure("Treeview.Heading", font=("Arial", 13, "bold"), background="#555555", foreground="black")
        style.map("Treeview", background=[("selected", "#4CAF50")])

        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroll_y.set)
        scroll_y.grid(row=0, column=1, sticky="ns")
        
        tree.grid(row=0, column=0, sticky="nsew")

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

        for bus in buses:
            tree.insert("", "end", values=bus)

        tk.Button(show_window, text="Close", font=("Arial", 12), bg="#FF5733", fg="white", command=show_window.destroy).grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(bus_window, text="Show All Buses", font=("Arial", 12), command=show_all_buses).grid(row=3, column=0, columnspan=2, pady=10)

def new_route_gui():
    route_window = tk.Toplevel()
    route_window.title("Manage Routes")
    route_window.geometry("600x500")
    route_window.configure(bg="#f0f0f0")  # Light background

    # ======= Heading Label =======
    tk.Label(route_window, text="Manage Routes", font=("Arial", 16, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(fill="x")

    # ======= Main Form Frame =======
    form_frame = tk.Frame(route_window, bg="#f0f0f0")
    form_frame.pack(pady=20, padx=20)

    # ======= Labels & Entries =======
    tk.Label(form_frame, text="Route ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    route_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    route_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Start Location Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    start_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    start_name_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Start Location ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    start_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    start_id_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="End Location Name:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    end_name_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    end_name_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="End Location ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    end_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    end_id_entry.grid(row=4, column=1, padx=10, pady=5)

    # ======= Add Route Logic =======
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

    # ======= Edit Route Logic =======
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
            cursor.execute('SELECT 1 FROM route WHERE r_id = ?', (r_id,))
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

    # ======= Clear Entries =======
    def clear_entries():
        route_id_entry.delete(0, tk.END)
        start_name_entry.delete(0, tk.END)
        start_id_entry.delete(0, tk.END)
        end_name_entry.delete(0, tk.END)
        end_id_entry.delete(0, tk.END)

    # ======= Show All Routes (Treeview) =======
    def show_all_routes():
        show_window = tk.Toplevel()
        show_window.title("All Routes")
        show_window.geometry("800x500")
        show_window.configure(bg="#f0f0f0")

        # Table Frame
        frame = tk.Frame(show_window, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, expand=True, fill="both")

        # Treeview Table
        columns = ("Route ID", "Start Name", "Start ID", "End Name", "End ID")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        # Column Headings
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=140, anchor="center")

        # Scrollbar
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

        # Fetch data
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM route")
        routes = cursor.fetchall()
        conn.close()

        # Insert data into Treeview
        for route in routes:
            tree.insert("", "end", values=route)

        # Close Button
        tk.Button(show_window, text="Close", font=("Arial", 12), bg="#FF5733", fg="white", command=show_window.destroy).pack(pady=10)

    # ======= Buttons (Styled) =======
    button_frame = tk.Frame(route_window, bg="#f0f0f0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Route", font=("Arial", 12), bg="#4CAF50", fg="white",
              command=add_route, width=12, relief="raised", bd=2).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(button_frame, text="Edit Route", font=("Arial", 12), bg="#2196F3", fg="white",
              command=edit_route, width=12, relief="raised", bd=2).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(button_frame, text="Show All", font=("Arial", 12), bg="#FF9800", fg="white",
              command=show_all_routes, width=12, relief="raised", bd=2).grid(row=0, column=2, padx=10, pady=10)

    # Close Button
    tk.Button(button_frame, text="Close", font=("Arial", 12), bg="#FF5733", fg="white",
              command=route_window.destroy, width=12, relief="raised", bd=2).grid(row=1, column=1, padx=10, pady=10)

def new_run_gui():
    run_window = tk.Toplevel()
    run_window.title("Manage Running Buses")
    run_window.geometry("600x500")
    run_window.configure(bg="#f0f0f0")

    # ======= Heading Label =======
    tk.Label(run_window, text="Manage Running Buses", font=("Arial", 16, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(fill="x")

    # ======= Main Form Frame =======
    form_frame = tk.Frame(run_window, bg="#f0f0f0")
    form_frame.pack(pady=20, padx=20)

    # ======= Labels & Entries =======
    tk.Label(form_frame, text="Bus ID:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    bus_id_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    bus_id_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Run Date (YYYY-MM-DD):", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    run_date_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    run_date_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(form_frame, text="Seats Available:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    seat_avail_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
    seat_avail_entry.grid(row=2, column=1, padx=10, pady=5)

    # ======= Add Running Bus Logic =======
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

    # ======= Edit Running Bus Logic =======
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

    # ======= Clear Entries =======
    def clear_entries():
        bus_id_entry.delete(0, tk.END)
        run_date_entry.delete(0, tk.END)
        seat_avail_entry.delete(0, tk.END)

    # ======= Show All Running Buses (Treeview) =======
    def show_all_running():
        show_window = tk.Toplevel()
        show_window.title("All Running Buses")
        show_window.geometry("800x500")
        show_window.configure(bg="#f0f0f0")

        # Table Frame
        frame = tk.Frame(show_window, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, expand=True, fill="both")

        # Treeview Table
        columns = ("Bus ID", "Bus Type", "Run Date", "Seats Available")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        # Column Headings
        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, width=140, anchor="center")

        # Scrollbar
        scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scroll_y.set)
        scroll_y.pack(side="right", fill="y")

        tree.pack(expand=True, fill="both")

        # Fetch data
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.b_id, b.bus_type, r.run_date, r.seat_avail
            FROM running r
            JOIN bus b ON r.b_id = b.bus_id
        ''')
        running_buses = cursor.fetchall()
        conn.close()

        # Insert data into Treeview
        for bus in running_buses:
            tree.insert("", "end", values=bus)

        # Close Button
        tk.Button(show_window, text="Close", font=("Arial", 12), bg="#FF5733", fg="white", command=show_window.destroy).pack(pady=10)

    # ======= Buttons (Styled) =======
    button_frame = tk.Frame(run_window, bg="#f0f0f0")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Add Running Bus", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
              command=add_running, width=15, relief="raised", bd=2).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(button_frame, text="Edit Running Bus", font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
              command=edit_running, width=15, relief="raised", bd=2).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(button_frame, text="Show All", font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
              command=show_all_running, width=15, relief="raised", bd=2).grid(row=0, column=2, padx=10, pady=10)

    # Close Button
    tk.Button(button_frame, text="Close", font=("Arial", 12, "bold"), bg="#FF5733", fg="white",
              command=run_window.destroy, width=15, relief="raised", bd=2).grid(row=1, column=1, padx=10, pady=10)

# Main application
def main():
    initialize_db()

    root = tk.Tk()
    root.title("Bus Reservation System")
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))        
    tk.Label(text="Bus Booking", font=("Arial", 20, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(pady=10, fill="x")


    root.configure(bg="#F0F0F0")

    image = PhotoImage(file="Bus_for_project.png")
    image_label = tk.Label(root, image=image, bg="#F0F0F0")  # Background color for label
    image_label.place(relx=0.5, rely=0.2, anchor='center')  # Image centered at the top

    # Customize button colors
    tk.Button(root, text="Check Booking", font=("Arial", 14), bg="#4CAF50", fg="white", command=check_booking_gui).place(relx=0.25, rely=0.5, anchor='center')
    tk.Button(root, text="Find Bus", font=("Arial", 14), bg="#2196F3", fg="white", command=find_bus_page).place(relx=0.4, rely=0.5, anchor='center')
    tk.Button(root, text="Admin", font=("Arial", 14), bg="#FF9800", fg="white", command=admin_gui).place(relx=0.55, rely=0.5, anchor='center')
    tk.Button(root, text="About Us", font=("Arial", 14), bg="#FF9800", fg="white", command=about_us_gui).place(relx=0.7, rely=0.5, anchor='center')

    # Exit button, centered below the other buttons
    tk.Button(root, text="Exit", font=("Arial", 14), bg="#F44336", fg="white", command=root.quit).place(relx=0.5, rely=0.7, anchor='center')

    root.mainloop()

def about_us_gui():
    about_window = tk.Toplevel()
    about_window.title("About Us")
    about_window.geometry("600x400")
    about_window.configure(bg="#f0f0f0")

    tk.Label(about_window, text="About Us", font=("Arial", 20, "bold"), fg="white", bg="#333333", padx=20, pady=10).pack(fill="x")
    tk.Label(about_window, text="This is a Bus Reservation System developed by XYZ.", font=("Arial", 14), bg="#f0f0f0", wraplength=500).pack(pady=20)
    tk.Button(about_window, text="Close", font=("Arial", 12), bg="#FF5733", fg="white", command=about_window.destroy).pack(pady=10)

if __name__ == "__main__":
    main()