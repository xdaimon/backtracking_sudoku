import random

# backtracking to solve locosudoku (https://www.pleacher.com/mp/puzzles/mathpuz/moblosu.html)

# hs[i] <=> the set of numbers not in this horizontal
hs = [{i for i in range(1,10)} for k in range(9)]
# vs[i] <=> the set of numbers not in this vertical
vs = [{j for j in range(1,10)} for k in range(9)]
# bs[i] the set of numbers not in this 9x9 block
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

open_positions = []
for i in range(9):
    for j in range(9):
        open_positions.append((i,j))

# a stack of plays we've made
plays = [] # (i,j,x)

def play(i,j,x,initial=False):
    hs[i].remove(x)
    vs[j].remove(x)
    bs[ij2b[i][j]].remove(x)
    if not initial:
        plays.append((i,j,x))
    else:
        open_positions.remove((i,j))

def backtrack(i,j):
    open_positions.append((i,j))
    i,j,x = plays.pop()
    bs[ij2b[i][j]].add(x)
    vs[j].add(x)
    hs[i].add(x)
    return i,j,x

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
    return hs[i].intersection(vs[j], bs[ij2b[i][j]])

def print_board():
    play_map = {}
    for play in plays:
        play_map[play[:2]] = play[2]
    for i in range(9):
        for j in range(9):
            if (i,j) in initial:
                print("{:>3}".format(initial[(i,j)]),end='')
            else:
                print("{:>3}".format(play_map[(i,j)]),end='')
        print()

while True:
    if len(open_positions) > 0:
        i,j = open_positions.pop()
    else:
        print('solution:')
        print_board()
        exit(1)
    # find something to play
    can_play = possible_plays(i,j)
    if len(can_play) == 0: # if we have made an incorrect play
        i,j,x = backtrack(i,j)
        can_play = possible_plays(i,j)
        while x == max(can_play): # possibly backtrack further
            # moves are tried in order so if x is the largest possible
            # move at this position then all moves have been exhausted
            i,j,x = backtrack(i,j)
            can_play = possible_plays(i,j)
        next = min(k for k in can_play if k > x)
    else:
        next = min(can_play)
    play(i,j,next)

