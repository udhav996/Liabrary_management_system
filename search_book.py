import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from db_config import create_connection
import os

BARCODE_DIR = "assets/barcodes"
barcode_image = None

def search_book():
    global barcode_image
    keyword = entry_search.get().strip()

    if not keyword:
        messagebox.showwarning("Missing Info", "Enter Book Title or Barcode.")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
        SELECT title, author, subject, barcode, available_copies, location
        FROM books
        WHERE title = %s OR barcode = %s
        """, (keyword, keyword))
        book = cursor.fetchone()
        conn.close()

        if not book:
            messagebox.showinfo("Not Found", "No book found with this title or barcode.")
            return

        title, author, subject, barcode, available, location = book
        result = (
            f"📘 Title: {title}\n👤 Author: {author}\n📚 Subject: {subject}\n"
            f"🔖 Barcode: {barcode}\n✅ Available Copies: {available}\n📍 Location: {location}"
        )
        lbl_result.config(text=result)

        # Load barcode image
        image_path = os.path.join(BARCODE_DIR, f"{barcode}.png")
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((200, 80))
            barcode_image = ImageTk.PhotoImage(img)
            barcode_label.config(image=barcode_image)
            barcode_label.image = barcode_image
        else:
            barcode_label.config(image=None)
            barcode_label.image = None

    except Exception as e:
        messagebox.showerror("Error", str(e))

def clear_fields():
    entry_search.delete(0, tk.END)
    lbl_result.config(text="")
    barcode_label.config(image="", text="")
    barcode_label.image = None

# GUI setup
root = tk.Tk()
root.title("Search Book")
root.geometry("420x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Search by Title or Barcode:", bg="#f0f0f0").pack(pady=10)
entry_search = tk.Entry(root, width=40)
entry_search.pack()

tk.Button(root, text="🔍 Search", command=search_book, bg="#007bff", fg="white", width=20).pack(pady=5)
tk.Button(root, text="❌ Clear", command=clear_fields, bg="gray", fg="white", width=20).pack(pady=5)

lbl_result = tk.Label(root, text="", justify="left", bg="#f0f0f0", font=("Arial", 10))
lbl_result.pack(pady=10)

barcode_label = tk.Label(root, bg="#f0f0f0")
barcode_label.pack(pady=10)

root.mainloop()
