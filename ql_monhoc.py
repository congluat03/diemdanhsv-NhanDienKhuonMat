import tkinter as tk
from tkinter import ttk, messagebox

import mysql


class QuanLyMonHoc:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()


    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Môn Học", font=("Arial", 16, "bold")).pack(pady=10)

        # Form nhập thông tin
        form_frame = tk.Frame(self.parent)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Tên môn học:").grid(row=0, column=0, padx=5, pady=5)
        self.entry_name = tk.Entry(form_frame)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)


        tk.Label(form_frame, text="Số tín chỉ:").grid(row=1, column=0, padx=5, pady=5)
        self.entry_tinchi = tk.Entry(form_frame)
        self.entry_tinchi.grid(row=1, column=1, padx=5, pady=5)

        # Thêm Combobox để chọn lớp học
        tk.Label(form_frame, text="Lớp học:").grid(row=2, column=0, padx=5, pady=5)
        self.combo_lop = ttk.Combobox(form_frame, state="readonly")
        self.combo_lop.grid(row=2, column=1, padx=5, pady=5)
        self.load_lop_hoc()  # Load danh sách lớp vào Combobox

        # Thêm Combobox để chọn gv
        tk.Label(form_frame, text="Giáo viên:").grid(row=3, column=0, padx=5, pady=5)
        self.combo_giaovien = ttk.Combobox(form_frame, state="readonly")
        self.combo_giaovien.grid(row=3, column=1, padx=5, pady=5)
        self.load_giao_vien()

        # Bảng dữ liệu
        columns = ("ID", "Tên môn", "Số tín chỉ", "Tên lớp", "Giáo viên")  # Thêm cột "Giáo viên"
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)  # Điều chỉnh độ rộng nếu cần

        self.tree.bind("<ButtonRelease-1>", self.select_monhoc)  # Lấy dữ liệu khi click vào dòng

        self.load_data()

        # Nút Thêm, Sửa, Xóa
        btn_frame = tk.Frame(self.parent)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Thêm", command=self.add_monhoc, bg="lightblue").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sửa", command=self.edit_monhoc, bg="lightgreen").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Xóa", command=self.delete_monhoc, bg="red", fg="white").pack(side=tk.LEFT, padx=5)

    def load_data(self):
        """Load dữ liệu môn học, lớp học và giáo viên lên Treeview"""
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ

        query = """
        SELECT M.ID_MON, M.TENMON, M.SOTINCHI, L.TENLOP, G.TENGIAOVIEN
        FROM MONHOC M
        LEFT JOIN LOPHOC_MONHOC LM ON M.ID_MON = LM.ID_MON
        LEFT JOIN LOPHOC L ON LM.ID_LOP = L.ID_LOP
        LEFT JOIN GIAOVIEN G ON M.ID_GIAOVIEN = G.ID_GIAOVIEN
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        for row in rows:
            self.tree.insert("", tk.END, values=row)  # Thêm dữ liệu vào bảng

    def load_lop_hoc(self):
        """Load danh sách lớp học vào Combobox"""
        self.cursor.execute("SELECT ID_LOP, TENLOP FROM LOPHOC")
        rows = self.cursor.fetchall()
        self.lop_dict = {lop[1]: lop[0] for lop in rows}  # Lưu dưới dạng {Tên lớp: ID}
        self.combo_lop["values"] = list(self.lop_dict.keys())  # Hiển thị tên lớp trong Combobox

    def load_giao_vien(self):
        self.cursor.execute("SELECT ID_GIAOVIEN, TENGIAOVIEN FROM GIAOVIEN")
        rows = self.cursor.fetchall()
        self.giaovien_dict = {lop[1]: lop[0] for lop in rows}
        self.combo_giaovien["values"] = list(self.giaovien_dict.keys())


    def select_monhoc(self, event):
        """Lấy dữ liệu từ dòng được chọn để hiển thị lên form nhập"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item, "values")

        # Điền thông tin môn học vào ô nhập
        self.entry_name.delete(0, tk.END)
        self.entry_name.insert(0, item[1])

        self.entry_tinchi.delete(0, tk.END)
        self.entry_tinchi.insert(0, item[2])

        # Cập nhật Combobox chọn lớp học và giáo viên
        selected_lop = item[3] if len(item) > 3 else ""
        self.combo_lop.set(selected_lop)

        selected_giaovien = item[4] if len(item) > 4 else ""
        self.combo_giaovien.set(selected_giaovien)


    def add_monhoc(self):
        name = self.entry_name.get().strip()
        tinchi = self.entry_tinchi.get().strip()
        lop_selected = self.combo_lop.get()
        giaovien_selected = self.combo_giaovien.get()

        if not name or not tinchi or not lop_selected or not giaovien_selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            lop_id = self.lop_dict[lop_selected]
            giaovien_id = self.giaovien_dict[giaovien_selected]

            # Thêm môn học vào bảng MONHOC
            self.cursor.execute(
                "INSERT INTO MONHOC (TENMON, SOTINCHI, ID_GIAOVIEN) VALUES (%s, %s, %s)",
                (name, tinchi, giaovien_id)
            )
            monhoc_id = self.cursor.lastrowid  # Lấy ID môn học vừa thêm

            # Thêm dữ liệu vào bảng trung gian LOPHOC_MONHOC
            self.cursor.execute("INSERT INTO LOPHOC_MONHOC (ID_LOP, ID_MON) VALUES (%s, %s)", (lop_id, monhoc_id))

            self.db.commit()
            messagebox.showinfo("Thông báo", "Thêm môn học thành công!")
            self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm môn học: {err}")

    def edit_monhoc(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để sửa.")
            return

        item = self.tree.item(selected_item, "values")
        monhoc_id = item[0]

        name = self.entry_name.get().strip()
        tinchi = self.entry_tinchi.get().strip()
        lop_selected = self.combo_lop.get().strip()
        giaovien_selected = self.combo_giaovien.get().strip()

        if not name or not tinchi or not lop_selected or not giaovien_selected:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            lop_id = self.lop_dict[lop_selected]
            giaovien_id = self.giaovien_dict[giaovien_selected]

            # Cập nhật thông tin môn học
            self.cursor.execute(
                "UPDATE MONHOC SET TENMON = %s, SOTINCHI = %s, ID_GIAOVIEN = %s WHERE ID_MON = %s",
                (name, tinchi, giaovien_id, monhoc_id)
            )

            # Cập nhật thông tin trong bảng trung gian
            self.cursor.execute(
                "UPDATE LOPHOC_MONHOC SET ID_LOP = %s WHERE ID_MON = %s",
                (lop_id, monhoc_id)
            )

            self.db.commit()
            messagebox.showinfo("Thông báo", "Cập nhật thông tin môn học thành công!")
            self.load_data()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi khi cập nhật: {err}")

    def delete_monhoc(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một môn học để xóa.")
            return

        item = self.tree.item(selected_item, "values")
        monhoc_id = item[0]

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa môn học này?")
        if not confirm:
            return

        try:
            # Xóa môn học khỏi bảng trung gian trước
            self.cursor.execute("DELETE FROM LOPHOC_MONHOC WHERE ID_MON = %s", (monhoc_id,))

            # Sau đó mới xóa môn học khỏi bảng MONHOC
            self.cursor.execute("DELETE FROM MONHOC WHERE ID_MON = %s", (monhoc_id,))

            self.db.commit()
            messagebox.showinfo("Thông báo", "Xóa môn học thành công!")
            self.load_data()  # Tải lại dữ liệu sau khi xóa
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi khi xóa môn học: {err}")
