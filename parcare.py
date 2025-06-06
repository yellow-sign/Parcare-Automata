import tkinter as tk
import serial
import time

# === Conexiunea cu Arduino ===
try:
    arduino = serial.Serial('COM3', 9600)
    time.sleep(2)
    print("Connected to Arduino.")
except Exception as e:
    arduino = None
    print("Could not connect to Arduino:", e)

# === Date Parcare ===
parking_spots = {
    1: {'taken': False, 'name': '', 'code': ''},
    2: {'taken': False, 'name': '', 'code': ''},
    3: {'taken': False, 'name': '', 'code': ''},
    4: {'taken': False, 'name': '', 'code': ''},
}

# === Comanda spre Arduino ===
def send_command(slot):
    print(f"Trimis: Parcare {slot}")
    if arduino:
        arduino.write(f"{slot}\n".encode())

# === Centrare ===
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'+{x}+{y}')

# === Click asupra unei parcari ===
def handle_parking_spot(slot):
    current = parking_spots[slot]
    if not current['taken']:
        # Dialog pentru rezervare
        dialog = tk.Toplevel(root)
        dialog.title("Introduceti detalii")

        # Introducerea Numelui
        tk.Label(dialog, text="Nume:").grid(row=0, column=0, padx=5, pady=5)
        name_entry = tk.Entry(dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Alegerea Codului
        tk.Label(dialog, text="Cod:").grid(row=1, column=0, padx=5, pady=5)
        code_entry = tk.Entry(dialog, show="*")
        code_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button OK
        def ok_clicked():
            name = name_entry.get().strip()
            code = code_entry.get().strip()
            if name and code:
                parking_spots[slot]['taken'] = True
                parking_spots[slot]['name'] = name
                parking_spots[slot]['code'] = code
                buttons[slot-1].config(text=f"Parcare {slot}\n{name}", bg="#ff9999")
                send_command(slot)
                dialog.destroy()
            else:
                tk.Label(dialog, text="Va rugam, introduceti toate detaliile!", fg="red").grid(row=2, columnspan=2)
        tk.Button(dialog, text="OK", command=ok_clicked).grid(row=3, columnspan=2, pady=5)

        center_window(dialog)
        dialog.grab_set()

    else:
        # Introducerea Codului
        dialog = tk.Toplevel(root)
        dialog.title("Introduceti Codul")
        tk.Label(dialog, text="Cod:").grid(row=0, column=0, padx=5, pady=5)
        code_entry = tk.Entry(dialog, show="*")
        code_entry.grid(row=0, column=1, padx=5, pady=5)

        # Button OK
        def ok_clicked():
            entered_code = code_entry.get().strip()
            if entered_code == parking_spots[slot]['code']:
                # Free the parking spot
                parking_spots[slot]['taken'] = False
                parking_spots[slot]['name'] = ''
                parking_spots[slot]['code'] = ''
                buttons[slot-1].config(text=f"Parcare {slot}", bg="#4da6ff")
                send_command(slot)
                dialog.destroy()
            else:
                tk.Label(dialog, text="Cod gresit!", fg="red").grid(row=1, columnspan=2)
        tk.Button(dialog, text="OK", command=ok_clicked).grid(row=2, columnspan=2, pady=5)

        center_window(dialog)
        dialog.grab_set()

# === Setup GUI ===
root = tk.Tk()
root.title("Selector Parcare")
root.geometry("300x400")
root.configure(bg="#f5f5f5")

# Centerare
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'+{x}+{y}')

# === Interfata ===
title = tk.Label(root, text="Selectează o parcare", font=("Helvetica", 18, "bold"), bg="#f5f5f5", fg="#333")
title.pack(pady=30)

# === Butoane ===
buttons = []
for i in range(1, 5):
    button = tk.Button(root, text=f"Parcare {i}",
                       font=("Helvetica", 14),
                       bg="#4da6ff", fg="#4C7D4C",
                       activebackground="#3399ff",
                       relief="flat",
                       padx=10, pady=5,
                       command=lambda n=i: handle_parking_spot(n))
    button.pack(pady=10)
    buttons.append(button)

# === Run GUI Loop ===
root.mainloop()
