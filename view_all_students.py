import tkinter as tk
from tkinter import ttk, messagebox
from db_config import create_connection

def fetch_students():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, dob, address, library_id, barcode FROM students")
        rows = cursor.fetchall()
        conn.close()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", tk.END, values=row)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI
root = tk.Tk()
root.title("All Students")
root.geometry("800x500")
root.configure(bg="#f0f0f0")

tk.Label(root, text="📋 All Registered Students", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

columns = ("Name", "DOB", "Address", "Library ID", "Barcode")

tree = ttk.Treeview(root, columns=columns, show="headings", height=15)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=150)

tree.pack(padx=10, pady=10)

tk.Button(root, text="🔄 Refresh", command=fetch_students, bg="#007bff", fg="white", width=15).pack(pady=10)

# Fetch on load
fetch_students()

root.mainloop()
