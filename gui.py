import tkinter as tk
from tkinter import messagebox, ttk
import random
import datetime

# -----------------------------
# Data storage
# -----------------------------
nm = []
phno = []
add = []
checkin = []
checkout = []
room = []
price = []
rc = []
p = []
rm = []
custid = []
day = []
i = 0

# -----------------------------
# Helper: Validate Dates
# -----------------------------
def valid_date(d):
    try:
        datetime.datetime(d[2], d[1], d[0])
        return True
    except:
        return False

# -----------------------------
# GUI App Class
# -----------------------------
class HotelApp:
    def __init__(self, root):
        self.root = root
        root.title("Hotel Paradise Valley")
        root.geometry("500x450")
        self.home_screen()

    # -----------------------------
    # HOME SCREEN
    # -----------------------------
    def home_screen(self):
        self.clear()

        tk.Label(self.root, text="HOTEL PARADISE VALLEY", font=("Arial", 18, "bold")).pack(pady=20)

        btns = [
            ("Booking", self.booking_screen),
            ("Rooms Info", self.rooms_info_screen),
            ("Restaurant (Menu)", self.restaurant_screen),
            ("Payment", self.payment_screen),
            ("Records", self.records_screen),
            ("Exit", self.root.quit)
        ]

        for txt, cmd in btns:
            tk.Button(self.root, text=txt, width=25, height=2, command=cmd).pack(pady=8)

    # -----------------------------
    # BOOKING
    # -----------------------------
    def booking_screen(self):
        self.clear()
        tk.Label(self.root, text="Room Booking", font=("Arial", 16, "bold")).pack(pady=10)

        # Input fields
        labels = ["Name:", "Phone:", "Address:", "Check-in (dd/mm/yyyy):", "Check-out (dd/mm/yyyy):"]
        self.entries = []

        for L in labels:
            tk.Label(self.root, text=L).pack()
            e = tk.Entry(self.root)
            e.pack()
            self.entries.append(e)

        tk.Label(self.root, text="Room Type").pack(pady=5)
        self.room_choice = ttk.Combobox(self.root, values=[
            "Standard Non-AC",
            "Standard AC",
            "3-Bed Non-AC",
            "3-Bed AC",
        ])
        self.room_choice.pack()

        tk.Button(self.root, text="Book Room", command=self.book_room).pack(pady=20)
        tk.Button(self.root, text="Back", command=self.home_screen).pack()

    def book_room(self):
        global i

        name = self.entries[0].get()
        phone = self.entries[1].get()
        addr = self.entries[2].get()
        cin = self.entries[3].get()
        cout = self.entries[4].get()
        rtype = self.room_choice.get()

        if not (name and phone and addr and cin and cout and rtype):
            messagebox.showerror("Error", "All fields required.")
            return

        try:
            ci = list(map(int, cin.split("/")))
            co = list(map(int, cout.split("/")))
        except:
            messagebox.showerror("Error", "Date format must be dd/mm/yyyy")
            return

        if not (valid_date(ci) and valid_date(co)):
            messagebox.showerror("Error", "Invalid date.")
            return

        d1 = datetime.datetime(ci[2], ci[1], ci[0])
        d2 = datetime.datetime(co[2], co[1], co[0])
        if d2 <= d1:
            messagebox.showerror("Error", "Check-out must be after check-in.")
            return

        days = (d2 - d1).days

        nm.append(name)
        phno.append(phone)
        add.append(addr)
        checkin.append(cin)
        checkout.append(cout)
        day.append(days)

        price_map = {
            "Standard Non-AC": 3500,
            "Standard AC": 4000,
            "3-Bed Non-AC": 4500,
            "3-Bed AC": 5000
        }

        room.append(rtype)
        price.append(price_map[rtype])

        rn = random.randrange(300, 340)
        cid = random.randrange(10, 50)

        rm.append(rn)
        custid.append(cid)
        rc.append(0)
        p.append(0)
        i += 1

        messagebox.showinfo("Success", f"Room booked!\nRoom No: {rn}\nCustomer ID: {cid}")
        self.home_screen()

    # -----------------------------
    # ROOMS INFO
    # -----------------------------
    def rooms_info_screen(self):
        self.clear()
        info = (
            "STANDARD NON-AC: Bed, TV, Cupboard, Balcony\n\n"
            "STANDARD AC: Above + AC\n\n"
            "3-Bed NON-AC: Double + Single Bed, Balcony\n\n"
            "3-Bed AC: Above + AC"
        )
        tk.Label(self.root, text="Rooms Information", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text=info, justify="left").pack(pady=10)
        tk.Button(self.root, text="Back", command=self.home_screen).pack()

    # -----------------------------
    # RESTAURANT
    # -----------------------------
    def restaurant_screen(self):
        self.clear()

        tk.Label(self.root, text="Restaurant Billing", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="Customer ID:").pack()
        self.cid_entry = tk.Entry(self.root)
        self.cid_entry.pack()

        tk.Button(self.root, text="Open Menu", command=self.open_menu).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.home_screen).pack()

    def open_menu(self):
        cid = self.cid_entry.get()
        if not cid.isdigit():
            messagebox.showerror("Error", "Enter valid customer ID.")
            return
        cid = int(cid)

        if cid not in custid:
            messagebox.showerror("Error", "Customer not found.")
            return

        self.menu_window(cid)

    def menu_window(self, cid):
        win = tk.Toplevel(self.root)
        win.title("Restaurant Menu")
        win.geometry("400x500")

        items = {
            "Tea": 20, "Coffee": 25, "Sandwich": 50,
            "Shahi Paneer": 110, "Dal Makhani": 150,
            "Roti": 15, "Rice": 90, "Ice Cream": 60
        }

        tk.Label(win, text="Menu Items", font=("Arial", 14, "bold")).pack(pady=10)

        self.menu_vars = {}
        for item, cost in items.items():
            var = tk.IntVar()
            tk.Checkbutton(win, text=f"{item} - Rs {cost}", variable=var).pack(anchor="w")
            self.menu_vars[item] = (var, cost)

        tk.Button(win, text="Add to Bill", command=lambda: self.add_food(win, cid)).pack(pady=20)

    def add_food(self, win, cid):
        total = 0
        for item, (v, cost) in self.menu_vars.items():
            if v.get() == 1:
                total += cost

        idx = custid.index(cid)
        rc[idx] += total

        messagebox.showinfo("Added", f"Added Rs {total} to restaurant bill.")
        win.destroy()

    # -----------------------------
    # PAYMENT
    # -----------------------------
    def payment_screen(self):
        self.clear()
        tk.Label(self.root, text="Payment", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Label(self.root, text="Phone Number:").pack()
        self.pay_entry = tk.Entry(self.root)
        self.pay_entry.pack()

        tk.Button(self.root, text="Pay", command=self.process_payment).pack(pady=15)
        tk.Button(self.root, text="Back", command=self.home_screen).pack()

    def process_payment(self):
        ph = self.pay_entry.get()
        if ph not in phno:
            messagebox.showerror("Error", "Record not found.")
            return

        idx = phno.index(ph)
        total = price[idx] * day[idx] + rc[idx]

        p[idx] = 1  # Mark paid
        rm[idx] = 0
        custid[idx] = 0

        messagebox.showinfo("Paid", f"Payment Successful!\nTotal Paid: Rs {total}")
        self.home_screen()

    # -----------------------------
    # RECORDS
    # -----------------------------
    def records_screen(self):
        self.clear()
        tk.Label(self.root, text="Customer Records", font=("Arial", 16, "bold")).pack(pady=10)

        txt = tk.Text(self.root, width=60, height=15)
        txt.pack()

        if nm:
            for idx in range(len(nm)):
                txt.insert(tk.END, f"{nm[idx]} | {phno[idx]} | {add[idx]} | {checkin[idx]} → {checkout[idx]} | {room[idx]}\n")
        else:
            txt.insert(tk.END, "No Records")

        tk.Button(self.root, text="Back", command=self.home_screen).pack(pady=10)

    # -----------------------------
    # Utility: Clear Window
    # -----------------------------
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# -----------------------------
# Run App
# -----------------------------
root = tk.Tk()
app = HotelApp(root)
root.mainloop()
