import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import psycopg2

class RegistrationPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kayıt Sayfası")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.lbl_name = QLabel("İsim:", self)
        self.txt_name = QLineEdit(self)
        layout.addWidget(self.lbl_name)
        layout.addWidget(self.txt_name)

        self.lbl_surname = QLabel("Soyisim:", self)
        self.txt_surname = QLineEdit(self)
        layout.addWidget(self.lbl_surname)
        layout.addWidget(self.txt_surname)

        self.lbl_username = QLabel("Kullanıcı Adı:", self)
        self.txt_username = QLineEdit(self)
        layout.addWidget(self.lbl_username)
        layout.addWidget(self.txt_username)

        self.lbl_password = QLabel("Şifre:", self)
        self.txt_password = QLineEdit(self)
        layout.addWidget(self.lbl_password)
        layout.addWidget(self.txt_password)

        self.lbl_confirm_password = QLabel("Şifre Tekrarı:", self)
        self.txt_confirm_password = QLineEdit(self)
        layout.addWidget(self.lbl_confirm_password)
        layout.addWidget(self.txt_confirm_password)

        self.lbl_phone = QLabel("Telefon Numarası:", self)
        self.txt_phone = QLineEdit(self)
        layout.addWidget(self.lbl_phone)
        layout.addWidget(self.txt_phone)

        self.lbl_email = QLabel("E-Mail:", self)
        self.txt_email = QLineEdit(self)
        layout.addWidget(self.lbl_email)
        layout.addWidget(self.txt_email)

        self.btn_register = QPushButton("Kayıt Ol", self)
        self.btn_register.clicked.connect(self.register)
        layout.addWidget(self.btn_register)

        self.setLayout(layout)

    def register(self):
        name = self.txt_name.text()
        surname = self.txt_surname.text()
        username = self.txt_username.text()
        password = self.txt_password.text()
        confirm_password = self.txt_confirm_password.text()
        phone = self.txt_phone.text()
        email = self.txt_email.text()

        if password != confirm_password:
            print("Şifreler eşleşmiyor!")
            return

        try:
            conn = psycopg2.connect(
                dbname="RegAppPython",
                user="postgres",
                password="1234",
                host="localhost",
                port="5432"
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO userinfo (isim, soyisim, username, password, phone, email) VALUES (%s, %s, %s, %s, %s, %s)",
                        (name, surname, username, password, phone, email))
            conn.commit()
            print("Kullanıcı başarıyla kaydedildi.")
        except psycopg2.Error as e:
            print("Veritabanı hatası:", e)
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegistrationPage()
    window.show()
    sys.exit(app.exec_())
