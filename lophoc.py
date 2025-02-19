import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class QuanLyLopHoc:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Lớp Học", font=("Arial", 16, "bold"), fg="white", bg="blue").pack(pady=10, fill=tk.X)

        # Khung nhập thông tin lớp học
        form_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        form_frame.pack(pady=10, fill=tk.X)

        tk.Label(form_frame, text="Tên Lớp:", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)
        self.class_name_entry = tk.Entry(form_frame)
        self.class_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Khoa:", bg="lightgray").grid(row=1, column=0, padx=5, pady=5)
        self.department_combobox = ttk.Combobox(form_frame, state="readonly", width=18)
        self.department_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Load danh sách khoa vào combobox
        self.load_departments()

        # Nút thêm, sửa, xóa
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Thêm", bg="green", fg="black", command=self.add_class).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", bg="orange", fg="black", command=self.edit_class).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="red", fg="black", command=self.delete_class).pack(side=tk.LEFT, padx=5)

        # Tạo Treeview để hiển thị danh sách lớp học
        columns = ("ID", "Tên Lớp", "Khoa")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Gán sự kiện khi chọn dòng
        self.tree.bind("<<TreeviewSelect>>", self.select_class)

        self.load_data()

    def load_departments(self):
        """Nạp danh sách khoa vào Combobox"""
        self.cursor.execute("SELECT ID_KHOA, TENKHOA FROM khoa")
        rows = self.cursor.fetchall()
        self.department_dict = {row[1]: row[0] for row in rows}  # Tạo từ điển {Tên Khoa: ID_Khoa}
        self.department_combobox["values"] = list(self.department_dict.keys())

    def add_class(self):
        class_name = self.class_name_entry.get()
        department = self.department_combobox.get()
        department_id = self.department_dict.get(department)

        if not class_name or not department_id:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        query = "INSERT INTO lophoc (TENLOP, ID_KHOA) VALUES (%s, %s)"
        self.cursor.execute(query, (class_name, department_id))
        self.db.commit()
        messagebox.showinfo("Thành công", "Thêm lớp học thành công!")
        self.load_data()

    def edit_class(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn lớp học cần sửa!")
            return

        item = self.tree.item(selected_item[0])
        class_id = item['values'][0]
        class_name = self.class_name_entry.get()
        department = self.department_combobox.get()
        department_id = self.department_dict.get(department)

        if not class_name or not department_id:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        query = "UPDATE lophoc SET TENLOP=%s, ID_KHOA=%s WHERE ID_LOP=%s"
        self.cursor.execute(query, (class_name, department_id, class_id))
        self.db.commit()
        messagebox.showinfo("Thành công", "Sửa thông tin lớp học thành công!")
        self.load_data()

    def delete_class(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn lớp học cần xóa!")
            return

        item = self.tree.item(selected_item[0])
        class_id = item['values'][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa lớp học này?")
        if confirm:
            query = "DELETE FROM lophoc WHERE ID_LOP=%s"
            self.cursor.execute(query, (class_id,))
            self.db.commit()
            messagebox.showinfo("Thành công", "Xóa lớp học thành công!")
            self.load_data()

    def load_data(self):
        """Tải dữ liệu lớp học vào Treeview"""
        self.tree.delete(*self.tree.get_children())
        query = "SELECT lophoc.ID_LOP, lophoc.TENLOP, khoa.TENKHOA FROM lophoc INNER JOIN khoa ON lophoc.ID_KHOA = khoa.ID_KHOA"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def select_class(self, event):
        """Lấy dữ liệu từ dòng được chọn để hiển thị lên form nhập"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0], "values")

        # Điền thông tin vào ô nhập
        self.class_name_entry.delete(0, tk.END)
        self.class_name_entry.insert(0, item[1])

        # Điền thông tin khoa vào Combobox
        khoa_name = item[2]
        if khoa_name in self.department_dict:
            self.department_combobox.set(khoa_name)
        else:
            self.department_combobox.set("")
