# =========================================
# PRIYANSHU VEHICLE RENTAL SYSTEM
# =========================================

import os
import datetime
import getpass

vehicle_file = "vehicles.txt"
customer_file = "customers.txt"
rental_file = "rentals.txt"

ADMIN_USER = "priyanshu"
ADMIN_PASS = "4745"

# =========================================
# BASIC FUNCTIONS
# =========================================

def get_id(file):
    if not os.path.exists(file):
        return 1

    with open(file, "r") as f:
        lines = f.readlines()

    if not lines:
        return 1

    last = lines[-1].split(",")[0]
    return int(last) + 1


def input_int(msg):
    while True:
        try:
            return int(input(msg))
        except:
            print("Enter valid number")


def line():
    print("=" * 35)

# =========================================
# VEHICLES
# =========================================

def add_vehicle():
    print("\nAdd Vehicle")

    name = input("Name: ")
    price = float(input("Price per day: "))

    vid = get_id(vehicle_file)

    with open(vehicle_file, "a") as f:
        f.write(f"{vid},{name},{price},yes\n")

    print("Vehicle added")


def view_vehicles(only_available=False):
    print("\nVehicle List")

    if not os.path.exists(vehicle_file):
        print("No vehicles")
        return

    with open(vehicle_file, "r") as f:
        for line in f:
            v = line.strip().split(",")

            if only_available and v[3] != "yes":
                continue

            status = "Available" if v[3] == "yes" else "Rented"
            print(v[0], v[1], "Rs", v[2], status)


def remove_vehicle():
    print("\nRemove Vehicle")
    view_vehicles()

    vid = input_int("Enter ID: ")

    if not os.path.exists(vehicle_file):
        return

    with open(vehicle_file, "r") as f:
        lines = f.readlines()

    new = []
    found = False

    for line in lines:
        v = line.strip().split(",")
        if v[0] == str(vid):
            found = True
        else:
            new.append(line)

    if not found:
        print("Not found")
        return

    with open(vehicle_file, "w") as f:
        f.writelines(new)

    print("Removed")


def change_price():
    print("\nChange Price")
    view_vehicles()

    vid = input_int("Enter ID: ")

    with open(vehicle_file, "r") as f:
        lines = f.readlines()

    new = []

    for line in lines:
        v = line.strip().split(",")

        if v[0] == str(vid):
            new_price = float(input("New price: "))
            v[2] = str(new_price)

        new.append(",".join(v) + "\n")

    with open(vehicle_file, "w") as f:
        f.writelines(new)

    print("Price updated")


def update_vehicle(vid, status):
    with open(vehicle_file, "r") as f:
        lines = f.readlines()

    with open(vehicle_file, "w") as f:
        for line in lines:
            v = line.strip().split(",")
            if v[0] == str(vid):
                v[3] = status
                f.write(",".join(v) + "\n")
            else:
                f.write(line)


def get_price(vid):
    with open(vehicle_file, "r") as f:
        for line in f:
            v = line.strip().split(",")
            if v[0] == str(vid):
                return float(v[2])

# =========================================
# CUSTOMERS
# =========================================

def get_customer(name, phone):
    if os.path.exists(customer_file):
        with open(customer_file, "r") as f:
            for line in f:
                c = line.strip().split(",")
                if c[2] == phone:
                    return c[0]

    cid = get_id(customer_file)

    with open(customer_file, "a") as f:
        f.write(f"{cid},{name},{phone}\n")

    return cid


def view_customers():
    print("\nCustomers")

    if not os.path.exists(customer_file):
        print("No customers")
        return

    with open(customer_file, "r") as f:
        for line in f:
            c = line.strip().split(",")
            print(c[0], c[1], c[2])

# =========================================
# RENT
# =========================================

def rent_vehicle():
    print("\nRent Vehicle")

    view_vehicles(True)

    vid = input_int("Enter vehicle ID: ")

    name = input("Customer name: ")
    phone = input("Phone: ")

    cid = get_customer(name, phone)

    rid = get_id(rental_file)
    today = str(datetime.date.today())

    with open(rental_file, "a") as f:
        f.write(f"{rid},{vid},{cid},{today},None,None\n")

    update_vehicle(vid, "no")

    print("Vehicle rented successfully")


def return_vehicle():
    print("\nReturn Vehicle")

    rid = input_int("Enter rental ID: ")

    if not os.path.exists(rental_file):
        print("No rentals")
        return

    with open(rental_file, "r") as f:
        lines = f.readlines()

    new_lines = []
    found = False

    for line in lines:
        r = line.strip().split(",")

        if r[0] == str(rid) and r[4] == "None":
            found = True

            vid = r[1]
            rent_date = datetime.datetime.strptime(r[3], "%Y-%m-%d").date()
            today = datetime.date.today()

            days = max(1, (today - rent_date).days)
            cost = days * get_price(vid)

            r[4] = str(today)
            r[5] = str(cost)

            new_lines.append(",".join(r) + "\n")

            update_vehicle(vid, "yes")

            print("Total cost:", cost)

        else:
            new_lines.append(line)

    if not found:
        print("Invalid ID")
        return

    with open(rental_file, "w") as f:
        f.writelines(new_lines)

    print("Returned successfully")


def view_active_rentals():
    print("\nActive Rentals")

    if not os.path.exists(rental_file):
        print("No data")
        return

    with open(rental_file, "r") as f:
        for line in f:
            r = line.strip().split(",")
            if r[4] == "None":
                print("RID:", r[0], "Vehicle:", r[1], "Customer:", r[2])


def view_past():
    print("\nPast Rentals")

    if not os.path.exists(rental_file):
        return

    with open(rental_file, "r") as f:
        for line in f:
            r = line.strip().split(",")
            if r[4] != "None":
                print(r)

# =========================================
# REPORT
# =========================================

def report():
    print("\nReport")

    if not os.path.exists(rental_file):
        print("No data")
        return

    costs = []

    with open(rental_file, "r") as f:
        for line in f:
            r = line.strip().split(",")
            if r[5] != "None":
                costs.append(float(r[5]))

    if not costs:
        print("No completed rentals")
        return

    print("Total:", sum(costs))
    print("Average:", sum(costs)/len(costs))
    print("Max:", max(costs))
    print("Min:", min(costs))

# =========================================
# FEEDBACK
# =========================================

def add_feedback():
    print("\nFeedback")

    name = input("Your name: ")
    msg = input("Your feedback: ")

    with open("feedback.txt", "a") as f:
        f.write(f"{name}: {msg}\n")

    print("Thanks for your feedback")


def view_feedback():
    print("\nAll Feedback")

    if not os.path.exists("feedback.txt"):
        print("No feedback yet")
        return

    with open("feedback.txt", "r") as f:
        for line in f:
            print(line.strip())

# =========================================
# FAQ
# =========================================

def show_faq():
    print("""
--- FAQs ---

1. How to rent vehicle?
   → Go to rent option and enter vehicle ID

2. How is cost calculated?
   → Days × price per day

3. How to return?
   → Enter rental ID

4. Can I rent multiple vehicles?
   → Yes

5. Same day return?
   → Minimum 1 day charge
""")
    
# =========================================
# LOGIN
# =========================================

def admin_login():
    print("\nAdmin Login")

    for i in range(3):
        u = input("Username: ")
        p = getpass.getpass("Password: ")

        if u == ADMIN_USER and p == ADMIN_PASS:
            return True

        print("Wrong login")

    return False

# =========================================
# MENUS
# =========================================

def customer_menu():
    while True:
        print("\n1 View Vehicles")
        print("2 Rent")
        print("3 Return")
        print("4 View Active")
        print("5 FAQ")
        print("6 Give Feedback")
        print("7 Back")

        ch = input("Choice: ")

        if ch == "1":
            view_vehicles(True)
        elif ch == "2":
            rent_vehicle()
        elif ch == "3":
            return_vehicle()
        elif ch == "4":
            view_active_rentals()
        elif ch == "5":
            show_faq()
        elif ch == "6":
            add_feedback()
        elif ch == "7":
            break

def admin_menu():
    while True:
        print("\n1 Add Vehicle")
        print("2 Remove Vehicle")
        print("3 View Vehicles")
        print("4 Change Price")
        print("5 View Customers")
        print("6 Report")
        print("7 View Feedback")
        print("8 Back")

        ch = input("Choice: ")

        if ch == "1":
            add_vehicle()
        elif ch == "2":
            remove_vehicle()
        elif ch == "3":
            view_vehicles()
        elif ch == "4":
            change_price()
        elif ch == "5":
            view_customers()
        elif ch == "6":
            report()
        elif ch == "7":
            view_feedback()
        elif ch == "8":
            break

# =========================================
# MAIN
# =========================================

def main():
    while True:
        print("\n1 Customer")
        print("2 Admin")
        print("3 Exit")

        ch = input("Choice: ")

        if ch == "1":
            customer_menu()
        elif ch == "2":
            if admin_login():
                admin_menu()
        elif ch == "3":
            print("THANKS FOR ENGAGING WITH US")
            break

main()