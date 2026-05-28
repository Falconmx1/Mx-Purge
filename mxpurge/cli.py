#!/usr/bin/env python3
"""
Mx-Purge Command Line Interface
"""

import argparse
import sys
import os
from pathlib import Path

# Añadir directorio padre al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mxpurge.cleaner import SystemCleaner
from mxpurge.ai_engine import MxPurgeAI
from mxpurge.swap_manager import SwapManager
from mxpurge.utils import print_banner, print_stats, confirm_action

def main():
    parser = argparse.ArgumentParser(
        description="Mx-Purge - Intelligent System Cleaner",
        epilog="Ejemplo: mxpurge --clean --ai"
    )
    
    parser.add_argument("--scan", action="store_true", help="Escanear sistema")
    parser.add_argument("--clean", action="store_true", help="Limpiar sistema")
    parser.add_argument("--swap-clean", action="store_true", help="Limpiar swap")
    parser.add_argument("--learn", action="store_true", help="Entrenar IA")
    parser.add_argument("--stats", action="store_true", help="Mostrar estadísticas")
    parser.add_argument("--rollback", action="store_true", help="Restaurar backup")
    parser.add_argument("--ai", action="store_true", help="Usar IA para decisiones")
    parser.add_argument("--quiet", "-q", action="store_true", help="Modo silencioso")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        parser.print_help()
        return
    
    print_banner()
    
    cleaner = SystemCleaner()
    ai_engine = MxPurgeAI()
    
    if args.scan:
        print("[INFO] Escaneando sistema...\n")
        report = cleaner.scan()
        print_stats(report)
        
        if args.ai:
            print("\n[IA] Analizando con inteligencia artificial...")
            predictions = ai_engine.predict(report)
            for item, confidence in predictions.items():
                print(f"  - {item}: {confidence*100:.1f}% seguro de limpiar")
    
    elif args.clean:
        if args.ai:
            print("[IA] Modo inteligente activado")
            report = cleaner.scan()
            predictions = ai_engine.predict(report)
            to_clean = [item for item, conf in predictions.items() if conf > 0.7]
            
            if not args.quiet:
                print(f"[IA] Recomiendo limpiar: {', '.join(to_clean)}")
                if not confirm_action("¿Continuar?"):
                    return
        else:
            to_clean = None
        
        freed = cleaner.clean_all(ai_recommendations=to_clean if args.ai else None)
        print(f"\n✅ Liberados: {freed:.2f} MB")
    
    elif args.swap_clean:
        if sys.platform == "linux":
            swap_mgr = SwapManager()
            swap_mgr.clean()
        else:
            print("[WARN] Limpieza de swap solo disponible en Linux")
    
    elif args.learn:
        print("[IA] Recolectando datos del sistema...")
        ai_engine.train_on_system()
        print("✅ IA entrenada correctamente")
    
    elif args.stats:
        stats = cleaner.get_stats()
        print_stats(stats)
    
    elif args.rollback:
        cleaner.rollback()
        print("✅ Sistema restaurado")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
