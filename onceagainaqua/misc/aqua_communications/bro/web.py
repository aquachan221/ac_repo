import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Embedded Browser")
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.google.com"))

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)

        self.go_button = QPushButton("Go")
        self.go_button.clicked.connect(self.load_url)

        top_layout = QVBoxLayout()
        top_layout.addWidget(self.url_bar)
        top_layout.addWidget(self.go_button)
        top_layout.addWidget(self.browser)

        container = QWidget()
        container.setLayout(top_layout)
        self.setCentralWidget(container)

    def load_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
