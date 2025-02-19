import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import face_recognition
import numpy as np
import mysql.connector
import time
import pickle  # Import pickle để mã hóa dữ liệu khuôn mặt

class ThemGuongMat:
    def __init__(self, parent, db):
        self.parent = parent
        self.db = db
        self.cursor = self.db.cursor()
        self.known_face_encodings = []
        self.known_face_names = []
        self.create_gui()
        self.load_students()

    def create_gui(self):
        self.frame_top = tk.Frame(self.parent, bg="white")
        self.frame_top.pack(fill=tk.X, pady=10)

        self.label_sinhvien = tk.Label(self.frame_top, text="Chọn sinh viên:", font=("Arial", 12), bg="white")
        self.label_sinhvien.pack(side=tk.LEFT, padx=10)

        self.combobox_sinhvien = ttk.Combobox(self.frame_top, font=("Arial", 12), state="readonly")
        self.combobox_sinhvien.pack(side=tk.LEFT, padx=10)

        self.btn_scan_face = tk.Button(self.parent, text="Quét khuôn mặt", font=("Arial", 12), bg="#007acc", fg="white", command=self.scan_face)
        self.btn_scan_face.pack(pady=10)

    def load_students(self):
        try:
            self.cursor.execute("SELECT ID_SINHVIEN, TENSINHVIEN FROM SINHVIEN")
            students = self.cursor.fetchall()
            self.students_dict = {s[1]: s[0] for s in students}
            self.combobox_sinhvien['values'] = list(self.students_dict.keys())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể tải danh sách sinh viên: {e}")

    def scan_face(self):
        selected_student = self.combobox_sinhvien.get()
        if not selected_student:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn sinh viên trước khi quét khuôn mặt.")
            return

        messagebox.showinfo("Hướng dẫn", "Hãy nhìn vào camera và giữ nguyên trong vài giây để quét khuôn mặt.")
        cap = cv2.VideoCapture(0)
        face_encodings_list = []

        start_time = time.time()
        while time.time() - start_time < 5:  # Quét trong 5 giây
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            if face_encodings:
                face_encodings_list.append(face_encodings[0])

            cv2.imshow("Quét khuôn mặt", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if len(face_encodings_list) > 0:
            avg_encoding = np.mean(face_encodings_list, axis=0)
            self.save_face_encoding(selected_student, avg_encoding)
        else:
            messagebox.showwarning("Lỗi", "Không nhận diện được khuôn mặt nào. Hãy thử lại!")

    def save_face_encoding(self, student_name, face_encoding):
        student_id = self.students_dict[student_name]
        try:
            # encoding_bytes = pickle.dumps(face_encoding)  # Dùng pickle để lưu
            encoding_bytes = face_encoding.astype(np.float64).tobytes()
            self.cursor.execute("UPDATE SINHVIEN SET KHUONMAT = %s WHERE ID_SINHVIEN = %s", (encoding_bytes, student_id))
            self.db.commit()
            messagebox.showinfo("Thành công", "Đã lưu khuôn mặt thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu khuôn mặt: {e}")
