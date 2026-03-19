"""
Configuration management for Void Clint Launcher
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from cryptography.fernet import Fernet
import base64
import hashlib

class ConfigManager:
    """Manages application configuration and settings"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".voidclint"
        self.config_file = self.config_dir / "config.json"
        self.accounts_file = self.config_dir / "accounts.enc"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "theme": "dark",
            "language": "en",
            "java_path": self._find_java(),
            "game_directory": str(Path.home() / ".minecraft"),
            "ram": {
                "min": 1024,
                "max": 4096
            },
            "resolution": {
                "width": 854,
                "height": 480
            },
            "fullscreen": False,
            "show_logs": True,
            "auto_update": True,
            "news_enabled": True
        }
        
        self.config = self.load_config()
        
    def _find_java(self) -> str:
        """Find Java installation on the system"""
        common_paths = [
            "java",
            "javaw",
            "/usr/bin/java",
            "/usr/lib/jvm/default-java/bin/java",
            "C:\\Program Files\\Java\\*\\bin\\java.exe",
            "C:\\Program Files (x86)\\Java\\*\\bin\\java.exe"
        ]
        
        # Simple check for java in PATH
        import shutil
        java_path = shutil.which("java")
        if java_path:
            return java_path
            
        return "java"  # Default to hoping it's in PATH
    
    def _get_encryption_key(self) -> bytes:
        """Generate or load encryption key for sensitive data"""
        key_file = self.config_dir / ".key"
        
        if key_file.exists():
            with open(key_file, 'rb') as f:
                key = f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(key_file, 'wb') as f:
                f.write(key)
                
        return key
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    return {**self.default_config, **config}
            except:
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save_config()
    
    def save_account(self, account_data: Dict[str, Any]):
        """Save account data encrypted"""
        cipher = Fernet(self._get_encryption_key())
        encrypted_data = cipher.encrypt(json.dumps(account_data).encode())
        
        with open(self.accounts_file, 'wb') as f:
            f.write(encrypted_data)
    
    def load_account(self) -> Optional[Dict[str, Any]]:
        """Load encrypted account data"""
        if not self.accounts_file.exists():
            return None
            
        try:
            cipher = Fernet(self._get_encryption_key())
            with open(self.accounts_file, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        except:
            return None
    
    def clear_account(self):
        """Remove saved account data"""
        if self.accounts_file.exists():
            self.accounts_file.unlink()
