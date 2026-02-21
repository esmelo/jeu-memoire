# 📱 Guide de Compilation APK — Jeu de Mémoire

## Structure du projet Kivy

```
kivy_app/
├── main.py          ← Logique Python + Kivy
├── memory.kv        ← Design graphique (KV Language)
├── requirements.txt ← Dépendances
├── buildozer.spec   ← Config de compilation APK
└── scores.json      ← Généré automatiquement (scores)
```

---

## 🖥️ Tester sur Windows (Aperçu Bureau)

```powershell
cd c:\Users\ACER\Desktop\Claude\kivy_app
pip install kivy==2.3.0
python main.py
```

---

## 📦 Compiler l'APK (via WSL/Ubuntu)

> [!IMPORTANT]
> Buildozer **nécessite Linux**. Sur Windows, utiliser **WSL 2** (Ubuntu).

### 1. Installer WSL 2

```powershell
# Dans PowerShell (admin)
wsl --install
# Redémarrer, puis ouvrir Ubuntu depuis le menu démarrer
```

### 2. Préparer l'environnement Linux

```bash
sudo apt update && sudo apt install -y \
    python3-pip git zip unzip openjdk-17-jdk \
    autoconf automake libtool pkg-config \
    zlib1g-dev libncurses5-dev libffi-dev libssl-dev

pip3 install buildozer cython
```

### 3. Accéder au projet depuis WSL

```bash
# Votre disque C est accessible sous /mnt/c dans WSL
cd /mnt/c/Users/ACER/Desktop/Claude/kivy_app
```

### 4. Compiler l'APK

```bash
buildozer android debug
```

⏳ La première compilation prend **15–30 minutes** (téléchargement du NDK/SDK Android).

### 5. Récupérer l'APK

```
kivy_app/bin/jeumemoire-1.0-arm64-v8a-debug.apk
```

Transférez ce fichier sur votre téléphone Android et installez-le.

> [!NOTE]
> Sur Android, activez **Sources inconnues** dans Paramètres → Sécurité avant d'installer l'APK.

---

## 🐳 Alternative : Docker (sans WSL)

```bash
docker run --rm -v ${PWD}:/home/user/hostcwd \
    kivy/buildozer android debug
```

---

## ✅ Fonctionnalités de l'App

| Fonctionnalité | Console (FR) | App Kivy |
|---|---|---|
| Jeu de mémoire | ✅ | ✅ |
| Multi-joueurs (1–4) | ✅ | ✅ |
| Thèmes (animaux/fruits/symboles) | ✅ | ✅ |
| Niveaux de difficulté | ✅ | ✅ |
| Classement persistant | ✅ | ✅ |
| Interface graphique | ❌ | ✅ |
| Animations de cartes | ❌ | ✅ |
| Compatible Android | ❌ | ✅ |
