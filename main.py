import random

# backtracking to solve locosudoku (https://www.pleacher.com/mp/puzzles/mathpuz/moblosu.html)

# horizontals
hs = [{i for i in range(1,10)} for k in range(9)]
# verticals
vs = [{j for j in range(1,10)} for k in range(9)]
# 9x9 blocks
bs = [{b for b in range(1,10)} for k in range(9)]

# map from board position to block
ij2b = [[0,0,0,0,1,1,1,1,1],
        [0,0,0,0,2,2,1,1,1],
        [0,3,3,2,2,2,4,4,1],
        [3,3,5,5,5,2,4,4,4],
        [3,5,5,5,5,2,4,4,4],
        [3,3,3,5,5,2,2,4,6],
        [3,7,7,8,8,8,6,6,6],
        [7,7,7,8,8,8,6,6,6],
        [7,7,7,7,8,8,8,6,6]]

# open positions
open_positions = []
for i in range(9):
    for j in range(9):
        open_positions.append((i,j))

# a stack of plays (position, number)
plays = [] # (i,j,x)

# for each position record what number has been previously played
# at position i,j we try each possibility in increasing order. So
# to determine if we've checked all possible plays at i,j we just
# need to know if last_played[i][j] is greater than or equal to
# max(possible_plays(i,j))
last_played = []
for i in range(9):
    last_played.append([])
    for j in range(9):
        last_played[-1].append(-1) # -1 <=> no plays have been made

def play(i,j,x,initial=False):
    hs[i].remove(x)
    vs[j].remove(x)
    bs[ij2b[i][j]].remove(x)
    last_played[i][j] = x
    if not initial:
        plays.append((i,j,x))
    else:
        open_positions.remove((i,j))

def undo_last():
    i,j,x = plays.pop()
    hs[i].add(x)
    vs[j].add(x)
    bs[ij2b[i][j]].add(x)
    return i,j

# setup the board
initial = {
    (0,5):5,
    (0,6):4,
    (1,0):4,
    (1,1):5,
    (1,3):6,
    (2,4):7,
    (2,5):2,
    (3,1):4,
    (3,6):9,
    (3,7):7,
    (4,2):9,
    (4,3):7,
    (4,7):1,
    (5,2):8,
    (6,0):6,
    (6,3):1,
    (6,8):9,
    (7,1):6,
    (7,2):2,
    (8,5):7,
    (8,6):6,
    (8,7):4,
    (8,8):1
}

for (i,j),p in initial.items():
    play(i,j,p,initial=True)

def possible_plays(i,j):
    return set(hs[i]).intersection(set(vs[j]), set(bs[ij2b[i][j]]))

def print_board():
    for i in range(9):
        for j in range(9):
            if (i,j) in initial:
                print("{:>3}".format(initial[(i,j)]),end='')
            else:
                print("{:>3}".format(last_played[i][j]),end='')
        print()

while True:
    if len(open_positions) > 0:
        i,j = open_positions.pop()
    else:
        print('win')
        print_board()
        exit(1)
    # find something to play
    can_play = possible_plays(i,j)
    if len(can_play) == 0: # if we have made an incorrect play then backtrack
        # put i,j back
        open_positions.append((i,j))
        i,j = undo_last()
        can_play = possible_plays(i,j)
        while last_played[i][j] >= max(can_play): # while we have exhausted all moves
            last_played[i][j] = -1 # reset moves tried counter
            open_positions.append((i,j))
            i,j = undo_last()
            can_play = possible_plays(i,j)
    next = min(k for k in can_play if k > last_played[i][j])
    play(i,j,next)

