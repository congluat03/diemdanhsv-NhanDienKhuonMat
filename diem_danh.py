import tkinter as tk

class DiemDanh:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Điểm Danh", font=("Arial", 16, "bold")).pack(pady=10)
