import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2


def execute_query(query, params=(), fetch=False):
    try:
        with psycopg2.connect(
            dbname="dbms",  # Replace with your database name
            user="postgres",  # Replace with your PostgreSQL username
            password="postgres",  # Replace with your PostgreSQL password
            host="localhost",  # Replace with your host (e.g., 'localhost')
            port="5432"  # Replace with your PostgreSQL port (default is 5432)
        ) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if fetch:
                return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", str(e))


def initialize_db():
    query = '''CREATE TABLE IF NOT EXISTS houseboats (
                    HID SERIAL PRIMARY KEY,
                    HName TEXT,
                    Status TEXT,
                    FuelType TEXT,
                    PricePerDay DECIMAL(10, 2),
                    OID INTEGER)'''
    execute_query(query)


def add_houseboat(name, booking_status, fuel_type, price_per_day, oid):
    if not all([name, booking_status, fuel_type, price_per_day, oid]):
        messagebox.showerror("Error", "Please fill in all the fields.")
        return
    if booking_status not in ['Available', 'Booked']:
        messagebox.showerror("Error", "Booking Status must be 'Available' or 'Booked'.")
        return
    if fuel_type not in ['Petrol', 'Diesel', 'Electric']:
        messagebox.showerror("Error", "Fuel Type must be 'Petrol', 'Diesel', or 'Electric'.")
        return
    try:
        price_per_day = float(price_per_day)
        oid = int(oid)
    except ValueError:
        messagebox.showerror("Error", "Price Per Day and OID must be valid numbers.")
        return
    query = "INSERT INTO houseboats (HName, Status, FuelType, PricePerDay, OID) VALUES (%s, %s, %s, %s, %s) "
    execute_query(query, (name, booking_status, fuel_type, price_per_day, oid))
    messagebox.showinfo("Success", "Houseboat added successfully.")
    clear_input_fields()


def clear_input_fields():
    for field in app.input_fields:
        field.delete(0, tk.END)
    app.input_fields[1].set('Available')  # Reset Booking Status
    app.input_fields[2].set('Petrol')  # Reset Fuel Type


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Houseboat Management")
        initialize_db()  # Initialize the database
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True)
        self.houseboat_tab()

    def houseboat_tab(self):
        houseboat_frame = tk.Frame(self.notebook)
        self.notebook.add(houseboat_frame, text="Houseboat Management")

        tk.Label(houseboat_frame, text="Houseboat Name:").grid(row=0, column=0, pady=5, sticky="w")
        tk.Label(houseboat_frame, text="Booking Status:").grid(row=1, column=0, pady=5, sticky="w")
        tk.Label(houseboat_frame, text="Fuel Type:").grid(row=2, column=0, pady=5, sticky="w")
        tk.Label(houseboat_frame, text="Price per Day:").grid(row=3, column=0, pady=5, sticky="w")
        tk.Label(houseboat_frame, text="Owner ID (OID):").grid(row=4, column=0, pady=5, sticky="w")

        name = tk.Entry(houseboat_frame)
        booking_status = ttk.Combobox(houseboat_frame, values=['Available', 'Booked'], state="readonly")
        fuel_type = ttk.Combobox(houseboat_frame, values=['Petrol', 'Diesel', 'Electric'], state="readonly")
        price_per_day = tk.Entry(houseboat_frame)
        oid = tk.Entry(houseboat_frame)

        self.input_fields = [name, booking_status, fuel_type, price_per_day, oid]

        booking_status.set('Available')
        fuel_type.set('Petrol')

        name.grid(row=0, column=1, pady=5, padx=10)
        booking_status.grid(row=1, column=1, pady=5, padx=10)
        fuel_type.grid(row=2, column=1, pady=5, padx=10)
        price_per_day.grid(row=3, column=1, pady=5, padx=10)
        oid.grid(row=4, column=1, pady=5, padx=10)

        tk.Button(houseboat_frame, text="Add Houseboat",
                  command=lambda: add_houseboat(
                      name.get(), booking_status.get(), fuel_type.get(),
                      price_per_day.get(), oid.get()
                  )).grid(row=5, columnspan=2, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
