import sys
import os
import pygame
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QSlider, QFileDialog, QListWidget, QTabWidget
)
from PySide6.QtCore import Qt

# 🎧 Initialize Pygame mixer
pygame.mixer.init()

class AquaMusicPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AquaCore Music Console")
        self.setGeometry(100, 100, 700, 400)
        self.current_track = None

        tabs = QTabWidget()
        tabs.addTab(self.build_player_tab(), "🎶 Now Playing")
        tabs.addTab(self.build_playlist_tab(), "📂 Playlist")

        self.setCentralWidget(tabs)

    def build_player_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.track_label = QLabel("Track: None")
        self.track_label.setAlignment(Qt.AlignCenter)

        play_btn = QPushButton("▶️ Play")
        pause_btn = QPushButton("⏸️ Pause")
        load_btn = QPushButton("📁 Load Track")

        play_btn.clicked.connect(self.play_track)
        pause_btn.clicked.connect(self.pause_track)
        load_btn.clicked.connect(self.load_track)

        volume_slider = QSlider(Qt.Horizontal)
        volume_slider.setRange(0, 100)
        volume_slider.setValue(70)
        volume_slider.valueChanged.connect(self.set_volume)

        layout.addWidget(self.track_label)
        layout.addWidget(load_btn)
        layout.addWidget(play_btn)
        layout.addWidget(pause_btn)
        layout.addWidget(QLabel("🔊 Volume"))
        layout.addWidget(volume_slider)
        widget.setLayout(layout)
        return widget

    def build_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        self.playlist = QListWidget()
        add_btn = QPushButton("➕ Add Track to Playlist")
        add_btn.clicked.connect(self.add_to_playlist)

        layout.addWidget(self.playlist)
        layout.addWidget(add_btn)
        widget.setLayout(layout)
        return widget

    def load_track(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Audio File", filter="Audio Files (*.mp3 *.wav)")
        if file_path:
            self.current_track = file_path
            self.track_label.setText(f"Track: {os.path.basename(file_path)}")
            pygame.mixer.music.load(file_path)

    def play_track(self):
        if self.current_track:
            pygame.mixer.music.play()
            self.statusBar().showMessage(f"Playing: {os.path.basename(self.current_track)}")

    def pause_track(self):
        pygame.mixer.music.pause()
        self.statusBar().showMessage("Paused.")

    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100)

    def add_to_playlist(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Add Track", filter="Audio Files (*.mp3 *.wav)")
        if file_path:
            self.playlist.addItem(os.path.basename(file_path))

app = QApplication(sys.argv)
window = AquaMusicPlayer()
window.show()
sys.exit(app.exec())