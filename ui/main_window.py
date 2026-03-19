"""
Main Window for Void Clint Launcher
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QFrame,
    QApplication, QSystemTrayIcon, QMenu, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QFont, QPixmap

from ui.styles import get_theme
from ui.versions_tab import VersionsTab
from ui.ai_tab import AITab
from ui.settings_tab import SettingsTab
from core.auth import Authenticator
from core.launcher import GameLauncher
from core.version_manager import VersionManager
from core.ai_helper import AIAssistant
from core.config import ConfigManager

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize core components
        self.config = ConfigManager()
        self.auth = Authenticator(self.config)
        self.launcher = GameLauncher(self.config)
        self.version_manager = VersionManager(self.config)
        self.ai_assistant = AIAssistant(self.config)
        
        # Setup UI
        self.setWindowTitle("Void Clint Launcher")
        self.setMinimumSize(1200, 700)
        
        # Set window icon
        icon_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        # Apply theme
        self.apply_theme()
        
        # Setup UI
        self.setup_ui()
        
        # Connect signals
        self.connect_signals()
        
        # Check saved login
        self.check_saved_login()
        
        # Setup system tray
        self.setup_system_tray()
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.setup_sidebar(main_layout)
        
        # Content area
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        main_layout.addWidget(self.content_stack, 1)
        
        # Setup tabs
        self.setup_tabs()
    
    def setup_sidebar(self, parent_layout):
        """Setup the sidebar navigation"""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet("""
            QFrame#sidebar {
                background-color: #1e1f24;
                border-right: 1px solid #3d3f45;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(10)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setFixedSize(60, 60)
        
        # Load logo from URL
        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                pixmap = pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
        
        sidebar_layout.addWidget(logo_label)
        sidebar_layout.addSpacing(20)
        
        # Navigation buttons
        nav_buttons = [
            ("🏠", "Home", self.show_home),
            ("🚀", "Launch", self.show_launch),
            ("📦", "Versions", self.show_versions),
            ("⚙️", "Settings", self.show_settings),
            ("🤖", "AI Help", self.show_ai)
        ]
        
        self.nav_buttons = []
        
        for icon, text, callback in nav_buttons:
            btn = QPushButton(f"{icon}\n{text}")
            btn.setObjectName("navButton")
            btn.setFixedSize(70, 70)
            btn.setFont(QFont("Segoe UI", 9))
            btn.clicked.connect(callback)
            
            # Style
            btn.setStyleSheet("""
                QPushButton#navButton {
                    background-color: transparent;
                    border: none;
                    color: #8b8f9c;
                    text-align: center;
                    padding: 5px;
                }
                QPushButton#navButton:hover {
                    background-color: #2c2e33;
                    color: #ffffff;
                }
                QPushButton#navButton:checked {
                    color: #6c5ce7;
                }
            """)
            btn.setCheckable(True)
            
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
        
        sidebar_layout.addStretch()
        
        # User info at bottom
        self.user_frame = QFrame()
        self.user_frame.setObjectName("userFrame")
        user_layout = QVBoxLayout(self.user_frame)
        user_layout.setContentsMargins(5, 5, 5, 5)
        
        self.user_label = QLabel("Not logged in")
        self.user_label.setObjectName("userLabel")
        self.user_label.setAlignment(Qt.AlignCenter)
        self.user_label.setWordWrap(True)
        self.user_label.setStyleSheet("color: #8b8f9c; font-size: 10px;")
        
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("loginButton")
        self.login_btn.setFixedSize(60, 30)
        self.login_btn.clicked.connect(self.start_login)
        
        user_layout.addWidget(self.user_label)
        user_layout.addWidget(self.login_btn)
        
        sidebar_layout.addWidget(self.user_frame)
        
        parent_layout.addWidget(sidebar)
    
    def setup_tabs(self):
        """Setup the content tabs"""
        # Home tab
        home_tab = self.create_home_tab()
        self.content_stack.addWidget(home_tab)
        
        # Launch tab (placeholder - same as home for now)
        launch_tab = self.create_launch_tab()
        self.content_stack.addWidget(launch_tab)
        
        # Versions tab
        self.versions_tab = VersionsTab(self.version_manager, self.config)
        self.content_stack.addWidget(self.versions_tab)
        
        # Settings tab
        self.settings_tab = SettingsTab(self.config)
        self.content_stack.addWidget(self.settings_tab)
        
        # AI tab
        self.ai_tab = AITab(self.ai_assistant, self.config)
        self.content_stack.addWidget(self.ai_tab)
    
    def create_home_tab(self):
        """Create the home tab content"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Welcome message
        welcome_label = QLabel("Welcome to Void Clint")
        welcome_label.setObjectName("titleLabel")
        welcome_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(welcome_label)
        
        # News section
        news_label = QLabel("Latest Minecraft News")
        news_label.setFont(QFont("Segoe UI", 16))
        layout.addWidget(news_label)
        
        # News list (placeholder)
        news_widget = QFrame()
        news_widget.setObjectName("newsFrame")
        news_widget.setStyleSheet("""
            QFrame#newsFrame {
                background-color: #26282d;
                border: 1px solid #3d3f45;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        news_layout = QVBoxLayout(news_widget)
        
        # Sample news items
        news_items = [
            "Minecraft 1.20.5 released with new features!",
            "Void Clint Launcher v1.0.0 now available",
            "Performance improvements in latest snapshot"
        ]
        
        for item in news_items:
            item_label = QLabel(f"• {item}")
            item_label.setWordWrap(True)
            news_layout.addWidget(item_label)
        
        layout.addWidget(news_widget)
        layout.addStretch()
        
        return tab
    
    def create_launch_tab(self):
        """Create the launch tab content"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Launch Minecraft")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        layout.addWidget(title)
        
        # Launch controls
        controls_frame = QFrame()
        controls_frame.setObjectName("controlsFrame")
        controls_frame.setStyleSheet("""
            QFrame#controlsFrame {
                background-color: #26282d;
                border: 1px solid #3d3f45;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        
        controls_layout = QVBoxLayout(controls_frame)
        
        # Version selection
        version_layout = QHBoxLayout()
        version_label = QLabel("Select Version:")
        self.version_combo = self.versions_tab.version_combo if hasattr(self.versions_tab, 'version_combo') else None
        
        version_layout.addWidget(version_label)
        if self.version_combo:
            version_layout.addWidget(self.version_combo)
        version_layout.addStretch()
        
        controls_layout.addLayout(version_layout)
        
        # Launch button
        self.launch_btn = QPushButton("Launch Game")
        self.launch_btn.setObjectName("primaryButton")
        self.launch_btn.setFixedHeight(50)
        self.launch_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.launch_btn.clicked.connect(self.launch_game)
        controls_layout.addWidget(self.launch_btn)
        
        layout.addWidget(controls_frame)
        
        # Console output
        console_label = QLabel("Console Output:")
        console_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(console_label)
        
        self.console_output = QLabel("Ready to launch...")
        self.console_output.setObjectName("consoleOutput")
        self.console_output.setStyleSheet("""
            QLabel#consoleOutput {
                background-color: #1e1f24;
                border: 1px solid #3d3f45;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', monospace;
            }
        """)
        self.console_output.setWordWrap(True)
        self.console_output.setAlignment(Qt.AlignTop)
        self.console_output.setMinimumHeight(200)
        
        layout.addWidget(self.console_output)
        
        return tab
    
    def setup_system_tray(self):
        """Setup system tray icon and menu"""
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = Path(__file__).parent.parent / "assets" / "logo.png"
        if icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(icon_path)))
        
        # Create tray menu
        tray_menu = QMenu()
        
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)
        
        hide_action = tray_menu.addAction("Hide")
        hide_action.triggered.connect(self.hide)
        
        tray_menu.addSeparator()
        
        quit_action = tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def connect_signals(self):
        """Connect signal handlers"""
        # Auth signals
        self.auth.login_successful.connect(self.on_login_success)
        self.auth.login_failed.connect(self.on_login_failed)
        self.auth.login_started.connect(self.on_login_started)
        
        # Launcher signals
        self.launcher.log_line.connect(self.on_launcher_log)
        self.launcher.launch_finished.connect(self.on_launch_finished)
        self.launcher.launch_error.connect(self.on_launch_error)
    
    def check_saved_login(self):
        """Check for saved login and update UI"""
        if self.auth.is_logged_in():
            self.on_login_success(self.auth.current_account)
    
    def start_login(self):
        """Start Microsoft login process"""
        self.auth.start_login()
        self.login_btn.setEnabled(False)
        self.login_btn.setText("Logging in...")
    
    def on_login_started(self):
        """Handle login started"""
        self.user_label.setText("Opening browser for login...")
    
    def on_login_success(self, account_data):
        """Handle successful login"""
        self.user_label.setText(f"Logged in as\n{account_data['username']}")
        self.login_btn.setText("Logout")
        self.login_btn.setEnabled(True)
        self.login_btn.clicked.disconnect()
        self.login_btn.clicked.connect(self.logout)
    
    def on_login_failed(self, error_message):
        """Handle login failure"""
        self.user_label.setText("Login failed")
        self.login_btn.setText("Login")
        self.login_btn.setEnabled(True)
        
        QMessageBox.warning(self, "Login Failed", f"Failed to login: {error_message}")
    
    def logout(self):
        """Logout current user"""
        self.auth.logout()
        self.user_label.setText("Not logged in")
        self.login_btn.setText("Login")
        self.login_btn.clicked.disconnect()
        self.login_btn.clicked.connect(self.start_login)
    
    def launch_game(self):
        """Launch Minecraft"""
        if not self.auth.is_logged_in():
            QMessageBox.warning(self, "Not Logged In", "Please login first!")
            return
        
        # Get selected version
        if self.version_combo and self.version_combo.currentText():
            version_id = self.version_combo.currentText()
        else:
            QMessageBox.warning(self, "No Version", "Please select a version!")
            return
        
        # Refresh token if needed
        account_data = self.auth.refresh_token()
        if not account_data:
            QMessageBox.warning(self, "Auth Error", "Failed to refresh authentication")
            return
        
        # Launch game
        self.console_output.setText("Launching Minecraft...")
        self.launcher.launch_game(version_id, account_data)
    
    def on_launcher_log(self, log_line):
        """Handle launcher log output"""
        current_text = self.console_output.text()
        if len(current_text) > 10000:  # Limit log size
            current_text = current_text[-5000:]
        
        self.console_output.setText(current_text + "\n" + log_line)
    
    def on_launch_finished(self, return_code):
        """Handle game exit"""
        self.console_output.setText(self.console_output.text() + f"\nGame exited with code: {return_code}")
        
        # Check for crash
        if return_code != 0:
            self.analyze_crash()
    
    def on_launch_error(self, error):
        """Handle launch error"""
        self.console_output.setText(self.console_output.text() + f"\nERROR: {error}")
    
    def analyze_crash(self):
        """Analyze crash log"""
        reply = QMessageBox.question(
            self, "Game Crashed",
            "Minecraft crashed. Would you like to analyze the crash log?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.show_ai()
            self.ai_tab.analyze_crash()
    
    def apply_theme(self):
        """Apply current theme"""
        theme = self.config.get("theme", "dark")
        self.setStyleSheet(get_theme(theme))
    
    # Navigation methods
    def show_home(self):
        self.content_stack.setCurrentIndex(0)
        self.update_nav_buttons(0)
    
    def show_launch(self):
        self.content_stack.setCurrentIndex(1)
        self.update_nav_buttons(1)
    
    def show_versions(self):
        self.content_stack.setCurrentIndex(2)
        self.update_nav_buttons(2)
        self.versions_tab.refresh_versions()
    
    def show_settings(self):
        self.content_stack.setCurrentIndex(3)
        self.update_nav_buttons(3)
    
    def show_ai(self):
        self.content_stack.setCurrentIndex(4)
        self.update_nav_buttons(4)
    
    def update_nav_buttons(self, active_index):
        """Update navigation button states"""
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == active_index)
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.launcher.is_running():
            reply = QMessageBox.question(
                self, "Game Running",
                "Minecraft is still running. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.launcher.stop_game()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
