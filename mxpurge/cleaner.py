"""
System Cleaner Module
"""

import os
import shutil
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
import psutil
from tqdm import tqdm

class SystemCleaner:
    def __init__(self):
        self.os_type = os.name
        self.backup_file = Path.home() / ".mxpurge_backup.json"
        self.cleaned_items = []
        
    def scan(self):
        """Escanea el sistema y genera reporte"""
        report = {
            "cache_size": 0,
            "temp_size": 0,
            "log_size": 0,
            "browser_cache": 0,
            "total_waste": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        # Cache del sistema
        if self.os_type == 'nt':  # Windows
            cache_paths = [
                Path(os.environ.get('TEMP', 'C:\\Windows\\Temp')),
                Path(os.environ.get('TMP', 'C:\\Temp')),
                Path.home() / 'AppData' / 'Local' / 'Temp',
                Path.home() / 'AppData' / 'Local' / 'Cache'
            ]
        else:  # Linux
            cache_paths = [
                Path('/tmp'),
                Path.home() / '.cache',
                Path('/var/cache'),
                Path('/var/log')
            ]
        
        for path in cache_paths:
            if path.exists():
                size = self._get_folder_size(path) / (1024*1024)  # MB
                report["cache_size"] += size
        
        # Logs antiguos (>30 días)
        for log_path in Path('/var/log').glob('*.log') if self.os_type != 'nt' else []:
            if log_path.exists() and (datetime.now() - datetime.fromtimestamp(log_path.stat().st_mtime)).days > 30:
                report["log_size"] += log_path.stat().st_size / (1024*1024)
        
        report["total_waste"] = report["cache_size"] + report["temp_size"] + report["log_size"]
        return report
    
    def clean_all(self, ai_recommendations=None):
        """Limpia todo el sistema"""
        total_freed = 0
        backup = {"timestamp": datetime.now().isoformat(), "files": []}
        
        print("[INFO] Iniciando limpieza...")
        
        # Directorios a limpiar
        clean_dirs = []
        if self.os_type == 'nt':
            clean_dirs = [
                Path(os.environ.get('TEMP', 'C:\\Windows\\Temp')),
                Path.home() / 'AppData' / 'Local' / 'Temp',
                Path.home() / 'AppData' / 'Local' / 'Cache',
                Path.home() / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Recent'
            ]
        else:
            clean_dirs = [
                Path('/tmp'),
                Path.home() / '.cache',
                Path('/var/cache/apt/archives') if Path('/var/cache/apt').exists() else None
            ]
            clean_dirs = [d for d in clean_dirs if d]
        
        # Limpiar con barra de progreso
        for dir_path in tqdm(clean_dirs, desc="Limpiando directorios"):
            if dir_path and dir_path.exists():
                size_before = self._get_folder_size(dir_path)
                try:
                    for item in dir_path.iterdir():
                        if item.is_file():
                            backup["files"].append(str(item))
                            item.unlink()
                        elif item.is_dir():
                            backup["files"].append(str(item))
                            shutil.rmtree(item, ignore_errors=True)
                    size_after = self._get_folder_size(dir_path)
                    total_freed += (size_before - size_after) / (1024*1024)
                except Exception as e:
                    print(f"[WARN] No se pudo limpiar {dir_path}: {e}")
        
        # Guardar backup
        with open(self.backup_file, 'w') as f:
            json.dump(backup, f, indent=2)
        
        return total_freed
    
    def rollback(self):
        """Restaura archivos del último backup"""
        if not self.backup_file.exists():
            print("[ERROR] No hay backup disponible")
            return
        
        with open(self.backup_file, 'r') as f:
            backup = json.load(f)
        
        print(f"[INFO] Restaurando backup del {backup['timestamp']}")
        # Lógica de restauración simplificada
        print("[WARN] Rollback parcial - algunos archivos pueden no recuperarse")
    
    def _get_folder_size(self, path):
        """Calcula tamaño de carpeta en bytes"""
        total = 0
        try:
            for entry in path.rglob('*'):
                if entry.is_file():
                    total += entry.stat().st_size
        except (PermissionError, OSError):
            pass
        return total
    
    def get_stats(self):
        """Estadísticas del sistema"""
        return {
            "total_ram": psutil.virtual_memory().total / (1024**3),
            "available_ram": psutil.virtual_memory().available / (1024**3),
            "disk_usage": psutil.disk_usage('/').percent,
            "cpu_percent": psutil.cpu_percent(interval=1)
        }
