# Mx-Purge Installer for Windows
Write-Host "🧹 Instalando Mx-Purge..." -ForegroundColor Cyan

# Verificar Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "❌ Python no encontrado. Instálalo desde python.org" -ForegroundColor Red
    exit 1
}

# Crear venv
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Crear batch file
$batContent = '@echo off
cd /d "%~dp0"
call venv\Scripts\activate
python mxpurge\cli.py %*'
$batContent | Out-File -Encoding ascii -FilePath "mxpurge.bat"

Write-Host "✅ Mx-Purge instalado correctamente" -ForegroundColor Green
Write-Host "💡 Usa: .\mxpurge.bat --help" -ForegroundColor Yellow
