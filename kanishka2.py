import tkinter as tk
from tkinter import ttk, messagebox
from openpyxl import Workbook, load_workbook
import os

FILE = "patient_records.xlsx"

HEADERS = [
    "Patient ID", "Name", "Age", "Gender", "Mobile",
    "Blood Group", "Allergies", "Medical History",
    "Diagnosis", "Medications"
]


# Create Excel file if it does not exist
def setup_excel():
    if not os.path.exists(FILE):
        wb = Workbook()
        ws = wb.active
        ws.title = "Patients"
        ws.append(HEADERS)
        wb.save(FILE)


def get_records():
    wb = load_workbook(FILE)
    ws = wb["Patients"]
    records = list(ws.iter_rows(min_row=2, values_only=True))
    wb.close()
    return records


def clear_fields():
    for field in entries.values():
        field.delete(0, tk.END)
    entries["Patient ID"].config(state="normal")


def add_patient():
    data = [entries[h].get().strip() for h in HEADERS]

    if not data[0] or not data[1]:
        messagebox.showwarning(
            "Missing Information",
            "Patient ID and Name are required."
        )
        return

    try:
        if data[2]:
            age = int(data[2])
            if age < 0 or age > 130:
                raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Age", "Enter an age between 0 and 130."
        )
        return

    wb = load_workbook(FILE)
    ws = wb["Patients"]

    for row in ws.iter_rows(min_row=2, values_only=True):
        if str(row[0]) == data[0]:
            wb.close()
            messagebox.showerror(
                "Duplicate ID", "This Patient ID already exists."
            )
            return

    ws.append(data)
    wb.save(FILE)
    wb.close()

    show_patients()
    clear_fields()
    messagebox.showinfo("Success", "Patient record added.")


def show_patients(records=None):
    for item in table.get_children():
        table.delete(item)

    if records is None:
        records = get_records()

    for record in records:
        table.insert("", tk.END, values=record)


def select_patient(event=None):
    selected = table.selection()
    if not selected:
        return

    record = table.item(selected[0], "values")
    clear_fields()

    for header, value in zip(HEADERS, record):
        entries[header].insert(0, value if value is not None else "")

    entries["Patient ID"].config(state="disabled")


def update_patient():
    patient_id = entries["Patient ID"].get().strip()

    if not patient_id:
        messagebox.showwarning(
            "Select Patient", "Select a patient record first."
        )
        return

    data = [entries[h].get().strip() for h in HEADERS]

    if not data[1]:
        messagebox.showwarning("Missing Name", "Enter patient name.")
        return

    try:
        if data[2]:
            age = int(data[2])
            if age < 0 or age > 130:
                raise ValueError
    except ValueError:
        messagebox.showerror(
            "Invalid Age", "Enter an age between 0 and 130."
        )
        return

    wb = load_workbook(FILE)
    ws = wb["Patients"]
    found = False

    for row in range(2, ws.max_row + 1):
        if str(ws.cell(row, 1).value) == patient_id:
            for col, value in enumerate(data, start=1):
                ws.cell(row, col).value = value
            found = True
            break

    if found:
        wb.save(FILE)

    wb.close()

    if found:
        show_patients()
        clear_fields()
        messagebox.showinfo("Success", "Patient record updated.")
    else:
        messagebox.showerror("Error", "Patient record not found.")


def delete_patient():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "Select Patient", "Select a patient to delete."
        )
        return

    record = table.item(selected[0], "values")
    patient_id = str(record[0])

    if not messagebox.askyesno(
        "Confirm Delete",
        "Delete the selected patient record?"
    ):
        return

    wb = load_workbook(FILE)
    ws = wb["Patients"]

    for row in range(2, ws.max_row + 1):
        if str(ws.cell(row, 1).value) == patient_id:
            ws.delete_rows(row, 1)
            break

    wb.save(FILE)
    wb.close()

    show_patients()
    clear_fields()
    messagebox.showinfo("Success", "Patient record deleted.")


def search_patient():
    query = search_entry.get().strip().lower()

    if not query:
        show_patients()
        return

    records = get_records()
    matches = [
        record for record in records
        if query in str(record[0]).lower()
        or query in str(record[1]).lower()
    ]

    show_patients(matches)

    if not matches:
        messagebox.showinfo("Search", "No matching patient found.")


# Application window
setup_excel()

root = tk.Tk()
root.title("Patient Health Record Management System")
root.geometry("1200x720")
root.configure(bg="#eaf2f8")

title = tk.Label(
    root,
    text="PATIENT HEALTH RECORD & MEDICAL HISTORY",
    font=("Arial", 18, "bold"),
    bg="#154360",
    fg="white",
    pady=12
)
title.pack(fill="x")

# Patient form
form = tk.Frame(root, bg="#eaf2f8", padx=10, pady=10)
form.pack(fill="x")

entries = {}

for i, header in enumerate(HEADERS):
    row = i // 5
    col = i % 5

    tk.Label(
        form, text=header + ":",
        bg="#eaf2f8", font=("Arial", 9, "bold")
    ).grid(row=row * 2, column=col, padx=5, pady=3, sticky="w")

    entry = tk.Entry(form, width=22)
    entry.grid(row=row * 2 + 1, column=col, padx=5, pady=3)
    entries[header] = entry

# Buttons
buttons = tk.Frame(root, bg="#eaf2f8", pady=5)
buttons.pack()

tk.Button(
    buttons, text="Add Patient", width=14,
    command=add_patient, bg="#229954", fg="white"
).grid(row=0, column=0, padx=5)

tk.Button(
    buttons, text="Update Patient", width=14,
    command=update_patient, bg="#2874a6", fg="white"
).grid(row=0, column=1, padx=5)

tk.Button(
    buttons, text="Delete Patient", width=14,
    command=delete_patient, bg="#c0392b", fg="white"
).grid(row=0, column=2, padx=5)

tk.Button(
    buttons, text="Clear Fields", width=14,
    command=clear_fields
).grid(row=0, column=3, padx=5)

tk.Button(
    buttons, text="Show All", width=14,
    command=show_patients
).grid(row=0, column=4, padx=5)

# Search section
search_frame = tk.Frame(root, bg="#eaf2f8", pady=8)
search_frame.pack()

tk.Label(
    search_frame, text="Search by Patient ID or Name:",
    bg="#eaf2f8"
).pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame, text="Search",
    command=search_patient
).pack(side="left", padx=5)

# Patient records table
table_frame = tk.Frame(root, padx=10, pady=5)
table_frame.pack(fill="both", expand=True)

table = ttk.Treeview(
    table_frame, columns=HEADERS,
    show="headings"
)

for header in HEADERS:
    table.heading(header, text=header)
    table.column(header, width=115, minwidth=80)

yscroll = ttk.Scrollbar(
    table_frame, orient="vertical",
    command=table.yview
)
xscroll = ttk.Scrollbar(
    table_frame, orient="horizontal",
    command=table.xview
)

table.configure(
    yscrollcommand=yscroll.set,
    xscrollcommand=xscroll.set
)

table.grid(row=0, column=0, sticky="nsew")
yscroll.grid(row=0, column=1, sticky="ns")
xscroll.grid(row=1, column=0, sticky="ew")

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)

table.bind("<<TreeviewSelect>>", select_patient)

show_patients()

root.mainloop()