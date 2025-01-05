import psycopg2
from tkinter import *
from tkinter import messagebox


# Function to connect to PostgreSQL Database
def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="dbms",  # Replace with your database name
            user="postgres",  # Replace with your username
            password="postgres",  # Replace with your password
            host="localhost",
            port="5432"
        )
        return conn
    except Exception as e:
        messagebox.showerror("Database Error", str(e))
        return None


# Function to add feedback
def add_feedback():
    try:
        HID = int(entry_hid.get())
        CID = int(entry_cid.get())
        comment = entry_comment.get()
        rating = int(entry_rating.get())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """INSERT INTO Feedback (HID, CID, Comment, Rating) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (HID, CID, comment, rating))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Feedback added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to retrieve feedback
def retrieve_feedback():
    try:
        CID = int(entry_cid.get())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Feedback WHERE CID = %s"
            cursor.execute(query, (CID,))
            feedbacks = cursor.fetchall()
            conn.close()

            result = "\n".join([str(feedback) for feedback in feedbacks])
            messagebox.showinfo("Feedback Details", result or "No feedback found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to calculate average rating
def calculate_average_rating():
    try:
        CID = int(entry_cid.get())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT Rating FROM Feedback WHERE CID = %s"
            cursor.execute(query, (CID,))
            ratings = cursor.fetchall()
            conn.close()

            if ratings:
                avg_rating = sum([rating[0] for rating in ratings]) / len(ratings)
                messagebox.showinfo("Average Rating", f"Average Rating: {avg_rating:.2f}")
            else:
                messagebox.showinfo("No Feedback", "No feedback found for this Customer ID.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to update feedback comment
def update_feedback_comment():
    try:
        HID = int(entry_hid.get())
        CID = int(entry_cid.get())
        new_comment = entry_comment.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """UPDATE Feedback SET Comment = %s WHERE HID = %s AND CID = %s"""
            cursor.execute(query, (new_comment, HID, CID))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Comment updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to add insurance
def add_insurance():
    try:
        HID = int(entry_hid_insurance.get())
        policy_number = entry_policy_number.get()
        coverage_amount = float(entry_coverage_amount.get())
        expiry_date = entry_expiry_date.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """INSERT INTO Insurance (HID, PolicyNumber, CoverageAmount, ExpiryDate) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (HID, policy_number, coverage_amount, expiry_date))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Insurance added successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to retrieve insurance details
def retrieve_insurance():
    try:
        HID = int(entry_hid_insurance.get())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Insurance WHERE HID = %s"
            cursor.execute(query, (HID,))
            insurances = cursor.fetchall()
            conn.close()

            result = "\n".join([str(insurance) for insurance in insurances])
            messagebox.showinfo("Insurance Details", result or "No insurance found for this Houseboat ID.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Function to update insurance coverage amount
def update_insurance_coverage():
    try:
        HID = int(entry_hid_insurance.get())
        policy_number = entry_policy_number.get()
        new_coverage = float(entry_coverage_amount.get())

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            query = """UPDATE Insurance SET CoverageAmount = %s WHERE HID = %s AND PolicyNumber = %s"""
            cursor.execute(query, (new_coverage, HID, policy_number))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Insurance coverage updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = Tk()
root.title("Houseboat Management System")
root.geometry("800x700")
root.config(bg="#f4f4f4")

# Header
header = Label(root, text="Houseboat Management System", font=("Calibri", 20, "bold"), bg="#34495e", fg="white")
header.pack(fill="both", pady=15)

# Feedback Section
feedback_section = Frame(root, bg="#f4f4f4")
feedback_section.pack(pady=20)

Label(feedback_section, text="Feedback Management", font=("Calibri", 16, "bold"), bg="#f4f4f4", fg="#27ae60").grid(row=0, column=0, columnspan=2, pady=10)

Label(feedback_section, text="Houseboat ID:", bg="#f4f4f4").grid(row=1, column=0, pady=5)
entry_hid = Entry(feedback_section)
entry_hid.grid(row=1, column=1)

Label(feedback_section, text="Customer ID:", bg="#f4f4f4").grid(row=2, column=0, pady=5)
entry_cid = Entry(feedback_section)
entry_cid.grid(row=2, column=1)

Label(feedback_section, text="Comment:", bg="#f4f4f4").grid(row=3, column=0, pady=5)
entry_comment = Entry(feedback_section)
entry_comment.grid(row=3, column=1)

Label(feedback_section, text="Rating:", bg="#f4f4f4").grid(row=4, column=0, pady=5)
entry_rating = Entry(feedback_section)
entry_rating.grid(row=4, column=1)

Button(feedback_section, text="Add Feedback", bg="#2ecc71", fg="white", command=add_feedback).grid(row=5, column=0, pady=10)
Button(feedback_section, text="Retrieve Feedback", bg="#3498db", fg="white", command=retrieve_feedback).grid(row=5, column=1, pady=10)
Button(feedback_section, text="Calculate Average Rating", bg="#9b59b6", fg="white", command=calculate_average_rating).grid(row=6, column=0, pady=10)
Button(feedback_section, text="Update Comment", bg="#e67e22", fg="white", command=update_feedback_comment).grid(row=6, column=1, pady=10)

# Insurance Section
insurance_section = Frame(root, bg="#f4f4f4")
insurance_section.pack(pady=20)

Label(insurance_section, text="Insurance Management", font=("Calibri", 16, "bold"), bg="#f4f4f4", fg="#27ae60").grid(row=0, column=0, columnspan=2, pady=10)

Label(insurance_section, text="Houseboat ID:", bg="#f4f4f4").grid(row=1, column=0, pady=5)
entry_hid_insurance = Entry(insurance_section)
entry_hid_insurance.grid(row=1, column=1)

Label(insurance_section, text="Policy Number:", bg="#f4f4f4").grid(row=2, column=0, pady=5)
entry_policy_number = Entry(insurance_section)
entry_policy_number.grid(row=2, column=1)

Label(insurance_section, text="Coverage Amount:", bg="#f4f4f4").grid(row=3, column=0, pady=5)
entry_coverage_amount = Entry(insurance_section)
entry_coverage_amount.grid(row=3, column=1)

Label(insurance_section, text="Expiry Date:", bg="#f4f4f4").grid(row=4, column=0, pady=5)
entry_expiry_date = Entry(insurance_section)
entry_expiry_date.grid(row=4, column=1)

Button(insurance_section, text="Add Insurance", bg="#2ecc71", fg="white", command=add_insurance).grid(row=5, column=0, pady=10)
Button(insurance_section, text="Retrieve Insurance", bg="#3498db", fg="white", command=retrieve_insurance).grid(row=5, column=1, pady=10)
Button(insurance_section, text="Update Coverage", bg="#e67e22", fg="white", command=update_insurance_coverage).grid(row=6, column=0, pady=10)

# Run GUI
root.mainloop()
