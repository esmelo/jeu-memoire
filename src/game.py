"""Logique principale du jeu de mémoire."""

import random
from typing import List, Optional
from enum import Enum


class EtatCarte(Enum):
    """État d'une carte dans le jeu."""
    CACHEE = "cachee"
    REVELEE = "revelee"
    TROUVEE = "trouvee"


class Carte:
    """Représente une carte dans le jeu de mémoire."""

    def __init__(self, card_id: int, value: str):
        """Initialise une carte avec un identifiant et une valeur."""
        self.card_id = card_id
        self.value = value
        self.state = EtatCarte.CACHEE

    def reveal(self) -> None:
        """Révèle la carte."""
        self.state = EtatCarte.REVELEE

    def hide(self) -> None:
        """Cache la carte."""
        if self.state != EtatCarte.TROUVEE:
            self.state = EtatCarte.CACHEE

    def match(self) -> None:
        """Marque la carte comme trouvée."""
        self.state = EtatCarte.TROUVEE

    def is_hidden(self) -> bool:
        """Vérifie si la carte est cachée."""
        return self.state == EtatCarte.CACHEE

    def is_revealed(self) -> bool:
        """Vérifie si la carte est révélée."""
        return self.state == EtatCarte.REVELEE

    def is_matched(self) -> bool:
        """Vérifie si la carte est trouvée."""
        return self.state == EtatCarte.TROUVEE

    def __repr__(self) -> str:
        """Représentation textuelle de la carte."""
        if self.state == EtatCarte.CACHEE:
            return "?"
        elif self.state == EtatCarte.TROUVEE:
            return "✓"
        else:
            return self.value


# Alias pour la compatibilité avec le code existant
CardState = EtatCarte
Card = Carte


class Game:
    """Logique principale du jeu de mémoire."""

    # Thèmes de cartes
    THEMES = {
        "animals": ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼",
                    "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐙", "🦋"],
        "fruits": ["🍎", "🍊", "🍋", "🍌", "🍉", "🍓", "🍒", "🍑",
                   "🥝", "🍇", "🍍", "🥭", "🍑", "🫐", "🍈", "🍐"],
        "emojis": ["⭐", "❤️", "💎", "🎨", "🎭", "🎪", "🎯", "🎲",
                   "🌈", "🌟", "💫", "🔥", "🌊", "🍀", "🎵", "🏆"],
    }

    def __init__(self, theme: str = "animals", num_pairs: int = 8):
        """
        Initialise une nouvelle partie.

        Args:
            theme: Thème des cartes (animals, fruits, emojis)
            num_pairs: Nombre de paires (4-16)
        """
        if num_pairs < 4 or num_pairs > 16:
            raise ValueError("Le nombre de paires doit être entre 4 et 16")

        if theme not in self.THEMES:
            raise ValueError(f"Le thème doit être l'un des suivants : {list(self.THEMES.keys())}")

        self.theme = theme
        self.num_pairs = num_pairs
        self.cards: List[Carte] = []
        self.revealed_cards: List[Carte] = []
        self.matched_pairs = 0
        self.total_moves = 0

        self._initialiser_cartes()

    def _initialiser_cartes(self) -> None:
        """Crée et mélange les cartes."""
        symbols = self.THEMES[self.theme][:self.num_pairs]

        # Créer les paires
        self.cards = []
        for i, symbol in enumerate(symbols):
            self.cards.append(Carte(len(self.cards), symbol))
            self.cards.append(Carte(len(self.cards), symbol))

        # Mélanger
        random.shuffle(self.cards)

    def get_card(self, position: int) -> Optional[Carte]:
        """Récupère une carte à une position donnée."""
        if 0 <= position < len(self.cards):
            return self.cards[position]
        return None

    def reveal_card(self, position: int) -> bool:
        """
        Révèle une carte à la position donnée.

        Retourne True si la carte a été révélée, False sinon.
        """
        card = self.get_card(position)

        if card is None:
            return False

        if not card.is_hidden():
            return False

        card.reveal()
        self.revealed_cards.append(card)
        return True

    def check_match(self) -> bool:
        """
        Vérifie si les deux dernières cartes révélées correspondent.

        Retourne True si elles correspondent, False sinon.
        """
        if len(self.revealed_cards) != 2:
            return False

        card1, card2 = self.revealed_cards

        if card1.value == card2.value:
            # Paire trouvée
            card1.match()
            card2.match()
            self.matched_pairs += 1
            self.revealed_cards = []
            return True

        return False

    def hide_revealed_cards(self) -> None:
        """Cache les cartes révélées (appelé quand aucune paire n'est trouvée)."""
        for card in self.revealed_cards:
            card.hide()
        self.revealed_cards = []

    def reset_revealed(self) -> None:
        """Réinitialise la liste des cartes révélées (pour l'interface)."""
        self.revealed_cards = []

    def is_won(self) -> bool:
        """Vérifie si toutes les paires ont été trouvées."""
        return self.matched_pairs == self.num_pairs

    def get_board(self) -> List[Carte]:
        """Récupère l'état actuel du plateau."""
        return self.cards

    def get_stats(self) -> dict:
        """Récupère les statistiques actuelles de la partie."""
        return {
            "total_cards": len(self.cards),
            "pairs_total": self.num_pairs,
            "pairs_matched": self.matched_pairs,
            "moves": self.total_moves,
            "cards_revealed": len(self.revealed_cards),
        }

    def increment_moves(self) -> None:
        """Incrémente le compteur de coups."""
        self.total_moves += 1
