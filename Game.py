class Game:
    def __init__(self, _id):
        self.p1Went: bool = False
        self.p2Went: bool = False
        self.ready: bool = False
        self.id = _id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

    def connected(self):
        return self.ready

    def both_went(self):
        return self.p1Went and self.p2Went

    def winner(self):
        pass

    def reset_went(self):
        self.p1Went = False
        self.p2Went = False
