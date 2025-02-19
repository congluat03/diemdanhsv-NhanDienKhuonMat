import tkinter as tk
from tkinter import messagebox, colorchooser
import mysql.connector
from sinhvien import QuanLySinhVien
from lophoc import QuanLyLopHoc
from khoa import QuanLyKhoa
from ql_monhoc import QuanLyMonHoc
from diem_danh import DiemDanh
from ql_taikhoan import QuanLyTaiKhoan
from ql_diem import QuanLyDiem
from dk_monhoc import DKMonhoc
from diemdanhSV.diemdanhsv.quanlydiemsv.ql_guongmat import QuanLyGuongMat
from ql_giangvien import QuanLyGiangVien
from add_guongmat import ThemGuongMat
from ql_giangday import QuanLyGiangDay


class QuanLySinhVienApp(tk.Tk):
    def __init__(self, user_info):
        super().__init__()
        # Tui lấy dữ liệu array từ đăng nhập. Cái dữ liệu self.user_info_auth[1] sẽ lấy cái quyền trong array
        # Ví dụ như [Phuc, "student", 3] thì self.user_info_auth[1] nó sẽ trả về dữ liệu "student" trong cái array self.user_info_auth.
        self.user_info_auth = user_info
        if self.user_info_auth[1] == "teacher":
            self.Auth = "Giáo Viên"
        else:
            self.Auth = "Sinh Viên"
        self.title("Quản Lý Sinh Viên và Lớp Học")
        self.geometry("1200x700")
        self.configure(bg="#f5f5f5")

        self.sidebar_visible = True
        self.connect_database()
        self.create_header()
        self.create_sidebar()
        self.create_main_content()

    def connect_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost", user="root", password="", database="diemdanhsv"
            )
            self.cursor = self.db.cursor()
            print("Kết nối cơ sở dữ liệu thành công!")
        except mysql.connector.Error as err:
            print(f"Lỗi kết nối database: {err}")

    def create_header(self):
        header = tk.Frame(self, bg="#007acc", height=50)
        header.pack(fill=tk.X)

        toggle_btn = tk.Button(header, text="☰", fg="white", bg="#007acc", bd=0, font=("Arial", 16, "bold"),
                               command=self.toggle_sidebar)
        toggle_btn.pack(side=tk.LEFT, padx=10)

        title_label = tk.Label(header, text=f"Quản Lý Sinh Viên ({self.user_info_auth[0]}) | ({self.Auth})", fg="white",
                               bg="#007acc", font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT, padx=20)

        settings_btn = tk.Button(header, text="⚙️ Cài đặt", fg="white", bg="#007acc", bd=0, font=("Arial", 12, "bold"),
                                 command=self.open_settings)
        settings_btn.pack(side=tk.RIGHT, padx=10)

        logout_btn = tk.Button(header, text="Đăng xuất", fg="white", bg="#e74c3c", bd=0, font=("Arial", 12, "bold"),
                               command=self.logout)
        logout_btn.pack(side=tk.RIGHT, padx=10)

        info_btn = tk.Button(header, text="ℹ️ Thông tin", fg="white", bg="#007acc", bd=0, font=("Arial", 12, "bold"),
                             command=self.show_info)
        info_btn.pack(side=tk.LEFT, padx=10)

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
            self.sidebar_visible = True

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#333", width=220)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        if self.user_info_auth[1] == "teacher":
            menu_items = [
                ("🏠 Trang chủ", lambda: self.show_module("Trang chủ")),
                ("📚 Quản lý sinh viên", lambda: self.show_module(QuanLySinhVien)),
                ("🏫 Quản lý lớp học", lambda: self.show_module(QuanLyLopHoc)),
                ("🏫 Quản lý khoa", lambda: self.show_module(QuanLyKhoa)),
                ("📑 Quản lý môn học", lambda: self.show_module(QuanLyMonHoc)),
                ("👨‍🏫 Quản lý giảng viên", lambda: self.show_module(QuanLyGiangVien)),
                ("Quản lý giảng dạy", lambda: self.show_module(QuanLyGiangDay)),
                ("🎯 Điểm danh", lambda: self.show_module(DiemDanh)),
                ("🔑 Quản lý tài khoản", lambda: self.show_module(QuanLyTaiKhoan)),
                ("📊 Quản lý điểm", lambda: self.show_module(QuanLyDiem)),
                ("Quản lý gương mặt", lambda: self.show_module(QuanLyGuongMat)),
                ("Quản lý thêm gương mặt sinh viên", lambda: self.show_module(ThemGuongMat)),

            ]
        else:
            menu_items = [
                ("🏠 Trang chủ", lambda: self.show_module("Trang chủ")),
                ("📑 Quản lý môn học", lambda: self.show_module(QuanLyMonHoc)),
                ("🎯 Điểm danh", lambda: self.show_module(DiemDanh)),
                ("🔑 Quản lý tài khoản", lambda: self.show_module(QuanLyTaiKhoan)),
                ("📊 Quản lý điểm", lambda: self.show_module(QuanLyDiem)),
                ("🖼 Đăng ký môn học", lambda: self.show_module(DKMonhoc)),
            ]

        for text, command in menu_items:
            btn = tk.Button(self.sidebar, text=text, font=("Arial", 12), fg="white", bg="#444", bd=0, relief=tk.FLAT,
                            command=command, anchor="w", padx=20)
            btn.pack(fill=tk.X, pady=5)

    def create_main_content(self):
        self.main_content = tk.Frame(self, bg="white")
        self.main_content.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
        self.show_dashboard()

    def show_dashboard(self):
        # Xóa nội dung cũ
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Header trang chủ
        header_label = tk.Label(self.main_content, text="🏠 Trang chủ", font=("Arial", 20, "bold"), bg="white",
                                fg="#007acc")
        header_label.pack(pady=10)

        # Frame chứa các thông tin thống kê
        stats_frame = tk.Frame(self.main_content, bg="#e3f2fd", padx=20, pady=20, bd=2, relief=tk.GROOVE)
        stats_frame.pack(pady=20)

        # Danh sách nhãn thống kê
        # Lọc thông tin hiện trên trang chủ
        if self.user_info_auth[1] == "teacher":
            data_labels = ["📘 Sinh viên", "🏫 Lớp học", "👨‍🏫 Giảng viên", "📖 Môn học"]
            self.stats_values = []
        else:
            data_labels = ["🏫 Lớp học", "📖 Môn học"]
            self.stats_values = []

        for i, label in enumerate(data_labels):
            frame = tk.Frame(stats_frame, bg="white", relief=tk.RIDGE, bd=2)
            frame.grid(row=0, column=i, padx=15, pady=10)

            # Nhãn tiêu đề
            title_label = tk.Label(frame, text=label, font=("Arial", 12, "bold"), bg="white", fg="#333")
            title_label.pack(padx=10, pady=5)

            # Số liệu thống kê
            val_label = tk.Label(frame, text="0", font=("Arial", 16, "bold"), bg="white", fg="#d32f2f")
            val_label.pack(pady=5, padx=10)
            self.stats_values.append(val_label)

        # Nút cập nhật với hiệu ứng hover
        refresh_btn = tk.Button(
            self.main_content, text="🔄 Cập nhật", font=("Arial", 12, "bold"),
            bg="#007acc", fg="white", padx=10, pady=5, relief=tk.RAISED,
            command=self.update_dashboard
        )
        refresh_btn.pack(pady=15)

        refresh_btn.bind("<Enter>", lambda e: refresh_btn.config(bg="#005f99"))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.config(bg="#007acc"))

        self.update_dashboard()

    def update_dashboard(self):
        try:
            # Lọc thông tin dữ liệu của trang chủ
            if self.user_info_auth[1] == "teacher":
                queries = [
                    "SELECT COUNT(*) FROM sinhvien",
                    "SELECT COUNT(*) FROM lophoc",
                    "SELECT COUNT(*) FROM giaovien",
                    "SELECT COUNT(*) FROM monhoc"
                ]
            else:
                queries = [
                    "SELECT COUNT(*) FROM lophoc",
                    "SELECT COUNT(*) FROM monhoc"
                ]
            for i, query in enumerate(queries):
                self.cursor.execute(query)
                count = self.cursor.fetchone()[0]
                self.stats_values[i].config(text=str(count))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể cập nhật dữ liệu: {err}")

    def show_module(self, module_class):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        # Nếu một số class từ module khác có dùng ID từ tài khoản thì thêm vào Special_Module_List
        # Ví dụ Special_Module_List = [QuanLyTaiKhoan, QuanLySinhVien].
        Special_Module_List = [DKMonhoc ]
        if module_class == "Trang chủ":
            self.show_dashboard()
        elif module_class in Special_Module_List:
            module_class(self.main_content, self.db, self.user_info_auth)
        else:
            module_class(self.main_content, self.db)

    def logout(self):
        self.destroy()
        from dang_nhap import LoginWindow
        LoginWindow().mainloop()

    def open_settings(self):
        color = colorchooser.askcolor(title="Chọn màu nền ứng dụng")
        if color[1]:
            self.configure(bg=color[1])
            self.sidebar.configure(bg=color[1])
            self.main_content.configure(bg=color[1])

    def show_info(self):
        messagebox.showinfo("Thông tin ứng dụng",
                            "Ứng dụng Quản lý Sinh viên - Phiên bản 1.0\nLiên hệ: support@taydo.edu.vn")

    def on_exit(self):
        if messagebox.askokcancel("Thoát", "Bạn có chắc muốn thoát không?"):
            self.destroy()


if __name__ == "__main__":
    from dang_nhap import LoginWindow

    LoginWindow().mainloop()
