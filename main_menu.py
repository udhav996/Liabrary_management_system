import tkinter as tk
from tkinter import messagebox
import subprocess
import sys, os
from PIL import Image, ImageTk, ImageSequence

# ====== CONFIG ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GIF_PATH = os.path.join(BASE_DIR, "assets/book.gif")
SPLASH_DURATION = 2500  # ms (2.5 sec)

# ====== Functions ======
def open_script(script):
    try:
        script_path = os.path.join(BASE_DIR, script)
        subprocess.Popen([sys.executable, script_path], cwd=BASE_DIR)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open {script}:\n{e}")

# ====== Splash Screen ======
class SplashScreen(tk.Toplevel):
    def __init__(self, parent, on_close):
        super().__init__(parent)
        self.overrideredirect(True)
        self.geometry("600x400+400+200")  # adjust position
        self.configure(bg="white")

        self.gif = Image.open(GIF_PATH)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA"))
                       for frame in ImageSequence.Iterator(self.gif)]

        self.label = tk.Label(self, bg="white")
        self.label.pack(expand=True)

        self.frame_index = 0
        self.after(0, self.animate_gif)

        # Close splash and call main UI after delay
        self.after(SPLASH_DURATION, lambda: (self.destroy(), on_close()))

    def animate_gif(self):
        frame = self.frames[self.frame_index]
        self.label.configure(image=frame)
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(80, self.animate_gif)

# ====== Main Menu ======
def show_main_menu():
    root = tk.Tk()
    root.title("📚 Library Management System")
    root.geometry("600x520")
    root.configure(bg="#f0f0f0")

    tk.Label(root, text="📘 Library Dashboard", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack()

    buttons = [
        ("Add Student", "add_student.py"),
        ("Add Book", "add_book.py"),
        ("Issue Book", "issue_book.py"),
        ("View Student", "view_student.py"),
        ("Search Book", "search_book.py"),
        ("View Student Books", "view_student_books.py"),
        ("Dashboard ", "dashboard.py"),
        ("Generate ID Card", "generate_id_card.py"),
        ("View All Students", "view_all_students.py"),
        ("View Issued Books", "view_issued_books.py"),
        ("Return Book", "return_book.py"),
        ("Book Report", "book_report.py")
    ]

    left_column = tk.Frame(frame, bg="#f0f0f0")
    left_column.grid(row=0, column=0, padx=20)

    right_column = tk.Frame(frame, bg="#f0f0f0")
    right_column.grid(row=0, column=1, padx=20)

    for idx, (text, script) in enumerate(buttons):
        col = left_column if idx % 2 == 0 else right_column
        tk.Button(col, text=text, width=25, bg="#28a745", fg="white",
                  font=("Arial", 11), command=lambda f=script: open_script(f)).pack(pady=6)

    tk.Button(root, text="❌ Exit", command=root.destroy,
              bg="#dc3545", fg="white", font=("Arial", 11), width=30).pack(pady=20)

    root.mainloop()

# ====== App Start ======
if __name__ == "__main__":
    splash_root = tk.Tk()
    splash_root.withdraw()  # hide root window during splash

    SplashScreen(splash_root, show_main_menu)
    splash_root.mainloop()
