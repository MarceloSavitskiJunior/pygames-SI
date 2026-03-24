from settings import POINTS_TO_WIN

class Scoreboard:

    def __init__(self) -> None:
        self.player1_score = 0
        self.player2_score = 0

    def score_player1(self) -> None:
        self.player1_score += 1

    def score_player2(self) -> None:
        self.player2_score += 1

    def get_winner(self) -> str | None:
        if self.player1_score >= POINTS_TO_WIN:
            return "Player 1"
        if self.player2_score >= POINTS_TO_WIN:
            return "Player 2"
        return None

    def reset(self) -> None:
        self.player1_score = 0
        self.player2_score = 0