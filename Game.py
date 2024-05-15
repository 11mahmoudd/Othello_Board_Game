import copy
import PlayerClass

rows, cols = 8, 8
board = [['-'] * cols for _ in range(rows)]
board[3][3] = 'W'
board[3][4] = 'B'
board[4][3] = 'B'
board[4][4] = 'W'

copyBorad=copy.deepcopy(board)

empty,available='-','@'

def display_board(board):
    for row in board:
        print(row)
    print()


def flip_disks(move, color,board):
    directions = [(0, 1), (1, 0),  (1, -1),(-1,1), (0, -1), (-1, 0), (-1, -1),(1, 1)]
    for d_row, d_col in directions:
        r, c = move[0] + d_row, move[1] + d_col
        flips = []
        while 0 <= r < len(board) and 0 <= c < len(board[0]):
            if board[r][c] == empty:
                break
            elif board[r][c] == color:
                for flip_r, flip_c in flips:
                    board[flip_r][flip_c] = color
                break
            else:
                flips.append((r, c))
            r += d_row
            c += d_col
    return board


def get_moves(board,color):
    if color == "B":
        otherColor = "W"
    else:
        otherColor = "B"
    available_moves = []
    directions = [(0, 1), (1, 0),  (1, -1),(-1,1), (0, -1), (-1, 0), (-1, -1),(1, 1)]
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == empty:
                for d_row, d_col in directions:
                    r, c = row + d_row, col + d_col
                    found_color = False
                    found_other = False
                    while 0 <= r < len(board) and 0 <= c < len(board[0]):
                        if board[r][c] == empty:
                            break  
                        elif board[r][c] == color:
                            found_color = True
                            break
                        elif board[r][c] == otherColor:
                            found_other = True
                        r += d_row
                        c += d_col
                    if found_color and found_other:
                        available_moves.append((row, col))
                        break 
    return available_moves


def mark_moves(available_moves,boardd):
    for cell in available_moves:
        row, col = cell
        boardd[row][col]='@'


def is_game_over(board):
    return not get_moves(board,'B') and not get_moves(board,'W')

def make_move(boardd,move,color):
    row, col = move
    boardd[row][col] = color
    new_board=flip_disks(move, color,boardd)
    return new_board

def evaluate_board(board):
    score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 'W':
                score += 1
            elif board[i][j] == 'B':
                score -= 1
    return score

def minimax(board, depth,alpha,beta, maximizingPlayer):
    if depth == 0 or is_game_over(board):
        return evaluate_board(board) , None
    if maximizingPlayer:
        color="W"
        maxEval=float('-inf')
        bestMove = None
        copyBoard = copy.deepcopy(board)
        for move in get_moves(copyBoard,color):
            state=make_move(copyBoard,move,color)
            # print(move)
            eval , _= minimax(state, depth - 1, alpha, beta ,False)
            maxEval=max(maxEval,eval)
            alpha=max(alpha,eval)
            if beta <= alpha:
                break
            if eval==maxEval:
                bestMove=move
                # print(bestMove,"BEST MOVE MAX")
        return maxEval,bestMove
    else:
        color="B"
        minEval=float('+inf')
        bestMove = None
        copyBoard = copy.deepcopy(board)
        for move in get_moves(copyBoard,color):
            state=make_move(copyBoard,move,color)
            # print(move)   
            eval,_= minimax(state, depth - 1, alpha, beta ,True)
            minEval=min(minEval,eval)
            beta=min(beta,eval)
            if beta <= alpha:
                break
            if eval==minEval:
                bestMove=move
                # print(bestMove,"BEST MOVE MIN")
        return minEval,bestMove

def congrates(players: list[PlayerClass.Player]):
    print("The game has ended ")
    players[0].display_player()
    players[1].display_player()
    if players[0].get_score(board) > players[1].get_score(board):
        print("\nCongratulations!",players[0].getColor())
    elif players[0].get_score(board) < players[1].get_score(board):
        if(isinstance(players[1],PlayerClass.HU_Player)):
            print("\nCongratulations!",players[1].getColor())
        else:
            print("\n HARD LUCK LOSER DON'T QQ ")
    else: print("Draw")

def update_score(players: list[PlayerClass.Player]):
    players[0].set_score(players[0].calc_score(copyBorad))
    players[1].set_score(players[1].calc_score(copyBorad))


def display_score(players: list[PlayerClass.Player]):
    update_score(players)
    print (players[0].getColor(),"=",players[0].get_score(),"/",players[1].getColor(),"=",players[1].get_score())


def play():
    mode=(input("For PVP enter 1, for PVE enter 2, for EXIT enter 0: ")) 
    while(mode not in ['0','1','2']):
        mode=(input("For PVP enter 1, for PVE enter 2, for EXIT enter 0: "))
    global copyBorad
    if (mode=='2') :
        human = PlayerClass.HU_Player("Black")
        pc = PlayerClass.PC_Player()
        players = [human,pc]
        depth=int(input("difficulty levels: Easy 1, Medium 3, Hard 5.\nChoose a number :"))
        print('\n\n')
        while not is_game_over(board):
            for player in players:
                moves=get_moves(board,player.getColor()[0])
                if(moves):
                    print(player.getColor()+"'s Turn")
                    display_score(players)
                    mark_moves(moves,copyBorad)
                    display_board(copyBorad)
                    print("available moves on the board:",moves,'\n')
                    if isinstance(player,PlayerClass.HU_Player):
                        row,col = player.get_moves()
                        while((int(row), int(col)) not in moves):
                            print("invalid Move, please choose a valid move ")
                            row,col = player.get_moves()
                        make_move(board,(int(row), int(col)),"B")
                    else:
                        pc_move=minimax(board,depth,float('-inf') , float('inf') , True)[1]
                        # print (pc_move,"--------------------------")
                        make_move(board,pc_move,"W")
                    copyBorad=copy.deepcopy(board)
                    print('\n\n')

        display_board(board)
        congrates(players)

    elif(mode=='1'):
        human1 = PlayerClass.HU_Player('Black')
        human2 = PlayerClass.HU_Player('White')
        players = [human1,human2]
        print('\n\n')
        while not is_game_over(board):
            for player in players:
                moves=get_moves(board,player.getColor()[0])
                if(moves):
                    print(player.getColor()+"'s Turn")
                    display_score(players)
                    mark_moves(moves,copyBorad)
                    display_board(copyBorad)
                    print("available moves on the board:",moves,'\n')
                    row,col = player.get_moves()
                    while((int(row), int(col)) not in moves):
                        print("invalid Move, please choose a valid move ")
                        row,col = player.get_moves()
                    make_move(board,(int(row), int(col)),player.getColor()[0])
                    copyBorad=copy.deepcopy(board)
                    print('\n\n')

        display_board(board)
        congrates(players)
        
    elif(mode=='0'):
        print("GOOD BYE <3")

play()

