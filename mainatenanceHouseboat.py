import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

# Database connection setup
def get_connection():
    return psycopg2.connect(
        dbname="dbms",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )

def execute_query(query, params=None, fetch=False):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params)
        if fetch:
            result = cursor.fetchall()
        else:
            result = None
        connection.commit()
        cursor.close()
        connection.close()
        return result
    except psycopg2.Error as e:
        messagebox.showerror("Database Error", str(e))

class HouseboatManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Houseboat Management System")
        self.root.attributes('-fullscreen', True)  # Fullscreen
        self.root.configure(bg="white")  # White background

        # Exit button for fullscreen
        tk.Button(
            self.root,
            text="Exit Fullscreen",
            command=self.exit_fullscreen,
            font=("Calibri", 12, "bold"),
            bg="red",
            fg="white",
            width=15,
            height=1
        ).pack(pady=10, anchor="ne", padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=1, fill="both", padx=20, pady=20)

        self.maintenance_tab()

    def exit_fullscreen(self):
        self.root.attributes('-fullscreen', False)

    def maintenance_tab(self):
        maintenance_frame = tk.Frame(self.notebook, bg="white")
        self.notebook.add(maintenance_frame, text="Maintenance Management")

        # Add Maintenance Record Section
        section_label = tk.Label(
            maintenance_frame, 
            text="Add Maintenance Record", 
            font=("Calibri", 16, "bold"), 
            bg="white", 
            fg="black"
        )
        section_label.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(maintenance_frame, text="Maintenance ID:", font=("Calibri", 14), bg="white", fg="black").grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(maintenance_frame, text="Houseboat ID:", font=("Calibri", 14), bg="white", fg="black").grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(maintenance_frame, text="Maintenance Date (YYYY-MM-DD):", font=("Calibri", 14), bg="white", fg="black").grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(maintenance_frame, text="Description:", font=("Calibri", 14), bg="white", fg="black").grid(row=4, column=0, sticky="w", pady=5)

        mid = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)
        hid = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)
        mdate = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)
        description = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)

        mid.grid(row=1, column=1, pady=5, padx=10)
        hid.grid(row=2, column=1, pady=5, padx=10)
        mdate.grid(row=3, column=1, pady=5, padx=10)
        description.grid(row=4, column=1, pady=5, padx=10)

        tk.Button(
            maintenance_frame,
            text="Add Maintenance",
            command=lambda: self.add_maintenance(mid.get(), hid.get(), mdate.get(), description.get()),
            width=20,
            height=2,
            bg="green",
            fg="white",
            font=("Calibri", 14, "bold")
        ).grid(row=5, columnspan=2, pady=15)

        # View Maintenance Records Section
        section_label = tk.Label(
            maintenance_frame, 
            text="View Maintenance Records", 
            font=("Calibri", 16, "bold"), 
            bg="white", 
            fg="black"
        )
        section_label.grid(row=6, column=0, columnspan=2, pady=10)

        tk.Label(maintenance_frame, text="Houseboat ID to View Records:", font=("Calibri", 14), bg="white", fg="black").grid(row=7, column=0, sticky="w", pady=5)
        view_hid = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)
        view_hid.grid(row=7, column=1, pady=5, padx=10)

        tk.Button(
            maintenance_frame,
            text="View Records",
            command=lambda: self.view_maintenance(view_hid.get()),
            width=20,
            height=2,
            bg="green",
            fg="white",
            font=("Calibri", 14, "bold")
        ).grid(row=8, columnspan=2, pady=15)

        # Delete Maintenance Record Section
        section_label = tk.Label(
            maintenance_frame, 
            text="Delete Maintenance Record", 
            font=("Calibri", 16, "bold"), 
            bg="white", 
            fg="black"
        )
        section_label.grid(row=9, column=0, columnspan=2, pady=10)

        tk.Label(maintenance_frame, text="Maintenance ID to Delete:", font=("Calibri", 14), bg="white", fg="black").grid(row=10, column=0, sticky="w", pady=5)
        delete_mid = tk.Entry(maintenance_frame, font=("Calibri", 14), width=30)
        delete_mid.grid(row=10, column=1, pady=5, padx=10)

        tk.Button(
            maintenance_frame,
            text="Delete Record",
            command=lambda: self.delete_maintenance(delete_mid.get()),
            width=20,
            height=2,
            bg="green",
            fg="white",
            font=("Calibri", 14, "bold")
        ).grid(row=11, columnspan=2, pady=15)

    def add_maintenance(self, mid, hid, maintenance_date, description):
        if not all([mid, hid, maintenance_date, description]):
            messagebox.showerror("Error", "Please fill in all the fields.")
            return
        query = "INSERT INTO Maintenance (MID, HID, MaintenanceDate, Description) VALUES (%s, %s, %s, %s)"
        execute_query(query, (mid, hid, maintenance_date, description))
        messagebox.showinfo("Success", "Maintenance record added successfully.")

    def view_maintenance(self, hid):
        if not hid:
            messagebox.showerror("Error", "Invalid Houseboat ID.")
            return
        query = "SELECT MID, MaintenanceDate, Description FROM Maintenance WHERE HID = %s ORDER BY MaintenanceDate DESC"
        records = execute_query(query, (hid,), fetch=True)
        if records:
            result = "\n".join([f"ID: {r[0]}, Date: {r[1]}, Description: {r[2]}" for r in records])
            messagebox.showinfo("Maintenance Records", result)
        else:
            messagebox.showinfo("Maintenance Records", "No maintenance records found for this houseboat.")

    def delete_maintenance(self, mid):
        if not mid:
            messagebox.showerror("Error", "Invalid Maintenance ID.")
            return
        query = "DELETE FROM Maintenance WHERE MID = %s"
        execute_query(query, (mid,))
        messagebox.showinfo("Success", "Maintenance record deleted successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = HouseboatManagementApp(root)
    root.mainloop()
