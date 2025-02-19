import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class QuanLyGiangVien:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Giang Vien", font=("Arial", 16, "bold"), fg="white", bg="blue").pack(
            pady=10, fill=tk.X)

        form_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        form_frame.pack(pady=10, fill=tk.X)

        tk.Label(form_frame, text="Tên Giang Vien:", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)
        self.department_name_entry = tk.Entry(form_frame)
        self.department_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Chọn Khoa:", bg="lightgray").grid(row=1, column=0, padx=5, pady=5)
        self.combo_khoa = ttk.Combobox(form_frame, state="readonly")
        self.combo_khoa.grid(row=1, column=1, padx=5, pady=5)

        # Load danh sách khoa vào combobox
        self.load_khoa()

        # Nút thêm, sửa, xóa
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Thêm", bg="green", fg="black", command=self.add_GV).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", bg="orange", fg="black", command=self.edit_GV).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="red", fg="black", command=self.delete_GV).pack(side=tk.LEFT, padx=5)

        # Tạo Treeview để hiển thị danh sách khoa
        columns = ("ID", "Ten Giang Vien", "Ten Khoa")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

            # **Gán sự kiện khi chọn dòng**
        self.tree.bind("<<TreeviewSelect>>", self.select_giangvien)

        self.load_data()

    def add_GV(self):
        department_name = self.department_name_entry.get()
        selected_khoa_name = self.combo_khoa.get()  # Lấy tên khoa đã chọn từ combobox

        if not department_name or not selected_khoa_name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Lấy ID_KHOA tương ứng từ tên khoa
        selected_khoa_id = self.khoa_dict.get(selected_khoa_name)

        if selected_khoa_id is None:
            messagebox.showerror("Lỗi", "Khoa không hợp lệ!")
            return
        try:
            # Chèn dữ liệu vào bảng giaovien
            query = "INSERT INTO giaovien (TENGIAOVIEN, ID_KHOA) VALUES (%s, %s)"
            self.cursor.execute(query, (department_name, selected_khoa_id))
            self.db.commit()

            messagebox.showinfo("Thành công", "Thêm giáo viên thành công!")

            # Xóa dữ liệu sau khi thêm
            self.department_name_entry.delete(0, tk.END)
            self.combo_khoa.set("")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm giáo viên: {str(e)}")

        self.load_data()

    def load_khoa(self):
        self.cursor.execute("SELECT ID_KHOA, TENKHOA FROM khoa")
        rows = self.cursor.fetchall()
        self.khoa_dict = {row[1]: row[0] for row in rows}
        self.combo_khoa["values"] = list(self.khoa_dict.keys())

    def load_data(self, condition=""):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT giaovien.ID_GIAOVIEN, giaovien.TENGIAOVIEN, khoa.TENKHOA FROM giaovien INNER JOIN khoa ON giaovien.ID_KHOA = khoa.ID_KHOA" + condition
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def select_giangvien(self, event):
        """Lấy dữ liệu từ dòng được chọn để hiển thị lên form nhập"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0], "values")

        # Cập nhật thông tin vào Entry và Combobox
        self.department_name_entry.delete(0, tk.END)
        self.department_name_entry.insert(0, item[1])

        # Điền tên khoa vào combobox (đảm bảo combobox chứa giá trị hợp lệ)
        khoa_name = item[2]
        if khoa_name in self.khoa_dict:
            self.combo_khoa.set(khoa_name)
        else:
            self.combo_khoa.set("")

    def edit_GV(self):
        selected_item = self.tree.selection()
        selected_khoa_name = self.combo_khoa.get()
        department_name = self.department_name_entry.get()

        if not department_name or not selected_khoa_name:
            messagebox.showwarning("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        selected_khoa_id = self.khoa_dict.get(selected_khoa_name)

        if selected_khoa_id is None:
            messagebox.showerror("Lỗi", "Không hợp lệ!")
            return

        item = self.tree.item(selected_item)
        department_id = item['values'][0]
        department_name = self.department_name_entry.get()

        query = "UPDATE giaovien SET TENGIAOVIEN=%s, ID_KHOA=%s WHERE ID_GIAOVIEN=%s"
        self.cursor.execute(query, (department_name, selected_khoa_id, department_id))
        self.db.commit()
        messagebox.showinfo("Thành công", "Sửa thông tin thành công!")
        self.load_data()

    def delete_GV(self):
        selected_item = self.tree.selection()
        item = self.tree.item(selected_item)
        department_id = item['values'][0]
        # department_name = self.department_name_entry.get()
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa khoa này?")
        if confirm:
            query = "DELETE FROM giaovien WHERE ID_GIAOVIEN=%s"
            self.cursor.execute(query, (department_id,))
            self.db.commit()
            messagebox.showinfo("Thành công", "Xóa khoa thành công!")
            self.load_data()
