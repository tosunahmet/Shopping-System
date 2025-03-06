# Import Library
import sys
import json
import os

from PyQt5.QtGui import QIcon
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QVBoxLayout, QWidget, QDialog, QMessageBox, QHBoxLayout, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap

# Language Pack
translations = {
    'tr': {
        'title': "HuNi | Giriş Ekranı",
        'email_label': "E-Posta: ",
        'password_label': "Şifre: ",
        'login_button': "Giriş Yap",
        'login_tooltip': "Giriş yapmak için tıklayın",
        'guest_login_button': "Misafir Giriş",
        'guest_login_tooltip': "Misafir olarak giriş yapın",
        'register_tooltip': "Kayıt olmak için tıklayın",
        'forgot_password_button': "Şifremi Unuttum",
        'forgot_password_tooltip': "Şifrenizi sıfırlayın",
        'forgot_password_title': "Şifremi Unuttum",
        'forgot_password_success':"Şifre başarıyla güncellendi! Giriş yapabilirsin.",
        'save_button': "Kaydet",
        'login_msg': "Giriş Denemesi",
        'login_info': "E-Posta: {email}\nŞifre: {password}",
        'register_msg': "Kayıt butonu seçildi!",
        'guest_msg': "Misafir olarak giriş yapıldı",
        'forgot_msg': "Şifremi Unuttum seçildi!",
        'language_label': "Dil Seç:",
        'language_tr': "Türkçe",
        'language_en': "English",
        'register_title': "Kayıt Ekranı",
        'register_email_label': "E-Posta: ",
        'register_password_label': "Şifre: ",
        'register_confirm_password_label': "Şifreyi Onayla: ",
        'register_button': "Kayıt Ol",
        'register_success': "Kayıt başarılı! Giriş yapabilirsiniz.",
        'register_error_email': "Bu e-posta zaten kayıtlı!",
        'register_error_password': "Şifreler eşleşmiyor!",
        'no_registered_users':"Kayıtlı kullanıcı bulunamadı! Lütfen kayıt olunuz.",
        'please_register':"Kayıtlı Kullanıcı Bulanamadı!",
        'select_language':"Dil Seç"
    },
    'en': {
        'title': "HuNi | Login Screen",
        'email_label': "E-Mail: ",
        'password_label': "Password: ",
        'login_button': "Login",
        'login_tooltip': "Click to log in",
        'guest_login_button': "Guest Login",
        'guest_login_tooltip': "Log in as a guest",
        'register_tooltip': "Click to register",
        'forgot_password_button': "Forgot Password",
        'forgot_password_tooltip': "Reset your password",
        'forgot_password_title': "Forgot Password",
        'forgot_password_success':"Password updated successfully! You can log in",
        'save_button': "Save",
        'login_msg': "Login Attempt",
        'login_info': "E-Mail: {email}\nPassword: {password}",
        'register_msg': "Register button selected!",
        'guest_msg': "Logged in as guest",
        'forgot_msg': "Forgot Password Selected!",
        'language_label': "Select Language:",
        'language_tr': "Turkish",
        'language_en': "English",
        'register_title': "Register Screen",
        'register_email_label': "E-Mail: ",
        'register_password_label': "Password: ",
        'register_confirm_password_label': "Confirm Password: ",
        'register_button': "Register",
        'register_success': "Registration successful! You can log in now.",
        'register_error_email': "This email is already registered!",
        'register_error_password': "Passwords do not match!",
        'no_registered_users':"No registered users found! Please register",
        'please_register':"No Registered Users!",
        'select_language':"Select Language"
    }
}
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return []

def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as file:
        json.dump(users, file, indent=4, ensure_ascii=False)

# Register Window
class RegisterWindow(QDialog):
    def __init__(self, parent, language='en'):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(translations[self.language]['register_title'])
        self.setGeometry(200, 200, 300, 300)

        layout = QVBoxLayout()

        # E-Mail
        self.email_label = QLabel(translations[self.language]['register_email_label'])
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Password
        self.password_label = QLabel(translations[self.language]['register_password_label'])
        layout.addWidget(self.password_label)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Confirm Password
        self.confirm_password_label = QLabel(translations[self.language]['register_confirm_password_label'])
        layout.addWidget(self.confirm_password_label)
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.confirm_password_input)

        # Register Button
        self.register_button = QPushButton(translations[self.language]['register_button'])
        self.register_button.clicked.connect(self.register)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        email = self.email_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not email or not password or not confirm_password:
            QMessageBox.warning(self, translations[self.language]['register_title'], "All fields are required!")
            return

        if password != confirm_password:
            QMessageBox.warning(self, translations[self.language]['register_title'], translations[self.language]['register_error_password'])
            return

        users = load_users()
        if any(user['email'] == email for user in users):
            QMessageBox.warning(self, translations[self.language]['register_title'], translations[self.language]['register_error_email'])
            return

        users.append({'email': email, 'password': password})
        save_users(users)
        QMessageBox.information(self, translations[self.language]['register_title'], translations[self.language]['register_success'])
        self.close()

# Forgot Password Screen
class ForgotPasswordWindow(QDialog):
    def __init__(self, parent, language='en'):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(translations[self.language]['forgot_password_title'])
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.email_label = QLabel(translations[self.language]['register_email_label'])
        layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        layout.addWidget(self.email_input)

        # Password
        self.password_label = QLabel(translations[self.language]['register_password_label'])
        layout.addWidget(self.password_label)
        self.forgot_password_input = QLineEdit()
        self.forgot_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.forgot_password_input)

        # Confirm Password
        self.confirm_password_label = QLabel(translations[self.language]['register_confirm_password_label'])
        layout.addWidget(self.confirm_password_label)
        self.forgot_confirm_password_input = QLineEdit()
        self.forgot_confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.forgot_confirm_password_input)

        # Save Button
        self.save_button = QPushButton(translations[self.language]['save_button'])
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

        self.setLayout(layout)
    def save(self):
        users = load_users()
        email = self.email_input.text().strip()
        forgot_password = self.forgot_password_input.text()
        forgot_confirm_password = self.forgot_confirm_password_input.text()

        if not email or not forgot_password or not forgot_confirm_password:
            QMessageBox.warning(self, translations[self.language]['forgot_password_title'], "All fields are required!")
            return

        if forgot_password != forgot_confirm_password:
            QMessageBox.warning(self, translations[self.language]['forgot_password_title'],
                                translations[self.language]['register_error_password'])
            return
        if any(user['email'] == email for user in users):
            users = [shadow_data for shadow_data in users if shadow_data["email"] != email]
            users.append({'email': email, 'password': forgot_password})
            save_users(users)
            QMessageBox.information(self, translations[self.language]['forgot_password_title'],
                                    translations[self.language]['register_success'])
            self.close()
        else:
            QMessageBox.warning(self, translations[self.language]['please_register'], translations[self.language]['no_registered_users'])


# Main Screen
class LoginWindow(QDialog):
    def __init__(self, title):
        super().__init__()
        self.current_language = 'en'
        self.email = None
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        self.update_ui(title)
        self.setWindowIcon(QIcon("HuNi.png"))

    def update_ui(self, title):
        #print(f"Update Language: {self.current_language}")
        self.setWindowTitle(translations[self.current_language]['title'])
        self.setGeometry(150, 150, 400, 400)

        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Logo Upload
        self.image_label = QLabel(self)
        pixmap = QPixmap("HuNi.png")
        if pixmap.isNull():
            print("Resim yüklenemedi! Dosya yolunu kontrol edin.")
            self.image_label.setText("Picture not found!")
        else:
            pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio)
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.image_label)

        # Select language tag ve combo box
        language_label = QLabel(translations[self.current_language]['language_label'])
        self.main_layout.addWidget(language_label)
        language_combo = QComboBox()
        language_combo.addItems([translations[self.current_language]['select_language'], translations['tr']['language_tr'], translations['en']['language_en']])
        language_combo.currentTextChanged.connect(self.change_language)
        self.main_layout.addWidget(language_combo)

        # E-Mail Tag and Login Area
        self.email_label = QLabel(translations[self.current_language]['email_label'])
        self.main_layout.addWidget(self.email_label)
        self.email_input = QLineEdit(self)
        self.main_layout.addWidget(self.email_input)

        # Password Tag and Login Area
        self.password_label = QLabel(translations[self.current_language]['password_label'])
        self.main_layout.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.main_layout.addWidget(self.password_input)

        self.main_layout.addStretch()

        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        self.login_button = QPushButton(translations[self.current_language]['login_button'], self)
        self.login_button.setToolTip(translations[self.current_language]['login_tooltip'])
        self.login_button.clicked.connect(self.login_attempt)
        button_layout.addWidget(self.login_button)

        self.guest_login_button = QPushButton(translations[self.current_language]['guest_login_button'], self)
        self.guest_login_button.setToolTip(translations[self.current_language]['guest_login_tooltip'])
        self.guest_login_button.clicked.connect(self.guest_login_attempt)
        button_layout.addWidget(self.guest_login_button)

        self.register_button = QPushButton(translations[self.current_language]['register_button'], self)
        self.register_button.setToolTip(translations[self.current_language]['register_tooltip'])
        self.register_button.clicked.connect(self.register_attempt)
        button_layout.addWidget(self.register_button)

        self.forgot_password_button = QPushButton(translations[self.current_language]['forgot_password_button'], self)
        self.forgot_password_button.setToolTip(translations[self.current_language]['forgot_password_tooltip'])
        self.forgot_password_button.clicked.connect(self.forgot_password)
        button_layout.addWidget(self.forgot_password_button)

        self.main_layout.addLayout(button_layout)
        self.main_layout.addSpacing(5)
        self.update()

    def change_language(self, text):
        #print(f"Select language: {text}")
        if text == translations['tr']['language_tr']:
            self.current_language = 'tr'
        elif text == translations['en']['language_en']:
            self.current_language = 'en'
        else:
            print(f"Unknown language selection: {text}")
        self.update_ui(translations[self.current_language]['title'])

    def login_attempt(self):
        email = self.email_input.text()
        password = self.password_input.text()
        users = load_users()
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            QMessageBox.information(self, translations[self.current_language]['login_msg'],
                                   translations[self.current_language]['login_info'].format(email=email, password="****"))
        else:
            QMessageBox.warning(self, translations[self.current_language]['login_msg'], "Invalid email or password!")

    def register_attempt(self):
        register_window = RegisterWindow(self, self.current_language)
        register_window.exec()

    def guest_login_attempt(self):
        QMessageBox.information(self, translations[self.current_language]['guest_msg'],
                               translations[self.current_language]['guest_msg'])

    def forgot_password(self):
        forgot_password_window = ForgotPasswordWindow(self, self.current_language)
        forgot_password_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = LoginWindow("HuNi | Login Screen")
    screen.show()
    sys.exit(app.exec())