# 🧹 Mx-Purge

**Mx-Purge** es una herramienta inteligente de limpieza para **Windows y Linux** que elimina archivos basura, optimiza la memoria swap, libera espacio en disco y usa **IA** para recomendar qué limpiar según tu uso del sistema.

> Status: ✅ **Versión 1.0 - Estable**

## ✨ Características

- 🗑️ Limpieza de caché del sistema, navegadores, temporales y logs
- 🧠 **IA integrada** con modelo Random Forest
- 🔄 Limpieza y reconfiguración del **swap** en Linux
- 🧹 Liberación de espacio en Windows
- 🛡️ Modo seguro con rollback
- 📊 Estadísticas y reportes
- ⚙️ Automático o manual

## 🚀 Instalación rápida

```bash
# Linux/Mac
git clone https://github.com/Falconmx1/Mx-Purge.git
cd Mx-Purge
chmod +x install.sh
./install.sh

# Windows (PowerShell como Admin)
git clone https://github.com/Falconmx1/Mx-Purge.git
cd Mx-Purge
.\install.ps1

💻 Uso
mxpurge --scan              # Escanear sistema
mxpurge --clean             # Limpieza automática con IA
mxpurge --swap-clean        # Limpiar swap (Linux)
mxpurge --learn             # Entrenar IA
mxpurge --stats             # Ver estadísticas
mxpurge --rollback          # Restaurar última limpieza

📊 Ejemplo de salida
[INFO] Escaneando sistema...
[IA] Predicciones:
  - Cache del sistema: 95% seguro de limpiar (libera 2.3GB)
  - Logs antiguos: 88% seguro
  - Cache navegador: 76% seguro
[OK] Liberados 4.1GB en total
