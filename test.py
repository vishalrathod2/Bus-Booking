from logging import root
import sqlite3
from tkinter import *
from tkinter.messagebox import showinfo, showerror
from datetime import datetime, date

import tk


class BusBookingSystem:
    def __init__(self):
        # Database connection
        self.con = sqlite3.connect("bus_booking.db")  # Change the DB path if required
        self.cur = self.con.cursor()

        # Store image references
        self.bus_image = None
        self.home_image = None

    def cover_to_home(self, event):
        root.destroy()
        self.home_page()

    def home_page(self):
        root = Tk()
        root.title("HOME PAGE")
        self.bus_image = PhotoImage(file=r'C:/Users/ratho/OneDrive/Documents/Bus-Booking-system-main/Bus-Booking-system-main/Bus_Booking/Bus_for_project.png')
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry(f'{w}x{h}+0+0')
        for i in range (15):
         root.grid_rowconfigure(i, weight=1)
         root.grid_columnconfigure(i ,weight=1)

        Label(root, text="\n\n\n\n").grid(row=0, column=0, columnspan=15)
        Label(root, image=self.bus_image).grid(row=1, column=0, columnspan=15,sticky="nsew")
        Label(root, text="Online Bus Booking System", font='Arial 20 bold', bg='yellow', fg='black').grid(
            row=2, column=0, columnspan=15,sticky="nsew")

        def home_to_journey_detail():
            root.destroy()
            self.journey_detail_page()

        def home_to_check_booking():
            root.destroy()
            self.check_booking_page()

        def home_to_db_add_page():
            root.destroy()
            self.db_add_page()

        Button(root, text='Seat Booking', font='Arial 14 bold', bg='Light green', fg='black',
               command=home_to_journey_detail).grid(row=4, column=4)
        Button(root, text='Check Booked Seat', font='Arial 14 bold', bg='green3', fg='black',
               command=home_to_check_booking).grid(row=4, column=6)
        Button(root, text='Add Bus Details', font='Arial 14 bold', bg='green', fg='black',
               command=home_to_db_add_page).grid(row=4, column=8)

        Label(root, text='For Admin Only', fg='red').grid(row=6, column=8)
        root.mainloop()

    def journey_detail_page(self):
        root = Tk()
        root.title("SEAT BOOKING PAGE")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry(f'{w}x{h}+0+0')

        def journey_to_home():
            root.destroy()
            self.home_page()

        def show_bus():
            tp = to_place.get()
            fp = from_place.get()
            jd = journey_date.get()

            # Validate user input
            if not tp.isalpha() or not fp.isalpha():
                showerror("ERROR", "Enter valid 'To' and 'From' locations.")
                return

            if not jd:
                showerror("ERROR", "Enter a journey date.")
                return

            try:
                # Validate date format
                datetime.strptime(jd, "%Y-%m-%d")
            except ValueError:
                showerror("ERROR", "Enter a valid date (YYYY-MM-DD).")
                return

            tp, fp = tp.lower(), fp.lower()
            self.cur.execute('SELECT r_id FROM route WHERE s_name=? AND e_name=?', (fp, tp))
            res_route = self.cur.fetchall()
            if not res_route:
                showerror('No Route Found', 'We are currently not running on this route.')
                return

            # Process bus details and implement the booking system logic

        self.bus_image = PhotoImage(file=r'C:/Users/ratho/OneDrive/Documents/Bus-Booking-system-main/Bus-Booking-system-main/Bus_Booking/Bus_for_project.png')
        Label(root, image=self.bus_image).grid(row=0, column=3, columnspan=12)
        Label(root, text="Online Bus Booking System", font='Arial 28 bold', bg='sky blue', fg='red').grid(row=2,
                                                                                                          column=3,
                                                                                                          pady=20,
                                                                                                          columnspan=12)
        Label(root, text='Enter Journey Details', bg='light green', fg='dark green', font='Arial 18 bold').grid(row=3,
                                                                                                                column=3,
                                                                                                                columnspan=12,
                                                                                                                pady=20)
        Label(root, text='To', fg='black', font='Arial 12 bold').grid(row=4, column=3, padx=30)
        to_place = Entry(root, font='Arial 12 bold', fg='black')
        to_place.grid(row=4, column=4, padx=50)

        Label(root, text='From', fg='black', font='Arial 12 bold').grid(row=4, column=5, padx=30)
        from_place = Entry(root, font='Arial 12 bold', fg='black')
        from_place.grid(row=4, column=6, padx=50)

        Label(root, text='Journey date', fg='black', font='Arial 12 bold').grid(row=4, column=7, padx=30)
        journey_date = Entry(root, font='Arial 12 bold', fg='black')
        journey_date.grid(row=4, column=8, padx=50)
        Label(root, text="Date format YYYY-MM-DD").grid(row=5, column=8)

        Button(root, text='Show Bus', bg='green', fg='black', font='Arial 12 bold', command=show_bus).grid(row=4,
                                                                                                           column=9,
                                                                                                           padx=30)

        self.home_image = PhotoImage(file='C:/Users/ratho/OneDrive/Documents/Bus-Booking-system-main/Bus-Booking-system-main/Bus_Booking/home.png')
        Button(root, image=self.home_image, command=journey_to_home).grid(row=4, column=10)

        root.mainloop()

    def check_booking_page(self):
        root = Tk()
        root.title("CHECK BOOKING PAGE")
        h, w = root.winfo_screenheight(), root.winfo_screenwidth()
        root.geometry(f'{w}x{h}+0+0')
        self.bus_image = PhotoImage(file=r'C:/Users/ratho/OneDrive/Documents/Bus-Booking-system-main/Bus-Booking-system-main/Bus_Booking/Bus_for_project.png')
        self.home_image = PhotoImage(file='C:/Users/ratho/OneDrive/Documents/Bus-Booking-system-main/Bus-Booking-system-main/Bus_Booking/home.png')

        # Implement the logic for checking bookings here

        root.mainloop()


# Instantiate and run
if __name__ == "__main__":
    app = BusBookingSystem()
    app.home_page()
