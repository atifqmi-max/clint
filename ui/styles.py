"""
UI Styles for Void Clint Launcher
Contains theme definitions and styling
"""

# Dark theme (default)
DARK_THEME = """
QMainWindow {
    background-color: #1a1b1e;
}

QWidget {
    background-color: #1a1b1e;
    color: #e1e1e1;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 12px;
}

QPushButton {
    background-color: #2c2e33;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    padding: 8px 16px;
    color: #ffffff;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #3d3f45;
    border-color: #565b66;
}

QPushButton:pressed {
    background-color: #1e1f24;
}

QPushButton:disabled {
    background-color: #26282d;
    color: #6b6f7c;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #26282d;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    padding: 6px;
    color: #ffffff;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #6c5ce7;
}

QComboBox {
    background-color: #2c2e33;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    padding: 6px;
    color: #ffffff;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #ffffff;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #2c2e33;
    border: 1px solid #3d3f45;
    selection-background-color: #6c5ce7;
    color: #ffffff;
}

QListWidget, QTreeWidget {
    background-color: #26282d;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    outline: none;
}

QListWidget::item, QTreeWidget::item {
    padding: 8px;
    border-bottom: 1px solid #3d3f45;
}

QListWidget::item:selected, QTreeWidget::item:selected {
    background-color: #6c5ce7;
    color: #ffffff;
}

QListWidget::item:hover, QTreeWidget::item:hover {
    background-color: #3d3f45;
}

QTabWidget::pane {
    background-color: #1a1b1e;
    border: 1px solid #3d3f45;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #2c2e33;
    border: 1px solid #3d3f45;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #6c5ce7;
    border-color: #6c5ce7;
}

QTabBar::tab:hover:!selected {
    background-color: #3d3f45;
}

QScrollBar:vertical {
    background-color: #26282d;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #3d3f45;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #565b66;
}

QScrollBar:horizontal {
    background-color: #26282d;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #3d3f45;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #565b66;
}

QProgressBar {
    background-color: #26282d;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    text-align: center;
    color: #ffffff;
}

QProgressBar::chunk {
    background-color: #6c5ce7;
    border-radius: 3px;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #26282d;
    border: 1px solid #3d3f45;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #6c5ce7;
    border-color: #6c5ce7;
}

QCheckBox::indicator:hover {
    border-color: #6c5ce7;
}

QGroupBox {
    background-color: #26282d;
    border: 1px solid #3d3f45;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QSlider::groove:horizontal {
    background-color: #26282d;
    border: 1px solid #3d3f45;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #6c5ce7;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background-color: #8b7bf0;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #6c5ce7;
}

QLabel#statusLabel {
    color: #6c5ce7;
    font-style: italic;
}

QPushButton#primaryButton {
    background-color: #6c5ce7;
    border: none;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #8b7bf0;
}

QPushButton#dangerButton {
    background-color: #e74c3c;
}

QPushButton#dangerButton:hover {
    background-color: #c0392b;
}
"""

# Light theme
LIGHT_THEME = """
QMainWindow {
    background-color: #f5f5f5;
}

QWidget {
    background-color: #f5f5f5;
    color: #2c3e50;
    font-family: 'Segoe UI', 'Arial', sans-serif;
    font-size: 12px;
}

QPushButton {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 8px 16px;
    color: #2c3e50;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #e8e8e8;
    border-color: #95a5a6;
}

QPushButton:pressed {
    background-color: #d5d5d5;
}

QPushButton:disabled {
    background-color: #ecf0f1;
    color: #95a5a6;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    color: #2c3e50;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border-color: #3498db;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    padding: 6px;
    color: #2c3e50;
}

QComboBox::drop-down {
    border: none;
    width: 20px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid #2c3e50;
    margin-right: 5px;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    selection-background-color: #3498db;
    color: #2c3e50;
}

QListWidget, QTreeWidget {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    outline: none;
}

QListWidget::item, QTreeWidget::item {
    padding: 8px;
    border-bottom: 1px solid #ecf0f1;
}

QListWidget::item:selected, QTreeWidget::item:selected {
    background-color: #3498db;
    color: #ffffff;
}

QListWidget::item:hover, QTreeWidget::item:hover {
    background-color: #e8e8e8;
}

QTabWidget::pane {
    background-color: #f5f5f5;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    padding: 8px 16px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background-color: #3498db;
    border-color: #3498db;
    color: #ffffff;
}

QTabBar::tab:hover:!selected {
    background-color: #e8e8e8;
}

QScrollBar:vertical {
    background-color: #ecf0f1;
    width: 12px;
    border-radius: 6px;
}

QScrollBar::handle:vertical {
    background-color: #bdc3c7;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #95a5a6;
}

QScrollBar:horizontal {
    background-color: #ecf0f1;
    height: 12px;
    border-radius: 6px;
}

QScrollBar::handle:horizontal {
    background-color: #bdc3c7;
    border-radius: 6px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #95a5a6;
}

QProgressBar {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    text-align: center;
    color: #2c3e50;
}

QProgressBar::chunk {
    background-color: #3498db;
    border-radius: 3px;
}

QCheckBox {
    spacing: 8px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 3px;
}

QCheckBox::indicator:checked {
    background-color: #3498db;
    border-color: #3498db;
}

QCheckBox::indicator:hover {
    border-color: #3498db;
}

QGroupBox {
    background-color: #ffffff;
    border: 1px solid #bdc3c7;
    border-radius: 4px;
    margin-top: 12px;
    padding-top: 12px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

QSlider::groove:horizontal {
    background-color: #ecf0f1;
    border: 1px solid #bdc3c7;
    height: 6px;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background-color: #3498db;
    width: 16px;
    height: 16px;
    margin: -5px 0;
    border-radius: 8px;
}

QSlider::handle:horizontal:hover {
    background-color: #5dade2;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #3498db;
}

QLabel#statusLabel {
    color: #3498db;
    font-style: italic;
}

QPushButton#primaryButton {
    background-color: #3498db;
    border: none;
    color: #ffffff;
    font-weight: bold;
}

QPushButton#primaryButton:hover {
    background-color: #5dade2;
}

QPushButton#dangerButton {
    background-color: #e74c3c;
    color: #ffffff;
}

QPushButton#dangerButton:hover {
    background-color: #c0392b;
}
"""

# Get theme by name
def get_theme(theme_name: str = "dark") -> str:
    """Return the requested theme stylesheet"""
    if theme_name.lower() == "light":
        return LIGHT_THEME
    return DARK_THEME
