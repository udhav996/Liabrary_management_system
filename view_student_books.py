import tkinter as tk
from tkinter import messagebox
from db_config import create_connection

def fetch_student_and_books():
    barcode_value = entry_barcode.get().strip()

    if not barcode_value:
        messagebox.showwarning("Missing Input", "Please scan or enter student barcode.")
        return

    try:
        conn = create_connection()
        cursor = conn.cursor()

        # 🔍 Fetch student using barcode
        cursor.execute("SELECT name, dob, address, library_id FROM students WHERE barcode = %s", (barcode_value,))
        student = cursor.fetchone()

        if not student:
            messagebox.showerror("Not Found", f"No student found with barcode: {barcode_value}")
            return

        name, dob, address, library_id = student
        lbl_student.config(text=f"🆔 Library ID: {library_id}\n👤 Name: {name}\n📅 DOB: {dob}\n🏠 Address: {address}")

        # 📚 Get books using library_id
        cursor.execute("""
            SELECT b.title, b.barcode,
                   CASE WHEN ib.return_date IS NULL THEN 'Issued' ELSE 'Returned' END AS status
            FROM issued_books ib
            JOIN books b ON ib.barcode = b.barcode
            WHERE ib.student_id = %s
        """, (library_id,))
        books = cursor.fetchall()
        conn.close()

        if not books:
            lbl_books.config(text="📘 No books currently borrowed.")
            return

        book_list = "📚 Books Borrowed:\n"
        for title, barcode, status in books:
            book_list += f"🔖 {title} (Barcode: {barcode}) — {status}\n"

        lbl_books.config(text=book_list)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ✅ Clear Fields Function
def clear_fields():
    entry_barcode.delete(0, tk.END)
    lbl_student.config(text="")
    lbl_books.config(text="")
    entry_barcode.focus()

# GUI Setup
root = tk.Tk()
root.title("Student Book Record")
root.geometry("550x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="📷 Scan Student Barcode:", bg="#f0f0f0", font=("Arial", 12)).pack(pady=10)
entry_barcode = tk.Entry(root, width=30, font=("Arial", 12))
entry_barcode.pack()
entry_barcode.focus()

tk.Button(root, text="🔍 Search", command=fetch_student_and_books, bg="#007bff", fg="white", width=20).pack(pady=10)
tk.Button(root, text="❌ Clear", command=clear_fields, bg="gray", fg="white", width=20).pack(pady=5)

lbl_student = tk.Label(root, text="", bg="#f0f0f0", justify="left", font=("Arial", 11))
lbl_student.pack(pady=10)

lbl_books = tk.Label(root, text="", bg="#f0f0f0", justify="left", font=("Arial", 11))
lbl_books.pack(pady=10)

# 🔁 Enable Enter key to trigger search
entry_barcode.bind("<Return>", lambda event: fetch_student_and_books())

root.mainloop()
