import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime

# Database Setup
connection = psycopg2.connect(
    dbname="dbms",  # Your database name
    user="postgres",    # Your PostgreSQL username
    password="postgres", # Your PostgreSQL password
    host="localhost",        # Host address, adjust if needed
    port="5432"              # Default PostgreSQL port
)
cursor = connection.cursor()

# Tables Setup (Ensure these exist)
cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Houseboats (
    hid SERIAL PRIMARY KEY,
    name TEXT,
    priceperday REAL
);
''')

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS Rentals (
    rid SERIAL PRIMARY KEY,
    cid INTEGER,
    hid INTEGER,
    did INTEGER,
    paymentmethod TEXT,
    startdate DATE,
    enddate DATE,
    noofdays INTEGER,
    total REAL
); 
''')
connection.commit()

# Function to handle any database operation with proper error handling and transaction management
def execute_query(query, params=None):
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        connection.commit()
    except Exception as e:
        connection.rollback()  # Rollback the transaction in case of an error
        messagebox.showerror("Error", f"Database error: {e}")

# Function to Create a New Rental
def create_new_rental():
    rid = entry_rental_id.get()
    cid = entry_customer_id.get()
    hid = entry_houseboat_id.get()
    did = entry_driver_id.get()
    startdate = entry_rental_date.get()
    enddate = entry_return_date.get()
    paymentmethod = entry_payment_method.get()
    noofdays = entry_no_of_days.get()

    try:
        noofdays = int(noofdays)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of days.")
        return

    # Fetch price per day from the Houseboats table
    try:
        cursor.execute('SELECT priceperday FROM Houseboats WHERE hid = %s;', (hid,))
        result = cursor.fetchone()
        if result:
            priceperday = result[0]
            rental_cost = noofdays * priceperday
        else:
            messagebox.showerror("Error", "Houseboat not found.")
            return
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"Could not fetch price per day: {e}")
        return

    try:
        execute_query(''' 
        INSERT INTO Rentals (rid, cid, hid, did, paymentmethod, startdate, enddate, noofdays, total) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); 
        ''', (rid, cid, hid, did, paymentmethod, startdate, enddate, noofdays, rental_cost))
        messagebox.showinfo("Success", "Rental created successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Could not create rental: {e}")

# Function to Retrieve Rental Details
def retrieve_rental_details():
    rental_id = entry_rental_id.get()
    try:
        cursor.execute('SELECT * FROM Rentals WHERE rid = %s;', (rental_id,))
        rental = cursor.fetchone()
        if rental:
            messagebox.showinfo("Rental Details", f"Rental: {rental}")
        else:
            messagebox.showerror("Error", "Rental not found.")
    except Exception as e:
        connection.rollback()  # Rollback transaction if error occurs
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to Calculate Total Revenue
def calculate_total_revenue():
    try:
        cursor.execute('SELECT SUM(total) FROM Rentals;')
        total_revenue = cursor.fetchone()[0]
        if total_revenue is not None:
            messagebox.showinfo("Total Revenue", f"Total Revenue: {total_revenue}")
        else:
            messagebox.showinfo("Total Revenue", "No rentals found.")
    except Exception as e:
        connection.rollback()  # Rollback transaction if error occurs
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Function to Delete a Rental
def delete_rental():
    rental_id = entry_rental_id.get()
    try:
        execute_query('DELETE FROM Rentals WHERE rid = %s;', (rental_id,))
        messagebox.showinfo("Success", "Rental deleted.")
    except Exception as e:
        messagebox.showerror("Error", f"Could not delete rental: {e}")

# GUI Setup
root = tk.Tk()
root.title("Driver Rental System")

notebook = ttk.Notebook(root)

# Rental Tab
rental_tab = ttk.Frame(notebook)
notebook.add(rental_tab, text="Rental")

# Widgets for Rentals
tk.Label(rental_tab, text="Rental ID:").grid(row=0, column=0, padx=10, pady=5)
entry_rental_id = tk.Entry(rental_tab)
entry_rental_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Customer ID:").grid(row=1, column=0, padx=10, pady=5)
entry_customer_id = tk.Entry(rental_tab)
entry_customer_id.grid(row=1, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Houseboat ID:").grid(row=2, column=0, padx=10, pady=5)
entry_houseboat_id = tk.Entry(rental_tab)
entry_houseboat_id.grid(row=2, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Driver ID:").grid(row=3, column=0, padx=10, pady=5)
entry_driver_id = tk.Entry(rental_tab)
entry_driver_id.grid(row=3, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Rental Date:").grid(row=4, column=0, padx=10, pady=5)
entry_rental_date = tk.Entry(rental_tab)
entry_rental_date.grid(row=4, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Return Date:").grid(row=5, column=0, padx=10, pady=5)
entry_return_date = tk.Entry(rental_tab)
entry_return_date.grid(row=5, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="Payment Method:").grid(row=6, column=0, padx=10, pady=5)
entry_payment_method = tk.Entry(rental_tab)
entry_payment_method.grid(row=6, column=1, padx=10, pady=5)

tk.Label(rental_tab, text="No of Days:").grid(row=7, column=0, padx=10, pady=5)
entry_no_of_days = tk.Entry(rental_tab)
entry_no_of_days.grid(row=7, column=1, padx=10, pady=5)

# Buttons
tk.Button(rental_tab, text="Create Rental", command=create_new_rental).grid(row=8, column=0, padx=10, pady=5)
tk.Button(rental_tab, text="Retrieve Rental", command=retrieve_rental_details).grid(row=8, column=1, padx=10, pady=5)
tk.Button(rental_tab, text="Delete Rental", command=delete_rental).grid(row=9, column=0, padx=10, pady=5)
tk.Button(rental_tab, text="Calculate Total Revenue", command=calculate_total_revenue).grid(row=9, column=1, padx=10, pady=5)

notebook.pack(padx=10, pady=10)

root.mainloop()
