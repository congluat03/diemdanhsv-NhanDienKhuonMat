import tkinter as tk
from tkinter import messagebox
import mysql.connector

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng nhập hệ thống")
        self.geometry("400x500")
        self.configure(bg="#f0f4f7")

        tk.Label(self, text="Đăng nhập", font=("Arial", 22, "bold"), bg="#f0f4f7", fg="#007acc").pack(pady=20)

        # Tên đăng nhập
        tk.Label(self, text="Tên đăng nhập:", bg="#f0f4f7", anchor="w", font=("Arial", 12)).pack(padx=20, fill="x")
        self.username_entry = tk.Entry(self, font=("Arial", 12))
        self.username_entry.pack(padx=20, pady=5, fill="x")

        # Mật khẩu
        tk.Label(self, text="Mật khẩu:", bg="#f0f4f7", anchor="w", font=("Arial", 12)).pack(padx=20, fill="x")
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 12))
        self.password_entry.pack(padx=20, pady=5, fill="x")

        # Hiện mật khẩu
        self.show_password_var = tk.IntVar()
        tk.Checkbutton(self, text="Hiện mật khẩu", variable=self.show_password_var, command=self.toggle_password, bg="#f0f4f7", font=("Arial", 10)).pack(anchor="w", padx=40)

        # Chọn quyền
        tk.Label(self, text="Chọn quyền:", bg="#f0f4f7", anchor="w", font=("Arial", 12)).pack(padx=20, fill="x")
        self.role_var = tk.StringVar(value="student")
        tk.Radiobutton(self, text="Sinh viên", variable=self.role_var, value="student", bg="#f0f4f7", font=("Arial", 10)).pack(anchor="w", padx=40)
        tk.Radiobutton(self, text="Giảng viên", variable=self.role_var, value="teacher", bg="#f0f4f7", font=("Arial", 10)).pack(anchor="w", padx=40)

        # Nút đăng nhập
        login_btn = tk.Button(self, text="Đăng nhập", bg="#007acc", fg="white", font=("Arial", 14, "bold"), command=self.login)
        login_btn.pack(pady=20, ipadx=10, ipady=5)

        # Gán sự kiện Enter
        self.bind_enter_key()

    def bind_enter_key(self):
        """Gán sự kiện Enter để đăng nhập."""
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus())  # Chuyển focus qua ô mật khẩu
        self.password_entry.bind("<Return>", lambda event: self.login())

    def toggle_password(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def connect_database(self):
        try:
            return mysql.connector.connect(host="localhost", user="root", password="", database="diemdanhsv")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối tới cơ sở dữ liệu: {err}")
            return None

    def login(self):
        username = self.username_entry.get().strip().lower()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        db = self.connect_database()
        if db:
            cursor = db.cursor()

            # Kiểm tra tài khoản giảng viên trước
            if role == "teacher":
                query = "SELECT ID_TKGV, USERNAME, QUYENHAN, ID_GIAOVIEN FROM taikhoangv WHERE USERNAME=%s AND PASSWORD=%s"
            else:
                query = "SELECT ID_TKSV, USERNAME, ID_SINHVIEN FROM taikhoansv WHERE USERNAME=%s AND PASSWORD=%s"

            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                user_role = None
                if role == "teacher":
                    user_id, user_name_value, user_role, user = result
                else:
                    user_id, user_name_value,user = result
                    user_role = "student"
                messagebox.showinfo("Thành công", f"Chào mừng {user_name_value}!")
                self.destroy()

                from main import QuanLySinhVienApp
                # Cái này tui sửa {} lại thành [] để nó trở thành Array.
                # Cái dữ liệu [user_name_value, user_role, user_id] rất quan trọng để phân quyền
                QuanLySinhVienApp([user_name_value, user_role, user]).mainloop()
            else:
                messagebox.showerror("Không tìm thấy tài khoản", "Tên đăng nhập hoặc mật khẩu không đúng.")

            db.close()

if __name__ == "__main__":
    LoginWindow().mainloop()
