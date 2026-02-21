# 🧠 Jeu de Mémoire

Un jeu de mémoire classique développé en Python avec une **interface console** (Rich) et une **version mobile Kivy**. Testez vos capacités de mémorisation en jumelant les cartes!

## 🎯 Fonctionnalités

- ✅ **Mode solo et multijoueur** (1-4 joueurs)
- ✅ **4 niveaux de difficulté**: Easy (4 paires), Medium (8), Hard (12), Expert (16)
- ✅ **3 thèmes visuels**: Animaux 🐶, Fruits 🍎, Symboles ⭐
- ✅ **Système de scoring persistant**: Leaderboard JSON avec stats agrégées
- ✅ **2 versions**: 
  - 🖥️ Console avec interface Rich (Windows/Linux/macOS)
  - 📱 Mobile Kivy (Windows/Linux/macOS/Android)
- ✅ **APK Android officielle** prête à installer
- ✅ **Tests unitaires** (97%+ couverture)
- ✅ **Interface responsive** adaptée à tous les écrans

## ⚡ Démarrage Rapide

### Installation

```bash
# Cloner le repo
git clone https://github.com/USERNAME/jeu-memoire.git
cd jeu-memoire

# Installer les dépendances
pip install -r requirements.txt
```

### Lancer le jeu

**Version Console** (toutes plateformes):
```bash
python main.py
```

**Version Mobile Kivy** (interface graphique):
```bash
cd kivy_app
python main.py
```

### Tests

```bash
# Tous les tests
pytest tests/ -v

# Avec rapport de couverture
pytest tests/ --cov=src --cov-report=html
```

### APK Android

Téléchargez directement l'APK compilée:
```bash
# Depuis: bin/jeumemoire-1.0-release.apk
adb install jeumemoire-1.0-release.apk
```

## 🎮 Comment Jouer

1. **Configuration**: Choisissez nombre de joueurs, difficulté, et thème
2. **Révélez les cartes**: Cliquez sur 2 cartes à chaque tour
3. **Matching**: 
   - ✅ Paire correcte = +10 points + relancer
   - ❌ Mauvaise paire = tour suivant
4. **Objectif**: Trouver toutes les paires
5. **Gagnant**: Premier au leaderboard!

## 📂 Architecture

```
jeu-memoire/
├── src/                       # Version console
│   ├── game.py               # Moteur de jeu (Card, Game)
│   ├── player.py             # Gestion des joueurs
│   ├── storage.py            # Persistance JSON
│   └── ui.py                 # Interface Rich
├── kivy_app/                 # Version mobile/desktop
│   ├── main.py               # Application Kivy
│   ├── memory.kv             # UI en KV Language
│   ├── buildozer.spec        # Config Android
│   └── data/
│       ├── images/           # Logo (512x512) & favicons
│       └── leaderboard.json  # Scores persistants
├── tests/                    # Suite pytest (97%+ couverture)
├── requirements.txt
├── .gitignore
└── README.md
```

## Example Gameplay

## 🎨 Écrans Application

```
MENU                CONFIGURATION       PARTIE               CLASSEMENT
┌────────────┐      ┌────────────────┐   ┌──────────────┐    ┌──────────┐
│ NOUVELLE   │      │ Joueurs      ▼ │   │ 🐶 🍎 ⭐ 🐶 │    │TOP SCORES│
│ CLASSEMENT │──→   │ Difficulté   ▼ │──→│ 🍊   🐱 💫  │    │1. Alice  │
│ À PROPOS   │      │ Thème        ▼ │   │   🐱    🐹  │    │2. Bob    │
│ QUITTER    │      │ LANCER        (●)   │ 🍊 🐹 🍎   │    └──────────┘
└────────────┘      └────────────────┘   └──────────────┘
```

## 📦 Dépendances

**Console**:
- `rich`: Interface terminal
- `pydantic`: Validation données

**Mobile** (kivy_app):
- `kivy==2.3.0`: Framework GUI
- `python3==3.11.0`: Runtime
- `pydantic==2.5.0`: Validation

**Tests**:
- `pytest`: Framework tests
- `pytest-cov`: Coverage reporting

## ✅ Qualité

- ✅ 97%+ couverture de tests (logique de jeu)
- ✅ Type hints complets
- ✅ Zero API externes
- ✅ Architecture clean: UI ↔ Contrôleur ↔ Logique

## 🚀 Améliorations Futures

- Mode campagne solo progressif
- Effets sonores 🎵
- Mode temps limité ⏱️
- Skins additionnels
- Intégration cloud leaderboard

## 🤝 Contribution

Bienvenue! Pour contribuer:
1. Fork le repo
2. Branche: `git checkout -b feature/improvement`
3. Commit: `git commit -m "Add feature"`
4. Push: `git push origin feature/improvement`
5. Pull Request

Domaines à améliorer:
- Nouveaux thèmes emojis
- Défis chronométrés
- Bonnes visuelles (animations)
- Personnalisation des cartes

## 📄 Licence

MIT - Libre d'utilisation à des fins personnelles et éducatives

## 👨‍💼 À Propos du Développeur

**Kouton Vignon**
- 📚 M1 Data Science & AI
- 🏫 Université Félix Houphouët-Boigny (Côte d'Ivoire)
- 📧 esmelyann@gmail.com
- 📱 +225 0505411990
- 🌐 [Portfolio](https://portfolio-kouton.vercel.app/)

---

**Testez votre mémoire maintenant!** 🧠✨
