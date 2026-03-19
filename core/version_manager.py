"""
Minecraft Version Manager for Void Clint Launcher
"""

import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal, QThread
import requests
import minecraft_launcher_lib as mll

class VersionFetchThread(QThread):
    """Thread for fetching available versions"""
    
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    
    def run(self):
        """Fetch versions from Mojang"""
        try:
            version_manifest = mll.utils.get_version_manifest()
            versions = []
            
            for version in version_manifest["versions"]:
                versions.append({
                    "id": version["id"],
                    "type": version["type"],
                    "url": version["url"],
                    "release_time": version.get("releaseTime", ""),
                    "installed": False
                })
            
            self.finished.emit(versions)
        except Exception as e:
            self.error.emit(str(e))

class VersionInstallThread(QThread):
    """Thread for installing Minecraft versions"""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, version_id: str, minecraft_dir: str):
        super().__init__()
        self.version_id = version_id
        self.minecraft_dir = minecraft_dir
        
    def run(self):
        """Install the selected version"""
        try:
            # Create progress callback
            def callback(progress: dict):
                if progress.get("current", 0) > 0:
                    percent = int((progress["current"] / progress["total"]) * 100)
                    self.progress.emit(percent)
                self.status.emit(progress.get("status", ""))
            
            # Install version
            mll.install.install_minecraft_version(
                self.version_id,
                self.minecraft_dir,
                callback=callback
            )
            
            self.finished.emit(self.version_id)
        except Exception as e:
            self.error.emit(str(e))

class VersionManager(QObject):
    """Manages Minecraft versions"""
    
    versions_fetched = pyqtSignal(list)
    fetch_error = pyqtSignal(str)
    install_progress = pyqtSignal(int)
    install_status = pyqtSignal(str)
    install_finished = pyqtSignal(str)
    install_error = pyqtSignal(str)
    
    def __init__(self, config_manager):
        super().__init__()
        self.config = config_manager
        self.fetch_thread = None
        self.install_thread = None
        self.available_versions = []
        self.installed_versions = []
        
    def fetch_versions(self):
        """Fetch all available versions"""
        self.fetch_thread = VersionFetchThread()
        self.fetch_thread.finished.connect(self.on_versions_fetched)
        self.fetch_thread.error.connect(self.fetch_error)
        self.fetch_thread.start()
    
    def on_versions_fetched(self, versions: List[Dict]):
        """Handle fetched versions"""
        self.available_versions = versions
        self.scan_installed_versions()
        
        # Mark installed versions
        installed_ids = [v["id"] for v in self.installed_versions]
        for version in self.available_versions:
            version["installed"] = version["id"] in installed_ids
            
        self.versions_fetched.emit(self.available_versions)
    
    def scan_installed_versions(self):
        """Scan for installed versions"""
        minecraft_dir = self.config.get("game_directory")
        versions_dir = Path(minecraft_dir) / "versions"
        
        self.installed_versions = []
        
        if versions_dir.exists():
            for version_folder in versions_dir.iterdir():
                if version_folder.is_dir():
                    version_json = version_folder / f"{version_folder.name}.json"
                    if version_json.exists():
                        try:
                            with open(version_json, 'r') as f:
                                version_data = json.load(f)
                                self.installed_versions.append({
                                    "id": version_folder.name,
                                    "type": version_data.get("type", "unknown"),
                                    "release_time": version_data.get("releaseTime", ""),
                                    "path": str(version_folder)
                                })
                        except:
                            # If JSON is corrupted, still add as unknown
                            self.installed_versions.append({
                                "id": version_folder.name,
                                "type": "unknown",
                                "release_time": "",
                                "path": str(version_folder)
                            })
    
    def install_version(self, version_id: str):
        """Install a specific version"""
        minecraft_dir = self.config.get("game_directory")
        
        self.install_thread = VersionInstallThread(version_id, minecraft_dir)
        self.install_thread.progress.connect(self.install_progress)
        self.install_thread.status.connect(self.install_status)
        self.install_thread.finished.connect(self.on_install_finished)
        self.install_thread.error.connect(self.install_error)
        self.install_thread.start()
    
    def on_install_finished(self, version_id: str):
        """Handle successful installation"""
        self.scan_installed_versions()
        self.install_finished.emit(version_id)
    
    def delete_version(self, version_id: str):
        """Delete an installed version"""
        minecraft_dir = self.config.get("game_directory")
        version_dir = Path(minecraft_dir) / "versions" / version_id
        
        if version_dir.exists():
            shutil.rmtree(version_dir)
            self.scan_installed_versions()
            return True
        return False
    
    def get_installed_versions(self) -> List[Dict]:
        """Get list of installed versions"""
        self.scan_installed_versions()
        return self.installed_versions
    
    def get_version_info(self, version_id: str) -> Optional[Dict]:
        """Get detailed information about a version"""
        for version in self.available_versions:
            if version["id"] == version_id:
                return version
        return None
    
    def is_installed(self, version_id: str) -> bool:
        """Check if a version is installed"""
        for version in self.installed_versions:
            if version["id"] == version_id:
                return True
        return False
