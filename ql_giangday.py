import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector
from datetime import datetime

class QuanLyGiangDay:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Giảng Dạy", font=("Arial", 16, "bold"), fg="white", bg="blue").pack(pady=10, fill=tk.X)

        form_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        form_frame.pack(pady=10, fill=tk.X)

        tk.Label(form_frame, text="Ngày Dạy:", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)
        self.cal = DateEntry(form_frame, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.cal.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Tiết Giảng Dạy:", bg="lightgray").grid(row=0, column=2, padx=5, pady=5)
        self.tiet_entry = tk.Entry(form_frame)
        self.tiet_entry.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(form_frame, text="Giáo Viên:", bg="lightgray").grid(row=1, column=0, padx=5, pady=5)
        self.gv_entry = ttk.Entry(form_frame)
        self.gv_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Môn Học:", bg="lightgray").grid(row=1, column=2, padx=5, pady=5)
        self.mon_combobox = ttk.Combobox(form_frame)
        self.mon_combobox.grid(row=1, column=3, padx=5, pady=5)

        # Nút thêm, sửa, xóa
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Thêm", bg="green", fg="black", command=self.add_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", bg="orange", fg="black", command=self.update_entry).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="red", fg="black", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

        # Nút tải lại
        tk.Button(button_frame, text="Tải lại", bg="blue", fg="white", command=self.reload_data).pack(side=tk.LEFT, padx=5)


        # Khung lọc dữ liệu
        filter_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        filter_frame.pack(pady=5, fill=tk.X)

        tk.Label(filter_frame, text="Lọc theo môn học:", bg="lightgray").grid(row=0, column=2, padx=5, pady=5)
        self.filter_mon_combobox = ttk.Combobox(filter_frame)
        self.filter_mon_combobox.grid(row=0, column=3, padx=5, pady=5)
        tk.Button(filter_frame, text="Lọc", command=self.filter_data).grid(row=0, column=5, padx=9, pady=9)

        # Treeview hiển thị dữ liệu
        columns = ("ID", "Ngày Dạy", "Tiết", "Giáo Viên", "Môn Học")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=15)
        
        self.load_data()
        self.tree.bind("<ButtonRelease-1>", self.select_entry)  # Lấy dữ liệu khi click vào dòng
        self.load_combobox_data()

        # Gán sự kiện khi chọn môn học
        self.mon_combobox.bind("<<ComboboxSelected>>", self.update_teacher_entry)

    def filter_data(self):
        """Lọc dữ liệu theo môn học"""
        filter_subject = self.filter_mon_combobox.get()

        # Tạo câu lệnh SQL
        query = """
            SELECT giangday.ID_GIANGDAY, giangday.NGAYDAY, giangday.TIETGD, 
                giaovien.TENGIAOVIEN, monhoc.TENMON
            FROM giangday
            JOIN giaovien ON giangday.ID_GIAOVIEN = giaovien.ID_GIAOVIEN
            JOIN monhoc ON giangday.ID_MON = monhoc.ID_MON
        """

        conditions = []
        params = []

        if filter_subject:
            conditions.append("monhoc.TENMON = %s")
            params.append(filter_subject)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            self.cursor.execute(query, tuple(params))
            rows = self.cursor.fetchall()
            self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
            for row in rows:
                self.tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể lọc dữ liệu: {err}")


    def load_combobox_data(self):
        """Tải danh sách môn học vào combobox"""
        self.cursor.execute("SELECT TENMON FROM monhoc")
        subjects = self.cursor.fetchall()
        self.mon_combobox["values"] = [row[0] for row in subjects]
        self.filter_mon_combobox["values"] = [row[0] for row in subjects]

    def update_teacher_entry(self, event=None):
        """Tự động hiển thị giáo viên khi chọn môn học"""
        selected_subject = self.mon_combobox.get()  # Lấy môn học được chọn
        
        query = """
            SELECT giaovien.TENGIAOVIEN 
            FROM monhoc 
            JOIN giaovien ON monhoc.ID_GIAOVIEN = giaovien.ID_GIAOVIEN 
            WHERE monhoc.TENMON = %s
        """
        self.cursor.execute(query, (selected_subject,))
        result = self.cursor.fetchone()

        if result:
            self.gv_entry.config(state="normal")  # Mở khóa để chỉnh sửa
            self.gv_entry.delete(0, tk.END)  # Xóa nội dung cũ
            self.gv_entry.insert(0, result[0])  # Chèn tên giáo viên mới
            self.gv_entry.config(state="readonly")  # Khóa lại
    
    def reload_data(self):
        """Tải lại toàn bộ dữ liệu và xóa thông tin nhập"""
        self.load_data()  # Nạp lại dữ liệu vào TreeView

        # Xóa nội dung của tất cả các ô nhập liệu
        self.cal.set_date(datetime.today())  # Đặt lại ngày về hôm nay
        self.tiet_entry.delete(0, tk.END)  # Xóa tiết giảng dạy
        self.gv_entry.config(state="normal")  # Mở khóa ô giáo viên
        self.gv_entry.delete(0, tk.END)  # Xóa giáo viên
        self.gv_entry.config(state="readonly")  # Khóa lại ô giáo viên
        self.mon_combobox.set("")  # Đặt lại môn học về rỗng

        self.selected_id_gd = None  # Xóa ID giảng dạy đã chọn


    def load_data(self):
        """Tải lại dữ liệu từ cơ sở dữ liệu"""
        self.cursor.execute("""
            SELECT giangday.ID_GIANGDAY, giangday.NGAYDAY, giangday.TIETGD, 
                giaovien.TENGIAOVIEN, monhoc.TENMON
            FROM giangday
            JOIN giaovien ON giangday.ID_GIAOVIEN = giaovien.ID_GIAOVIEN
            JOIN monhoc ON giangday.ID_MON = monhoc.ID_MON
        """)
        rows = self.cursor.fetchall()
        self.tree.delete(*self.tree.get_children())  # Xóa dữ liệu cũ
        for row in rows:
            self.tree.insert("", "end", values=row)

    def add_entry(self):
        """Thêm dữ liệu vào cơ sở dữ liệu"""
        date_str = self.cal.get()
        date_obj = datetime.strptime(date_str, "%m/%d/%y")
        formatted_date_time = f"{date_obj.strftime('%Y-%m-%d')}"
        ngay, tiet, gv, mon = formatted_date_time, self.tiet_entry.get(), self.gv_entry.get(), self.mon_combobox.get()
        
        if not all([ngay, tiet, gv, mon]):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin")
            return

        self.cursor.execute("SELECT ID_GIAOVIEN FROM giaovien WHERE TENGIAOVIEN = %s", (gv,))
        id_gv = self.cursor.fetchone()
        if not id_gv:
            messagebox.showerror("Lỗi", "Không tìm thấy giáo viên này!")
            return
        id_gv = id_gv[0]

        self.cursor.execute("SELECT ID_MON FROM monhoc WHERE TENMON = %s", (mon,))
        id_mon = self.cursor.fetchone()
        if not id_mon:
            messagebox.showerror("Lỗi", "Không tìm thấy môn học này!")
            return
        id_mon = id_mon[0]

        try:
            self.cursor.execute(""" 
                INSERT INTO giangday (NGAYDAY, TIETGD, ID_GIAOVIEN, ID_MON) 
                VALUES (%s, %s, %s, %s)
            """, (ngay, tiet, id_gv, id_mon))
            self.db.commit()
            messagebox.showinfo("Thành công", "Thêm giảng dạy thành công")
            self.load_data()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Lỗi", "Đã tồn tại giảng dạy với ngày và tiết này")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi thêm: {str(e)}")

    def update_entry(self):
        """Cập nhật dữ liệu vào cơ sở dữ liệu"""
        if not hasattr(self, 'selected_id_gd') or not self.selected_id_gd:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng trước khi cập nhật!")
            return

        date_str = self.cal.get()
        date_obj = datetime.strptime(date_str, "%m/%d/%y")
        formatted_date_time = f"{date_obj.strftime('%Y-%m-%d')}"
        ngay, tiet, gv, mon = formatted_date_time, self.tiet_entry.get(), self.gv_entry.get(), self.mon_combobox.get()

        if not all([ngay, tiet, gv, mon]):
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Lấy ID_GIAOVIEN và ID_MON
        self.cursor.execute("SELECT ID_GIAOVIEN FROM giaovien WHERE TENGIAOVIEN = %s", (gv,))
        id_gv = self.cursor.fetchone()
        if not id_gv:
            messagebox.showerror("Lỗi", "Không tìm thấy giáo viên này!")
            return
        id_gv = id_gv[0]

        self.cursor.execute("SELECT ID_MON FROM monhoc WHERE TENMON = %s", (mon,))
        id_mon = self.cursor.fetchone()
        if not id_mon:
            messagebox.showerror("Lỗi", "Không tìm thấy môn học này!")
            return
        id_mon = id_mon[0]

        try:
            self.cursor.execute(""" 
                UPDATE giangday 
                SET NGAYDAY = %s, TIETGD = %s, ID_GIAOVIEN = %s, ID_MON = %s
                WHERE ID_GIANGDAY = %s
            """, (ngay, tiet, id_gv, id_mon, self.selected_id_gd))
            self.db.commit()
            messagebox.showinfo("Thành công", "Cập nhật thành công!")
            self.load_data()  # Refresh lại danh sách
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi MySQL: {err}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

    def delete_entry(self):
        """Xóa dữ liệu khỏi cơ sở dữ liệu"""
        if not hasattr(self, 'selected_id_gd') or not self.selected_id_gd:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dòng trước khi xóa!")
            return

        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa giảng dạy này?")
        if confirm:
            try:
                self.cursor.execute("DELETE FROM giangday WHERE ID_GIANGDAY = %s", (self.selected_id_gd,))
                self.db.commit()
                messagebox.showinfo("Thành công", "Xóa thành công")
                self.load_data()  # Cập nhật lại danh sách hiển thị
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi khi xóa: {err}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Lỗi khác: {e}")

    def select_entry(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0], "values")
        
        if len(item) != 5:  # Kiểm tra nếu số cột không đúng
            return

        try:
            # Xử lý ngày (cột 1)
            ngay = datetime.strptime(item[1], "%Y-%m-%d")
            self.cal.set_date(ngay)
        except ValueError:
            messagebox.showerror("Lỗi", f"Ngày không hợp lệ: {item[1]}")
            return

        # Điền dữ liệu vào các trường nhập liệu
        self.tiet_entry.delete(0, tk.END)
        self.tiet_entry.insert(0, item[2])  # Tiết dạy

        self.gv_entry.config(state="normal")
        self.gv_entry.delete(0, tk.END)
        self.gv_entry.insert(0, item[3])  # Tên giáo viên
        self.gv_entry.config(state="readonly")

        self.mon_combobox.set(item[4])  # Môn học

        # Lưu ID_GIANGDAY cho mục đích sửa và xóa
        try:
            # Truy vấn ID_GIANGDAY từ cơ sở dữ liệu
            self.cursor.execute("""
                SELECT ID_GIANGDAY FROM giangday
                WHERE NGAYDAY = %s AND TIETGD = %s
                AND ID_GIAOVIEN = (SELECT ID_GIAOVIEN FROM giaovien WHERE TENGIAOVIEN = %s)
                AND ID_MON = (SELECT ID_MON FROM monhoc WHERE TENMON = %s)
            """, (item[1], item[2], item[3], item[4]))

            # Đảm bảo xử lý kết quả của truy vấn trước khi tiếp tục
            result = self.cursor.fetchall()

            if result:
                self.selected_id_gd = result[0][0]  # Lưu ID_GIANGDAY
            else:
                self.selected_id_gd = None
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi MySQL: {err}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khác: {e}")


