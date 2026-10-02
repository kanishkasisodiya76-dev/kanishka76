from openpyxl import Workbook, load_workbook
from datetime import datetime
import os
import random

file = "banking_system.xlsx"


# ================= CREATE ACCOUNT =================

def create_account():
    print("\n===== CREATE ACCOUNT =====")

    name = input("Enter Account Holder Name: ")
    mobile = input("Enter Mobile Number: ")
    pin = input("Enter 4-digit PIN: ")

    # Check PIN
    if len(pin) != 4 or not pin.isdigit():
        print("Invalid PIN! PIN must be exactly 4 digits.")
        return

    try:
        initial_deposit = float(input("Enter Initial Deposit: "))
    except ValueError:
        print("Invalid amount!")
        return

    if initial_deposit < 0:
        print("Initial deposit cannot be negative!")
        return

    # Open existing Excel file or create new one
    if os.path.exists(file):
        wb = load_workbook(file)

        if "Account" in wb.sheetnames:
            ws = wb["Account"]
        else:
            ws = wb.create_sheet("Account")
            ws.append([
                "Date",
                "Account Number",
                "Name",
                "Mobile Number",
                "PIN",
                "Balance"
            ])

    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Account"

        ws.append([
            "Date",
            "Account Number",
            "Name",
            "Mobile Number",
            "PIN",
            "Balance"
        ])

    # Generate unique account number
    existing_accounts = [
        ws.cell(row=row, column=2).value
        for row in range(2, ws.max_row + 1)
    ]

    while True:
        account_number = random.randint(1000, 9999)

        if account_number not in existing_accounts:
            break

    # Add account details
    ws.append([
        datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        account_number,
        name,
        mobile,
        pin,
        initial_deposit
    ])

    wb.save(file)
    wb.close()

    print("\nAccount created successfully!")
    print("Your Account Number is:", account_number)
    print("Your Balance is:", initial_deposit)


# ================= DEPOSIT MONEY =================

def deposit_money():
    print("\n===== DEPOSIT MONEY =====")

    if not os.path.exists(file):
        print("No account exists. Please create an account first.")
        return

    try:
        ac = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number!")
        return

    pin = input("Enter PIN: ")

    wb = load_workbook(file)
    ws = wb["Account"]

    found = False

    for row in range(2, ws.max_row + 1):

        if (
            ws.cell(row, 2).value == ac
            and str(ws.cell(row, 5).value) == pin
        ):

            found = True

            try:
                amount = float(input("Enter Deposit Amount: "))
            except ValueError:
                print("Invalid Amount!")
                wb.close()
                return

            if amount <= 0:
                print("Invalid Amount!")
                wb.close()
                return

            balance = float(ws.cell(row, 6).value)
            new_balance = balance + amount

            # Update balance in Excel
            ws.cell(row, 6).value = new_balance

            # Save updated balance
            wb.save(file)

            print("\nMoney deposited successfully!")
            print("Deposited Amount:", amount)
            print("Updated Balance:", new_balance)

            break

    if not found:
        print("\nInvalid Account Number or PIN!")

    wb.close()


# ================= WITHDRAW MONEY =================

def withdraw_money():
    print("\n===== WITHDRAW MONEY =====")

    if not os.path.exists(file):
        print("No account exists. Please create an account first.")
        return

    try:
        ac = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number!")
        return

    pin = input("Enter PIN: ")

    wb = load_workbook(file)
    ws = wb["Account"]

    found = False

    for row in range(2, ws.max_row + 1):

        if (
            ws.cell(row, 2).value == ac
            and str(ws.cell(row, 5).value) == pin
        ):

            found = True

            try:
                amount = float(input("Enter Withdraw Amount: "))
            except ValueError:
                print("Invalid Amount!")
                wb.close()
                return

            if amount <= 0:
                print("Invalid Amount!")
                wb.close()
                return

            balance = float(ws.cell(row, 6).value)

            # Check balance
            if amount > balance:
                print("\nInsufficient Balance!")
                print("Your Balance is:", balance)
                wb.close()
                return

            new_balance = balance - amount

            # Update Excel balance
            ws.cell(row, 6).value = new_balance

            # Save changes
            wb.save(file)

            print("\nMoney withdrawn successfully!")
            print("Withdrawn Amount:", amount)
            print("Remaining Balance:", new_balance)

            break

    if not found:
        print("\nInvalid Account Number or PIN!")

    wb.close()


# ================= CHECK BALANCE =================

def check_balance():
    print("\n===== CHECK BALANCE =====")

    if not os.path.exists(file):
        print("No account exists. Please create an account first.")
        return

    try:
        ac = int(input("Enter Account Number: "))
    except ValueError:
        print("Invalid Account Number!")
        return

    pin = input("Enter PIN: ")

    wb = load_workbook(file)
    ws = wb["Account"]

    found = False

    for row in range(2, ws.max_row + 1):

        if (
            ws.cell(row, 2).value == ac
            and str(ws.cell(row, 5).value) == pin
        ):

            found = True

            name = ws.cell(row, 3).value
            balance = ws.cell(row, 6).value

            print("\n===== ACCOUNT DETAILS =====")
            print("Account Number:", ac)
            print("Account Holder:", name)
            print("Current Balance:", balance)

            break

    if not found:
        print("\nInvalid Account Number or PIN!")

    wb.close()


# ================= MAIN MENU =================

def main():

    while True:

        print("\n============================================")
        print("          BANK MANAGEMENT SYSTEM")
        print("============================================")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")
        print("============================================")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid Choice! Please enter a number from 1 to 5.")
            continue

        if choice == 1:
            create_account()

        elif choice == 2:
            deposit_money()

        elif choice == 3:
            withdraw_money()

        elif choice == 4:
            check_balance()

        elif choice == 5:
            print("\nThank you for using our Banking System!")
            break

        else:
            print("Invalid Choice! Please select 1 to 5.")


# ================= RUN PROGRAM =================

main()