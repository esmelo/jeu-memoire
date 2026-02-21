"""Interface console du jeu de mémoire utilisant la bibliothèque Rich."""

import time
from typing import List, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from .game import Game
from .player import Player


class GameUI:
    """Gère toutes les interactions avec l'utilisateur."""

    def __init__(self):
        """Initialise l'interface."""
        self.console = Console()

    def display_title(self) -> None:
        """Affiche le titre du jeu."""
        title = Text("JEU DE MÉMOIRE", style="bold cyan", justify="center")
        self.console.print(Panel(title, expand=False))

    def display_menu(self) -> str:
        """Affiche le menu principal et récupère le choix de l'utilisateur."""
        self.console.print("\n[bold yellow]Menu Principal[/bold yellow]")
        self.console.print("1. Nouvelle Partie")
        self.console.print("2. Classement")
        self.console.print("3. Statistiques du Joueur")
        self.console.print("4. Quitter")

        choice = Prompt.ask("Choisissez une option", choices=["1", "2", "3", "4"])
        return choice

    def get_number_of_players(self) -> int:
        """Récupère le nombre de joueurs."""
        num = IntPrompt.ask("Combien de joueurs ?", default=1)
        if num < 1 or num > 4:
            self.console.print("[red]Veuillez entrer un nombre entre 1 et 4[/red]")
            return self.get_number_of_players()
        return num

    def get_player_names(self, num_players: int) -> List[str]:
        """Récupère les noms de tous les joueurs."""
        names = []
        for i in range(num_players):
            name = Prompt.ask(f"Entrez le nom du Joueur {i+1}")
            names.append(name)
        return names

    def select_difficulty(self) -> int:
        """Permet au joueur de choisir la difficulté (nombre de paires)."""
        self.console.print("\n[bold yellow]Choisissez la Difficulté[/bold yellow]")
        self.console.print("1. Facile (4 paires)")
        self.console.print("2. Moyen (8 paires)")
        self.console.print("3. Difficile (12 paires)")
        self.console.print("4. Expert (16 paires)")

        choice = Prompt.ask("Choisissez la difficulté", choices=["1", "2", "3", "4"])
        difficulty_map = {"1": 4, "2": 8, "3": 12, "4": 16}
        return difficulty_map[choice]

    def display_board(self, game: Game) -> None:
        """Affiche le plateau de jeu."""
        cards = game.get_board()
        num_cards = len(cards)

        # Crée un tableau avec les cartes disposées en lignes
        table = Table.grid(padding=1)

        for i in range(0, num_cards, 4):
            row_cards = cards[i:i+4]
            row_positions = list(range(i, min(i+4, num_cards)))

            row_text = []
            for pos, card in zip(row_positions, row_cards):
                if card.is_matched():
                    card_display = f"[green]{card}[/green]"
                elif card.is_revealed():
                    card_display = f"[bold yellow]{card}[/bold yellow]"
                else:
                    card_display = f"[cyan]{pos}[/cyan]"

                row_text.append(f"[{card_display}]")

            table.add_row(*row_text)

        self.console.print(Panel(table, title="[bold]Plateau de Jeu[/bold]"))

    def display_stats(self, game: Game, players: List[Player], current_player: int) -> None:
        """Affiche les statistiques actuelles de la partie."""
        stats = game.get_stats()

        # Infos joueur
        player_text = f"\n[bold cyan]Joueur Actuel : {players[current_player].name}[/bold cyan]\n"

        # Tableau des scores
        table = Table(title="Scores des Joueurs", show_header=True, header_style="bold magenta")
        table.add_column("Joueur", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Paires Trouvées", style="yellow")

        for player in players:
            table.add_row(player.name, str(player.score), str(player.pairs_found))

        self.console.print(player_text)
        self.console.print(table)

        # Progression de la partie
        progress_text = (
            f"\nPaires : {stats['pairs_matched']}/{stats['pairs_total']} | "
            f"Coups : {stats['moves']} | "
            f"Révélées : {stats['cards_revealed']}"
        )
        self.console.print(f"[bold blue]{progress_text}[/bold blue]")

    def get_card_selection(self, game: Game, prompt_text: str = "Sélectionnez une carte (position)") -> int:
        """Récupère la sélection de carte du joueur."""
        num_cards = len(game.get_board())

        while True:
            try:
                position = IntPrompt.ask(prompt_text)
                if 0 <= position < num_cards:
                    return position
                else:
                    self.console.print(f"[red]Veuillez entrer un nombre entre 0 et {num_cards-1}[/red]")
            except ValueError:
                self.console.print("[red]Veuillez entrer un nombre valide[/red]")

    def display_match_result(self, matched: bool, card1_value: str, card2_value: str) -> None:
        """Affiche le résultat d'une tentative de correspondance."""
        if matched:
            self.console.print(f"[green bold]✓ Paire trouvée ! {card1_value} = {card2_value}[/green bold]")
        else:
            self.console.print(f"[red]✗ Pas de paire ! {card1_value} ≠ {card2_value}[/red]")
        time.sleep(1.5)

    def display_winner(self, players: List[Player]) -> None:
        """Affiche l'annonce du gagnant."""
        # Trouver le gagnant (score le plus élevé)
        winner = max(players, key=lambda p: p.score)

        message = f"\n🎉 [bold green]PARTIE TERMINÉE ![/bold green] 🎉\n\n[bold cyan]{winner.name} gagne ![/bold cyan]"
        self.console.print(Panel(message, expand=False))

        # Scores finaux
        table = Table(title="Scores Finaux", show_header=True, header_style="bold magenta")
        table.add_column("Joueur", style="cyan")
        table.add_column("Score", style="green")
        table.add_column("Paires Trouvées", style="yellow")

        for player in sorted(players, key=lambda p: p.score, reverse=True):
            table.add_row(player.name, str(player.score), str(player.pairs_found))

        self.console.print(table)

    def display_leaderboard(self, leaderboard: List[dict]) -> None:
        """Affiche le classement."""
        if not leaderboard:
            self.console.print("[yellow]Aucune partie jouée ! Commencez une partie pour apparaître au classement.[/yellow]")
            return

        table = Table(title="🏆 Classement 🏆", show_header=True, header_style="bold magenta")
        table.add_column("Rang", style="cyan")
        table.add_column("Joueur", style="bold")
        table.add_column("Score Total", style="green")
        table.add_column("Parties Jouées", style="yellow")
        table.add_column("Paires Totales", style="blue")

        for i, entry in enumerate(leaderboard, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            table.add_row(
                medal,
                entry["name"],
                str(entry["total_score"]),
                str(entry["games_played"]),
                str(entry["pairs_total"]),
            )

        self.console.print(table)

    def display_player_stats(self, stats: dict) -> None:
        """Affiche les statistiques d'un joueur spécifique."""
        if not stats:
            self.console.print("[red]Joueur introuvable ![/red]")
            return

        message = (
            f"\n[bold cyan]{stats['name']}[/bold cyan]\n"
            f"Score Total : [green]{stats['total_score']}[/green]\n"
            f"Parties Jouées : [yellow]{stats['games_played']}[/yellow]\n"
            f"Paires Trouvées (total) : [blue]{stats['pairs_total']}[/blue]"
        )
        self.console.print(Panel(message))

    def clear_screen(self) -> None:
        """Efface l'écran de la console."""
        self.console.clear()

    def pause(self, seconds: float = 2) -> None:
        """Pause l'exécution pendant un certain temps."""
        time.sleep(seconds)

    def display_error(self, message: str) -> None:
        """Affiche un message d'erreur."""
        self.console.print(f"[red bold]Erreur : {message}[/red bold]")

    def display_info(self, message: str) -> None:
        """Affiche un message d'information."""
        self.console.print(f"[cyan]{message}[/cyan]")
