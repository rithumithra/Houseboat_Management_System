import psycopg2
from tkinter import *
from tkinter import messagebox, ttk, simpledialog

DB_HOST = "localhost"
DB_NAME = "dbms"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# Initialize database
def init_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Create Customers table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Customers (
            CID SERIAL PRIMARY KEY,
            CName VARCHAR(50) NOT NULL,
            Membership VARCHAR(20),
            City VARCHAR(50),
            State VARCHAR(50)
        )
        """)

        # Create Owners table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Owners (
            OID SERIAL PRIMARY KEY,
            OName VARCHAR(50) NOT NULL,
            City VARCHAR(50),
            State VARCHAR(50)
        )
        """)

        conn.commit()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Common Function to Fetch Data
def fetch_data(table_name, tree):
    try:
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        
        for row in rows:
            tree.insert("", END, values=row)
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Add Record
def add_record(table_name, fields, values, fetch_function):
    try:
        if any(value == "" for value in values):  # Check if any field is empty
            messagebox.showwarning("Warning", "All fields must be filled in!")
            return

        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(values))
        cursor.execute(f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})", values)
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record added successfully to {table_name}!")
        fetch_function()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Delete Record with ID Prompt
def delete_record(table_name, id_column, tree, fetch_function):
    try:
        id_value = simpledialog.askstring("Delete", f"Enter the {id_column} to delete:")
        if not id_value:
            messagebox.showwarning("Warning", "No ID entered!")
            return

        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE {id_column} = %s", (id_value,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record with {id_column} {id_value} deleted successfully from {table_name}!")
        fetch_function()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# Update Record with ID and Field Selection Prompt
def update_record(table_name, id_column, fields, tree, fetch_function):
    try:
        id_value = simpledialog.askstring("Update", f"Enter the {id_column} of the record to update:")
        if not id_value:
            messagebox.showwarning("Warning", "No ID entered!")
            return

        # Prompt user for which field they want to update
        field = simpledialog.askstring("Field Selection", f"Which field do you want to update?\nOptions: {', '.join(fields)}")
        if not field or field not in fields:
            messagebox.showwarning("Warning", "Invalid field selected!")
            return
        
        # Ask for new value for the selected field
        new_value = simpledialog.askstring("New Value", f"Enter the new value for {field}:")
        if not new_value:
            messagebox.showwarning("Warning", "No new value entered!")
            return
        
        conn = psycopg2.connect(
            host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"UPDATE {table_name} SET {field} = %s WHERE {id_column} = %s", (new_value, id_value))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Record with {id_column} {id_value} updated successfully in {table_name}!")
        fetch_function()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# GUI Setup
root = Tk()
root.title("Customer and Owner Management")
root.geometry("900x600")

# Tabs
tab_control = ttk.Notebook(root)
customer_tab = Frame(tab_control)
owner_tab = Frame(tab_control)
tab_control.add(customer_tab, text="Customers")
tab_control.add(owner_tab, text="Owners")
tab_control.pack(expand=1, fill="both")

# Customer Management
Label(customer_tab, text="Customer Name").grid(row=0, column=0, padx=5, pady=5)
entry_cname = Entry(customer_tab)
entry_cname.grid(row=0, column=1, padx=5, pady=5)

Label(customer_tab, text="Membership").grid(row=1, column=0, padx=5, pady=5)
entry_membership = Entry(customer_tab)
entry_membership.grid(row=1, column=1, padx=5, pady=5)

Label(customer_tab, text="City").grid(row=2, column=0, padx=5, pady=5)
entry_city = Entry(customer_tab)
entry_city.grid(row=2, column=1, padx=5, pady=5)

Label(customer_tab, text="State").grid(row=2, column=2, padx=5, pady=5)
entry_state = Entry(customer_tab)
entry_state.grid(row=2, column=3, padx=5, pady=5)

# Customer Buttons
def fetch_customers():
    fetch_data("Customers", customer_tree)

Button(customer_tab, text="Add Customer", command=lambda: add_record(
    "Customers", 
    "CName, Membership, City, State",  # Exclude CID
    (
        entry_cname.get(),
        entry_membership.get(),
        entry_city.get(),
        entry_state.get()
    ),
    fetch_customers
)).grid(row=3, column=0, pady=10)

Button(customer_tab, text="Delete Customer", command=lambda: delete_record(
    "Customers", "CID", customer_tree, fetch_customers
)).grid(row=3, column=1, pady=10)

Button(customer_tab, text="Update Customer", command=lambda: update_record(
    "Customers", "CID", ["CName", "Membership", "City", "State"], customer_tree, fetch_customers
)).grid(row=3, column=2, pady=10)

customer_tree = ttk.Treeview(customer_tab, columns=("CID", "CName", "Membership", "City", "State"), show="headings")
customer_tree.heading("CID", text="ID")
customer_tree.heading("CName", text="Name")
customer_tree.heading("Membership", text="Membership")
customer_tree.heading("City", text="City")
customer_tree.heading("State", text="State")
customer_tree.grid(row=4, column=0, columnspan=4, pady=10)

# Owner Management
Label(owner_tab, text="Owner Name").grid(row=0, column=0, padx=5, pady=5)
entry_oname = Entry(owner_tab)
entry_oname.grid(row=0, column=1, padx=5, pady=5)

Label(owner_tab, text="City").grid(row=1, column=0, padx=5, pady=5)
entry_ocity = Entry(owner_tab)
entry_ocity.grid(row=1, column=1, padx=5, pady=5)

Label(owner_tab, text="State").grid(row=1, column=2, padx=5, pady=5)
entry_ostate = Entry(owner_tab)
entry_ostate.grid(row=1, column=3, padx=5, pady=5)

# Owner Buttons
def fetch_owners():
    fetch_data("Owners", owner_tree)

Button(owner_tab, text="Add Owner", command=lambda: add_record(
    "Owners", 
    "OName, City, State",  # Exclude OID
    (
        entry_oname.get(),
        entry_ocity.get(),
        entry_ostate.get()
    ),
    fetch_owners
)).grid(row=2, column=0, pady=10)

Button(owner_tab, text="Delete Owner", command=lambda: delete_record(
    "Owners", "OID", owner_tree, fetch_owners
)).grid(row=2, column=1, pady=10)

Button(owner_tab, text="Update Owner", command=lambda: update_record(
    "Owners", "OID", ["OName", "City", "State"], owner_tree, fetch_owners
)).grid(row=2, column=2, pady=10)

owner_tree = ttk.Treeview(owner_tab, columns=("OID", "OName", "City", "State"), show="headings")
owner_tree.heading("OID", text="ID")
owner_tree.heading("OName", text="Name")
owner_tree.heading("City", text="City")
owner_tree.heading("State", text="State")
owner_tree.grid(row=3, column=0, columnspan=4, pady=10)

# Initialize DB and Fetch Initial Data
init_db()
fetch_customers()
fetch_owners()

root.mainloop()
