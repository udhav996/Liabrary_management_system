import tkinter as tk
from tkinter import messagebox
from db_config import create_connection
import datetime

def issue_book():
    student_id = entry_student.get().strip()
    barcode = entry_barcode.get().strip()

    if not student_id or not barcode:
        messagebox.showwarning("Missing Info", "Please enter Student ID and Book Barcode.")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # ✅ Check if book is available
        cursor.execute("SELECT available_copies FROM books WHERE barcode = %s", (barcode,))
        book = cursor.fetchone()

        if not book:
            messagebox.showerror("Not Found", "Book not found with this barcode.")
            return

        available = book[0]
        if available <= 0:
            messagebox.showinfo("Unavailable", "This book is currently not available.")
            return

        # ✅ Issue the book
        cursor.execute("""
            INSERT INTO issued_books (student_id, barcode, issue_date, status)
            VALUES (%s, %s, %s, 'Issued')
        """, (student_id, barcode, datetime.datetime.now()))

        # ✅ Decrease available copies
        cursor.execute("""
            UPDATE books SET available_copies = available_copies - 1 WHERE barcode = %s
        """, (barcode,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Book issued successfully!")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to issue book: {e}")

def clear_fields():
    entry_student.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)

# 🖼️ GUI
root = tk.Tk()
root.title("Issue Book")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Student ID", bg="#f0f0f0").pack(pady=(20, 5))
entry_student = tk.Entry(root, width=40)
entry_student.pack()

tk.Label(root, text="Book Barcode", bg="#f0f0f0").pack(pady=(10, 5))
entry_barcode = tk.Entry(root, width=40)
entry_barcode.pack()

tk.Button(root, text="📤 Issue Book", command=issue_book, bg="#28a745", fg="white", width=20).pack(pady=20)
tk.Button(root, text="❌ Clear", command=clear_fields, bg="gray", fg="white", width=20).pack()

root.mainloop()
