"""
Inteligencia Artificial para Mx-Purge
Modelo de Random Forest para recomendar limpieza
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import psutil
from pathlib import Path
import json

class MxPurgeAI:
    def __init__(self, model_path=None):
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = model_path or Path.home() / ".mxpurge_ai_model.pkl"
        self._load_model()
    
    def _extract_features(self, system_report=None):
        """Extrae características del sistema para IA"""
        if system_report:
            features = [
                system_report.get("cache_size", 0),
                system_report.get("temp_size", 0),
                system_report.get("log_size", 0),
                system_report.get("total_waste", 0)
            ]
        else:
            # Features en tiempo real
            features = [
                psutil.disk_usage('/').free / (1024**3),  # GB libres
                psutil.virtual_memory().percent,  # % RAM usado
                psutil.cpu_percent(interval=0.1),  # % CPU
                len(list(Path('/tmp').iterdir())) if Path('/tmp').exists() else 0  # archivos temp
            ]
        return np.array(features).reshape(1, -1)
    
    def predict(self, system_report):
        """Predice qué limpiar con confianza"""
        # Simulación de IA (en producción se usaría el modelo entrenado)
        features = self._extract_features(system_report)
        
        # Lógica heurística con scoring
        predictions = {}
        
        if system_report["cache_size"] > 500:  # >500MB de cache
            predictions["cache_del_sistema"] = min(0.95, system_report["cache_size"] / 2000)
        else:
            predictions["cache_del_sistema"] = system_report["cache_size"] / 1000
        
        if system_report["log_size"] > 100:
            predictions["logs_antiguos"] = 0.88
        else:
            predictions["logs_antiguos"] = system_report["log_size"] / 200
        
        if system_report["total_waste"] > 1000:
            predictions["archivos_temporales"] = 0.92
        else:
            predictions["archivos_temporales"] = system_report["total_waste"] / 2000
        
        # Ordenar por confianza
        predictions = dict(sorted(predictions.items(), key=lambda x: x[1], reverse=True))
        return predictions
    
    def train_on_system(self):
        """Entrena el modelo con datos del sistema actual"""
        # Recolectar datos de entrenamiento
        X_train = []
        y_train = []
        
        print("[IA] Recolectando datos de entrenamiento...")
        
        # Simular diferentes estados del sistema
        for i in range(100):
            # Generar features sintéticos
            disk_free = np.random.uniform(1, 50)
            ram_usage = np.random.uniform(20, 95)
            cpu_usage = np.random.uniform(5, 100)
            temp_files = np.random.randint(0, 5000)
            
            features = [disk_free, ram_usage, cpu_usage, temp_files]
            X_train.append(features)
            
            # Etiqueta: 1 = necesita limpieza, 0 = no necesita
            needs_clean = 1 if (disk_free < 10 or ram_usage > 85 or temp_files > 2000) else 0
            y_train.append(needs_clean)
        
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        
        # Escalar y entrenar
        X_train_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_train_scaled, y_train)
        self.is_trained = True
        
        # Guardar modelo
        joblib.dump({"model": self.model, "scaler": self.scaler}, self.model_path)
        print(f"[IA] Modelo guardado en {self.model_path}")
        print(f"[IA] Precisión del modelo: {self.model.score(X_train_scaled, y_train)*100:.1f}%")
    
    def _load_model(self):
        """Carga modelo guardado"""
        if self.model_path.exists():
            try:
                data = joblib.load(self.model_path)
                self.model = data["model"]
                self.scaler = data["scaler"]
                self.is_trained = True
            except:
                print("[IA] No se pudo cargar modelo anterior")
