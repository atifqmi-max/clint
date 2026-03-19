"""
Microsoft Authentication for Void Clint Launcher
"""

import json
import webbrowser
from typing import Optional, Dict, Any
from pathlib import Path
import requests
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import minecraft_launcher_lib as mll

class MicrosoftAuthThread(QThread):
    """Thread for handling Microsoft authentication"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.auth_url = None
        self.auth_code = None
        
    def run(self):
        """Run the authentication process"""
        try:
            # Get Microsoft login URL
            login_url, self.auth_code = mll.microsoft.get_login_url(
                "https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize",
                "54497a29-6d78-40b6-984e-ea79bc45d52e"  # Azure App ID for Minecraft
            )
            
            self.auth_url = login_url
            
            # Wait for user to complete login
            # This will be handled by the main window
            
        except Exception as e:
            self.error.emit(str(e))
    
    def complete_login(self, auth_url: str):
        """Complete the login process with the redirect URL"""
        try:
            # Get token from redirect URL
            auth_code = mll.microsoft.parse_auth_code_url(auth_url)
            
            # Complete login
            login_data = mll.microsoft.complete_login(
                "54497a29-6d78-40b6-984e-ea79bc45d52e",
                None,  # client_secret is not needed
                "https://login.live.com/oauth20_desktop.srf",
                auth_code
            )
            
            # Get Minecraft profile
            profile = mll.microsoft.get_profile(login_data["access_token"])
            
            self.finished.emit({
                "username": profile["name"],
                "uuid": profile["id"],
                "access_token": login_data["access_token"],
                "refresh_token": login_data["refresh_token"],
                "expires_in": login_data["expires_in"]
            })
            
        except Exception as e:
            self.error.emit(str(e))

class Authenticator(QObject):
    """Main authentication handler"""
    
    login_successful = pyqtSignal(dict)
    login_failed = pyqtSignal(str)
    login_started = pyqtSignal()
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.auth_thread = None
        self.current_account = None
        
        # Try to load saved account
        self.load_saved_account()
    
    def load_saved_account(self):
        """Load saved account if available"""
        saved_account = self.config.load_account()
        if saved_account:
            self.current_account = saved_account
    
    def start_login(self):
        """Start the Microsoft login process"""
        self.login_started.emit()
        
        self.auth_thread = MicrosoftAuthThread()
        self.auth_thread.finished.connect(self.on_login_complete)
        self.auth_thread.error.connect(self.on_login_error)
        self.auth_thread.start()
        
        # Open browser for login
        if self.auth_thread.auth_url:
            webbrowser.open(self.auth_thread.auth_url)
    
    def on_login_complete(self, account_data: Dict[str, Any]):
        """Handle successful login"""
        self.current_account = account_data
        self.config.save_account(account_data)
        self.login_successful.emit(account_data)
    
    def on_login_error(self, error_message: str):
        """Handle login error"""
        self.login_failed.emit(error_message)
    
    def handle_redirect(self, redirect_url: str):
        """Handle OAuth redirect URL"""
        if self.auth_thread:
            self.auth_thread.complete_login(redirect_url)
    
    def refresh_token(self) -> Optional[Dict[str, Any]]:
        """Refresh the access token"""
        if not self.current_account:
            return None
            
        try:
            refresh_data = mll.microsoft.complete_refresh(
                "54497a29-6d78-40b6-984e-ea79bc45d52e",
                None,
                "https://login.live.com/oauth20_desktop.srf",
                self.current_account["refresh_token"]
            )
            
            # Update account data
            self.current_account.update({
                "access_token": refresh_data["access_token"],
                "refresh_token": refresh_data.get("refresh_token", self.current_account["refresh_token"]),
                "expires_in": refresh_data["expires_in"]
            })
            
            # Save updated account
            self.config.save_account(self.current_account)
            
            return self.current_account
            
        except Exception as e:
            print(f"Token refresh failed: {e}")
            return None
    
    def logout(self):
        """Log out current user"""
        self.current_account = None
        self.config.clear_account()
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in"""
        return self.current_account is not None
    
    def get_username(self) -> Optional[str]:
        """Get current username"""
        if self.current_account:
            return self.current_account.get("username")
        return None
