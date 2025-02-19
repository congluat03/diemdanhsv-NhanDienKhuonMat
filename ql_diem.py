import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class QuanLyDiem:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = db.cursor()
        self.create_ui()

    def create_ui(self):
        # Xóa các widget hiện có
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Tiêu đề
        header_label = tk.Label(self.parent, text="📊 Quản Lý Điểm Số", font=("Arial", 20, "bold"), fg="#007acc")
        header_label.pack(pady=10)

        # Bảng hiển thị điểm số
        columns = (
            "ID sinh viên", "Tên Sinh Viên", "Mã Môn", "Tên Môn",
            "Học kỳ","Niên khóa",
            "Điểm 1", "Điểm 2", "Tổng Kết",
            "Điểm Chữ", "Thang Điểm 4", "Xếp Loại"
        )

        self.grade_table = ttk.Treeview(self.parent, columns=columns, show="headings", height=15)

        # Tạo tiêu đề cột và căn chỉnh
        for col in columns:
            self.grade_table.heading(col, text=col, anchor=tk.CENTER)
            self.grade_table.column(col, anchor=tk.CENTER, width=120 if col != "Tên Sinh Viên" else 180)

        # Cuộn dọc
        scroll_y = ttk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.grade_table.yview)
        self.grade_table.configure(yscroll=scroll_y.set)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.grade_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Load dữ liệu điểm
        self.load_diem()

        # Frame chứa các nút chức năng
        button_frame = tk.Frame(self.parent)
        button_frame.pack(pady=10)

        style = {"font": ("Arial", 12), "bg": "#007acc", "fg": "white", "width": 15}

        edit_btn = tk.Button(button_frame, text="📝 Quản lý điểm", **style, command=self.edit_grade)
        edit_btn.grid(row=0, column=1, padx=5, pady=5)

        # Chức năng tìm kiếm
        search_label = tk.Label(button_frame, text="Tìm kiếm:", font=("Arial", 12))
        search_label.grid(row=0, column=3, padx=5, pady=5)

        self.search_entry = tk.Entry(button_frame, font=("Arial", 12), width=20)
        self.search_entry.grid(row=0, column=4, padx=5, pady=5)
        self.search_entry.bind("<Return>", lambda event: self.search_grades())

        search_btn = tk.Button(button_frame, text="🔍", font=("Arial", 12), command=self.search_grades, width=5)
        search_btn.grid(row=0, column=5, padx=5, pady=5)

    def convert_grade(self, score):
        if score is None:
            return "", "", ""

        try:
            score = float(score)
        except ValueError:
            return "", "", ""

        if score < 4.0:
            return "E", 0.0, "Kém"
        elif 4.0 <= score < 5.0:
            return "D", 1.0, "Yếu"
        elif 5.0 <= score < 5.5:
            return "D+", 1.5, "Trung Bình Yếu"
        elif 5.5 <= score < 6.5:
            return "C", 2.0, "Trung Bình"
        elif 6.5 <= score < 7.0:
            return "C+", 2.5, "Trung Bình Khá"
        elif 7.0 <= score < 8.0:
            return "B", 3.0, "Khá"
        elif 8.0 <= score < 9.0:
            return "B+", 3.5, "Giỏi"
        elif 9.0 <= score <= 10.0:
            return "A", 4.0, "Xuất Sắc"
        return "", "", ""

    def load_diem(self):
        # Xóa dữ liệu cũ trên bảng
        for row in self.grade_table.get_children():
            self.grade_table.delete(row)

        try:
            # Truy vấn dữ liệu từ 3 bảng: SINHVIEN, DANGKY, MONHOC
            query = """
                SELECT sv.ID_SINHVIEN AS MSSV, sv.TENSINHVIEN, 
                       mh.ID_MON, mh.TENMON, 
                       dk.DIEM1, dk.DIEM2, dk.KETQUA,
                       dk.HOCKY, dk.NIENKHOA
                FROM DANGKY dk
                JOIN SINHVIEN sv ON dk.ID_SINHVIEN = sv.ID_SINHVIEN
                JOIN MONHOC mh ON dk.ID_MON = mh.ID_MON
            """
            self.cursor.execute(query)

            # Lấy dữ liệu từ kết quả truy vấn
            for row in self.cursor.fetchall():
                mssv, ten_sv, id_mon, ten_mon, diem1, diem2, tong_ket, hocky, nienkhoa = row

                # Chuyển đổi kiểu dữ liệu nếu cần
                diem1 = float(diem1) if diem1 is not None else None
                diem2 = float(diem2) if diem2 is not None else None
                tong_ket = float(tong_ket) if tong_ket is not None else None

                # Chuyển đổi tổng kết sang Điểm Chữ, Thang Điểm 4, Xếp Loại
                letter_grade, gpa, classification = self.convert_grade(tong_ket)

                # Thêm dữ liệu vào bảng giao diện
                self.grade_table.insert("", tk.END, values=(
                    mssv, ten_sv, id_mon, ten_mon,
                    hocky if hocky is not None else "",
                    nienkhoa if nienkhoa is not None else "",
                    diem1 if diem1 is not None else "",
                    diem2 if diem2 is not None else "",
                    tong_ket if tong_ket is not None else "",
                    letter_grade, gpa, classification

                ))

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách điểm số: {err}")

    def edit_grade(self):
        selected_item = self.grade_table.selection()
        if not selected_item:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bản ghi để sửa.")
            return

        grade = self.grade_table.item(selected_item)["values"]
        grade_data = {
            "ID sinh viên": grade[0],
            "Tên Sinh Viên": grade[1],
            "ID_MON": grade[2],
            "Tên Môn": grade[3],
            "Điểm 1": grade[6],
            "Điểm 2": grade[7],
        }
        self.grade_form(grade_data)

    def grade_form(self, grade=None):
        form = tk.Toplevel(self.parent)
        form.title("Nhập Điểm" if not grade else "Sửa Điểm")
        form.geometry("400x400")
        form.config(bg="white")

        header_text = "➕ Nhập Điểm" if not grade else "📝 Sửa Điểm"
        header_label = tk.Label(form, text=header_text, font=("Arial", 20, "bold"), bg="white", fg="#007acc")
        header_label.pack(pady=10)

        form_frame = tk.Frame(form, bg="white")
        form_frame.pack(pady=10)

        # Danh sách các thông tin cần hiển thị
        labels = ["ID sinh viên", "Tên Sinh Viên", "ID_MON", "Tên Môn"]
        for idx, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text + ":", font=("Arial", 12, "bold"), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            # Hiển thị thông tin bằng Label (không chỉnh sửa)
            value = grade.get(label_text, "") if grade else ""
            value_label = tk.Label(form_frame, text=value, font=("Arial", 12), bg="white", fg="black")
            value_label.grid(row=idx, column=1, padx=10, pady=5, sticky="w")

        # Ô nhập điểm 1 và điểm 2
        diem_labels = ["Điểm 1", "Điểm 2"]
        entries = {
            "ID sinh viên": tk.StringVar(value=grade["ID sinh viên"] if grade else ""),
            "Mã Môn": tk.StringVar(value=grade["ID_MON"] if grade else "")
        }

        for idx, diem_text in enumerate(diem_labels, start=len(labels)):
            label = tk.Label(form_frame, text=diem_text + ":", font=("Arial", 12, "bold"), bg="white")
            label.grid(row=idx, column=0, padx=10, pady=5, sticky="w")

            entry = tk.Entry(form_frame, font=("Arial", 12), bg="#f5f5f5", width=10)
            entry.grid(row=idx, column=1, padx=10, pady=5)
            if grade:
                entry.insert(0, grade[diem_text])
            entries[diem_text] = entry

        # Nút Lưu và Thoát
        button_frame = tk.Frame(form, bg="white")
        button_frame.pack(pady=20)

        save_btn = tk.Button(button_frame, text="Lưu", font=("Arial", 12, "bold"), bg="#007acc", fg="white",
                             command=lambda: self.save_grade(entries, grade, form))
        save_btn.grid(row=0, column=0, padx=10)

        cancel_btn = tk.Button(button_frame, text="Thoát", font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white",
                               command=form.destroy)
        cancel_btn.grid(row=0, column=1, padx=10)

        print(entries.keys())  # Kiểm tra danh sách khóa có đúng không

    def update_student_name(self, entries):
        mssv = entries["Mã Sinh Viên"].get()
        self.cursor.execute("SELECT TENSINHVIEN FROM SINHVIEN WHERE ID_SINHVIEN = %s", (mssv,))
        name = self.cursor.fetchone()
        if name:
            entries["Tên Sinh Viên"].config(text=name[0])
        else:
            entries["Tên Sinh Viên"].config(text="")

    def update_subject_name(self, entries):
        ma_mon = entries["Mã Môn"].get()
        self.cursor.execute("SELECT TENMON FROM MONHOC WHERE ID_MON = %s", (ma_mon,))
        name = self.cursor.fetchone()
        if name:
            entries["Tên Môn"].config(text=name[0])
        else:
            entries["Tên Môn"].config(text="")

    def get_students(self):
        """Lấy danh sách ID sinh viên từ bảng SINHVIEN"""
        try:
            self.cursor.execute("SELECT ID_SINHVIEN FROM SINHVIEN")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi khi lấy danh sách sinh viên: {e}")
            return []

    def get_subjects(self):
        """Lấy danh sách ID môn học từ bảng MONHOC"""
        try:
            self.cursor.execute("SELECT ID_MON FROM MONHOC")
            return [row[0] for row in self.cursor.fetchall()]
        except Exception as e:
            print(f"Lỗi khi lấy danh sách môn học: {e}")
            return []

    def save_grade(self, entries, grade=None, form=None):
        # Kiểm tra dữ liệu đầu vào
        for field in ["ID sinh viên", "Mã Môn", "Điểm 1", "Điểm 2"]:
            if not entries[field].get():
                messagebox.showwarning("Cảnh báo", f"Vui lòng nhập {field.lower()}!")
                return

        try:
            # Chuyển đổi điểm sang số thực
            diem1 = float(entries["Điểm 1"].get())
            diem2 = float(entries["Điểm 2"].get())

            # Kiểm tra khoảng điểm hợp lệ
            if not (0 <= diem1 <= 10) or not (0 <= diem2 <= 10):
                messagebox.showwarning("Cảnh báo", "Điểm phải nằm trong khoảng từ 0 đến 10!")
                return

            # Tính điểm tổng kết theo công thức: 30% điểm 1 + 70% điểm 2
            ketqua = round((diem1 * 0.3) + (diem2 * 0.7), 2)

        except ValueError:
            messagebox.showwarning("Cảnh báo", "Điểm phải là số hợp lệ!")
            return

        # Lấy mã sinh viên và mã môn
        id_sinhvien = entries["ID sinh viên"].get()
        id_mon = entries["Mã Môn"].get()

        try:
            # Kiểm tra xem bản ghi có tồn tại không
            self.cursor.execute(
                "SELECT * FROM DANGKY WHERE ID_SINHVIEN = %s AND ID_MON = %s",
                (id_sinhvien, id_mon)
            )
            existing_record = self.cursor.fetchone()

            if existing_record:
                # Nếu tồn tại, cập nhật điểm
                query = """
                    UPDATE DANGKY
                    SET DIEM1 = %s, DIEM2 = %s, KETQUA = %s
                    WHERE ID_SINHVIEN = %s AND ID_MON = %s
                """
                values = (diem1, diem2, ketqua, id_sinhvien, id_mon)

                # Thực thi truy vấn
                self.cursor.execute(query, values)
                self.db.commit()

                # Hiển thị thông báo thành công
                messagebox.showinfo("Thành công", "Cập nhật điểm số thành công!")
                self.load_diem()  # Cập nhật lại bảng hiển thị

                # Đóng form nếu có
                if form:
                    form.destroy()
            else:
                # Nếu bản ghi không tồn tại, cảnh báo không thể thêm mới
                messagebox.showwarning("Cảnh báo",
                                       "Không tìm thấy bản ghi. Chỉ có thể cập nhật điểm của sinh viên đã đăng ký môn học!")

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể cập nhật điểm số: {err}")

    def search_grades(self):
        search_text = self.search_entry.get().strip()
        if not search_text:
            self.load_grades()
            return
        for row in self.grade_table.get_children():
            self.grade_table.delete(row)
        try:
            query = """
                SELECT sv.ID_SINHVIEN, sv.ID_SINHVIEN AS MSSV, sv.TENSINHVIEN, 
                       mh.ID_MON, mh.TENMON, 
                       dk.DIEM1, dk.DIEM2, dk.KETQUA
                FROM DANGKY dk
                JOIN SINHVIEN sv ON dk.ID_SINHVIEN = sv.ID_SINHVIEN
                JOIN MONHOC mh ON dk.ID_MON = mh.ID_MON
                WHERE sv.TENSINHVIEN LIKE %s OR sv.ID_SINHVIEN LIKE %s
            """
            self.cursor.execute(query, (f"%{search_text}%", f"%{search_text}%"))

            for row in self.cursor.fetchall():
                letter_grade, gpa, classification = self.convert_grade(row[8])
                self.grade_table.insert("", tk.END, values=row + (letter_grade, gpa, classification))
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể tìm kiếm: {err}")




