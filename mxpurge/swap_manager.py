"""
Swap Manager para Linux
"""

import subprocess
import os
from pathlib import Path

class SwapManager:
    def __init__(self):
        self.swap_path = "/swapfile"
    
    def clean(self):
        """Limpia y optimiza swap"""
        if os.geteuid() != 0:
            print("[ERROR] Se necesitan permisos root para limpiar swap")
            print("[INFO] Ejecuta: sudo mxpurge --swap-clean")
            return
        
        print("[INFO] Limpiando swap...")
        
        try:
            # Desactivar swap
            subprocess.run(["swapoff", self.swap_path], check=True)
            print("[OK] Swap desactivado")
            
            # Recrear swap limpio
            subprocess.run(["dd", "if=/dev/zero", f"of={self.swap_path}", "bs=1M", "count=1024"], 
                          check=True, capture_output=True)
            subprocess.run(["mkswap", self.swap_path], check=True)
            subprocess.run(["swapon", self.swap_path], check=True)
            print("[OK] Swap recreado y activado")
            
            # Configurar swappiness óptimo
            with open("/proc/sys/vm/swappiness", "w") as f:
                f.write("10")
            print("[OK] Swappiness ajustado a 10 (óptimo)")
            
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Fallo al limpiar swap: {e}")
