import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_config import create_connection
import os
import uuid
from barcode import Code128
from barcode.writer import ImageWriter

BARCODE_DIR = "assets/barcodes"
os.makedirs("assets", exist_ok=True)
os.makedirs(BARCODE_DIR, exist_ok=True)

barcode_photo = None

def generate_barcode_id():
    return f"BOOK{uuid.uuid4().int % 10000:04d}"

def generate_barcode_image(barcode_id):
    barcode = Code128(barcode_id, writer=ImageWriter())
    file_path = os.path.join(BARCODE_DIR, barcode_id)
    full_path = barcode.save(file_path)
    return full_path

def save_book():
    global barcode_photo

    title = entry_title.get().strip()
    author = entry_author.get().strip()
    subject = entry_subject.get().strip()
    copies = entry_available.get().strip()
    location = entry_location.get().strip()

    if not title or not author or not subject or not copies.isdigit():
        messagebox.showwarning("Missing Info", "Please fill in all fields properly.")
        return

    copies = int(copies)
    barcode_id = generate_barcode_id()
    barcode_path = generate_barcode_image(barcode_id)

    try:
        conn = create_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO books (title, author, subject, barcode, available_copies, location)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (title, author, subject, barcode_id, copies, location)
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"Book added!\nBarcode: {barcode_id}")
        clear_form()

        img = Image.open(barcode_path).resize((200, 80))
        barcode_photo = ImageTk.PhotoImage(img)
        barcode_label.config(image=barcode_photo)
        barcode_label.image = barcode_photo

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save book: {e}")

def clear_form():
    entry_title.delete(0, tk.END)
    entry_author.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_available.delete(0, tk.END)
    entry_location.delete(0, tk.END)
    barcode_label.config(image=None)
    barcode_label.image = None

# 🖼️ GUI
root = tk.Tk()
root.title("Add Book")
root.geometry("400x600")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Book Title", bg="#f0f0f0").pack(pady=(10, 0))
entry_title = tk.Entry(root, width=40)
entry_title.pack()

tk.Label(root, text="Author", bg="#f0f0f0").pack(pady=(10, 0))
entry_author = tk.Entry(root, width=40)
entry_author.pack()

tk.Label(root, text="Subject", bg="#f0f0f0").pack(pady=(10, 0))
entry_subject = tk.Entry(root, width=40)
entry_subject.pack()

tk.Label(root, text="Available Copies", bg="#f0f0f0").pack(pady=(10, 0))
entry_available = tk.Entry(root, width=40)
entry_available.pack()

tk.Label(root, text="Location (e.g., A1, B3)", bg="#f0f0f0").pack(pady=(10, 0))
entry_location = tk.Entry(root, width=40)
entry_location.pack()

tk.Button(root, text="📚 Add Book", command=save_book, bg="#28a745", fg="white", width=20).pack(pady=15)
tk.Button(root, text="❌ Clear", command=clear_form, bg="gray", fg="white", width=20).pack()

barcode_label = tk.Label(root, bg="#f0f0f0")
barcode_label.pack(pady=20)

root.mainloop()
