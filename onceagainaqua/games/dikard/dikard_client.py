import sys
import socket
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton

class MessagingClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("dikard")

        # Apply dark mode stylesheet
        dark_stylesheet = """
            QWidget { background-color: #232629; color: #f0f0f0; }
            QTextEdit, QLineEdit { background-color: #2b2b2b; color: #f0f0f0; border: 1px solid #444; }
            QPushButton { background-color: #444; color: #f0f0f0; border: 1px solid #666; padding: 5px; }
            QPushButton:hover { background-color: #555; }
        """
        self.setStyleSheet(dark_stylesheet)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('Jojopooter', 5000))

        layout = QVBoxLayout()
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.input_field = QLineEdit()
        layout.addWidget(self.input_field)

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

        # Start thread to listen for messages
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        message = self.input_field.text()
        if message:
            self.client_socket.send(message.encode('utf-8'))
            self.input_field.clear()

    def receive_messages(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode('utf-8')
                self.chat_display.append(msg)
            except:
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = MessagingClient()
    client.show()
    sys.exit(app.exec())