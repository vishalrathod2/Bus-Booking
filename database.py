# # import sqlite3
# # import tkinter as tk
# # from tkinter import messagebox

# # def initialize_db():
# #     conn = sqlite3.connect("bus_reservation.db")
# #     cursor = conn.cursor()

# #     # Create buses table
# #     cursor.execute('''
# #         CREATE TABLE IF NOT EXISTS buses (
# #             bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             bus_number TEXT NOT NULL,
# #             source TEXT NOT NULL,
# #             destination TEXT NOT NULL,
# #             capacity INTEGER NOT NULL,
# #             available_seats INTEGER NOT NULL
# #         )
# #     ''')

# #     # Create reservations table
# #     cursor.execute('''
# #         CREATE TABLE IF NOT EXISTS reservations (
# #             reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
# #             bus_id INTEGER NOT NULL,
# #             passenger_name TEXT NOT NULL,
# #             seats_booked INTEGER NOT NULL,
# #             FOREIGN KEY (bus_id) REFERENCES buses (bus_id)
# #         )
# #     ''')

# #     conn.commit()
# #     conn.close()

# # def add_bus_gui():
# #     def add_bus():
# #         bus_number = bus_number_entry.get()
# #         source = source_entry.get()
# #         destination = destination_entry.get()
# #         try:
# #             capacity = int(capacity_entry.get())
# #         except ValueError:
# #             messagebox.showerror("Invalid Input", "Capacity must be a number")
# #             return

# #         conn = sqlite3.connect("bus_reservation.db")
# #         cursor = conn.cursor()
# #         cursor.execute('''
# #             INSERT INTO buses (bus_number, source, destination, capacity, available_seats)
# #             VALUES (?, ?, ?, ?, ?)
# #         ''', (bus_number, source, destination, capacity, capacity))
# #         conn.commit()
# #         conn.close()

# #         messagebox.showinfo("Success", "Bus added successfully!")
# #         add_bus_window.destroy()

# #     add_bus_window = tk.Toplevel()
# #     add_bus_window.title("Add Bus")

# #     tk.Label(add_bus_window, text="Bus Number:").grid(row=0, column=0)
# #     bus_number_entry = tk.Entry(add_bus_window)
# #     bus_number_entry.grid(row=0, column=1)

# #     tk.Label(add_bus_window, text="Source:").grid(row=1, column=0)
# #     source_entry = tk.Entry(add_bus_window)
# #     source_entry.grid(row=1, column=1)

# #     tk.Label(add_bus_window, text="Destination:").grid(row=2, column=0)
# #     destination_entry = tk.Entry(add_bus_window)
# #     destination_entry.grid(row=2, column=1)

# #     tk.Label(add_bus_window, text="Capacity:").grid(row=3, column=0)
# #     capacity_entry = tk.Entry(add_bus_window)
# #     capacity_entry.grid(row=3, column=1)

# #     tk.Button(add_bus_window, text="Add Bus", command=add_bus).grid(row=4, column=0, columnspan=2)

# # def view_buses_gui():
# #     conn = sqlite3.connect("bus_reservation.db")
# #     cursor = conn.cursor()
# #     cursor.execute("SELECT * FROM buses")
# #     buses = cursor.fetchall()
# #     conn.close()

# #     view_window = tk.Toplevel()
# #     view_window.title("Available Buses")

# #     if not buses:
# #         tk.Label(view_window, text="No buses available.").pack()
# #     else:
# #         for bus in buses:
# #             bus_info = f"ID: {bus[0]}, Number: {bus[1]}, Source: {bus[2]}, Destination: {bus[3]}, Capacity: {bus[4]}, Available Seats: {bus[5]}"
# #             tk.Label(view_window, text=bus_info).pack()

# # def book_ticket_gui():
# #     def book_ticket():
# #         try:
# #             bus_id = int(bus_id_entry.get())
# #             seats_to_book = int(seats_entry.get())
# #         except ValueError:
# #             messagebox.showerror("Invalid Input", "Bus ID and Seats must be numbers")
# #             return

# #         passenger_name = name_entry.get()
# #         conn = sqlite3.connect("bus_reservation.db")
# #         cursor = conn.cursor()

# #         cursor.execute("SELECT available_seats FROM buses WHERE bus_id = ?", (bus_id,))
# #         result = cursor.fetchone()

# #         if result and result[0] >= seats_to_book:
# #             cursor.execute('''
# #                 INSERT INTO reservations (bus_id, passenger_name, seats_booked)
# #                 VALUES (?, ?, ?)
# #             ''', (bus_id, passenger_name, seats_to_book))
# #             cursor.execute('''
# #                 UPDATE buses SET available_seats = available_seats - ? WHERE bus_id = ?
# #             ''', (seats_to_book, bus_id))
# #             conn.commit()
# #             messagebox.showinfo("Success", "Booking successful!")
# #             book_ticket_window.destroy()
# #         else:
# #             messagebox.showerror("Error", "Not enough seats available.")

# #         conn.close()

# #     book_ticket_window = tk.Toplevel()
# #     book_ticket_window.title("Book Ticket")

# #     tk.Label(book_ticket_window, text="Bus ID:").grid(row=0, column=0)
# #     bus_id_entry = tk.Entry(book_ticket_window)
# #     bus_id_entry.grid(row=0, column=1)

# #     tk.Label(book_ticket_window, text="Passenger Name:").grid(row=1, column=0)
# #     name_entry = tk.Entry(book_ticket_window)
# #     name_entry.grid(row=1, column=1)

# #     tk.Label(book_ticket_window, text="Seats to Book:").grid(row=2, column=0)
# #     seats_entry = tk.Entry(book_ticket_window)
# #     seats_entry.grid(row=2, column=1)

# #     tk.Button(book_ticket_window, text="Book", command=book_ticket).grid(row=3, column=0, columnspan=2)

# # def cancel_reservation_gui():
# #     def cancel_reservation():
# #         try:
# #             reservation_id = int(reservation_id_entry.get())
# #         except ValueError:
# #             messagebox.showerror("Invalid Input", "Reservation ID must be a number")
# #             return

# #         conn = sqlite3.connect("bus_reservation.db")
# #         cursor = conn.cursor()
# #         cursor.execute("SELECT bus_id, seats_booked FROM reservations WHERE reservation_id = ?", (reservation_id,))
# #         result = cursor.fetchone()

# #         if result:
# #             bus_id, seats_booked = result
# #             cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id,))
# #             cursor.execute("UPDATE buses SET available_seats = available_seats + ? WHERE bus_id = ?", (seats_booked, bus_id))
# #             conn.commit()
# #             messagebox.showinfo("Success", "Reservation canceled successfully!")
# #             cancel_reservation_window.destroy()
# #         else:
# #             messagebox.showerror("Error", "Reservation not found.")

# #         conn.close()

# #     cancel_reservation_window = tk.Toplevel()
# #     cancel_reservation_window.title("Cancel Reservation")

# #     tk.Label(cancel_reservation_window, text="Reservation ID:").grid(row=0, column=0)
# #     reservation_id_entry = tk.Entry(cancel_reservation_window)
# #     reservation_id_entry.grid(row=0, column=1)

# #     tk.Button(cancel_reservation_window, text="Cancel", command=cancel_reservation).grid(row=1, column=0, columnspan=2)

# # def main():
# #     initialize_db()

# #     root = tk.Tk()
# #     root.title("Bus Reservation System")

# #     tk.Label(root, text="Bus Reservation System", font=("Arial", 16)).pack(pady=10)

# #     tk.Button(root, text="Add Bus", command=add_bus_gui).pack(pady=5)
# #     tk.Button(root, text="View Buses", command=view_buses_gui).pack(pady=5)
# #     tk.Button(root, text="Book Ticket", command=book_ticket_gui).pack(pady=5)
# #     tk.Button(root, text="Cancel Reservation", command=cancel_reservation_gui).pack(pady=5)

# #     root.mainloop()

# # if __name__ == "__main__":
# #     main()
# import sqlite3
# import tkinter as tk
# from tkinter import messagebox
# from tkinter import PhotoImage

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

# def check_booking_gui():
#     # Placeholder for "Check Booking" functionality
#     messagebox.showinfo("Info", "Check Booking feature coming soon!")

# def find_bus_gui():
#     # Placeholder for "Find Bus" functionality
#     messagebox.showinfo("Info", "Find Bus feature coming soon!")

# def admin_gui():
#     # Admin panel placeholder
#     messagebox.showinfo("Info", "Admin Panel coming soon!")

# def main():
#     initialize_db()

#     root = tk.Tk()
#     root.title("Bus Reservation System")
#     root.geometry("600x500")  # Set the size of the window

#     # Add an image to the home page
#     image = PhotoImage(file="C:\\Users\\ratho\\OneDrive\\Desktop\\bus booking\\Bus-Booking\\Bus_for_project.png")
#     image_label = tk.Label(root, image=image)
#     image_label.place(relx=0.5, rely=0.2, anchor='center')  # Center the image at 20% of the window height

#     # Add buttons for Check Booking, Find Bus, and Admin
#     tk.Button(root, text="Check Booking", font=("Arial", 14), command=check_booking_gui).place(relx=0.5, rely=0.5, anchor='center')
#     tk.Button(root, text="Find Bus", font=("Arial", 14), command=find_bus_gui).place(relx=0.5, rely=0.6, anchor='center')
#     tk.Button(root, text="Admin", font=("Arial", 14), command=admin_gui).place(relx=0.5, rely=0.7, anchor='center')

#     root.mainloop()

# if __name__ == "__main__":
#     main()

