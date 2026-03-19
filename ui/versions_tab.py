"""
Versions Management Tab for Void Clint Launcher
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QListWidget, QListWidgetItem, QComboBox,
    QProgressBar, QMessageBox, QFrame, QSplitter,
    QGroupBox
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

class VersionsTab(QWidget):
    """Versions management tab"""
    
    version_selected = pyqtSignal(str)
    
    def __init__(self, version_manager, config):
        super().__init__()
        self.version_manager = version_manager
        self.config = config
        self.current_versions = []
        
        self.setup_ui()
        self.connect_signals()
        
        # Load versions
        self.refresh_versions()
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Version Manager")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(title)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Available versions
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_layout = QVBoxLayout(left_panel)
        
        left_layout.addWidget(QLabel("Available Versions:"))
        
        self.version_list = QListWidget()
        self.version_list.setIconSize(QSize(32, 32))
        left_layout.addWidget(self.version_list)
        
        # Version controls
        controls_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_versions)
        controls_layout.addWidget(self.refresh_btn)
        
        self.install_btn = QPushButton("Install Selected")
        self.install_btn.setObjectName("primaryButton")
        self.install_btn.clicked.connect(self.install_selected)
        controls_layout.addWidget(self.install_btn)
        
        left_layout.addLayout(controls_layout)
        
        # Right panel - Installed versions
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_layout = QVBoxLayout(right_panel)
        
        right_layout.addWidget(QLabel("Installed Versions:"))
        
        self.installed_list = QListWidget()
        right_layout.addWidget(self.installed_list)
        
        # Installed version controls
        installed_controls = QHBoxLayout()
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.clicked.connect(self.delete_selected)
        installed_controls.addWidget(self.delete_btn)
        
        self.select_btn = QPushButton("Select for Launch")
        self.select_btn.setObjectName("primaryButton")
        self.select_btn.clicked.connect(self.select_for_launch)
        installed_controls.addWidget(self.select_btn)
        
        right_layout.addLayout(installed_controls)
        
        # Add panels to splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([400, 400])
        
        layout.addWidget(splitter)
        
        # Progress section
        progress_group = QGroupBox("Installation Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
    
    def connect_signals(self):
        """Connect signals to handlers"""
        self.version_manager.versions_fetched.connect(self.on_versions_fetched)
        self.version_manager.fetch_error.connect(self.on_fetch_error)
        self.version_manager.install_progress.connect(self.update_progress)
        self.version_manager.install_status.connect(self.update_status)
        self.version_manager.install_finished.connect(self.on_install_finished)
        self.version_manager.install_error.connect(self.on_install_error)
    
    def refresh_versions(self):
        """Refresh the versions list"""
        self.status_label.setText("Fetching versions...")
        self.version_manager.fetch_versions()
    
    def on_versions_fetched(self, versions):
        """Handle fetched versions"""
        self.current_versions = versions
        self.version_list.clear()
        
        for version in versions:
            item = QListWidgetItem(self.version_list)
            
            # Set icon based on version type
            if version["type"] == "release":
                item.setIcon(self.style().standardIcon(self.style().SP_DialogApplyButton))
            elif version["type"] == "snapshot":
                item.setIcon(self.style().standardIcon(self.style().SP_DialogWarningButton))
            else:
                item.setIcon(self.style().standardIcon(self.style().SP_FileIcon))
            
            # Format text
            status = "✓" if version["installed"] else ""
            text = f"{version['id']} ({version['type']}) {status}"
            item.setText(text)
            item.setData(Qt.UserRole, version["id"])
        
        self.status_label.setText(f"Found {len(versions)} versions")
        
        # Update installed list
        self.update_installed_list()
    
    def update_installed_list(self):
        """Update the installed versions list"""
        self.installed_list.clear()
        
        installed = self.version_manager.get_installed_versions()
        
        for version in installed:
            item = QListWidgetItem(self.installed_list)
            item.setText(f"{version['id']} ({version['type']})")
            item.setData(Qt.UserRole, version["id"])
    
    def install_selected(self):
        """Install the selected version"""
        current_item = self.version_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a version to install")
            return
        
        version_id = current_item.data(Qt.UserRole)
        
        # Check if already installed
        for version in self.current_versions:
            if version["id"] == version_id and version["installed"]:
                QMessageBox.information(self, "Already Installed", f"Version {version_id} is already installed")
                return
        
        # Confirm installation
        reply = QMessageBox.question(
            self, "Confirm Installation",
            f"Install Minecraft {version_id}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.status_label.setText(f"Installing {version_id}...")
            self.version_manager.install_version(version_id)
    
    def delete_selected(self):
        """Delete the selected installed version"""
        current_item = self.installed_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a version to delete")
            return
        
        version_id = current_item.data(Qt.UserRole)
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Deletion",
            f"Are you sure you want to delete Minecraft {version_id}?\nThis cannot be undone!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.version_manager.delete_version(version_id):
                self.update_installed_list()
                self.refresh_versions()  # Refresh to update status
                self.status_label.setText(f"Deleted {version_id}")
            else:
                QMessageBox.warning(self, "Deletion Failed", f"Failed to delete {version_id}")
    
    def select_for_launch(self):
        """Select version for launch and switch to launch tab"""
        current_item = self.installed_list.currentItem()
        if current_item:
            version_id = current_item.data(Qt.UserRole)
            self.version_selected.emit(version_id)
            
            # Find main window and switch to launch tab
            main_window = self.window()
            if hasattr(main_window, 'show_launch'):
                main_window.show_launch()
    
    def update_progress(self, value):
        """Update progress bar"""
        self.progress_bar.setValue(value)
    
    def update_status(self, status):
        """Update status label"""
        self.status_label.setText(status)
    
    def on_install_finished(self, version_id):
        """Handle successful installation"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Successfully installed {version_id}")
        self.refresh_versions()
    
    def on_install_error(self, error):
        """Handle installation error"""
        self.progress_bar.setVisible(False)
        self.status_label.setText(f"Installation failed")
        QMessageBox.critical(self, "Installation Failed", f"Failed to install: {error}")
    
    def on_fetch_error(self, error):
        """Handle fetch error"""
        self.status_label.setText("Failed to fetch versions")
        QMessageBox.critical(self, "Error", f"Failed to fetch versions: {error}")
