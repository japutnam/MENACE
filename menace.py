"""menace.py is a Python version of Donald Michie's Matchbox Educable Naughts And Crosses Engine (MENACE) Penguin Science Survey 1961, Vol 2.

Originally written on Easter Sunday, March 31,2013 by Nicholas Putnam with help from his father, James and his son David Asahel.

An public github repository for the code is at https://github.com/japutnam/MENACE.git

To run in a Mac OS terminal, put the program into a directory then issue the command: python menace.py <starting_brain_file> <ending_brain_file>

"""

import random
import sys

starting_brain_file = sys.argv[1]
ending_brain_file=sys.argv[2]

print "hello world", starting_brain_file,ending_brain_file

def draw_board(state):
        print state[1],"|",state[2],"|",state[3]
        print "--+---+--"
        print state[4],"|",state[5],"|",state[6]
        print "--+---+--"
        print state[7],"|",state[8],"|",state[9]


forward_map={}
reverse_map={}
forward_map[ 1 ]=  { 1 : 1 , 2 : 2 , 3 : 3 , 4 : 4 , 5 : 5 , 6 : 6 , 7 : 7 , 8 : 8 , 9 : 9  }  # identity
forward_map[ 2 ]=  { 1 : 1 , 2 : 4 , 3 : 7 , 4 : 2 , 5 : 5 , 6 : 8 , 7 : 3 , 8 : 6 , 9 : 9  }  # flip diagonl 1  
forward_map[ 3 ]=  { 1 : 3 , 2 : 2 , 3 : 1 , 4 : 6 , 5 : 5 , 6 : 4 , 7 : 9 , 8 : 8 , 9 : 7  }  # flip left-right
forward_map[ 4 ]=  { 1 : 3 , 2 : 6 , 3 : 9 , 4 : 2 , 5 : 5 , 6 : 8 , 7 : 1 , 8 : 4 , 9 : 7  }  # rot cw 90
forward_map[ 5 ]=  { 1 : 7 , 2 : 8 , 3 : 9 , 4 : 4 , 5 : 5 , 6 : 6 , 7 : 1 , 8 : 2 , 9 : 3  }  # flip up-down
forward_map[ 6 ]=  { 1 : 7 , 2 : 4 , 3 : 1 , 4 : 8 , 5 : 5 , 6 : 2 , 7 : 9 , 8 : 6 , 9 : 3  }  # rot ccw 90
forward_map[ 7 ]=  { 1 : 9 , 2 : 8 , 3 : 7 , 4 : 6 , 5 : 5 , 6 : 4 , 7 : 3 , 8 : 2 , 9 : 1  }  # rot 180
forward_map[ 8 ]=  { 1 : 9 , 2 : 6 , 3 : 3 , 4 : 8 , 5 : 5 , 6 : 2 , 7 : 7 , 8 : 4 , 9 : 1  }  # flip diagonal 2
reverse_map[ 1 ]=  forward_map[ 1 ]
reverse_map[ 2 ]=  forward_map[ 2 ]
reverse_map[ 3 ]=  forward_map[ 3 ]
reverse_map[ 4 ]=  forward_map[ 6 ] # rot
reverse_map[ 5 ]=  forward_map[ 5 ]
reverse_map[ 6 ]=  forward_map[ 4 ] # rot
reverse_map[ 7 ]=  forward_map[ 7 ]
reverse_map[ 8 ]=  forward_map[ 8 ]

    

def cannonical_rep(state):
    cans = []
    #    print cans
    can = tuple( [ state[i] for i in (1,2,3,4,5,6,7,8,9) ] )
    # print can
    #    print can
    return(can)

def rotate(state,r):
    new_state={}
    for color in range(1,10):
        new_state[ forward_map[r][color] ] = state[ color ]
    return(new_state)

def unrotate_move(move,r):
    return( reverse_map[r][move] )

def best_rotation(state):
    cans = []
    for r in range(1,9):
        new_state=rotate(state,r)
        cans.append( (cannonical_rep(new_state), r ) )
    cans.sort()
    #for c in cans:
    #    print c
    return cans[0][1]


class Matchbox:
    def __init__(self, position={1:' ', 2:' ', 3:' ', 4:' ', 5:' ', 6:' ', 7:' ', 8:' ', 9:' ' } ):
        print "made",self
        self.contents = {} #  1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4  }
        for color in range(1,10):
            if position[color]==' ' :
                self.contents[color] = 4
            else:
                self.contents[color] = 0
        self.position = position

    def show(self):
        print "contents",self.contents
        print "position",self.position


    def pick_move(self,move_candidates=(1,2,3,4,5,6,7,8,9)):

        pool = []
        for color in move_candidates:
            pool += [color] * self.contents[color]
            if not pool:    #applies if you run out of beads
                print "Matchbox ran out of beads"
                self.contents = {} #  1:4, 2:4, 3:4, 4:4, 5:4, 6:4, 7:4, 8:4, 9:4  }
                for color in range(1,10):
                    if self.position[color]==' ' :
                        self.contents[color] = 4
                    else:
                        self.contents[color] = 0
                return(random.choice(move_candidates))

        move = random.choice(pool)
        print "pool:",pool
        print "move:",move
        return move

winning_sets=(
(1,2,3),
(4,5,6),
(7,8,9),
(1,4,7),
(2,5,8),
(3,6,9),
(1,5,9),
(3,5,7)
    )


def winner(state):
    for win in winning_sets:
        t = tuple([ state[i] for i in win ])
        #        print win,t
        if  t == ("X","X","X"):
            return "X"
        if t == ("O","O","O"):
            return "O"
    return False
class Brain:
    def __init__(self,init_file=False):
        self.rack = {}
        self.state_sequence=[]
        self.computers_moves={}
        self.game_count=0
        self.wins=0
        self.losses=0
        self.draws=0
        if init_file:
            f=open(init_file)
            l = f.readline()
            if l:
                (self.game_count,self.wins,self.losses,self.draws) = eval(l.strip())
            while True:
                l = f.readline()
                if not l:
                    break
                t = eval(l.strip())
                state = {}
                for color in range(1,10):
                    state[color]=t[1][color]
                self.rack[t[0]] = Matchbox( state )
                self.rack[t[0]].contents=t[1]

    def save_to_file(self,filename):
        f=open(filename,"w")

        f.write(str((self.game_count,self.wins,self.losses,self.draws)))
        f.write("\n")
        
        for state in self.rack.keys():
            f.write(str((state,self.rack[state].contents)))
            f.write("\n")
            #            f.write(str(self.rack))    
        f.close()

    def pick_move(self,game_state):
        r = best_rotation(game_state)
        print "best rotation:",r
        rotated_game_state = rotate(game_state,r)
        can = cannonical_rep(rotated_game_state)
        print "rotated cannonical rep:",can
        if not can in self.rack:
            self.rack[can] = Matchbox(rotated_game_state)

        box = self.rack[can]

        posmove=[]
        for color in range(1,10):
            if rotated_game_state[color]==" ":
                posmove.append(color)
        print "posmove:",posmove
        degenerate_moves={}
        for move in posmove:
            game_state2 = dict(rotated_game_state)
            game_state2[move]="X"
            r2 = best_rotation(game_state2)
            game_state2r = rotate(game_state2,r2)
            can2 = cannonical_rep(game_state2r)
            degenerate_moves[can2] = [ move ] + degenerate_moves.get(can2,[])

        for c2 in  degenerate_moves.keys() :
            print c2,"reached by moves:",degenerate_moves[c2]

        nr_moves = [ degenerate_moves[i][0] for i in degenerate_moves.keys() ]
        print "non-redundant moves:",nr_moves

        move = box.pick_move( move_candidates=nr_moves )
        
        self.state_sequence.append( can )
        self.computers_moves[ can ] = move

        print "move:",move
        print "unrotated move:",unrotate_move(move,r), "r=",r
        return unrotate_move(move,r)

    def record_result(self,result):
        self.game_count+=1
        if result == "Win":
            self.wins=self.wins+1
        if result == "Draw":
            self.draws=self.draws+1
        if result == "Loss":
            self.losses=self.losses+1
        for state in self.state_sequence:
            move = self.computers_moves[state]
            # print move
            # print "before",self.rack[state].contents
            if result == "Win":
                self.rack[state].contents[move]+=3
            elif result == "Draw":
                self.rack[state].contents[move]+=1
            else:
                self.rack[state].contents[move]-=1
                # print "after ",self.rack[state].contents
        self.computers_moves={}
        self.state_sequence=[]


game_state =  {1:' ', 2:' ', 3:' ', 4:' ', 5:' ', 6:' ', 7:' ', 8:' ', 9:' ' } 

print cannonical_rep(game_state)

b = Brain(starting_brain_file)


def play_game():
    state_sequence=[]
    computers_moves={}
    result="Draw"


    game_not_over=True
    nmoves=0
    while game_not_over:
        nmoves+=1
        
        move = b.pick_move(game_state)
        
        game_state[move] = "X"
        draw_board(game_state)
        if winner(game_state) == "X":
            print "I win"
            result="Win"
            break
        if nmoves==9:
            print "Draw!"
            break
        
        nmoves+=1
        move = "a"
        while not move in range(1,10):
            raw_move = raw_input("your move:")
            try:
                move = int(raw_move)
                if not game_state[move]==" ":
                    move="a"
                    print "someone already moved there"
            except:
                print "enter a digit from 1-9"
        game_state[move]="O"
        draw_board(game_state)
        if winner(game_state) == "O":
            print "You win"
            result = "Loss"
            break


    b.record_result(result)
    print "Record"
    print "Games played ", b.game_count
    print "Games MENACE won ", b.wins
    print "Games MENACE lost ", b.losses
    print "Games MENACE drew ", b.draws


while True:
    game_state =  {1:' ', 2:' ', 3:' ', 4:' ', 5:' ', 6:' ', 7:' ', 8:' ', 9:' ' } 
    play_game()
    a = raw_input("Play again?")
    print a
    if a=="N":
        break

b.save_to_file(ending_brain_file)

#x.show()
#x.draw()






