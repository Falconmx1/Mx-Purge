"""
Utilidades para Mx-Purge
"""

import platform
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    """Muestra banner de Mx-Purge"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════╗
{Fore.CYAN}║{Fore.GREEN}      🧹 Mx-Purge v1.0 - Cleaner IA      {Fore.CYAN}║
{Fore.CYAN}║{Fore.YELLOW}   Limpieza inteligente para {platform.system()}   {Fore.CYAN}║
{Fore.CYAN}╚══════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)

def print_stats(stats):
    """Muestra estadísticas formateadas"""
    print(f"\n{Fore.CYAN}📊 Estadísticas del sistema:{Style.RESET_ALL}")
    
    if "cache_size" in stats:
        print(f"  🗂️  Cache: {stats['cache_size']:.2f} MB")
        print(f"  📝 Logs antiguos: {stats['log_size']:.2f} MB")
        print(f"  💾 Total desperdiciado: {stats['total_waste']:.2f} MB")
        print(f"  ✅ Espacio potencial: {stats['total_waste']:.2f} MB")
    else:
        print(f"  💾 RAM total: {stats['total_ram']:.1f} GB")
        print(f"  🧠 RAM disponible: {stats['available_ram']:.1f} GB")
        print(f"  💿 Uso de disco: {stats['disk_usage']:.1f}%")
        print(f"  🔥 CPU: {stats['cpu_percent']:.1f}%")

def confirm_action(message):
    """Solicita confirmación al usuario"""
    response = input(f"{Fore.YELLOW}❓ {message} (s/N): {Style.RESET_ALL}")
    return response.lower() in ['s', 'si', 'sí', 'y', 'yes']
