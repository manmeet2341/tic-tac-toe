from math import inf
from random import choice


class Player():
    def __init__(self, letter) -> None:
        self.letter = letter

    def get_move(self, game):
        pass


class HumanPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None

        while not valid_square:
            square = input(f"{self.letter}'s turn. Input move (0-8): ")

            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True

            except ValueError:
                print("Invalid square. Try again.")

        return val


class RandomComputerPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        square = choice(game.available_moves())
        return square


class SmartComputerPlayer(Player):
    def __init__(self, letter) -> None:
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = choice([0, 2, 4, 6, 8])
        else:
            square = self.minimax(game, self.letter)["position"]

        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = "0" if player == "X" else "X"

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {"position": None, "score": 0}

        best = self.set_best(player, max_player)

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = " "
            state.current_winner = None
            sim_score["position"] = possible_move

            best = self.set_score(player, max_player, sim_score, best)

        return best

    def set_score(self, player, max_player, sim_score, best):
        if player == max_player:
            if sim_score["score"] > best["score"]:
                best = sim_score
        else:
            if sim_score["score"] < best["score"]:
                best = sim_score

        return best

    def set_best(self, player, max_player):
        if player == max_player:
            best = {"posiiton": None, "score": -inf}
        else:
            best = {"position": None, "score": inf}

        return best
