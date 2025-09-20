import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import shutil
import os
import uuid
from datetime import datetime
from db_config import create_connection
from barcode import Code128
from barcode.writer import ImageWriter

# ---------------- Setup ----------------
PHOTO_DIR = "assets/photos"
BARCODE_DIR = "assets/barcodes"
DEFAULT_IMG_PATH = "assets/udhav_image.png"

os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(BARCODE_DIR, exist_ok=True)

photo_img = None
default_photo = None

def generate_library_id():
    return f"LIB{uuid.uuid4().int % 10000:04d}"

# ---------------- Upload Photo ----------------
def upload_photo():
    global photo_img
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        img = Image.open(file_path).resize((100, 100))
        photo_img = ImageTk.PhotoImage(img)
        photo_label.config(image=photo_img)
        photo_label.image = photo_img
        photo_label.image_path = file_path
        print("Uploaded:", file_path)

# ---------------- Save Student ----------------
def save_student():
    name = entry_name.get().strip()
    dob_input = entry_dob.get().strip()
    address = entry_address.get("1.0", tk.END).strip()
    photo_path = getattr(photo_label, 'image_path', '')

    try:
        dob = datetime.strptime(dob_input, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Invalid Date", "Please enter DOB in DD/MM/YYYY format (e.g., 19/07/2002).")
        return

    if not name or not dob or not address or not photo_path:
        messagebox.showwarning("Missing Info", "Please fill in all fields and upload a photo.")
        return

    lib_id = generate_library_id()
    barcode_id = lib_id  # barcode same as library_id for now

    filename = f"{lib_id}_{os.path.basename(photo_path)}"
    target_path = os.path.join(PHOTO_DIR, filename)
    shutil.copy(photo_path, target_path)

    # ✅ Generate Barcode Image
    barcode_path = os.path.join(BARCODE_DIR, barcode_id)
    barcode_image = Code128(barcode_id, writer=ImageWriter())
    barcode_image.save(barcode_path)  # Saves as .png

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = """
            INSERT INTO students (name, dob, address, photo_path, library_id, barcode)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (name, dob, address, target_path, lib_id, barcode_id)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Student added!\nLibrary ID: {lib_id}")
        clear_form()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save student: {e}")

# ---------------- Clear Form ----------------
def clear_form():
    entry_name.delete(0, tk.END)
    entry_dob.delete(0, tk.END)
    entry_address.delete("1.0", tk.END)
    photo_label.config(image=default_photo)
    photo_label.image = default_photo
    photo_label.image_path = ""

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Add Student - Library Manager")
root.geometry("400x650")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20, padx=20, fill='both', expand=True)

tk.Label(frame, text="Student Name", bg="#f0f0f0").pack(pady=(10, 0))
entry_name = tk.Entry(frame, width=40)
entry_name.pack()

tk.Label(frame, text="Date of Birth (DD/MM/YYYY)", bg="#f0f0f0").pack(pady=(10, 0))
entry_dob = tk.Entry(frame, width=40)
entry_dob.pack()

tk.Label(frame, text="Address", bg="#f0f0f0").pack(pady=(10, 0))
entry_address = tk.Text(frame, width=30, height=4)
entry_address.pack()

tk.Label(frame, text="Upload Student Photo", bg="#f0f0f0").pack(pady=(10, 0))
default_img = Image.open(DEFAULT_IMG_PATH).resize((100, 100))
default_photo = ImageTk.PhotoImage(default_img)

photo_label = tk.Label(frame, image=default_photo, relief="solid", bd=2)
photo_label.image = default_photo
photo_label.image_path = ""
photo_label.pack(pady=5)

tk.Button(frame, text="📷 Choose Photo", command=upload_photo, bg="#007bff", fg="white", width=20).pack(pady=5)
tk.Button(frame, text="✅ Add Student", command=save_student, bg="#28a745", fg="white", width=20).pack(pady=15)

root.mainloop()
