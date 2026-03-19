"""
Minecraft Game Launcher for Void Clint
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import minecraft_launcher_lib as mll

class LaunchThread(QThread):
    """Thread for launching Minecraft"""
    
    log_output = pyqtSignal(str)
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)
    error = pyqtSignal(str)
    
    def __init__(self, version_id: str, account_data: Dict, config: Dict):
        super().__init__()
        self.version_id = version_id
        self.account_data = account_data
        self.config = config
        self.process = None
        
    def run(self):
        """Launch Minecraft"""
        try:
            # Get minecraft directory
            minecraft_dir = self.config.get("game_directory")
            
            # Set up login options
            login_options = {
                "username": self.account_data["username"],
                "uuid": self.account_data["uuid"],
                "token": self.account_data["access_token"]
            }
            
            # Set up Minecraft options
            minecraft_options = {
                "gameDirectory": minecraft_dir,
                "launcherName": "Void Clint",
                "launcherVersion": "1.0.0"
            }
            
            # Set up JVM arguments for RAM
            jvm_args = []
            
            # RAM settings
            min_ram = self.config.get("ram.min", 1024)
            max_ram = self.config.get("ram.max", 4096)
            
            jvm_args.append(f"-Xms{min_ram}M")
            jvm_args.append(f"-Xmx{max_ram}M")
            
            # Additional JVM arguments for better performance
            jvm_args.extend([
                "-XX:+UnlockExperimentalVMOptions",
                "-XX:+UseG1GC",
                "-XX:G1NewSizePercent=20",
                "-XX:G1ReservePercent=20",
                "-XX:MaxGCPauseMillis=50",
                "-XX:G1HeapRegionSize=32M"
            ])
            
            # Resolution settings
            if self.config.get("resolution"):
                width = self.config.get("resolution.width", 854)
                height = self.config.get("resolution.height", 480)
                minecraft_options["customResolution"] = True
                minecraft_options["resolutionWidth"] = width
                minecraft_options["resolutionHeight"] = height
            
            # Fullscreen
            if self.config.get("fullscreen", False):
                minecraft_options["fullscreen"] = True
            
            # Generate launch command
            command = mll.command.get_minecraft_command(
                self.version_id,
                minecraft_dir,
                login_options,
                jvm_args=jvm_args,
                minecraft_options=minecraft_options
            )
            
            # Log the command if enabled
            if self.config.get("show_logs", True):
                self.log_output.emit(f"Launch command: {' '.join(command)}")
            
            # Launch the game
            self.process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Stream output
            for line in iter(self.process.stdout.readline, ''):
                if self.config.get("show_logs", True):
                    self.log_output.emit(line.strip())
                    
            # Wait for process to finish
            return_code = self.process.wait()
            self.finished.emit(return_code)
            
        except Exception as e:
            self.error.emit(str(e))
    
    def stop(self):
        """Stop the launched game"""
        if self.process:
            self.process.terminate()

class GameLauncher(QObject):
    """Main game launcher controller"""
    
    launch_started = pyqtSignal()
    log_line = pyqtSignal(str)
    launch_progress = pyqtSignal(int)
    launch_finished = pyqtSignal(int)
    launch_error = pyqtSignal(str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.launch_thread = None
        
    def launch_game(self, version_id: str, account_data: Dict):
        """Launch Minecraft with given version and account"""
        
        # Check if version is installed
        versions_dir = Path(self.config.get("game_directory")) / "versions" / version_id
        if not versions_dir.exists():
            self.launch_error.emit(f"Version {version_id} is not installed")
            return
        
        # Create and start launch thread
        self.launch_thread = LaunchThread(version_id, account_data, self.config)
        self.launch_thread.log_output.connect(self.log_line)
        self.launch_thread.progress.connect(self.launch_progress)
        self.launch_thread.finished.connect(self.launch_finished)
        self.launch_thread.error.connect(self.launch_error)
        
        self.launch_started.emit()
        self.launch_thread.start()
    
    def stop_game(self):
        """Stop the currently running game"""
        if self.launch_thread:
            self.launch_thread.stop()
    
    def is_running(self) -> bool:
        """Check if game is currently running"""
        return self.launch_thread is not None and self.launch_thread.isRunning()
