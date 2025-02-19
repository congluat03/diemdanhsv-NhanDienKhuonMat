import tkinter as tk
from tkinter import ttk, messagebox


class DKMonhoc:
    def __init__(self, parent, db, auth_info_array):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.auth_info_array = auth_info_array
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Đăng ký môn học", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.parent, text=f"Thông tin biến: {self.auth_info_array[2]}", font=("Arial", 16, "bold")).pack(
            pady=10)
        print(f"auth_info_array: {self.auth_info_array}")

        # Frame chính chứa bảng dữ liệu và menu bên phải
        main_frame = tk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Bảng danh sách đăng ký
        self.tree = ttk.Treeview(main_frame, columns=("Học kỳ", "Niên khóa", "ID Sinh viên", "ID Môn"), show="headings")
        for col in ("Học kỳ", "Niên khóa", "ID Sinh viên", "ID Môn"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.load_dangky_data()

        # Thanh menu bên phải
        menu_frame = tk.Frame(main_frame, width=250, relief=tk.RIDGE, borderwidth=2)
        menu_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.btn_dangky = tk.Button(menu_frame, text="Đăng ký môn học", command=self.show_dangky_menu)
        self.btn_dangky.pack(pady=10)

        # # Combobox chọn sinh viên
        # tk.Label(menu_frame, text="Chọn sinh viên:").pack()
        # self.combo_sinhvien = ttk.Combobox(menu_frame, state="readonly")
        # self.combo_sinhvien.pack()
        # self.load_sinhvien()

        # Combobox chọn lớp học
        tk.Label(menu_frame, text="Chọn lớp học:").pack()
        self.combo_lop = ttk.Combobox(menu_frame, state="readonly")
        self.combo_lop.pack()
        self.combo_lop.bind("<<ComboboxSelected>>", self.load_monhoc_theo_lop)

        # Combobox chọn môn học
        tk.Label(menu_frame, text="Chọn môn học:").pack()
        self.combo_mon = ttk.Combobox(menu_frame, state="readonly")
        self.combo_mon.pack()

        # Textbox chọn học kỳ
        tk.Label(menu_frame, text="Học kỳ:").pack()
        self.entry_hocky = tk.Entry(menu_frame)
        self.entry_hocky.pack()

        # Textbox chọn niên khóa
        tk.Label(menu_frame, text="Niên khóa:").pack()
        self.entry_nienkhoa = tk.Entry(menu_frame)
        self.entry_nienkhoa.pack()

        self.btn_xacnhan = tk.Button(menu_frame, text="Xác nhận", command=self.dangky_monhoc)
        self.btn_xacnhan.pack(pady=10)

        self.load_lop_hoc()

    def load_dangky_data(self):
        """Hiển thị danh sách đăng ký môn học hiện tại"""
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("""
            SELECT d.HOCKY, d.NIENKHOA, s.TENSINHVIEN, m.TENMON 
            FROM DANGKY d
            JOIN SINHVIEN s ON d.ID_SINHVIEN = s.ID_SINHVIEN
            JOIN MONHOC m ON d.ID_MON = m.ID_MON
        """)
        for row in self.cursor.fetchall():
            self.tree.insert("", tk.END, values=row)

    def load_lop_hoc(self):
        """Load danh sách lớp học vào Combobox"""
        self.cursor.execute("SELECT ID_LOP, TENLOP FROM LOPHOC")
        rows = self.cursor.fetchall()
        self.lop_dict = {lop[1]: lop[0] for lop in rows}
        self.combo_lop["values"] = list(self.lop_dict.keys())

    # Load danh sách sinh viên
    def load_sinhvien(self):
        self.cursor.execute("SELECT ID_SINHVIEN, TENSINHVIEN FROM SINHVIEN")
        rows = self.cursor.fetchall()
        self.sinhvien_dict = {sv[1]: sv[0] for sv in rows}
        self.combo_sinhvien["values"] = list(self.sinhvien_dict.keys())

    def load_monhoc_theo_lop(self, event):
        """Hiển thị danh sách môn học của lớp được chọn"""
        lop_selected = self.combo_lop.get()
        lop_id = self.lop_dict.get(lop_selected)
        if not lop_id:
            return

        self.cursor.execute("""
            SELECT M.ID_MON, M.TENMON FROM MONHOC M
            JOIN LOPHOC_MONHOC LM ON M.ID_MON = LM.ID_MON
            WHERE LM.ID_LOP = %s
        """, (lop_id,))
        rows = self.cursor.fetchall()
        self.mon_dict = {mon[1]: mon[0] for mon in rows}
        self.combo_mon["values"] = list(self.mon_dict.keys())

        def load_dangky_data(self):
            """Hiển thị danh sách đăng ký môn học hiện tại"""
            self.tree.delete(*self.tree.get_children())
            self.cursor.execute("SELECT HOCKY, NIENKHOA, ID_SINHVIEN, ID_MON FROM dangky")
            for row in self.cursor.fetchall():
                self.tree.insert("", tk.END, values=row)

    def dangky_monhoc(self):
        """Xác nhận đăng ký môn học"""
        #sinhvien_selected = self.combo_sinhvien.get()
        sinhvien_selected = self.auth_info_array[2]
        lop_selected = self.combo_lop.get()
        mon_selected = self.combo_mon.get()
        hocky = self.entry_hocky.get().strip()
        nienkhoa = self.entry_nienkhoa.get().strip()

        # Kiểm tra dữ liệu đầu vào
        if not sinhvien_selected or not lop_selected or not mon_selected or not hocky or not nienkhoa:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin.")
            return

        # sinhvien_id = self.sinhvien_dict.get(sinhvien_selected)
        sinhvienid = int(self.auth_info_array[2])
        mon_id = self.mon_dict.get(mon_selected)
        print(f"ID Sinh viên từ auth_info_array: {sinhvienid}")

        # Kiểm tra sinh viên có tồn tại không
        self.cursor.execute("SELECT COUNT(*) FROM SINHVIEN WHERE ID_SINHVIEN = %s", (sinhvienid,))
        if self.cursor.fetchone()[0] == 0:
            messagebox.showerror("Lỗi", "Sinh viên không tồn tại trong hệ thống!")
            return

        # Kiểm tra xem sinh viên đã đăng ký môn này chưa
        self.cursor.execute("SELECT COUNT(*) FROM DANGKY WHERE ID_SINHVIEN = %s AND ID_MON = %s", (sinhvienid, mon_id))
        if self.cursor.fetchone()[0] > 0:
            messagebox.showwarning("Cảnh báo", "Sinh viên đã đăng ký môn học này rồi.")
            return

        # Thêm đăng ký môn học
        try:
            self.cursor.execute("INSERT INTO dangky (HOCKY, NIENKHOA, ID_SINHVIEN, ID_MON) VALUES (%s, %s, %s, %s)",
                                (hocky, nienkhoa, sinhvienid, mon_id))
            self.db.commit()
            messagebox.showinfo("Thông báo", "Đăng ký môn học thành công!")
            self.load_dangky_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đăng ký: {e}")

    def show_dangky_menu(self):
        """Hiển thị menu chọn lớp và môn học"""
        self.combo_lop.set("")
        self.combo_mon.set("")
