import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Connect to MySQL database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="Iffat_sheema",
        password="Iffatsheema@9010",
        database="govt_school"
    )

# Add student
def add_student():
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_var.get()
    course = course_entry.get()
    mobile = mobile_entry.get()
    email = email_entry.get()

    if name == "" or age == "" or course == "":
        messagebox.showerror(
            "Error", "Please fill Name, Age and Course"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
        INSERT INTO students
        (name, age, gender, course, mobile, email)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (name, age, gender, course, mobile, email)

        cursor.execute(sql, values)
        db.commit()

        messagebox.showinfo(
            "Success", "Student added successfully!"
        )

        clear_fields()
        show_students()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


# Display students
def show_students():
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        for item in student_table.get_children():
            student_table.delete(item)

        for row in records:
            student_table.insert("", tk.END, values=row)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


# Search student
def search_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning(
            "Warning", "Enter Student ID"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE student_id=%s",
            (student_id,)
        )

        record = cursor.fetchone()

        if record:
            clear_fields()

            name_entry.insert(0, record[1])
            age_entry.insert(0, record[2])
            gender_var.set(record[3])
            course_entry.insert(0, record[4])
            mobile_entry.insert(0, record[5])
            email_entry.insert(0, record[6])

        else:
            messagebox.showinfo(
                "Not Found", "Student not found"
            )

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


# Update student
def update_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning(
            "Warning", "Enter Student ID"
        )
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        sql = """
        UPDATE students
        SET name=%s, age=%s, gender=%s,
            course=%s, mobile=%s, email=%s
        WHERE student_id=%s
        """

        values = (
            name_entry.get(),
            age_entry.get(),
            gender_var.get(),
            course_entry.get(),
            mobile_entry.get(),
            email_entry.get(),
            student_id
        )

        cursor.execute(sql, values)
        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success", "Student updated successfully!"
            )
        else:
            messagebox.showinfo(
                "Info", "Student ID not found"
            )

        show_students()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


# Delete student
def delete_student():
    student_id = id_entry.get()

    if student_id == "":
        messagebox.showwarning(
            "Warning", "Enter Student ID"
        )
        return

    confirm = messagebox.askyesno(
        "Confirm", "Do you want to delete this student?"
    )

    if not confirm:
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "DELETE FROM students WHERE student_id=%s",
            (student_id,)
        )

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo(
                "Success", "Student deleted successfully!"
            )
        else:
            messagebox.showinfo(
                "Info", "Student ID not found"
            )

        clear_fields()
        show_students()

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", str(e))

    finally:
        if 'db' in locals() and db.is_connected():
            cursor.close()
            db.close()


# Clear fields
def clear_fields():
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    mobile_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    gender_var.set("Male")


# Main window
root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x650")
root.configure(bg="#eaf2f8")

# Heading
title = tk.Label(
    root,
    text="STUDENT MANAGEMENT SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#154360",
    fg="white",
    pady=15
)
title.pack(fill=tk.X)

# Form frame
form_frame = tk.LabelFrame(
    root,
    text="Student Details",
    font=("Arial", 12, "bold"),
    bg="#eaf2f8",
    padx=15,
    pady=10
)
form_frame.pack(fill=tk.X, padx=20, pady=15)

# Student ID
tk.Label(
    form_frame, text="Student ID:",
    bg="#eaf2f8"
).grid(row=0, column=0, padx=10, pady=8)

id_entry = tk.Entry(form_frame, width=25)
id_entry.grid(row=0, column=1, padx=10, pady=8)

# Name
tk.Label(
    form_frame, text="Name:",
    bg="#eaf2f8"
).grid(row=0, column=2, padx=10, pady=8)

name_entry = tk.Entry(form_frame, width=25)
name_entry.grid(row=0, column=3, padx=10, pady=8)

# Age
tk.Label(
    form_frame, text="Age:",
    bg="#eaf2f8"
).grid(row=1, column=0, padx=10, pady=8)

age_entry = tk.Entry(form_frame, width=25)
age_entry.grid(row=1, column=1, padx=10, pady=8)

# Gender
tk.Label(
    form_frame, text="Gender:",
    bg="#eaf2f8"
).grid(row=1, column=2, padx=10, pady=8)

gender_var = tk.StringVar(value="Male")

gender_box = ttk.Combobox(
    form_frame,
    textvariable=gender_var,
    values=["Male", "Female", "Other"],
    width=22,
    state="readonly"
)
gender_box.grid(row=1, column=3, padx=10, pady=8)

# Course
tk.Label(
    form_frame, text="Course:",
    bg="#eaf2f8"
).grid(row=2, column=0, padx=10, pady=8)

course_entry = tk.Entry(form_frame, width=25)
course_entry.grid(row=2, column=1, padx=10, pady=8)

# Mobile
tk.Label(
    form_frame, text="Mobile:",
    bg="#eaf2f8"
).grid(row=2, column=2, padx=10, pady=8)

mobile_entry = tk.Entry(form_frame, width=25)
mobile_entry.grid(row=2, column=3, padx=10, pady=8)

# Email
tk.Label(
    form_frame, text="Email:",
    bg="#eaf2f8"
).grid(row=3, column=0, padx=10, pady=8)

email_entry = tk.Entry(form_frame, width=25)
email_entry.grid(row=3, column=1, padx=10, pady=8)

# Buttons
button_frame = tk.Frame(root, bg="#eaf2f8")
button_frame.pack(pady=10)

tk.Button(
    button_frame, text="Add Student",
    command=add_student,
    bg="#27ae60", fg="white",
    width=15
).grid(row=0, column=0, padx=5)

tk.Button(
    button_frame, text="Show Students",
    command=show_students,
    bg="#2980b9", fg="white",
    width=15
).grid(row=0, column=1, padx=5)

tk.Button(
    button_frame, text="Search",
    command=search_student,
    bg="#8e44ad", fg="white",
    width=15
).grid(row=0, column=2, padx=5)

tk.Button(
    button_frame, text="Update",
    command=update_student,
    bg="#f39c12", fg="white",
    width=15
).grid(row=0, column=3, padx=5)

tk.Button(
    button_frame, text="Delete",
    command=delete_student,
    bg="#c0392b", fg="white",
    width=15
).grid(row=0, column=4, padx=5)

tk.Button(
    button_frame, text="Clear",
    command=clear_fields,
    bg="#7f8c8d", fg="white",
    width=15
).grid(row=0, column=5, padx=5)

# Student table
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

columns = (
    "ID", "Name", "Age", "Gender",
    "Course", "Mobile", "Email"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)

for col in columns:
    student_table.heading(col, text=col)
    student_table.column(col, width=120)

student_table.pack(fill=tk.BOTH, expand=True)

# Load records when app starts
show_students()

root.mainloop()