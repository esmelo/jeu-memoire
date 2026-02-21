"""Tests for the GameStorage class."""

import pytest
import json
from pathlib import Path
from src.storage import GameStorage
from src.player import Player


@pytest.fixture
def temp_storage(tmp_path):
    """Create a temporary storage instance for testing."""
    storage_path = tmp_path / "test_leaderboard.json"
    return GameStorage(str(storage_path))


class TestGameStorage:
    """Test the GameStorage class."""

    def test_storage_initialization(self, temp_storage):
        """Test that storage initializes correctly."""
        assert temp_storage.storage_path.exists()
        
        data = json.loads(temp_storage.storage_path.read_text())
        assert "games" in data
        assert "leaderboard" in data
        assert data["games"] == []
        assert data["leaderboard"] == []

    def test_save_game(self, temp_storage):
        """Test saving a game."""
        players = [
            Player(name="Alice", score=50, pairs_found=5),
            Player(name="Bob", score=30, pairs_found=3),
        ]
        
        temp_storage.save_game(players, 120.5)
        
        data = json.loads(temp_storage.storage_path.read_text())
        assert len(data["games"]) == 1
        assert len(data["leaderboard"]) == 2

    def test_leaderboard_sorting(self, temp_storage):
        """Test that leaderboard is sorted by score."""
        players1 = [Player(name="Alice", score=50, pairs_found=5)]
        players2 = [Player(name="Bob", score=100, pairs_found=10)]
        
        temp_storage.save_game(players1, 100)
        temp_storage.save_game(players2, 80)
        
        leaderboard = temp_storage.get_leaderboard()
        assert leaderboard[0]["name"] == "Bob"
        assert leaderboard[1]["name"] == "Alice"

    def test_get_leaderboard_limit(self, temp_storage):
        """Test leaderboard limit."""
        for i in range(15):
            players = [Player(name=f"Player{i}", score=i*10, pairs_found=i)]
            temp_storage.save_game(players, 100)
        
        leaderboard = temp_storage.get_leaderboard(limit=5)
        assert len(leaderboard) == 5

    def test_get_player_stats(self, temp_storage):
        """Test retrieving player statistics."""
        players = [Player(name="Charlie", score=75, pairs_found=7)]
        temp_storage.save_game(players, 100)
        
        stats = temp_storage.get_player_stats("Charlie")
        assert stats["name"] == "Charlie"
        assert stats["total_score"] == 75
        assert stats["games_played"] == 1

    def test_get_nonexistent_player_stats(self, temp_storage):
        """Test getting stats for non-existent player."""
        stats = temp_storage.get_player_stats("NonExistent")
        assert stats == {}

    def test_multiple_games_same_player(self, temp_storage):
        """Test accumulating stats across multiple games."""
        temp_storage.save_game([Player(name="Diana", score=50, pairs_found=5)], 100)
        temp_storage.save_game([Player(name="Diana", score=30, pairs_found=3)], 80)
        
        stats = temp_storage.get_player_stats("Diana")
        assert stats["total_score"] == 80
        assert stats["games_played"] == 2
        assert stats["pairs_total"] == 8

    def test_clear_storage(self, temp_storage):
        """Test clearing storage."""
        players = [Player(name="Eve", score=40, pairs_found=4)]
        temp_storage.save_game(players, 90)
        
        temp_storage.clear_storage()
        
        leaderboard = temp_storage.get_leaderboard()
        assert leaderboard == []
