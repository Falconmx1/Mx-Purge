#!/bin/bash
# Mx-Purge Installer for Linux/Mac

set -e

echo "🧹 Instalando Mx-Purge..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no encontrado. Instálalo primero."
    exit 1
fi

# Crear directorio virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# Crear ejecutable global
sudo cat > /usr/local/bin/mxpurge << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"
source venv/bin/activate
python3 mxpurge/cli.py "$@"
EOF

sudo chmod +x /usr/local/bin/mxpurge

echo "✅ Mx-Purge instalado correctamente"
echo "💡 Usa: mxpurge --help"
