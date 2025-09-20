import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from db_config import create_connection
import csv
import datetime

LOW_STOCK_LIMIT = 2

def get_options(column):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT DISTINCT {column} FROM books")
        results = [row[0] for row in cursor.fetchall()]
        conn.close()
        return ["All"] + results
    except:
        return ["All"]

def load_report():
    subject = subject_var.get()
    author = author_var.get()
    low_stock = low_stock_var.get()
    title_keyword = entry_title_search.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    query = """
        SELECT 
    b.title, b.author, b.subject, b.barcode, 
    SUM(CASE WHEN i.issue_id IS NOT NULL THEN 1 ELSE 0 END) AS issued_count,
    b.available_copies, b.location, b.added_on
FROM books b
LEFT JOIN issued_books i 
    ON b.barcode = i.barcode AND i.return_date IS NULL

    """

    conditions = []
    values = []

    if subject != "All":
        conditions.append("b.subject = %s")
        values.append(subject)

    if author != "All":
        conditions.append("b.author = %s")
        values.append(author)

    if title_keyword:
        conditions.append("b.title LIKE %s")
        values.append(f"%{title_keyword}%")

    if start_date:
        conditions.append("DATE(b.added_on) >= %s")
        values.append(start_date)

    if end_date:
        conditions.append("DATE(b.added_on) <= %s")
        values.append(end_date)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " GROUP BY b.book_id"

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(query, tuple(values))
        rows = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())

        for row in rows:
            tag = "low" if low_stock and row[5] <= LOW_STOCK_LIMIT else "normal"
            tree.insert("", tk.END, values=row[:-1], tags=(tag,))

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load report: {e}")

def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV Files", "*.csv")],
                                             title="Save Report As")
    if not file_path:
        return

    try:
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(columns)
            for row in tree.get_children():
                writer.writerow(tree.item(row)["values"])
        messagebox.showinfo("Success", "Report exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {e}")

# 🖼️ GUI Setup
root = tk.Tk()
root.title("Library Book Report")
root.geometry("1100x570")
root.configure(bg="#f8f9fa")

# Filters Frame
filters_frame = tk.Frame(root, bg="#f8f9fa")
filters_frame.pack(pady=8)

# Title Search
tk.Label(filters_frame, text="Book Title:", bg="#f8f9fa").grid(row=0, column=0, padx=5)
entry_title_search = tk.Entry(filters_frame, width=20)
entry_title_search.grid(row=0, column=1, padx=5)

# Subject Dropdown
tk.Label(filters_frame, text="Subject:", bg="#f8f9fa").grid(row=0, column=2, padx=5)
subject_var = tk.StringVar(value="All")
subject_menu = ttk.Combobox(filters_frame, textvariable=subject_var, state="readonly", width=20)
subject_menu.grid(row=0, column=3, padx=5)

# Author Dropdown
tk.Label(filters_frame, text="Author:", bg="#f8f9fa").grid(row=0, column=4, padx=5)
author_var = tk.StringVar(value="All")
author_menu = ttk.Combobox(filters_frame, textvariable=author_var, state="readonly", width=20)
author_menu.grid(row=0, column=5, padx=5)

# Low Stock Checkbox
low_stock_var = tk.BooleanVar()
tk.Checkbutton(filters_frame, text="Low Stock Only (≤2)", variable=low_stock_var, bg="#f8f9fa").grid(row=0, column=6, padx=5)

# Date Range Filters
tk.Label(filters_frame, text="From (YYYY-MM-DD):", bg="#f8f9fa").grid(row=1, column=0, padx=5)
start_date_entry = tk.Entry(filters_frame, width=15)
start_date_entry.grid(row=1, column=1)

tk.Label(filters_frame, text="To:", bg="#f8f9fa").grid(row=1, column=2, padx=5)
end_date_entry = tk.Entry(filters_frame, width=15)
end_date_entry.grid(row=1, column=3)

tk.Button(filters_frame, text="🔄 Apply Filters", command=load_report, bg="#007bff", fg="white").grid(row=1, column=4, padx=10)

# Report Table
columns = ("Title", "Author", "Subject", "Barcode", "Issued", "Available", "Location")
tree = ttk.Treeview(root, columns=columns, show="headings", height=18)
tree.tag_configure("low", background="#ffdddd")
tree.tag_configure("normal", background="white")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130)

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

tk.Button(root, text="📤 Export to CSV", command=export_to_csv, bg="#28a745", fg="white", width=20).pack(pady=5)

# Load dropdown values and report
subject_menu["values"] = get_options("subject")
author_menu["values"] = get_options("author")
load_report()

root.mainloop()
