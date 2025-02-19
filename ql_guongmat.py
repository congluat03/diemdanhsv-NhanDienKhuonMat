import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import pandas as pd
from PIL import Image, ImageTk
import face_recognition
import numpy as np
import mysql.connector
import time


class QuanLyGuongMat:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = self.db.cursor()
        self.create_gui()
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def create_gui(self):
        # combobox chọn môn học
        self.frame_top = tk.Frame(self.parent, bg="white")
        self.frame_top.pack(fill=tk.X, pady=10)

        self.label_monhoc = tk.Label(self.frame_top, text="Chọn môn học:", font=("Arial", 12), bg="white")
        self.label_monhoc.pack(side=tk.LEFT, padx=10)

        self.combobox_monhoc = ttk.Combobox(self.frame_top, font=("Arial", 12), state="readonly")
        self.combobox_monhoc.pack(side=tk.LEFT, padx=10)
        self.combobox_monhoc.bind("<<ComboboxSelected>>", self.on_monhoc_selected)

        # khung hình webcam
        self.frame_cam = tk.Frame(self.parent, bg="white")
        self.frame_cam.pack(fill=tk.BOTH, expand=True, pady=10)

        self.label_cam = tk.Label(self.frame_cam, bg="black")
        self.label_cam.pack(fill=tk.BOTH, expand=True)

        # Nút bắt đầu điểm danh
        self.btn_start = tk.Button(self.parent, text="Bắt đầu điểm danh", font=("Arial", 12), bg="#007acc", fg="white",
                                   command=self.start_diem_danh)
        self.btn_start.pack(pady=10)

        # Nút xuất danh sách điểm danh ra Excel
        self.btn_export_excel = tk.Button(self.parent, text="Xuất Excel", font=("Arial", 12), bg="#28a745", fg="white",
                                          command=self.export_diemdanh_to_excel)
        self.btn_export_excel.pack(pady=10)

        # Load danh sách môn học
        self.load_monhoc()

    def load_monhoc(self):
        try:
            self.cursor.execute("SELECT TENMON FROM MONHOC")
            monhoc_list = self.cursor.fetchall()
            self.combobox_monhoc['values'] = [m[0] for m in monhoc_list]
            if monhoc_list:
                self.combobox_monhoc.current(0)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách môn học: {e}")

    def load_known_faces(self):
        try:
            self.cursor.execute("SELECT TENSINHVIEN, KHUONMAT FROM SINHVIEN")
            sinhvien_list = self.cursor.fetchall()
            for tensinhvien, khuonmat in sinhvien_list:
                if khuonmat:
                    face_encoding = np.frombuffer(khuonmat, dtype=np.float64)
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(tensinhvien)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải dữ liệu khuôn mặt: {e}")

    def on_monhoc_selected(self, event):
        selected_monhoc = self.combobox_monhoc.get()
        self.selected_monhoc = selected_monhoc
        messagebox.showinfo("Thông báo", f"Bạn đã chọn môn học: {selected_monhoc}")

    def start_diem_danh(self):
        if not hasattr(self, 'selected_monhoc'):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học trước khi điểm danh.")
            return

        # Khởi động webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở webcam.")
            return

        # Chờ 2 giây trước khi bắt đầu quét khuôn mặt
        self.parent.after(2000, self.show_webcam)

    def show_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            # Chuyển đổi sang RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Nhận diện khuôn mặt
            face_locations = face_recognition.face_locations(rgb_frame, model="hog")
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]
                    self.update_diem_danh(name)

                # Vẽ khung và tên
                top, right, bottom, left = face_locations[0]
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

            # Hiển thị frame lên giao diện
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.label_cam.imgtk = imgtk
            self.label_cam.configure(image=imgtk)
            self.label_cam.after(10, self.show_webcam)
        else:
            messagebox.showerror("Lỗi", "Không thể khởi động webcam.")

    def update_diem_danh(self, tensinhvien):
        try:
            # Lấy ID_SINHVIEN
            self.cursor.execute("SELECT ID_SINHVIEN FROM SINHVIEN WHERE TENSINHVIEN = %s", (tensinhvien,))
            result = self.cursor.fetchone()
            if result is None:
                messagebox.showerror("Lỗi", f"Sinh viên {tensinhvien} không tồn tại!")
                return
            id_sinhvien = result[0]

            # Lấy ID_MON
            self.cursor.execute("SELECT ID_MON FROM MONHOC WHERE TENMON = %s", (self.selected_monhoc,))
            result = self.cursor.fetchone()
            if result is None:
                messagebox.showerror("Lỗi", "Môn học không tồn tại trong hệ thống!")
                return
            id_mon = result[0]

            # Kiểm tra xem sinh viên đã điểm danh chưa
            self.cursor.execute("""
                SELECT * FROM DIEMDANH 
                WHERE ID_SINHVIEN = %s AND ID_MON = %s AND NGAYDIEMDANH = CURDATE()
            """, (id_sinhvien, id_mon))
            if self.cursor.fetchone():
                messagebox.showinfo("Thông báo", f"Sinh viên {tensinhvien} đã điểm danh hôm nay.")
                return

            # Cập nhật điểm danh vào bảng DIEMDANH
            self.cursor.execute("""
                INSERT INTO DIEMDANH (ID_SINHVIEN, ID_MON, ID_GIAOVIEN, NGAYDIEMDANH, TIET)
                VALUES (%s, %s, %s, NOW(), 'Tiết 1')
            """, (id_sinhvien, id_mon, 1))  # Giả sử ID_GIAOVIEN = 1
            self.db.commit()

            messagebox.showinfo("Thành công", f"Điểm danh thành công cho sinh viên: {tensinhvien}")

            # Dừng webcam sau khi điểm danh thành công
            self.cap.release()
            self.label_cam.config(image='')  # Xóa hình ảnh webcam hiển thị

        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật điểm danh: {e}")

    def show_ds_diemdanh(self):
        if not hasattr(self, 'selected_monhoc'):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học trước khi xem danh sách điểm danh.")
            return

        try:
            # Lấy ID_MON 
            self.cursor.execute("SELECT ID_MON FROM MONHOC WHERE TENMON = %s", (self.selected_monhoc,))
            id_mon = self.cursor.fetchone()[0]

            # Lấy danh sách sinh viên đã điểm danh trong ngày
            self.cursor.execute("""
                SELECT S.TENSINHVIEN 
                FROM DIEMDANH D
                JOIN SINHVIEN S ON D.ID_SINHVIEN = S.ID_SINHVIEN
                WHERE D.ID_MON = %s AND D.NGAYDIEMDANH = CURDATE()
            """, (id_mon,))
            ds_diemdanh = self.cursor.fetchall()

            # Hiển thị danh sách trong Listbox
            self.listbox_ds_diemdanh.delete(0, tk.END)
            for sinhvien in ds_diemdanh:
                self.listbox_ds_diemdanh.insert(tk.END, sinhvien[0])
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách điểm danh: {e}")
            

    def export_diemdanh_to_excel(self):
        if not hasattr(self, 'selected_monhoc'):
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học trước khi xuất danh sách điểm danh.")
            return

        try:
            # Lấy ID môn học
            self.cursor.execute("SELECT ID_MON FROM MONHOC WHERE TENMON = %s", (self.selected_monhoc,))
            id_mon = self.cursor.fetchone()[0]

            # Lấy danh sách tất cả sinh viên trong môn học
            self.cursor.execute("SELECT ID_SINHVIEN, TENSINHVIEN FROM SINHVIEN WHERE ID_MON = %s", (id_mon,))
            all_students = {row[0]: row[1] for row in self.cursor.fetchall()}

            # Lấy danh sách sinh viên đã điểm danh hôm nay
            self.cursor.execute("""
                SELECT ID_SINHVIEN FROM DIEMDANH
                WHERE ID_MON = %s AND NGAYDIEMDANH = CURDATE()
            """, (id_mon,))
            present_students = {row[0] for row in self.cursor.fetchall()}

            # Tạo danh sách với trạng thái có mặt hoặc vắng
            data = []
            for id_sinhvien, tensinhvien in all_students.items():
                trang_thai = "Có mặt" if id_sinhvien in present_students else "Vắng"
                data.append([tensinhvien, trang_thai])

            # Xuất file Excel
            df = pd.DataFrame(data, columns=["Tên Sinh Viên", "Trạng Thái"])
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Thành công", "Xuất danh sách điểm danh thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất file Excel: {e}")

    def __del__(self):
        if hasattr(self, 'cap'):
            self.cap.release()