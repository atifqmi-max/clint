"""
Settings Tab for Void Clint Launcher
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QSpinBox, QSlider, QCheckBox,
    QComboBox, QGroupBox, QFileDialog, QMessageBox,
    QScrollArea, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class SettingsTab(QWidget):
    """Settings management tab"""
    
    settings_changed = pyqtSignal()
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        """Setup the UI"""
        # Scroll area for settings
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(QScrollArea.NoFrame)
        
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("Settings")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(title)
        
        # Java Settings
        java_group = QGroupBox("Java Settings")
        java_layout = QGridLayout(java_group)
        
        java_layout.addWidget(QLabel("Java Path:"), 0, 0)
        self.java_path = QLineEdit()
        self.java_path.setReadOnly(True)
        java_layout.addWidget(self.java_path, 0, 1)
        
        self.java_browse = QPushButton("Browse")
        self.java_browse.clicked.connect(self.browse_java)
        java_layout.addWidget(self.java_browse, 0, 2)
        
        layout.addWidget(java_group)
        
        # Game Settings
        game_group = QGroupBox("Game Settings")
        game_layout = QGridLayout(game_group)
        
        game_layout.addWidget(QLabel("Game Directory:"), 0, 0)
        self.game_dir = QLineEdit()
        self.game_dir.setReadOnly(True)
        game_layout.addWidget(self.game_dir, 0, 1)
        
        self.game_browse = QPushButton("Browse")
        self.game_browse.clicked.connect(self.browse_game_dir)
        game_layout.addWidget(self.game_browse, 0, 2)
        
        layout.addWidget(game_group)
        
        # Memory Settings
        memory_group = QGroupBox("Memory Settings")
        memory_layout = QVBoxLayout(memory_group)
        
        # Min RAM
        min_ram_layout = QHBoxLayout()
        min_ram_layout.addWidget(QLabel("Minimum RAM:"))
        self.min_ram = QSpinBox()
        self.min_ram.setRange(512, 16384)
        self.min_ram.setSingleStep(512)
        self.min_ram.setSuffix(" MB")
        min_ram_layout.addWidget(self.min_ram)
        min_ram_layout.addStretch()
        memory_layout.addLayout(min_ram_layout)
        
        # Max RAM
        max_ram_layout = QHBoxLayout()
        max_ram_layout.addWidget(QLabel("Maximum RAM:"))
        self.max_ram = QSpinBox()
        self.max_ram.setRange(1024, 16384)
        self.max_ram.setSingleStep(512)
        self.max_ram.setSuffix(" MB")
        max_ram_layout.addWidget(self.max_ram)
        max_ram_layout.addStretch()
        memory_layout.addLayout(max_ram_layout)
        
        # RAM slider
        ram_label = QLabel("Quick RAM Selection:")
        memory_layout.addWidget(ram_label)
        
        self.ram_slider = QSlider(Qt.Horizontal)
        self.ram_slider.setRange(1, 16)
        self.ram_slider.setTickInterval(1)
        self.ram_slider.setTickPosition(QSlider.TicksBelow)
        self.ram_slider.valueChanged.connect(self.on_ram_slider_changed)
        memory_layout.addWidget(self.ram_slider)
        
        # RAM labels
        ram_labels_layout = QHBoxLayout()
        for i in range(1, 17, 2):
            label = QLabel(f"{i}GB")
            label.setAlignment(Qt.AlignCenter)
            ram_labels_layout.addWidget(label)
        memory_layout.addLayout(ram_labels_layout)
        
        layout.addWidget(memory_group)
        
        # Video Settings
        video_group = QGroupBox("Video Settings")
        video_layout = QGridLayout(video_group)
        
        # Resolution
        video_layout.addWidget(QLabel("Resolution:"), 0, 0)
        
        res_layout = QHBoxLayout()
        self.res_width = QSpinBox()
        self.res_width.setRange(640, 3840)
        self.res_width.setSingleStep(10)
        res_layout.addWidget(self.res_width)
        
        res_layout.addWidget(QLabel("x"))
        
        self.res_height = QSpinBox()
        self.res_height.setRange(480, 2160)
        self.res_height.setSingleStep(10)
        res_layout.addWidget(self.res_height)
        
        video_layout.addLayout(res_layout, 0, 1)
        
        # Fullscreen
        self.fullscreen = QCheckBox("Fullscreen Mode")
        video_layout.addWidget(self.fullscreen, 1, 0, 1, 2)
        
        layout.addWidget(video_group)
        
        # Interface Settings
        interface_group = QGroupBox("Interface Settings")
        interface_layout = QGridLayout(interface_group)
        
        # Theme
        interface_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.theme = QComboBox()
        self.theme.addItems(["Dark", "Light"])
        interface_layout.addWidget(self.theme, 0, 1)
        
        # Language
        interface_layout.addWidget(QLabel("Language:"), 1, 0)
        self.language = QComboBox()
        self.language.addItems(["English", "Urdu"])
        interface_layout.addWidget(self.language, 1, 1)
        
        # Show logs
        self.show_logs = QCheckBox("Show Console Logs")
        interface_layout.addWidget(self.show_logs, 2, 0, 1, 2)
        
        layout.addWidget(interface_group)
        
        # Other Settings
        other_group = QGroupBox("Other Settings")
        other_layout = QVBoxLayout(other_group)
        
        self.auto_update = QCheckBox("Auto-update Launcher")
        other_layout.addWidget(self.auto_update)
        
        self.news_enabled = QCheckBox("Show Minecraft News")
        other_layout.addWidget(self.news_enabled)
        
        layout.addWidget(other_group)
        
        # Save Button
        self.save_btn = QPushButton("Save Settings")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setFixedHeight(40)
        self.save_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.save_btn.clicked.connect(self.save_settings)
        layout.addWidget(self.save_btn)
        
        layout.addStretch()
        
        scroll.setWidget(main_widget)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
    
    def load_settings(self):
        """Load settings from config"""
        self.java_path.setText(self.config.get("java_path", ""))
        self.game_dir.setText(self.config.get("game_directory", ""))
        
        # RAM settings
        self.min_ram.setValue(self.config.get("ram.min", 1024))
        self.max_ram.setValue(self.config.get("ram.max", 4096))
        self.ram_slider.setValue(self.max_ram.value() // 1024)
        
        # Video settings
        self.res_width.setValue(self.config.get("resolution.width", 854))
        self.res_height.setValue(self.config.get("resolution.height", 480))
        self.fullscreen.setChecked(self.config.get("fullscreen", False))
        
        # Interface
        theme = self.config.get("theme", "dark")
        self.theme.setCurrentText(theme.capitalize())
        
        language = self.config.get("language", "en")
        self.language.setCurrentText("English" if language == "en" else "Urdu")
        
        self.show_logs.setChecked(self.config.get("show_logs", True))
        
        # Other
        self.auto_update.setChecked(self.config.get("auto_update", True))
        self.news_enabled.setChecked(self.config.get("news_enabled", True))
    
    def save_settings(self):
        """Save settings to config"""
        # Java path
        self.config.set("java_path", self.java_path.text())
        
        # Game directory
        self.config.set("game_directory", self.game_dir.text())
        
        # RAM settings
        self.config.set("ram.min", self.min_ram.value())
        self.config.set("ram.max", self.max_ram.value())
        
        # Video settings
        self.config.set("resolution.width", self.res_width.value())
        self.config.set("resolution.height", self.res_height.value())
        self.config.set("fullscreen", self.fullscreen.isChecked())
        
        # Interface
        theme = self.theme.currentText().lower()
        self.config.set("theme", theme)
        
        language = "en" if self.language.currentText() == "English" else "ur"
        self.config.set("language", language)
        
        self.config.set("show_logs", self.show_logs.isChecked())
        
        # Other
        self.config.set("auto_update", self.auto_update.isChecked())
        self.config.set("news_enabled", self.news_enabled.isChecked())
        
        # Save
        self.config.save_config()
        
        # Apply theme
        self.window().apply_theme()
        
        QMessageBox.information(self, "Success", "Settings saved successfully!")
        self.settings_changed.emit()
    
    def on_ram_slider_changed(self, value):
        """Handle RAM slider change"""
        self.max_ram.setValue(value * 1024)
    
    def browse_java(self):
        """Browse for Java executable"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Java Executable",
            str(Path.home()),
            "Java Executable (java.exe java);;All Files (*)"
        )
        
        if file_path:
            self.java_path.setText(file_path)
    
    def browse_game_dir(self):
        """Browse for game directory"""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Minecraft Directory",
            str(Path.home())
        )
        
        if dir_path:
            self.game_dir.setText(dir_path)
