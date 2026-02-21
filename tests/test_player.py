"""Tests for the Player class."""

import pytest
from src.player import Player


class TestPlayer:
    """Test the Player class."""

    def test_player_creation(self):
        """Test creating a player."""
        player = Player(name="Alice")
        assert player.name == "Alice"
        assert player.score == 0
        assert player.pairs_found == 0

    def test_add_score(self):
        """Test adding points to a player's score."""
        player = Player(name="Bob")
        player.add_score(10)
        assert player.score == 10
        
        player.add_score(5)
        assert player.score == 15

    def test_add_score_negative(self):
        """Test that negative points are rejected."""
        player = Player(name="Charlie")
        with pytest.raises(ValueError):
            player.add_score(-5)

    def test_increment_pairs(self):
        """Test incrementing pairs found."""
        player = Player(name="Diana")
        player.increment_pairs()
        assert player.pairs_found == 1
        
        player.increment_pairs()
        assert player.pairs_found == 2

    def test_reset(self):
        """Test resetting player stats."""
        player = Player(name="Eve", score=50, pairs_found=5)
        player.reset()
        assert player.score == 0
        assert player.pairs_found == 0
        assert player.turn_index == 0

    def test_player_str(self):
        """Test string representation."""
        player = Player(name="Frank", score=25, pairs_found=3)
        assert "Frank" in str(player)
        assert "25" in str(player)
        assert "3" in str(player)

    def test_invalid_name(self):
        """Test that empty names are rejected."""
        with pytest.raises(ValueError):
            Player(name="")

    def test_name_too_long(self):
        """Test that very long names are rejected."""
        long_name = "A" * 100
        with pytest.raises(ValueError):
            Player(name=long_name)
