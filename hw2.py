#!/usr/bin/python3
import os, sys
from game_board import game_board
import random
    
class dungeon_game(game_board):
    def __init__(self):
        input_file_path = sys.argv[1]
        self.output_file_path = sys.argv[2]
        
        list_of_lists = []
        with open(input_file_path, 'r') as input_file:
            input_file_list = input_file.read().splitlines()
        
        inputs = input_file_list[0].split()
        rows, cols = int(inputs[0]), int(inputs[1])
            
        #convert input file to list of lists
        input_file_grid = []
        for line in input_file_list:
            input_file_grid.append(list(line))
        
        #get section of map within bounds
        grid = input_file_grid[1:1+rows][:cols]
    
        super().__init__(grid=grid, turn_count=0, points=50)
        self.moves = ''
    
    #prints current state in game in manner similar to output file
    def _output_final_game_state(self):
        with open(self.output_file_path, 'w') as output_file:
            output_file.write(f"{self.moves}\n")
            output_file.write(f"{self.points}\n")
            for line in self.grid:
                output_file.write(f"{''.join(line)}\n")
                   
    def _choose_and_move_actman(self):
        valid_options = self._get_valid_options(self.act_man)

        #data structure to store queue of options
        queue = [{'initial_move': option, 'current_move': option, 'turns': 6, 'game_board': game_board(grid=self.grid, turn_count=self.turn_count, points=self.points, moves=self.moves)} for option in valid_options]

        #testing iterating through queue
        selected_option = None
        
        #print(valid_options)
        #iterate through the loop until goal condition met or queue becomes empty
        while queue:
            option: dict = queue.pop(0)
            #move act man and move the monsters
            #print(option['game_board'].act_man.current_position)
            option['game_board']._move_actman(option['current_move'])
            #print(option['game_board'].act_man.current_position)
            option['game_board']._move_monsters()
            #print(len(option['game_board'].monsters))

            #did act man die from doing this action?
            if option['game_board'].game_state == 'defeat':
                continue
            #did act man kill all the monsters (thereby winning)?
            #is act man still alive after 7 turns (i.e. 6 turns plus this one)?
            elif option['game_board'].game_state == 'victory' or option['turns'] == 6:
                print("Found a good move")
                print(option['current_move'])
                selected_option = option['current_move']
                break
            else:
                pass

        #contingency if queue becomes empty and goal is not empty
        else:
            print("No good option found. Choosing option at random")
            selected_option = random.choice(valid_options)

        self._move_actman(move=selected_option)            
    
    def _play_turn(self):    
        #not sure if sys exiting will cause an error in the program
        #so, I'm being safe and using multiple return checks only
        
        #decrease points by 1, check if points <= 0
        #if <= 0, kill Act-Man and exit game
        #since 'game ends' when score <= 0, I'm default to saying act man dies
        if self.points <= 0:
            self._kill_actman()
        #game end check
        if self.game_state != "playing": return
        
        #increment turn count pre_emptively,
        #in case act man killed by demons or demons get killed
        self.turn_count += 1
        #move act man
        self._choose_and_move_actman()
        if self.game_state != "playing": return
        
        #move the monsters
        self._move_monsters()
        
        #initial state should already be printed
        #prints the game state at the end of each turn
        print()
        print(f"End of Turn {self.turn_count}")
        self._pprint_game_state()
        #exit out of the loop since you won the game
        
    
    #the 'main' function
    def play_game(self):
        print("Initial Board State")
        self._pprint_game_state()
        print()
        
        while self.game_state == "playing":
            self._play_turn()
            #comment / remove break to run full game
            break
        
        #print game state for last turn
        print() 
        print(f"Final Board State: End of Turn {self.turn_count}")
        self._pprint_game_state()
        
        
        self._output_final_game_state()
        print("Game Completed!")
    

new_dungeon = dungeon_game()
new_dungeon.play_game()
#new_dungeon._play_turn()