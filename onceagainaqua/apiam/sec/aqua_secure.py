import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QPushButton, QFileDialog, QLineEdit, QMessageBox
)
from PyQt6.QtCore import Qt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from base64 import urlsafe_b64encode

# === Key Derivation ===
salt = b'250731_44ad63f6_0f081d043d78e0a46da3f264e96d21c9f11c20f591eff0f4512bd922ffd0d5fa72fe06be630e5577ea86baf67ab57385dc1716a9f6b29fd45e86b62bfdcfeb9d67bdf6e12fd3d4732c022fe158f7aad8e04b2af0dcbc171244da8c8fc99f9cef6036776e760cbcb62e89c2b1a2c995ec96fc6e1eff085016a48bb4efba8d460d'  # Replace with securely generated salt in production

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),  # ✅ Fixed hash algorithm import
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

class VaultApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("aqua secure vault")
        self.resize(420, 240)
        self.setAcceptDrops(True)

        # === UI Layout ===
        self.layout = QVBoxLayout()

        self.label = QLabel("password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.info_label = QLabel("drag and drop files")
        self.encrypt_btn = QPushButton("encrypt")
        self.decrypt_btn = QPushButton("decrypt")

        # === Layout Assembly ===
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.info_label)
        self.layout.addWidget(self.encrypt_btn)
        self.layout.addWidget(self.decrypt_btn)
        self.setLayout(self.layout)

        # === Button Actions ===
        self.encrypt_btn.clicked.connect(self.encrypt_file)
        self.decrypt_btn.clicked.connect(self.decrypt_file)

    def get_key(self):
        password = self.password_input.text()
        if not password:
            QMessageBox.warning(self, "Missing Password", "Please enter a password.")
            return None
        return Fernet(derive_key(password, salt))

    def encrypt_file(self):
        fernet = self.get_key()
        if not fernet: return

        path, _ = QFileDialog.getOpenFileName(self, "Choose File to Encrypt")
        if not path: return

        try:
            with open(path, 'rb') as f:
                data = f.read()
            encrypted = fernet.encrypt(data)

            out_path = path + ".aquasv"
            with open(out_path, 'wb') as f:
                f.write(encrypted)

            QMessageBox.information(self, "Encrypted", f"File saved as:\n{out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Encryption Failed", str(e))

    def decrypt_file(self):
        fernet = self.get_key()
        if not fernet: return

        path, _ = QFileDialog.getOpenFileName(self, "Choose AquaSV File", filter="*.aquasv")
        if not path: return

        try:
            with open(path, 'rb') as f:
                data = f.read()
            decrypted = fernet.decrypt(data)

            out_path = path.replace(".aquasv", ".decrypted")
            with open(out_path, 'wb') as f:
                f.write(decrypted)

            QMessageBox.information(self, "Decrypted", f"File saved as:\n{out_path}")
        except Exception as e:
            QMessageBox.critical(self, "Decryption Failed", str(e))

    # === Drag & Drop Support ===
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        fernet = self.get_key()
        if not fernet: return

        dropped_files = [url.toLocalFile() for url in event.mimeData().urls()]
        for path in dropped_files:
            if os.path.isfile(path):
                try:
                    with open(path, 'rb') as f:
                        data = f.read()

                    if path.endswith(".aquasv"):
                        # Decrypt
                        decrypted = fernet.decrypt(data)
                        out_path = path.replace(".aquasv", ".decrypted")
                        with open(out_path, 'wb') as f:
                            f.write(decrypted)
                        QMessageBox.information(self, "Decrypted", f"File decrypted:\n{out_path}")
                    else:
                        # Encrypt
                        encrypted = fernet.encrypt(data)
                        out_path = path + ".aquasv"
                        with open(out_path, 'wb') as f:
                            f.write(encrypted)
                        QMessageBox.information(self, "Encrypted", f"File encrypted:\n{out_path}")

                except Exception as e:
                    QMessageBox.critical(self, "Error", f"{path}\n{str(e)}")

# === Launch the Vault ===
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VaultApp()
    window.show()
    sys.exit(app.exec())