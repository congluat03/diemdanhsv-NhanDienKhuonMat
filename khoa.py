import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class QuanLyKhoa:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Khoa", font=("Arial", 16, "bold"), fg="white", bg="blue").pack(pady=10, fill=tk.X)

        # Khung nhập thông tin khoa
        form_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        form_frame.pack(pady=10, fill=tk.X)

        tk.Label(form_frame, text="Tên Khoa:", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)
        self.department_name_entry = tk.Entry(form_frame)
        self.department_name_entry.grid(row=0, column=1, padx=5, pady=5)

        # Nút thêm, sửa, xóa
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Thêm", bg="green", fg="black", command=self.add_department).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", bg="orange", fg="black", command=self.edit_department).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="red", fg="black", command=self.delete_department).pack(side=tk.LEFT, padx=5)

        # Tạo Treeview để hiển thị danh sách khoa
        columns = ("ID", "Tên Khoa")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        self.tree.bind("<ButtonRelease-1>", self.select_khoa)  # Lấy dữ liệu khi click vào dòng

        self.load_data()


    def select_khoa(self, event):
        """Lấy dữ liệu từ dòng được chọn để hiển thị lên form nhập"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item, "values")

        self.department_name_entry.delete(0, tk.END)
        self.department_name_entry.insert(0, item[1])

    def add_department(self):
        department_name = self.department_name_entry.get()

        query = "INSERT INTO khoa (TENKHOA) VALUES (%s)"
        self.cursor.execute(query, (department_name,))
        self.db.commit()
        messagebox.showinfo("Thành công", "Thêm khoa thành công!")
        self.load_data()

    def edit_department(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khoa cần sửa!")
            return

        item = self.tree.item(selected_item)
        department_id = item['values'][0]
        department_name = self.department_name_entry.get()

        query = "UPDATE khoa SET TENKHOA=%s WHERE ID_KHOA=%s"
        self.cursor.execute(query, (department_name, department_id))
        self.db.commit()
        messagebox.showinfo("Thành công", "Sửa thông tin khoa thành công!")
        self.load_data()

    def delete_department(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn khoa cần xóa!")
            return

        item = self.tree.item(selected_item)
        department_id = item['values'][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khoa này?")
        if confirm:
            query = "DELETE FROM khoa WHERE ID_KHOA=%s"
            self.cursor.execute(query, (department_id,))
            self.db.commit()
            messagebox.showinfo("Thành công", "Xóa khoa thành công!")
            self.load_data()

    def load_data(self, condition=""):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT ID_KHOA, TENKHOA FROM khoa" + condition
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)
