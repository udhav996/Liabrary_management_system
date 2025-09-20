import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_config import create_connection
import os

# 📁 Fallback image path (optional, used only if actual image missing)
DEFAULT_IMG_PATH = "assets/default.png"

# 🔁 Clear all fields and remove photo
def clear_fields():
    entry_name.delete(0, tk.END)
    lbl_result.config(text="")
    photo_label.config(image=None, text="")  # 🧹 remove image
    photo_label.image = None

# 🔍 View student by ID or name
def view_student():
    keyword = entry_name.get().strip()

    if not keyword:
        messagebox.showwarning("Input Required", "Please enter a student name or library ID.")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, dob, address, photo_path, library_id
            FROM students
            WHERE library_id = %s OR name = %s
        """, (keyword, keyword))
        result = cursor.fetchone()
        conn.close()

        if not result:
            messagebox.showinfo("Not Found", "No student found with that ID or name.")
            return

        name, dob, address, photo_path, lib_id = result
        lbl_result.config(text=f"Name: {name}\nDOB: {dob}\nAddress: {address}\nLibrary ID: {lib_id}")

        # Load image from path (or fallback to default if missing)
        if os.path.exists(photo_path):
            img = Image.open(photo_path).resize((100, 100))
        else:
            img = Image.open(DEFAULT_IMG_PATH).resize((100, 100))

        photo = ImageTk.PhotoImage(img)
        photo_label.config(image=photo)
        photo_label.image = photo

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI Setup
root = tk.Tk()
root.title("View Student")
root.geometry("400x450")
root.configure(bg="#f0f0f0")

# --- UI Layout ---
tk.Label(root, text="Enter Library ID or Name:", bg="#f0f0f0").pack(pady=(10, 2))
entry_name = tk.Entry(root, width=30)
entry_name.pack()

# Buttons
tk.Button(root, text="🔍 Search", command=view_student, bg="#007bff", fg="white").pack(pady=5)
tk.Button(root, text="❌ Clear", command=clear_fields, bg="gray", fg="white").pack(pady=5)

# Result area
lbl_result = tk.Label(root, text="", justify="left", bg="#f0f0f0", font=("Arial", 10))
lbl_result.pack(pady=10)

# Image display (blank initially)
photo_label = tk.Label(root, bg="white", width=100, height=100, relief="solid")
photo_label.image = None
photo_label.pack(pady=10)

root.mainloop()
