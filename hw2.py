#!/usr/bin/python3
import os, sys
from game_state import game_state
import random
    
class dungeon_game(game_state):
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
            
    def _pprint_game_state(self):
        self._update_board()
        print(self.moves)
        print(self.points)
        for line in self.grid:
            print(''.join(line))
    
    #function to update board state after pieces have been moved
    def _update_board(self):
        # Replace 'A', 'G', 'D' with '  ' using a nested list comprehension
        self.grid = [[' ' if element in ['A', 'G', 'D'] else element for element in line] for line in self.grid]
        
        #show all living demons' positions on the board (will be alive if in list)
        for monster in self.monsters.values(): self.grid[monster.current_position[0]][monster.current_position[1]] = monster.monster_type
        
        #show act man's current position on board if he's alive
        #if a demon is in the same position as act man, then act man's dead X should show over the demon
        if self.act_man.is_alive: self.grid[self.act_man.current_position[0]][self.act_man.current_position[1]] = 'A'
        else: self.grid[self.act_man.current_position[0]][self.act_man.current_position[1]] = 'X'
        return
                   
    def _choose_and_move_actman(self):
        valid_options = self._get_valid_options(self.act_man)

        selected_option = random.choice(valid_options)
        self.moves += str(selected_option)
        self._move_actman(move=selected_option)                
    
    def _play_turn(self):    
        #not sure if sys exiting will cause an error in the program
        #so, I'm being safe and using multiple return checks only
        
        #decrease points by 1, check if points <= 0
        #if <= 0, kill Act-Man and exit game
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
        print(f"End of Turn {self.turn_count}")
        self._pprint_game_state()
        #exit out of the loop since you won the game
        
    
    #the 'main' function
    def play_game(self):
        print("Initial Board State")
        self._pprint_game_state()
        
        while self.game_state == "playing":
            self._play_turn()
            #comment / remove break to run full game
            break
        
        #print game state for last turn   
        print(f"Final Board State: End of Turn {self.turn_count}")
        self._pprint_game_state()
        
        
        self._output_final_game_state()
        print("Game Completed!")
    

new_dungeon = dungeon_game()
new_dungeon.play_game()
#new_dungeon._play_turn()