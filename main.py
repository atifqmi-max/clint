#!/usr/bin/env python3
"""
Void Clint Minecraft Launcher
Main entry point for the application
"""

import sys
import os
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from dotenv import load_dotenv

from ui.main_window import MainWindow
from core.config import ConfigManager

# Load environment variables
load_dotenv()

def main():
    """Main application entry point"""
    
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    app = QApplication(sys.argv)
    app.setApplicationName("Void Clint")
    app.setApplicationVersion("1.0.0")
    
    # Set application icon
    icon_path = Path(__file__).parent / "assets" / "logo.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
