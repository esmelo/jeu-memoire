"""Point d'entrée principal du Jeu de Mémoire."""

import time
from src.game import Game
from src.player import Player
from src.ui import GameUI
from src.storage import GameStorage


class ControleurJeuMemoire:
    """Contrôleur principal qui orchestre le déroulement du jeu."""

    def __init__(self):
        """Initialise le contrôleur du jeu."""
        self.ui = GameUI()
        self.storage = GameStorage()
        self.players: list[Player] = []
        self.current_game: Game | None = None
        self.current_player_index = 0

    def run(self) -> None:
        """Lance la boucle principale du jeu."""
        self.ui.display_title()

        while True:
            choice = self.ui.display_menu()

            if choice == "1":
                self.demarrer_nouvelle_partie()
            elif choice == "2":
                self.afficher_classement()
            elif choice == "3":
                self.afficher_stats_joueur()
            elif choice == "4":
                self.ui.console.print("[cyan]Merci d'avoir joué ! À bientôt ![/cyan]")
                break

    def demarrer_nouvelle_partie(self) -> None:
        """Démarre une nouvelle session de jeu."""
        self.ui.clear_screen()
        self.ui.display_title()

        # Récupérer les joueurs
        num_players = self.ui.get_number_of_players()
        player_names = self.ui.get_player_names(num_players)
        self.players = [Player(name=name) for name in player_names]

        # Choisir la difficulté
        num_pairs = self.ui.select_difficulty()

        # Créer la partie
        self.current_game = Game(theme="animals", num_pairs=num_pairs)
        self.current_player_index = 0
        game_start_time = time.time()

        # Jouer la partie
        self.jouer_partie()

        # Sauvegarder les résultats
        game_duration = time.time() - game_start_time
        self.storage.save_game(self.players, game_duration)

        # Afficher le gagnant
        self.ui.clear_screen()
        self.ui.display_winner(self.players)

        input("\nAppuyez sur Entrée pour continuer...")

    def jouer_partie(self) -> None:
        """Boucle principale du jeu."""
        while not self.current_game.is_won():
            self.ui.clear_screen()
            self.ui.display_title()
            self.ui.display_board(self.current_game)

            current_player = self.players[self.current_player_index]
            self.ui.display_stats(self.current_game, self.players, self.current_player_index)

            # Le joueur choisit la première carte
            self.ui.console.print(f"\n[bold cyan]Tour de {current_player.name}[/bold cyan]")
            pos1 = self.ui.get_card_selection(self.current_game, "Sélectionnez la première carte")

            if not self.current_game.reveal_card(pos1):
                self.ui.display_error("Cette carte est déjà révélée !")
                self.ui.pause()
                continue

            self.current_game.increment_moves()

            # Afficher le plateau avec la première carte révélée
            self.ui.clear_screen()
            self.ui.display_title()
            self.ui.display_board(self.current_game)
            self.ui.display_stats(self.current_game, self.players, self.current_player_index)

            # Le joueur choisit la deuxième carte
            pos2 = self.ui.get_card_selection(self.current_game, "Sélectionnez la deuxième carte")

            if pos1 == pos2:
                self.ui.display_error("Veuillez sélectionner une carte différente !")
                self.current_game.reset_revealed()
                self.ui.pause()
                continue

            if not self.current_game.reveal_card(pos2):
                self.ui.display_error("Cette carte est déjà révélée !")
                self.current_game.reset_revealed()
                self.ui.pause()
                continue

            # Afficher les deux cartes
            self.ui.clear_screen()
            self.ui.display_title()
            self.ui.display_board(self.current_game)

            # Vérifier la correspondance
            card1 = self.current_game.cards[pos1]
            card2 = self.current_game.cards[pos2]

            matched = self.current_game.check_match()
            self.ui.display_match_result(matched, card1.value, card2.value)

            if matched:
                # Attribuer les points au joueur actuel
                current_player.add_score(10)
                current_player.increment_pairs()
                self.ui.console.print(f"[green]+10 points pour {current_player.name} ![/green]")
                self.ui.pause()
            else:
                # Cacher les cartes et passer au joueur suivant
                self.current_game.hide_revealed_cards()
                self.current_player_index = (self.current_player_index + 1) % len(self.players)
                self.ui.pause(1)

    def afficher_classement(self) -> None:
        """Affiche le classement."""
        self.ui.clear_screen()
        self.ui.display_title()
        leaderboard = self.storage.get_leaderboard()
        self.ui.display_leaderboard(leaderboard)
        input("\nAppuyez sur Entrée pour continuer...")

    def afficher_stats_joueur(self) -> None:
        """Affiche les statistiques d'un joueur spécifique."""
        self.ui.clear_screen()
        self.ui.display_title()
        player_name = self.ui.console.input("[cyan]Entrez le nom du joueur : [/cyan]")
        stats = self.storage.get_player_stats(player_name)
        self.ui.display_player_stats(stats)
        input("\nAppuyez sur Entrée pour continuer...")


def main() -> None:
    """Point d'entrée principal."""
    controller = ControleurJeuMemoire()
    controller.run()


if __name__ == "__main__":
    main()
