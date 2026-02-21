"""Tests for the Game class."""

import pytest
from src.game import Game, Card, CardState


class TestCard:
    """Test the Card class."""

    def test_card_creation(self):
        """Test creating a card."""
        card = Card(0, "🐶")
        assert card.card_id == 0
        assert card.value == "🐶"
        assert card.state == CardState.HIDDEN

    def test_reveal_card(self):
        """Test revealing a card."""
        card = Card(0, "🐱")
        card.reveal()
        assert card.is_revealed()
        assert not card.is_hidden()

    def test_hide_card(self):
        """Test hiding a card."""
        card = Card(0, "🐭")
        card.reveal()
        card.hide()
        assert card.is_hidden()
        assert not card.is_revealed()

    def test_matched_card_cannot_hide(self):
        """Test that matched cards cannot be hidden."""
        card = Card(0, "🐹")
        card.reveal()
        card.match()
        card.hide()
        assert card.is_matched()

    def test_card_repr(self):
        """Test card string representation."""
        card_hidden = Card(0, "🐰")
        assert str(card_hidden) == "?"
        
        card_revealed = Card(0, "🦊")
        card_revealed.reveal()
        assert str(card_revealed) == "🦊"
        
        card_matched = Card(0, "🐻")
        card_matched.reveal()
        card_matched.match()
        assert str(card_matched) == "✓"


class TestGame:
    """Test the Game class."""

    def test_game_creation(self):
        """Test creating a game."""
        game = Game(num_pairs=4)
        assert game.num_pairs == 4
        assert len(game.cards) == 8
        assert game.matched_pairs == 0

    def test_game_invalid_pairs(self):
        """Test that invalid pair counts are rejected."""
        with pytest.raises(ValueError):
            Game(num_pairs=2)
        
        with pytest.raises(ValueError):
            Game(num_pairs=20)

    def test_game_invalid_theme(self):
        """Test that invalid themes are rejected."""
        with pytest.raises(ValueError):
            Game(theme="invalid")

    def test_cards_are_paired(self):
        """Test that cards are properly paired."""
        game = Game(num_pairs=4)
        values = [card.value for card in game.cards]
        
        for value in set(values):
            assert values.count(value) == 2

    def test_cards_are_shuffled(self):
        """Test that cards are shuffled."""
        game1 = Game(num_pairs=4)
        game2 = Game(num_pairs=4)
        
        values1 = [card.value for card in game1.cards]
        values2 = [card.value for card in game2.cards]
        
        # Probability of being in same order is very low
        assert values1 != values2

    def test_reveal_card(self):
        """Test revealing a card."""
        game = Game(num_pairs=4)
        result = game.reveal_card(0)
        
        assert result is True
        assert game.cards[0].is_revealed()

    def test_cannot_reveal_twice(self):
        """Test that already revealed cards cannot be revealed again."""
        game = Game(num_pairs=4)
        game.reveal_card(0)
        result = game.reveal_card(0)
        
        assert result is False

    def test_invalid_position(self):
        """Test revealing at invalid position."""
        game = Game(num_pairs=4)
        result = game.reveal_card(100)
        assert result is False

    def test_check_match_success(self):
        """Test matching cards."""
        game = Game(num_pairs=4)
        # Find a matching pair
        first_value = game.cards[0].value
        second_idx = None
        for i in range(1, len(game.cards)):
            if game.cards[i].value == first_value:
                second_idx = i
                break
        
        game.reveal_card(0)
        game.reveal_card(second_idx)
        
        matched = game.check_match()
        assert matched is True
        assert game.matched_pairs == 1

    def test_check_match_fail(self):
        """Test non-matching cards."""
        game = Game(num_pairs=4)
        # Pick two from different pairs
        while game.cards[0].value == game.cards[2].value:
            # Shuffle until we get different values
            import random
            random.shuffle(game.cards)
        
        game.reveal_card(0)
        game.reveal_card(2)
        
        matched = game.check_match()
        assert matched is False
        assert game.matched_pairs == 0

    def test_hide_revealed_cards(self):
        """Test hiding revealed cards."""
        game = Game(num_pairs=4)
        game.reveal_card(0)
        game.reveal_card(1)
        game.hide_revealed_cards()
        
        assert game.cards[0].is_hidden()
        assert game.cards[1].is_hidden()
        assert game.revealed_cards == []

    def test_is_won(self):
        """Test win condition."""
        game = Game(num_pairs=4)
        assert not game.is_won()
        
        # Match all pairs
        for i in range(game.num_pairs):
            first_value = None
            first_idx = None
            second_idx = None
            
            # Find first unmatched card
            for j in range(len(game.cards)):
                if game.cards[j].state.value == "hidden":
                    first_value = game.cards[j].value
                    first_idx = j
                    break
            
            # Find its pair
            for j in range(first_idx + 1, len(game.cards)):
                if game.cards[j].state.value == "hidden" and game.cards[j].value == first_value:
                    second_idx = j
                    break
            
            # Reveal and match
            game.reveal_card(first_idx)
            game.reveal_card(second_idx)
            game.check_match()
        
        assert game.is_won()

    def test_increment_moves(self):
        """Test move counter."""
        game = Game(num_pairs=4)
        assert game.total_moves == 0
        
        game.increment_moves()
        assert game.total_moves == 1

    def test_get_stats(self):
        """Test getting game statistics."""
        game = Game(num_pairs=4)
        stats = game.get_stats()
        
        assert stats["total_cards"] == 8
        assert stats["pairs_total"] == 4
        assert stats["pairs_matched"] == 0
        assert stats["moves"] == 0
