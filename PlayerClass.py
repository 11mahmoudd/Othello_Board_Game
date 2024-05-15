class Player:

    def __init__(self,color='', discs=2):
        self.color = color
        self.discs=discs

    def display_player(self):
        print("Color : ",self.color,"\nNumber of Discs :",self.discs)

    def calc_score(self,board):
        score=0
        for row in range(len(board)):
            for col in range(len(board[0])):
                if (board[row][col] == self.color[0]):
                    score+=1
        return score

    def get_score(self):
        return self.discs

    def set_score(self,score):
        self.discs=score

    def getColor(self):
        return self.color


class HU_Player(Player):
    def __init__(self,color):
        self.color = color
        self.discs=2

    def get_moves(self):
        row,col = input('Enter row and col : ').split()
        return (row,col)


class PC_Player(Player):
    def __init__(self,color="White"):
        self.color = color
        self.discs=2
