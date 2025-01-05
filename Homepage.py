import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

# Functions to open corresponding Python files
def open_ownercustomer():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\CustomerOwner.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Owner and Customer module: {e}")

def open_feedback():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\feedbackinsuranceFinal.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Feedback and Insurance module: {e}")

def open_maintenance():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\maintenanceHouseboat.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Maintenance module: {e}")

def open_rentals():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\Rental.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Rentals module: {e}")

def open_houseboat():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\houseboatFinal.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Houseboat module: {e}")

def open_driver():
    try:
        subprocess.Popen(['python', r'C:\Users\megha\OneDrive\Desktop\SEM 3\DBMS\RentalDriver.py'], shell=True)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening Driver module: {e}")

# Create the main window
root = tk.Tk()
root.title("Houseboat Management System")
root.geometry("800x600")
root.config(bg="#f7f7f7")

# Define styles
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background="#4CAF50", tabmargins=[2, 5, 2, 0])
style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), background="#4CAF50", foreground="white", padding=[10, 5])
style.map("TNotebook.Tab", background=[("selected", "#2E7D32")])

# Header Label
header_label = tk.Label(
    root, 
    text="Welcome to the Houseboat Management System", 
    font=("Arial", 20, "bold"), 
    bg="#4CAF50", 
    fg="white", 
    padx=20, 
    pady=10
)
header_label.pack(fill="x")

# Create a Notebook (tabbed interface)
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True, padx=20, pady=20)

# Create frames for each tab
frame_owner = tk.Frame(notebook, bg="#ffffff")
frame_feedback = tk.Frame(notebook, bg="#ffffff")
frame_rentals = tk.Frame(notebook, bg="#ffffff")
frame_houseboat = tk.Frame(notebook, bg="#ffffff")
frame_driver = tk.Frame(notebook, bg="#ffffff")
frame_maintenance = tk.Frame(notebook, bg="#ffffff")

# Add tabs to the notebook
notebook.add(frame_owner, text="Owner & Customer")
notebook.add(frame_feedback, text="Feedback & Insurance")
notebook.add(frame_rentals, text="Rentals")
notebook.add(frame_houseboat, text="Houseboat")
notebook.add(frame_driver, text="Driver")
notebook.add(frame_maintenance, text="Maintenance")

# Function to create buttons
def create_button(frame, text, command):
    return tk.Button(
        frame, 
        text=text, 
        command=command, 
        font=("Arial", 14, "bold"), 
        bg="#2E7D32", 
        fg="white", 
        activebackground="#66BB6A", 
        activeforeground="white", 
        relief="raised", 
        bd=3, 
        width=30, 
        height=2
    )

# Add buttons to frames
create_button(frame_owner, "Open Owner and Customer", open_ownercustomer).pack(pady=30)
create_button(frame_feedback, "Open Feedback and Insurance", open_feedback).pack(pady=30)
create_button(frame_rentals, "Open Rentals", open_rentals).pack(pady=30)
create_button(frame_houseboat, "Open Houseboat", open_houseboat).pack(pady=30)
create_button(frame_driver, "Open Driver", open_driver).pack(pady=30)
create_button(frame_maintenance, "Open Maintenance", open_maintenance).pack(pady=30)

# Footer Label
footer_label = tk.Label(
    root, 
    text="Houseboat Management System © 2024", 
    font=("Arial", 10, "italic"), 
    bg="#f7f7f7", 
    fg="#4CAF50", 
    pady=10
)
footer_label.pack(side="bottom", fill="x")

# Run the Tkinter event loop
root.mainloop()
