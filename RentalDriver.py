import tkinter as tk
from tkinter import messagebox
import psycopg2

# Connect to your PostgreSQL database
def connect_db():
    return psycopg2.connect(database="dbms", user="postgres", password="postgres", host="localhost", port="5432")

# Function to add driver
def add_driver():
    name = entry_name.get()
    city = entry_city.get()
    state = entry_state.get()

    if name:
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Drivers (DName, City, State) 
                VALUES (%s, %s, %s)
                RETURNING DID
                """, (name, city, state))

            driver_id = cur.fetchone()[0]
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Driver added successfully! Driver ID: {driver_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Name is required!")

# Function to delete a driver by ID
def delete_driver():
    driver_id = entry_driver_id.get()
    if driver_id:
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM Drivers WHERE DID = %s", (driver_id,))
            conn.commit()
            conn.close()

            if cur.rowcount > 0:
                messagebox.showinfo("Success", "Driver deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "No driver found with the given ID!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Driver ID is required!")

# Function to update driver details by ID
def update_driver():
    driver_id = entry_driver_id.get()
    name = entry_name.get()
    city = entry_city.get()
    state = entry_state.get()

    if driver_id and name:
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("""
                UPDATE Drivers
                SET DName = %s, City = %s, State = %s
                WHERE DID = %s
                """, (name, city, state, driver_id))

            conn.commit()
            conn.close()

            if cur.rowcount > 0:
                messagebox.showinfo("Success", "Driver details updated successfully!")
            else:
                messagebox.showwarning("Not Found", "No driver found with the given ID!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Input Error", "Driver ID and Name are required!")

# Main window
root = tk.Tk()
root.title("Driver and Rental Management System")

# Driver section
tk.Label(root, text="Driver ID:").grid(row=0, column=0, padx=10, pady=5)
entry_driver_id = tk.Entry(root)
entry_driver_id.grid(row=0, column=1, padx=10, pady=5)

# Add Driver Button
tk.Button(root, text="Add Driver", command=add_driver).grid(row=1, column=0, columnspan=2, pady=10)

# Delete Driver Button
tk.Button(root, text="Delete Driver", command=delete_driver).grid(row=2, column=0, columnspan=2, pady=10)

# Update Driver Details Button
tk.Button(root, text="Update Driver Details", command=update_driver).grid(row=3, column=0, columnspan=2, pady=10)

# Driver input fields
tk.Label(root, text="Name:").grid(row=4, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=4, column=1, padx=10, pady=5)

# City and State Fields
tk.Label(root, text="City:").grid(row=5, column=0, padx=10, pady=5)
entry_city = tk.Entry(root)
entry_city.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="State:").grid(row=6, column=0, padx=10, pady=5)
entry_state = tk.Entry(root)
entry_state.grid(row=6, column=1, padx=10, pady=5)

# Run the main loop
root.mainloop()
