"""Module de stockage pour les scores et statistiques du jeu."""

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from .player import Player


class GameStorage:
    """Gère le chargement et la sauvegarde des statistiques de jeu."""

    def __init__(self, storage_path: str = "data/leaderboard.json"):
        """Initialise le stockage avec un chemin de fichier donné."""
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.storage_path.exists():
            self._initialiser_stockage()

    def _initialiser_stockage(self) -> None:
        """Initialise un fichier de stockage vide."""
        data = {"parties": [], "classement": []}
        self.storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def save_game(self, players: List[Player], game_duration: float) -> None:
        """Sauvegarde les résultats d'une partie."""
        data = self._charger()

        partie = {
            "horodatage": datetime.now().isoformat(),
            "duree_secondes": game_duration,
            "joueurs": [
                {
                    "name": p.name,
                    "score": p.score,
                    "pairs_found": p.pairs_found,
                }
                for p in players
            ],
        }

        # Compatibilité avec les anciennes clés
        if "games" not in data:
            data["games"] = data.get("parties", [])
        if "leaderboard" not in data:
            data["leaderboard"] = data.get("classement", [])

        data["games"].append(partie)
        data["parties"] = data["games"]
        self._mettre_a_jour_classement(data, players)

        self.storage_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))

    def _charger(self) -> Dict[str, Any]:
        """Charge les données depuis le fichier."""
        data = json.loads(self.storage_path.read_text(encoding="utf-8"))
        # Normaliser les clés (compatibilité FR/EN)
        if "leaderboard" not in data:
            data["leaderboard"] = data.get("classement", [])
        if "games" not in data:
            data["games"] = data.get("parties", [])
        return data

    def _mettre_a_jour_classement(self, data: Dict[str, Any], players: List[Player]) -> None:
        """Met à jour le classement avec les joueurs actuels."""
        leaderboard = data.get("leaderboard", data.get("classement", []))

        for player in players:
            existing = next(
                (p for p in leaderboard if p["name"] == player.name), None
            )
            if existing:
                existing["total_score"] += player.score
                existing["games_played"] += 1
                existing["pairs_total"] += player.pairs_found
            else:
                leaderboard.append({
                    "name": player.name,
                    "total_score": player.score,
                    "games_played": 1,
                    "pairs_total": player.pairs_found,
                })

        # Trier par score total décroissant
        data["leaderboard"] = sorted(
            leaderboard, key=lambda x: x["total_score"], reverse=True
        )
        data["classement"] = data["leaderboard"]

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupère les meilleurs joueurs du classement."""
        data = self._charger()
        return data.get("leaderboard", data.get("classement", []))[:limit]

    def get_player_stats(self, player_name: str) -> Dict[str, Any]:
        """Récupère les statistiques d'un joueur spécifique."""
        data = self._charger()

        leaderboard = data.get("leaderboard", data.get("classement", []))
        games = data.get("games", data.get("parties", []))

        player_data = next(
            (p for p in leaderboard if p["name"] == player_name), None
        )

        if not player_data:
            return {}

        player_games = [
            g for g in games
            if any(p["name"] == player_name for p in g["joueurs" if "joueurs" in g else "players"])
        ]

        return {
            **player_data,
            "games_history": len(player_games),
            "recent_games": player_games[-5:],
        }

    def clear_storage(self) -> None:
        """Efface toutes les données stockées (pour les tests)."""
        self._initialiser_stockage()
