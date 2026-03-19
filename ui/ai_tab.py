"""
AI Assistant Tab for Void Clint Launcher
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QTextEdit, QLineEdit, QScrollArea,
    QFrame, QGroupBox, QSplitter, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QTextCursor

class MessageBubble(QFrame):
    """Chat message bubble widget"""
    
    def __init__(self, message, is_user=True):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.setObjectName("messageBubble")
        
        # Style based on sender
        if is_user:
            self.setStyleSheet("""
                QFrame#messageBubble {
                    background-color: #6c5ce7;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
                QLabel {
                    color: white;
                }
            """)
            alignment = Qt.AlignRight
        else:
            self.setStyleSheet("""
                QFrame#messageBubble {
                    background-color: #2c2e33;
                    border-radius: 10px;
                    margin: 5px;
                    padding: 10px;
                }
                QLabel {
                    color: #e1e1e1;
                }
            """)
            alignment = Qt.AlignLeft
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Sender label
        sender = QLabel("You" if is_user else "Void AI")
        sender.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(sender)
        
        # Message content
        content = QLabel(message)
        content.setWordWrap(True)
        content.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(content)
        
        # Set alignment
        self.setLayout(layout)

class AITab(QWidget):
    """AI Assistant tab"""
    
    def __init__(self, ai_assistant, config):
        super().__init__()
        self.ai = ai_assistant
        self.config = config
        self.messages = []
        
        self.setup_ui()
        self.connect_signals()
        
        # Add welcome message
        self.add_ai_message("Hello! I'm your Void AI assistant. How can I help you with Minecraft today?")
    
    def setup_ui(self):
        """Setup the UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("AI Assistant")
        title.setObjectName("titleLabel")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        layout.addWidget(title)
        
        # Main splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Chat area
        chat_widget = QWidget()
        chat_layout = QVBoxLayout(chat_widget)
        
        # Scroll area for messages
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameStyle(QFrame.NoFrame)
        
        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.setSpacing(5)
        
        self.scroll_area.setWidget(self.chat_container)
        chat_layout.addWidget(self.scroll_area)
        
        splitter.addWidget(chat_widget)
        
        # Input area
        input_widget = QFrame()
        input_widget.setFrameStyle(QFrame.StyledPanel)
        input_layout = QVBoxLayout(input_widget)
        
        # Quick actions
        actions_layout = QHBoxLayout()
        
        self.crash_btn = QPushButton("Analyze Crash")
        self.crash_btn.clicked.connect(self.analyze_crash)
        actions_layout.addWidget(self.crash_btn)
        
        self.fps_btn = QPushButton("FPS Boost Tips")
        self.fps_btn.clicked.connect(self.get_fps_tips)
        actions_layout.addWidget(self.fps_btn)
        
        self.mod_btn = QPushButton("Mod Help")
        self.mod_btn.clicked.connect(self.get_mod_help)
        actions_layout.addWidget(self.mod_btn)
        
        self.clear_btn = QPushButton("Clear Chat")
        self.clear_btn.clicked.connect(self.clear_chat)
        actions_layout.addWidget(self.clear_btn)
        
        actions_layout.addStretch()
        input_layout.addLayout(actions_layout)
        
        # Text input
        input_row = QHBoxLayout()
        
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Ask me anything about Minecraft...")
        self.message_input.returnPressed.connect(self.send_message)
        input_row.addWidget(self.message_input)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setObjectName("primaryButton")
        self.send_btn.clicked.connect(self.send_message)
        input_row.addWidget(self.send_btn)
        
        input_layout.addLayout(input_row)
        
        splitter.addWidget(input_widget)
        
        # Set initial sizes (70% chat, 30% input)
        splitter.setSizes([500, 150])
        
        layout.addWidget(splitter)
    
    def connect_signals(self):
        """Connect AI signals"""
        self.ai.response_ready.connect(self.on_ai_response)
        self.ai.error_occurred.connect(self.on_ai_error)
        self.ai.analysis_complete.connect(self.on_analysis_complete)
    
    def send_message(self):
        """Send a message to AI"""
        message = self.message_input.text().strip()
        if not message:
            return
        
        # Add user message to chat
        self.add_user_message(message)
        self.message_input.clear()
        
        # Show typing indicator
        self.add_ai_message("Typing...", is_typing=True)
        
        # Send to AI
        self.ai.ask_question(message)
    
    def add_user_message(self, message):
        """Add user message to chat"""
        bubble = MessageBubble(message, is_user=True)
        self.chat_layout.addWidget(bubble)
        self.messages.append(("user", message))
        self.scroll_to_bottom()
    
    def add_ai_message(self, message, is_typing=False):
        """Add AI message to chat"""
        # Remove typing indicator if present
        if is_typing:
            # Store typing indicator reference
            self.typing_indicator = MessageBubble(message, is_user=False)
            self.chat_layout.addWidget(self.typing_indicator)
        else:
            # Remove typing indicator if exists
            if hasattr(self, 'typing_indicator'):
                self.typing_indicator.deleteLater()
                delattr(self, 'typing_indicator')
            
            bubble = MessageBubble(message, is_user=False)
            self.chat_layout.addWidget(bubble)
            self.messages.append(("ai", message))
        
        self.scroll_to_bottom()
    
    def on_ai_response(self, response):
        """Handle AI response"""
        self.add_ai_message(response)
    
    def on_ai_error(self, error):
        """Handle AI error"""
        self.add_ai_message(f"Sorry, I encountered an error: {error}")
    
    def on_analysis_complete(self, analysis):
        """Handle crash analysis"""
        # Format analysis nicely
        formatted = "🔍 **Crash Analysis**\n\n"
        
        if analysis["problem"]:
            formatted += f"**Problem:** {analysis['problem']}\n\n"
        
        if analysis["causes"]:
            formatted += "**Possible Causes:**\n"
            for cause in analysis["causes"]:
                formatted += f"• {cause}\n"
            formatted += "\n"
        
        if analysis["solutions"]:
            formatted += "**Solutions:**\n"
            for solution in analysis["solutions"]:
                formatted += f"• {solution}\n"
        
        self.add_ai_message(formatted)
    
    def analyze_crash(self):
        """Analyze Minecraft crash log"""
        self.add_user_message("Please analyze the latest crash log")
        self.add_ai_message("Analyzing crash logs...", is_typing=True)
        
        if not self.ai.analyze_crash_log():
            self.on_ai_error("No crash logs found")
    
    def get_fps_tips(self):
        """Get FPS boost tips"""
        self.add_user_message("Give me FPS boost tips")
        self.add_ai_message("Fetching FPS optimization tips...", is_typing=True)
        self.ai.get_fps_boost_tips()
    
    def get_mod_help(self):
        """Get mod installation help"""
        # Simple dialog for mod name
        from PyQt5.QtWidgets import QInputDialog
        
        mod_name, ok = QInputDialog.getText(
            self, "Mod Help", "Enter the mod name:"
        )
        
        if ok and mod_name:
            self.add_user_message(f"How do I install {mod_name}?")
            self.add_ai_message(f"Getting help for {mod_name}...", is_typing=True)
            self.ai.get_mod_help(mod_name)
    
    def clear_chat(self):
        """Clear all chat messages"""
        # Clear layout
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.messages.clear()
        self.add_ai_message("Chat cleared. How can I help you?")
    
    def scroll_to_bottom(self):
        """Scroll chat to bottom"""
        QTimer.singleShot(100, lambda: self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        ))
