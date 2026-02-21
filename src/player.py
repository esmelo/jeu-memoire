"""Player class for the memory game."""

from pydantic import BaseModel, Field


class Player(BaseModel):
    """Represents a player in the memory game."""

    name: str = Field(..., min_length=1, max_length=50)
    score: int = Field(default=0, ge=0)
    pairs_found: int = Field(default=0, ge=0)
    turn_index: int = Field(default=0, ge=0)

    def add_score(self, points: int) -> None:
        """Add points to the player's score."""
        if points < 0:
            raise ValueError("Points must be non-negative")
        self.score += points

    def increment_pairs(self) -> None:
        """Increment the number of pairs found."""
        self.pairs_found += 1

    def reset(self) -> None:
        """Reset player score and pairs for a new game."""
        self.score = 0
        self.pairs_found = 0
        self.turn_index = 0

    def __str__(self) -> str:
        """Return string representation of the player."""
        return f"{self.name} (Score: {self.score}, Pairs: {self.pairs_found})"
