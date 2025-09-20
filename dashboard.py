import tkinter as tk
from tkinter import messagebox, filedialog
from db_config import create_connection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Summary Counts
def fetch_summary():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(available_copies) FROM books")
    total_books = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL")
    total_issued = cursor.fetchone()[0]
    conn.close()
    return total_books, total_students, total_issued

# Pie Chart
def draw_pie_chart(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(available_copies) FROM books")
    available = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM issued_books WHERE return_date IS NULL")
    issued = cursor.fetchone()[0] or 0
    conn.close()

    fig = Figure(figsize=(4.5, 3.8))
    ax = fig.add_subplot(111)
    ax.pie([available, issued], labels=["Available", "Issued"], autopct='%1.1f%%', startangle=90,
           colors=['#28a745', '#dc3545'])
    ax.set_title("Book Availability")

    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Bar Chart
def draw_subject_bar_chart(frame):
    for widget in frame.winfo_children():
        widget.destroy()

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT subject, SUM(available_copies)
        FROM books
        GROUP BY subject
        ORDER BY SUM(available_copies) DESC
    """)
    results = cursor.fetchall()
    conn.close()

    subjects = [r[0] for r in results]
    counts = [r[1] for r in results]

    fig = Figure(figsize=(5.5, 3.8))
    ax = fig.add_subplot(111)
    bars = ax.bar(subjects, counts, color="#007bff", edgecolor='black', width=0.4)

    ax.set_title("Books by Subject", fontsize=11)
    ax.set_ylabel("Available Copies")
    ax.set_xlabel("Subjects")
    ax.tick_params(axis='x', rotation=30)

    # Orange-colored count text above each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.3, str(int(height)),
                ha='center', fontsize=9, color='orange', fontweight='bold')

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Export to PDF
def export_pdf():
    file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
    if not file:
        return

    pdf = canvas.Canvas(file, pagesize=letter)
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(40, 750, "Library Dashboard Report")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, 730, f"📚 Total Books: {total_books}")
    pdf.drawString(200, 730, f"👤 Total Students: {total_students}")
    pdf.drawString(400, 730, f"📤 Issued Books: {total_issued}")
    pdf.save()
    messagebox.showinfo("Exported", "PDF saved successfully.")

# Refresh Handler
def refresh_charts():
    draw_pie_chart(frame_pie)
    draw_subject_bar_chart(frame_bar)

# GUI Setup
root = tk.Tk()
root.title("Library Dashboard")
root.geometry("1050x720")
root.configure(bg="#f0f0f0")

# Summary
summary_frame = tk.Frame(root, bg="#f0f0f0")
summary_frame.pack(pady=15)

total_books, total_students, total_issued = fetch_summary()

tk.Label(summary_frame, text=f"📚 Books: {total_books}", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=0, padx=30)
tk.Label(summary_frame, text=f"👤 Students: {total_students}", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=1, padx=30)
tk.Label(summary_frame, text=f"📤 Issued: {total_issued}", font=("Arial", 14), bg="#f0f0f0").grid(row=0, column=2, padx=30)

# Charts Section
chart_frame = tk.Frame(root, bg="#f0f0f0")
chart_frame.pack(pady=10)

frame_pie = tk.LabelFrame(chart_frame, text="Book Availability", bg="#f0f0f0")
frame_pie.grid(row=0, column=0, padx=20)

frame_bar = tk.LabelFrame(chart_frame, text="Books by Subject", bg="#f0f0f0")
frame_bar.grid(row=0, column=1, padx=20)

# Initial Chart Load
draw_pie_chart(frame_pie)
draw_subject_bar_chart(frame_bar)

# Export + Refresh Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)

tk.Button(button_frame, text="📄 Export to PDF", command=export_pdf, bg="#007bff", fg="white", font=("Arial", 11)).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="🔁 Refresh Charts", command=refresh_charts, bg="#28a745", fg="white", font=("Arial", 11)).grid(row=0, column=1, padx=10)

root.mainloop()
