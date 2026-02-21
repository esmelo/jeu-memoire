#!/usr/bin/env python3
"""
Guide pour télécharger le projet sur GitHub

Étapes (à faire manuellement):
1. Créer un compte sur GitHub.com (si pas d'accès)
2. Cliquer "+" → "New repository"
3. Nom: jeu-memoire (ou autre)
4. Description: Jeu de mémoire en Python avec Kivy pour mobile/desktop
5. Public ou Private (votre choix)
6. NE PAS créer README/license (on en a déjà)
7. Cliquer "Create repository"

Ensuite, dans le terminal:
"""

import subprocess
import sys

def upload_github():
    """Assistant pour uploader sur GitHub"""
    
    print("=" * 60)
    print("📤 GUIDE GITHUB UPLOAD")
    print("=" * 60)
    
    print("\n1️⃣  d'abord, créez votre dépôt sur GitHub:")
    print("   • Allez sur: https://github.com/new")
    print("   • Nom: jeu-memoire")
    print("   • Description: Jeu de mémoire Python + Kivy")
    print("   • Public ✓")
    print("   • Ne créez PAS de README")
    print("   • Cliquez 'Create repository'")
    
    print("\n2️⃣  Ensuite, copier les commandes ci-dessous:\n")
    
    # Demander l'URL du repo
    repo_url = input("Entrez l'URL de votre repo GitHub (ex: https://github.com/username/jeu-memoire.git):\n> ").strip()
    
    if not repo_url.startswith('https://github.com/'):
        print("❌ URL invalide!")
        return
    
    commands = [
        f"git branch -M main",
        f"git remote add origin {repo_url}",
        f"git push -u origin main"
    ]
    
    print("\n📋 Commandes à exécuter:\n")
    for cmd in commands:
        print(f"   $ {cmd}")
    
    print("\n" + "=" * 60)
    print("✅ Puis votre code sera sur GitHub!")
    print("=" * 60)
    
    choice = input("\nVoulez vous exécuter ces commandes? (oui/non): ").lower().strip()
    
    if choice in ['oui', 'o', 'yes']:
        try:
            print("\n⏳ Exécution...")
            for cmd in commands:
                print(f"\n$ {cmd}")
                subprocess.run(cmd, shell=True, check=True, cwd=".")
            
            print("\n✅ Upload réussi!")
            print(f"Votre repo: {repo_url}")
            
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Erreur: {e}")
            print("Vérifiez votre connexion et l'URL du repo")
    else:
        print("\n📝 Vous pouvez le faire plus tard en copiant les commandes ci-dessus")

if __name__ == "__main__":
    upload_github()
