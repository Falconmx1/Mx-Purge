# 🧹 Mx-Purge

**Mx-Purge** es una herramienta inteligente de limpieza para **Windows y Linux** que elimina archivos basura, optimiza la memoria swap, libera espacio en disco y usa **IA** para recomendar qué limpiar según tu uso del sistema.

> Status: 🚧 En desarrollo activo

---

## ✨ Características

- 🗑️ Limpieza de caché del sistema, navegadores, temporales y logs.
- 🧠 **IA integrada** (modelo local o API) para analizar patrones de uso y sugerir limpieza segura.
- 🔄 Limpieza y reconfiguración del **swap** en Linux.
- 🧹 Liberación de espacio en Windows (basura de actualizaciones, `%temp%`, Prefetch, etc.)
- 🛡️ Modo seguro con rollback.
- 📊 Estadísticas de limpieza y ahorro de espacio.
- ⚙️ Modo automático o manual.

---

## 🧠 IA en Mx-Purge

Usamos un modelo ligero (ej. `scikit-learn` o `TensorFlow Lite`) que aprende:

- Qué archivos puedes borrar sin riesgo.
- Frecuencia de limpieza óptima.
- Predicción de liberación de espacio.

La IA corre **localmente** (privacidad total) o con API opcional.

---

## 📦 Instalación

### Linux / macOS
```bash
git clone https://github.com/Falconmx1/Mx-Purge.git
cd Mx-Purge
chmod +x install.sh
./install.sh

Windows
git clone https://github.com/Falconmx1/Mx-Purge.git
cd Mx-Purge
.\install.ps1

🚀 Uso básico
mxpurge --scan          # Escanea el sistema
mxpurge --clean         # Limpieza automática (con IA)
mxpurge --swap-clean    # Limpia swap (Linux)
mxpurge --learn         # Entrena IA con tu uso
