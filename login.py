import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import re

# Initialize Database
def initialize_db():
    conn = sqlite3.connect("bus_reservation.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL CHECK(length(phone) = 10),
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to Register User
def register_user():
    name = name_entry.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()
    password = password_entry.get().strip()

    if not name or not email or not phone or not password:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Error", "Invalid email format!")
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Phone number must be 10 digits!")
        return

    try:
        conn = sqlite3.connect("bus_reservation.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)", 
                       (name, email, phone, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Registration Successful!")
        clear_fields()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already registered!")

# Function to Clear Fields
def clear_fields():
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Initialize Database
initialize_db()

# Create GUI Window
root = tk.Tk()
root.title("User Registration")
root.geometry("450x500")
root.configure(bg="#D5F3FE")  # Light blue background

# Style Configuration
style = ttk.Style()
style.configure("TButton", font=("Arial", 12, "bold"), padding=5)
style.map("TButton", background=[("active", "#1E90FF")])  # Hover effect

# Heading Frame
header_frame = tk.Frame(root, bg="#007ACC", height=60)
header_frame.pack(fill="x")
tk.Label(header_frame, text="Register", font=("Arial", 18, "bold"), fg="white", bg="#007ACC").pack(pady=15)

# Main Form Frame
form_frame = tk.Frame(root, bg="white", padx=20, pady=20)
form_frame.pack(pady=20, padx=10, fill="both", expand=True)

# Input Fields
tk.Label(form_frame, text="Name:", font=("Arial", 12), bg="white").grid(row=0, column=0, sticky="w", pady=5)
name_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
name_entry.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Email:", font=("Arial", 12), bg="white").grid(row=1, column=0, sticky="w", pady=5)
email_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
email_entry.grid(row=1, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Phone:", font=("Arial", 12), bg="white").grid(row=2, column=0, sticky="w", pady=5)
phone_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30)
phone_entry.grid(row=2, column=1, pady=5, padx=10)

tk.Label(form_frame, text="Password:", font=("Arial", 12), bg="white").grid(row=3, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
password_entry.grid(row=3, column=1, pady=5, padx=10)

# Buttons
btn_frame = tk.Frame(form_frame, bg="white")
btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

register_btn = ttk.Button(btn_frame, text="Register", command=register_user)
register_btn.grid(row=0, column=0, padx=10)

clear_btn = ttk.Button(btn_frame, text="Clear", command=clear_fields)
clear_btn.grid(row=0, column=1, padx=10)

# Run GUI
root.mainloop()
