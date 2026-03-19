"""
AI Assistant for Void Clint Launcher
Handles OpenAI integration, crash analysis, and game help
"""

import os
import re
from typing import List, Dict, Any, Optional
from pathlib import Path
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import requests
import json

class AIRequestThread(QThread):
    """Thread for making AI API requests"""
    
    response_received = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, prompt: str, system_message: str = ""):
        super().__init__()
        self.prompt = prompt
        self.system_message = system_message
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def run(self):
        """Send request to OpenAI API"""
        if not self.api_key:
            self.error_occurred.emit("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
            return
            
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            messages = []
            if self.system_message:
                messages.append({"role": "system", "content": self.system_message})
            
            messages.append({"role": "user", "content": self.prompt})
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 500
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result["choices"][0]["message"]["content"]
                self.response_received.emit(ai_response)
            else:
                self.error_occurred.emit(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            self.error_occurred.emit(f"Request failed: {str(e)}")

class AIAssistant(QObject):
    """AI Assistant for Minecraft help and crash analysis"""
    
    response_ready = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    analysis_complete = pyqtSignal(dict)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.current_thread = None
        
        # System prompts
        self.help_system_prompt = """You are a Minecraft expert assistant named Void AI, part of the Void Clint Launcher. 
        Help users with Minecraft problems, performance tips, mod installation, and general questions. 
        Be concise, friendly, and provide practical solutions."""
        
        self.crash_system_prompt = """You are a Minecraft crash analysis expert. 
        Analyze the provided crash log and identify the main problem, likely causes, and specific solutions.
        Format your response with clear sections: PROBLEM, LIKELY CAUSES, SOLUTIONS."""
    
    def ask_question(self, question: str):
        """Ask a general Minecraft question"""
        self.current_thread = AIRequestThread(question, self.help_system_prompt)
        self.current_thread.response_received.connect(self.response_ready)
        self.current_thread.error_occurred.connect(self.error_occurred)
        self.current_thread.start()
    
    def analyze_crash_log(self) -> bool:
        """Analyze the latest Minecraft crash log"""
        minecraft_dir = self.config.get("game_directory")
        logs_dir = Path(minecraft_dir) / "logs"
        crash_reports_dir = Path(minecraft_dir) / "crash-reports"
        
        # Try to find latest crash log
        latest_log = None
        latest_time = 0
        
        # Check crash reports first
        if crash_reports_dir.exists():
            for crash_file in crash_reports_dir.glob("*.txt"):
                if crash_file.stat().st_mtime > latest_time:
                    latest_time = crash_file.stat().st_mtime
                    latest_log = crash_file
        
        # Check latest log if no crash report
        if not latest_log:
            latest_log = logs_dir / "latest.log"
            if not latest_log.exists():
                self.error_occurred.emit("No crash logs found")
                return False
        
        # Read log file
        try:
            with open(latest_log, 'r', encoding='utf-8', errors='ignore') as f:
                log_content = f.read()
            
            # Extract relevant parts (last 100 lines or stack trace)
            lines = log_content.split('\n')
            if len(lines) > 100:
                log_content = '\n'.join(lines[-100:])
            
            # Send to AI for analysis
            prompt = f"""Analyze this Minecraft crash log and provide a detailed diagnosis:
          
