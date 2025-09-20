import tkinter as tk
from tkinter import messagebox
from db_config import create_connection
import datetime

def return_book():
    student_id = entry_student.get().strip()
    barcode = entry_barcode.get().strip()

    if not student_id or not barcode:
        messagebox.showwarning("Missing Info", "Please enter Student ID and Book Barcode.")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # ✅ Check if this book is issued to the student and not yet returned
        cursor.execute("""
            SELECT issue_id FROM issued_books 
            WHERE student_id = %s AND barcode = %s AND return_date IS NULL
        """, (student_id, barcode))
        record = cursor.fetchone()

        if not record:
            messagebox.showinfo("Not Found", "No active issue found for this student and book.")
            return

        issue_id = record[0]

        # ✅ Update return_date and status
        cursor.execute("""
            UPDATE issued_books 
            SET return_date = %s, status = 'Returned' 
            WHERE issue_id = %s
        """, (datetime.date.today(), issue_id))

        # ✅ Increase available copies in books table
        cursor.execute("""
            UPDATE books 
            SET available_copies = available_copies + 1 
            WHERE barcode = %s
        """, (barcode,))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Book returned successfully.")
        clear_fields()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to return book: {e}")

def clear_fields():
    entry_student.delete(0, tk.END)
    entry_barcode.delete(0, tk.END)

# 🖼️ GUI
root = tk.Tk()
root.title("Return Book")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Student ID", bg="#f0f0f0").pack(pady=(20, 5))
entry_student = tk.Entry(root, width=40)
entry_student.pack()

tk.Label(root, text="Book Barcode", bg="#f0f0f0").pack(pady=(10, 5))
entry_barcode = tk.Entry(root, width=40)
entry_barcode.pack()

tk.Button(root, text="🔁 Return Book", command=return_book, bg="#17a2b8", fg="white", width=20).pack(pady=20)
tk.Button(root, text="❌ Clear", command=clear_fields, bg="gray", fg="white", width=20).pack()

root.mainloop()
