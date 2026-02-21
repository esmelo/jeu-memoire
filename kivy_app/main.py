"""
Point d'entrée principal de l'application Jeu de Mémoire (Kivy - Android).
"""
import os
import json
import random
import time
from pathlib import Path
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty, ListProperty
)
from kivy.core.text import LabelBase
from kivy.uix.widget import Widget

# Charger le fichier KV
Builder.load_file(os.path.join(os.path.dirname(__file__), 'memory.kv'))

# ─── Configuration de la police pour le support des emojis ────────────────────
try:
    # Essayer d'enregistrer une police système qui supporte les emojis
    LabelBase.register(
        name='EmojiFont',
        fn_regular='C:\\Windows\\Fonts\\seguiemj.ttf'  # Segoe UI Emoji (Windows)
    )
except Exception as e:
    print(f"[WARN] Police Segoe UI Emoji non trouvee: {e}")
    try:
        # Fallback: Arial Unicode MS
        LabelBase.register(
            name='EmojiFont',
            fn_regular='C:\\Windows\\Fonts\\arial.ttf'
        )
    except:
        print("[WARN] Impossible de configurer une police emoji. Utilisation de symboles alternatifs.")

# ─── Couleurs ───────────────────────────────────────────────────────────────
COULEUR_FOND        = get_color_from_hex("#0D0D1A")
COULEUR_PRIMAIRE    = get_color_from_hex("#6C63FF")
COULEUR_SECONDAIRE  = get_color_from_hex("#FF6584")
COULEUR_SUCCES      = get_color_from_hex("#43E97B")
COULEUR_CARTE_DOS   = get_color_from_hex("#1E1E3F")
COULEUR_TEXTE       = get_color_from_hex("#EAEAEA")

# ─── Palette de couleurs pour les cartes ─────────────────────────────────────
COULEURS_BASE = [
    [0.96, 0.26, 0.21, 1],  # Rouge
    [0.91, 0.46, 0.13, 1],  # Orange
    [0.95, 0.76, 0.05, 1],  # Jaune
    [0.25, 0.70, 0.30, 1],  # Vert
    [0.13, 0.59, 0.95, 1],  # Bleu vif
    [0.55, 0.15, 0.75, 1],  # Violet
    [0.00, 0.74, 0.83, 1],  # Cyan
    [0.95, 0.14, 0.57, 1],  # Rose
    [0.40, 0.73, 0.42, 1],  # Vert menthe
    [0.07, 0.27, 0.70, 1],  # Bleu marine
    [0.74, 0.02, 0.18, 1],  # Bordeaux
    [0.13, 0.70, 0.67, 1],  # Turquoise
    [0.62, 0.32, 0.18, 1],  # Marron
    [0.38, 0.49, 0.55, 1],  # Gris bleu
    [0.85, 0.40, 0.00, 1],  # Orange brule
    [0.48, 0.11, 0.61, 1],  # Violet fonce
]

# ─── Thèmes avec vrais emojis par catégorie ────────────────────────────────
THEMES = {
    "animaux": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐔"],
    "fruits":  ["🍎", "🍊", "🍋", "🍌", "🍉", "🍓", "🍒", "🍑", "🥝", "🍍", "🥭", "🍅", "🥥", "🍆", "🌶", "🍄"],
    "symboles": ["⭐", "💫", "✨", "🌟", "💥", "🔥", "💎", "🎨", "🎭", "🎪", "🎯", "🎲", "🎮", "🎸", "🎹", "🎺"],
}

DIFFICULTE = {
    "Facile":    4,
    "Moyen":     8,
    "Difficile": 12,
    "Expert":    16,
}


class EtatCarte:
    CACHEE  = "cachee"
    REVELEE = "revelee"
    TROUVEE = "trouvee"


class CarteLogique:
    def __init__(self, cid, valeur):
        self.cid    = cid
        self.valeur = valeur
        self.etat   = EtatCarte.CACHEE

    @property
    def cachee(self):  return self.etat == EtatCarte.CACHEE
    @property
    def revelee(self): return self.etat == EtatCarte.REVELEE
    @property
    def trouvee(self): return self.etat == EtatCarte.TROUVEE

    def reveler(self):
        if self.cachee: self.etat = EtatCarte.REVELEE
    def cacher(self):
        if not self.trouvee: self.etat = EtatCarte.CACHEE
    def trouver(self):
        self.etat = EtatCarte.TROUVEE


class PartieLogique:
    def __init__(self, theme="animaux", nb_paires=8):
        self.nb_paires      = nb_paires
        self.paires_trouvees = 0
        self.nb_coups       = 0
        symboles = THEMES[theme][:nb_paires]
        cartes = []
        for s in symboles:
            cartes.append(CarteLogique(len(cartes), s))
            cartes.append(CarteLogique(len(cartes), s))
        random.shuffle(cartes)
        self.cartes          = cartes
        self.cartes_revelees: list[CarteLogique] = []

    def reveler(self, idx) -> bool:
        c = self.cartes[idx]
        if not c.cachee: return False
        c.reveler()
        self.cartes_revelees.append(c)
        return True

    def verifier_correspondance(self) -> bool:
        if len(self.cartes_revelees) != 2: return False
        c1, c2 = self.cartes_revelees
        if c1.valeur == c2.valeur:
            c1.trouver(); c2.trouver()
            self.paires_trouvees += 1
            self.cartes_revelees = []
            return True
        return False

    def cacher_revelees(self):
        for c in self.cartes_revelees: c.cacher()
        self.cartes_revelees = []

    @property
    def gagnee(self): return self.paires_trouvees == self.nb_paires


# ─── Stockage ────────────────────────────────────────────────────────────────
def chemin_stockage():
    from kivy.utils import platform
    if platform == 'android':
        from android.storage import app_storage_path  # noqa
        return os.path.join(app_storage_path(), "scores.json")
    return os.path.join(os.path.dirname(__file__), "scores.json")

def charger_scores():
    p = chemin_stockage()
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {"classement": []}

def sauvegarder_score(nom, score, paires):
    data = charger_scores()
    lb   = data.get("classement", [])
    ex   = next((x for x in lb if x["nom"] == nom), None)
    if ex:
        ex["score_total"]    += score
        ex["parties"]        += 1
        ex["paires_totales"] += paires
    else:
        lb.append({"nom": nom, "score_total": score, "parties": 1, "paires_totales": paires})
    data["classement"] = sorted(lb, key=lambda x: x["score_total"], reverse=True)
    with open(chemin_stockage(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ─── Widgets ─────────────────────────────────────────────────────────────────
class CarteWidget(Button):
    """Bouton représentant une carte du jeu avec couleur unique."""
    symbole        = StringProperty("?")
    est_dos        = BooleanProperty(True)
    est_match      = BooleanProperty(False)
    couleur_carte  = ListProperty([0.12, 0.12, 0.25, 1])

    def __init__(self, index, symbole, couleur, callback, **kw):
        super().__init__(**kw)
        self.index         = index
        self.symbole       = symbole
        self.couleur_carte = couleur
        self.callback      = callback
        self.text          = "?"
        self.bold          = True
        self.font_name     = 'EmojiFont'  # Utiliser la police emoji
        self._update_style()

    def _update_style(self):
        if self.est_match:
            self.background_color = list(COULEUR_SUCCES)
            self.color            = [0.05, 0.05, 0.05, 1]
            self.text             = self.symbole
        elif self.est_dos:
            self.background_color = list(COULEUR_CARTE_DOS)
            self.color            = [0.5, 0.5, 0.8, 1]
            self.text             = "?"
        else:
            self.background_color = self.couleur_carte
            self.color            = [1, 1, 1, 1]
            self.text             = self.symbole

    def reveler(self):
        self.est_dos = False
        self._update_style()
        anim = Animation(font_size=self.font_size * 1.2, duration=0.08) + \
               Animation(font_size=self.font_size,       duration=0.08)
        anim.start(self)

    def cacher(self):
        self.est_dos = True
        self._update_style()

    def marquer_trouve(self):
        self.est_match = True
        self.est_dos   = False
        self.disabled  = True
        self._update_style()
        anim = Animation(font_size=self.font_size * 1.3, duration=0.1) + \
               Animation(font_size=self.font_size,       duration=0.1)
        anim.start(self)

    def on_press(self):
        if not self.disabled and self.est_dos:
            self.callback(self.index)


# ─── Écrans ──────────────────────────────────────────────────────────────────
class EcranMenu(Screen):
    pass


class EcranParametres(Screen):
    theme_choisi      = StringProperty("animaux")
    diff_choisie      = StringProperty("Moyen")
    noms_joueurs      = ListProperty(["Joueur 1"])
    nb_joueurs        = NumericProperty(1)

    def on_enter(self):
        self._refresh_joueurs()

    def set_theme(self, theme):
        self.theme_choisi = theme

    def set_diff(self, diff):
        self.diff_choisie = diff

    def set_nb_joueurs(self, n):
        self.nb_joueurs = int(n)
        self.noms_joueurs = [f"Joueur {i+1}" for i in range(int(n))]
        self._refresh_joueurs()

    def _refresh_joueurs(self):
        conteneur = self.ids.get("conteneur_joueurs")
        if not conteneur: return
        conteneur.clear_widgets()
        from kivy.uix.textinput import TextInput
        for i in range(self.nb_joueurs):
            ti = TextInput(
                hint_text=f"Nom du Joueur {i+1}",
                text=self.noms_joueurs[i] if i < len(self.noms_joueurs) else f"Joueur {i+1}",
                multiline=False,
                size_hint_y=None,
                height=dp(48),
                font_size=dp(16),
                background_color=[0.12, 0.12, 0.25, 1],
                foreground_color=[1, 1, 1, 1],
                cursor_color=list(COULEUR_PRIMAIRE),
                padding=[dp(12), dp(12)],
            )
            ti.bind(text=lambda inst, val, idx=i: self._update_nom(idx, val))
            conteneur.add_widget(ti)

    def _update_nom(self, idx, val):
        noms = list(self.noms_joueurs)
        while len(noms) <= idx: noms.append(f"Joueur {idx+1}")
        noms[idx] = val
        self.noms_joueurs = noms

    def lancer(self):
        gs = self.manager.get_screen("jeu")
        gs.demarrer(
            theme=self.theme_choisi,
            diff=self.diff_choisie,
            noms=[n if n.strip() else f"Joueur {i+1}"
                  for i, n in enumerate(self.noms_joueurs[:self.nb_joueurs])],
        )
        self.manager.current = "jeu"


class EcranJeu(Screen):
    score_texte    = StringProperty("Score : 0")
    info_texte     = StringProperty("Choisissez une carte")
    joueur_texte   = StringProperty("Tour de : Joueur 1")
    paires_texte   = StringProperty("Paires : 0/0")
    coups_texte    = StringProperty("Coups : 0")

    def __init__(self, **kw):
        super().__init__(**kw)
        self.partie          = None
        self.joueurs_noms    = []
        self.scores          = []
        self.paires_j        = []
        self.idx_joueur      = 0
        self.premiere_carte  = None
        self.en_attente      = False
        self._widgets_cartes = []
        self._debut          = 0
        self._partie_info    = None

    def on_enter(self):
        """Appelé quand l'écran devient actif. On construit le plateau ici."""
        if self._partie_info:
            try:
                self._construire_plateau()
                self._maj_hud()
            except Exception as e:
                print(f"[ERROR] Erreur lors de la construction du plateau: {e}")
                import traceback
                traceback.print_exc()
                self.info_texte = f"ERREUR: {str(e)}"

    def demarrer(self, theme, diff, noms):
        """Prépare le jeu sans construire immédiatement le plateau."""
        self.partie       = PartieLogique(theme=theme, nb_paires=DIFFICULTE[diff])
        self.joueurs_noms = noms
        self.scores       = [0] * len(noms)
        self.paires_j     = [0] * len(noms)
        self.idx_joueur   = 0
        self.premiere_carte = None
        self.en_attente   = False
        self._debut       = time.time()
        self._partie_info = (theme, diff, noms)  # Sauvegarde pour on_enter()

    def _construire_plateau(self):
        from kivy.core.window import Window
        
        # Vérification que l'écran est complètement chargé
        if not hasattr(self, 'ids') or 'grille_cartes' not in self.ids:
            print("[WARN] Les IDs n'etaient pas encore disponibles. Nouvelle tentative...")
            Clock.schedule_once(lambda dt: self._construire_plateau(), 0.1)
            return
        
        grille = self.ids.grille_cartes
        grille.clear_widgets()
        self._widgets_cartes = []
        
        # Créer une correspondance symbole unique -> couleur
        symboles_uniques = list(dict.fromkeys(c.valeur for c in self.partie.cartes))
        couleurs_map = {
            s: COULEURS_BASE[i % len(COULEURS_BASE)]
            for i, s in enumerate(symboles_uniques)
        }
        
        nb   = len(self.partie.cartes)
        cols = 4 if nb <= 16 else 6
        rows = (nb + cols - 1) // cols
        grille.cols = cols

        # Calculer la taille de chaque carte pour remplir l'écran
        esp     = dp(6)
        pad     = dp(4)
        w_disp  = Window.width  - pad * 2 - esp * (cols - 1)
        h_disp  = Window.height - dp(90) - dp(44) - dp(20) - pad * 2 - esp * (rows - 1)
        taille  = max(dp(48), min(w_disp / cols, h_disp / rows))

        grille.col_default_width   = taille
        grille.row_default_height  = taille
        grille.size_hint_min_x     = taille * cols + esp * (cols - 1)

        for i, c in enumerate(self.partie.cartes):
            couleur = couleurs_map.get(c.valeur, [0.5, 0.5, 0.5, 1])
            # Calculer la taille de police (70% de la taille de la carte)
            font_size_emoji = max(dp(32), taille * 0.7)
            w = CarteWidget(
                index=i, 
                symbole=c.valeur, 
                couleur=couleur,
                callback=self._clic_carte,
                size_hint=(None, None),
                size=(taille, taille),
                font_size=font_size_emoji,
            )
            grille.add_widget(w)
            self._widgets_cartes.append(w)

    def _clic_carte(self, idx):
        if self.en_attente: return
        carte_l = self.partie.cartes[idx]
        carte_w = self._widgets_cartes[idx]

        if not carte_l.cachee: return

        # Révéler
        self.partie.reveler(idx)
        carte_w.reveler()

        if self.premiere_carte is None:
            self.premiere_carte = idx
            self.info_texte = "Choisissez la deuxième carte…"
        else:
            if idx == self.premiere_carte: return
            self.partie.nb_coups += 1
            matched = self.partie.verifier_correspondance()

            if matched:
                self._widgets_cartes[self.premiere_carte].marquer_trouve()
                carte_w.marquer_trouve()
                self.scores[self.idx_joueur]  += 10
                self.paires_j[self.idx_joueur] += 1
                self.info_texte = f"[OK] Paire trouvee ! +10 pts pour {self.joueurs_noms[self.idx_joueur]}"
                self.premiere_carte = None
                self._maj_hud()
                if self.partie.gagnee:
                    Clock.schedule_once(lambda dt: self._fin_partie(), 0.8)
            else:
                self.en_attente = True
                self.info_texte = "[X] Pas de paire..."
                Clock.schedule_once(lambda dt: self._cacher_cartes(self.premiere_carte, idx), 1.2)

    def _cacher_cartes(self, i1, i2):
        self.partie.cacher_revelees()
        self._widgets_cartes[i1].cacher()
        self._widgets_cartes[i2].cacher()
        self.premiere_carte = None
        self.en_attente     = False
        # Passer au joueur suivant
        self.idx_joueur = (self.idx_joueur + 1) % len(self.joueurs_noms)
        self._maj_hud()

    def _maj_hud(self):
        j   = self.joueurs_noms[self.idx_joueur]
        sc  = self.scores[self.idx_joueur]
        self.joueur_texte = f"Tour de : {j}"
        self.score_texte  = f"Score : {sc}"
        self.paires_texte = f"Paires : {self.partie.paires_trouvees}/{self.partie.nb_paires}"
        self.coups_texte  = f"Coups : {self.partie.nb_coups}"

    def _fin_partie(self):
        # Sauvegarder les scores
        for nom, sc, pa in zip(self.joueurs_noms, self.scores, self.paires_j):
            sauvegarder_score(nom, sc, pa)

        # Trouver gagnant
        idx_max  = self.scores.index(max(self.scores))
        gagnant  = self.joueurs_noms[idx_max]
        sc_max   = self.scores[idx_max]
        duree    = int(time.time() - self._debut)
        m, s     = divmod(duree, 60)

        lignes = "\n".join(
            f"  {n} : {sc} pts ({pa} paires)"
            for n, sc, pa in zip(self.joueurs_noms, self.scores, self.paires_j)
        )
        msg = f"[VICTOIRE] Partie terminee !\n\nVainqueur : {gagnant} ({sc_max} pts)\nDuree : {m}m {s}s\n\n{lignes}"

        layout = BoxLayout(orientation="vertical", padding=dp(24), spacing=dp(16))
        lbl    = Label(text=msg, font_size=dp(16), color=[1, 1, 1, 1], halign="center")
        lbl.bind(size=lbl.setter("text_size"))

        btn_rejouer = Button(
            text="(>) Rejouer",
            size_hint_y=None, height=dp(50),
            background_color=list(COULEUR_PRIMAIRE),
            font_size=dp(16),
        )
        btn_menu = Button(
            text="[>] Menu Principal",
            size_hint_y=None, height=dp(50),
            background_color=[0.3, 0.3, 0.5, 1],
            font_size=dp(16),
        )

        layout.add_widget(lbl)
        layout.add_widget(btn_rejouer)
        layout.add_widget(btn_menu)

        popup = Popup(
            title=" ",
            content=layout,
            size_hint=(0.88, 0.72),
            background="",
            background_color=[0.08, 0.08, 0.18, 0.97],
            separator_color=[0, 0, 0, 0],
        )

        def rejouer(dt_or_btn):
            popup.dismiss()
            ecran_params = self.manager.get_screen("parametres")
            ecran_params.lancer()

        def menu(dt_or_btn):
            popup.dismiss()
            self.manager.current = "menu"

        btn_rejouer.bind(on_press=rejouer)
        btn_menu.bind(on_press=menu)
        popup.open()


class EcranClassement(Screen):
    def on_enter(self):
        self._charger()

    def _charger(self):
        conteneur = self.ids.get("liste_classement")
        if not conteneur: return
        conteneur.clear_widgets()
        data = charger_scores()
        lb   = data.get("classement", [])

        medailles = ["🥇", "🥈", "🥉"]

        if not lb:
            conteneur.add_widget(Label(
                text="Aucune partie jouée !\nLancez une partie pour apparaître ici.",
                font_size=dp(16), color=[0.7, 0.7, 1, 1], halign="center",
            ))
            return

        for i, entry in enumerate(lb[:10]):
            med = medailles[i] if i < 3 else f"{i+1}."
            txt = (f"{med}  {entry['nom']}\n"
                   f"     Score : {entry['score_total']} pts  |  "
                   f"Parties : {entry['parties']}  |  "
                   f"Paires : {entry['paires_totales']}")
            lbl = Label(
                text=txt, font_size=dp(14),
                color=[1, 1, 1, 1], halign="left", valign="middle",
                size_hint_y=None, height=dp(64),
            )
            lbl.bind(size=lbl.setter("text_size"))
            conteneur.add_widget(lbl)


class EcranAPropos(Screen):
    """Écran À propos avec infos du développeur."""
    def on_enter(self):
        self._charger()

    def _charger(self):
        conteneur = self.ids.get("contenu_apropos")
        if not conteneur: return
        conteneur.clear_widgets()

        from kivy.uix.scrollview import ScrollView
        
        # Contenu principal
        infos_text = """Jeu de Mémoire - v1.0

DÉVELOPPEUR
Kouton Vignon
Étudiant en M1 Data Science et IA
Université Félix Houphouët-Boigny

À PROPOS DU JEU
Retrouvez toutes les paires dans cette version 
colorée et amusante du jeu classique de mémoire.
Testez votre concentration avec des thèmes variés !

AGE RECOMMANDÉ
3-99 ans | Tous publics

CONTACT & PORTFOLIO
Tel: +225 0505411990
Email: esmelyann@gmail.com
Portfolio: https://portfolio-kouton.vercel.app/

N'hésitez pas à nous envoyer vos suggestions 
ou corrections pour améliorer le jeu !"""

        lbl = Label(
            text=infos_text,
            font_size=dp(14),
            color=[1, 1, 1, 1],
            valign="top",
            halign="left",
            text_size=(self.width * 0.9, None),
            size_hint_y=None,
            markup=True,
        )
        lbl.bind(texture_size=lbl.setter('size'))
        conteneur.add_widget(lbl)


# ─── Application ─────────────────────────────────────────────────────────────
class JeuMemoireApp(App):
    def build(self):
        Window.clearcolor = (0.05, 0.05, 0.10, 1)
        sm = ScreenManager(transition=FadeTransition(duration=0.3))
        sm.add_widget(EcranMenu(name="menu"))
        sm.add_widget(EcranParametres(name="parametres"))
        sm.add_widget(EcranJeu(name="jeu"))
        sm.add_widget(EcranClassement(name="classement"))
        sm.add_widget(EcranAPropos(name="apropos"))
        return sm

    def get_application_name(self):
        return "Jeu de Mémoire"


if __name__ == "__main__":
    JeuMemoireApp().run()
