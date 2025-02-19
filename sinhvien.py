import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import mysql.connector
import csv
import openpyxl
from io import BytesIO
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class QuanLySinhVien:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        tk.Label(self.parent, text="Quản Lý Sinh Viên", font=("Arial", 16, "bold"), fg="white", bg="blue").pack(pady=10, fill=tk.X)

        # Khung nhập thông tin sinh viên
        form_frame = tk.Frame(self.parent, bg="lightgray", padx=10, pady=10)
        form_frame.pack(pady=10, fill=tk.X)

        tk.Label(form_frame, text="Họ Tên:", bg="lightgray").grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Ngày Sinh:", bg="lightgray").grid(row=1, column=0, padx=5, pady=5)
        self.dob_entry = DateEntry(form_frame, width=18, background="blue", foreground="black", date_pattern="dd-MM-yyyy")
        self.dob_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Giới Tính:", bg="lightgray").grid(row=2, column=0, padx=5, pady=5)
        self.gender_combobox = ttk.Combobox(form_frame, values=["Nam", "Nữ", "Khác"], width=18)
        self.gender_combobox.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Lớp Học:", bg="lightgray").grid(row=3, column=0, padx=5, pady=5)
        self.class_combobox = ttk.Combobox(form_frame, width=18)
        self.class_combobox.grid(row=3, column=1, padx=5, pady=5)
        self.load_classes()  # Gọi hàm để tải danh sách lớp học


        # Nút thêm, sửa, xóa
        button_frame = tk.Frame(self.parent, bg="white")
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Thêm", bg="green", fg="black", command=self.add_student).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Sửa", bg="orange", fg="black", command=self.edit_student).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="red", fg="black", command=self.delete_student).pack(side=tk.LEFT, padx=5)

        # Tạo khung tìm kiếm và lọc dữ liệu
        filter_frame = tk.Frame(self.parent)
        filter_frame.pack(pady=5, fill=tk.X)

        tk.Label(filter_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(filter_frame)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="🔍", command=self.search_student).pack(side=tk.LEFT, padx=5)

        tk.Label(filter_frame, text="Lọc theo giới tính:").pack(side=tk.LEFT, padx=5)
        self.filter_gender = ttk.Combobox(filter_frame, values=["Tất cả", "Nam", "Nữ", "Khác"], width=10)
        self.filter_gender.current(0)
        self.filter_gender.pack(side=tk.LEFT, padx=5)
        tk.Button(filter_frame, text="Lọc", command=self.filter_students).pack(side=tk.LEFT, padx=5)

        tk.Button(filter_frame, text="Xuất CSV", command=self.export_to_csv).pack(side=tk.RIGHT, padx=5)
        tk.Button(filter_frame, text="Xuất Excel", command=self.export_to_excel).pack(side=tk.RIGHT, padx=5)
        tk.Button(filter_frame, text="Thống kê", command=self.show_statistics).pack(side=tk.RIGHT, padx=5)

        # Tạo Treeview để hiển thị danh sách sinh viên
        columns = ("ID", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp Học")
        self.tree = ttk.Treeview(self.parent, columns=columns, show="headings")
        self.tree.pack(expand=True, fill=tk.BOTH)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.load_data()
        self.tree.bind("<ButtonRelease-1>", self.select_sinhvien)  # Lấy dữ liệu khi click vào dòng

    def select_sinhvien(self, event):
        """Lấy dữ liệu từ dòng được chọn để hiển thị lên form nhập"""
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item, "values")

        # Điền thông tin môn học vào ô nhập
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, item[1])

        self.dob_entry.delete(0, tk.END)
        self.dob_entry.insert(0, item[2])

        # Cập nhật Combobox chọn lớp học và giáo viên
        selected_gender = item[3] if len(item) > 3 else ""
        self.gender_combobox.set(selected_gender)

        # Cập nhật Combobox chọn lớp học và giáo viên
        selected_lop = item[4] if len(item) > 4 else ""
        self.class_combobox.set(selected_lop)


    def add_student(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get_date().strftime("%Y-%m-%d")  # Khi lưu vào database
        gender_text = self.gender_combobox.get()
        class_name = self.class_combobox.get()

        # Chuyển giới tính từ chữ thành số
        gender_map = {"Nam": 0, "Nữ": 1, "Khác": 2}
        gender = gender_map.get(gender_text, 2)

        class_id = self.get_class_id(class_name)
        if class_id is None:
            return

        query = "INSERT INTO sinhvien (TENSINHVIEN, NGAYSINH, GIOITINH, ID_LOP) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (name, dob, gender, class_id))
        self.db.commit()
        messagebox.showinfo("Thành công", "Thêm sinh viên thành công!")
        self.load_data()

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn sinh viên cần sửa!")
            return

        item = self.tree.item(selected_item)
        student_id = item['values'][0]
        name = self.name_entry.get()
        dob = self.dob_entry.get_date().strftime("%Y-%m-%d")  # Khi lưu vào database

        gender_str = self.gender_combobox.get()
        gender = 0 if gender_str == "Nam" else 1  # Chuyển đổi sang số

        class_name = self.class_combobox.get()
        class_id = self.get_class_id(class_name)

        if class_id is None:
            return

        query = "UPDATE sinhvien SET TENSINHVIEN=%s, NGAYSINH=%s, GIOITINH=%s, ID_LOP=%s WHERE ID_SINHVIEN=%s"
        self.cursor.execute(query, (name, dob, gender, class_id, student_id))
        self.db.commit()

        messagebox.showinfo("Thành công", "Sửa thông tin sinh viên thành công!")
        self.load_data()

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn sinh viên cần xóa!")
            return

        item = self.tree.item(selected_item)
        student_id = item['values'][0]
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa sinh viên này?")
        if confirm:
            query = "DELETE FROM sinhvien WHERE ID_SINHVIEN=%s"
            self.cursor.execute(query, (student_id,))
            self.db.commit()
            messagebox.showinfo("Thành công", "Xóa sinh viên thành công!")
            self.load_data()

    def load_data(self, condition=""):
        self.tree.delete(*self.tree.get_children())
        query = "SELECT ID_SINHVIEN, TENSINHVIEN, NGAYSINH, GIOITINH, ID_LOP FROM sinhvien" + condition
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        for row in rows:
            row = list(row)
            row[2] = row[2].strftime("%d/%m/%Y")  # Chuyển đổi ngày sinh
            row[3] = row[3]  # Giới tính giữ nguyên định dạng
            row[4] = self.get_class_name(row[4])  # Thay ID lớp bằng tên lớp
            self.tree.insert("", "end", values=row)

    def load_classes(self):
        """Lấy danh sách lớp từ CSDL và cập nhật vào combobox"""
        query = "SELECT TENLOP FROM lophoc"
        self.cursor.execute(query)
        classes = [row[0] for row in self.cursor.fetchall()]
        self.class_combobox['values'] = classes  # Gán danh sách lớp vào combobox

    def get_class_name(self, class_id):
        query = "SELECT TENLOP FROM lophoc WHERE ID_LOP=%s"
        self.cursor.execute(query, (class_id,))
        result = self.cursor.fetchone()

        if result is None:
            return "Không xác định"  # Nếu không tìm thấy lớp, trả về giá trị mặc định tránh lỗi

        return result[0]

    def get_class_id(self, class_name):
        query = "SELECT ID_LOP FROM lophoc WHERE TENLOP=%s"
        self.cursor.execute(query, (class_name,))
        result = self.cursor.fetchone()

        if result is None:
            messagebox.showerror("Lỗi", f"Lớp học '{class_name}' không tồn tại!")
            return None  # Tránh lỗi truy cập phần tử trên None

        return result[0]
    def search_student(self):
        keyword = self.search_entry.get()
        condition = f" WHERE TENSINHVIEN LIKE '%{keyword}%'"
        self.load_data(condition)

    def filter_students(self):
        gender = self.filter_gender.get()
        if gender == "Tất cả":
            self.load_data()
        else:
            condition = f" WHERE GIOITINH = '{gender}'"
            self.load_data(condition)

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp Học"])
            for row in self.tree.get_children():
                writer.writerow(self.tree.item(row)['values'])

        messagebox.showinfo("Thành công", "Xuất file CSV thành công!")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["ID", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp Học"])

        for row in self.tree.get_children():
            sheet.append(self.tree.item(row)['values'])

        workbook.save(file_path)
        messagebox.showinfo("Thành công", "Xuất file Excel thành công!")

    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(["ID", "Họ Tên", "Ngày Sinh", "Giới Tính", "Lớp Học"])

        for row in self.tree.get_children():
            sheet.append(self.tree.item(row)['values'])

        workbook.save(file_path)
        messagebox.showinfo("Thành công", "Xuất file Excel thành công!")

    def show_statistics(self):
        # Lấy thống kê giới tính
        self.cursor.execute("SELECT GIOITINH, COUNT(*) FROM sinhvien GROUP BY GIOITINH")
        data = self.cursor.fetchall()
        labels = ["Nam", "Nữ", "Khác"]
        sizes = [0, 0, 0]

        for row in data:
            if row[0] == "Nam":
                sizes[0] = row[1]
            elif row[0] == "Nữ":
                sizes[1] = row[1]
            else:
                sizes[2] = row[1]

        # Tạo biểu đồ hình tròn
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['blue', 'pink', 'gray'])
        ax.set_title("Thống kê giới tính sinh viên")

        # Lưu biểu đồ vào bộ đệm
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        img = Image.open(buffer)
        img = ImageTk.PhotoImage(img)

        # Hiển thị biểu đồ hình tròn trong cửa sổ popup
        popup = tk.Toplevel()
        popup.title("Thống kê")
        tk.Label(popup, image=img).pack()
        popup.mainloop()
