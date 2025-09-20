import tkinter as tk
from tkinter import ttk, messagebox
from db_config import create_connection

def fetch_issued_books():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.title, b.barcode, s.name, s.library_id, ib.issue_date,
                   IFNULL(ib.return_date, '---') AS return_date,
                   CASE WHEN ib.return_date IS NULL THEN 'Issued' ELSE 'Returned' END AS status
            FROM issued_books ib
            JOIN books b ON ib.barcode = b.barcode
            JOIN students s ON ib.student_id = s.library_id
            ORDER BY ib.issue_date DESC
        """)
        rows = cursor.fetchall()
        conn.close()

        # Clear previous data
        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("Issued Book Records")
root.geometry("1000x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="📘 Issued Book History", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

columns = ("Title", "Barcode", "Student Name", "Library ID", "Issue Date", "Return Date", "Status")
tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)

tree.pack(padx=10, pady=10)

tk.Button(root, text="🔄 Refresh", command=fetch_issued_books, bg="#007bff", fg="white", width=15).pack(pady=10)

# Load on start
fetch_issued_books()

root.mainloop()
