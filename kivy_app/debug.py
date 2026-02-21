"""Script de débogage pour identifier les erreurs."""
import sys
import traceback

try:
    from main import MemoryApp
    
    print("✅ App importée avec succès")
    app = MemoryApp()
    print("✅ MemoryApp() initialisé")
    app.run()
    print("✅ App lancée")
    
except Exception as e:
    print(f"❌ ERREUR CRITIQUE : {e}")
    print("\n📋 Traceback complet :")
    traceback.print_exc()
    input("Appuyez sur Entrée pour continuer...")
    sys.exit(1)
