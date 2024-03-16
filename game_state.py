from character import character, monster, act_man
from typing import Tuple, List
from math import sqrt
import random

#game state class to store temporary boards for bfs
#need to have everything to move the board independently of act man making a decision to move
class game_state():
    def __init__(self, grid: List[List]=None, turn_count: int=None, points: int=None):    
        self.grid = grid
        self.turn_count = turn_count
        #keep track of current game state
        #victory, defeat or playing. Used for BFS
        game_state = "playing"
        self.act_man = None
        self.monsters = {}
        monsters_index = 0
        #iterate through matrix, determine monsters and actman positions     
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'A':  self.act_man = act_man((i, j), fired_bullet=False, is_alive=True)
                elif self.grid[i][j] == 'G':
                    self.monsters[monsters_index] = monster((i, j), 'G')
                    monsters_index += 1
                elif self.grid[i][j] == 'D':
                    self.monsters[monsters_index] = monster((i, j), 'D')
                    monsters_index += 1
    
    def _kill_monster(self, monster_index):
        monster_row, monster_col = self.monsters[monster_index].current_position
        self.grid[monster_row][monster_col] = '@'
        del self.monsters[monster_index]
        #five points gained if monster is killed
        self.points += 5
        
    def _move_monsters(self):
        #quick utility function
        def euclidean_distance(coord1: Tuple[int], coord2: Tuple[int]):
            return sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord2[1])**2)
        
        #move the monsters one at a time
        monsters_to_remove = []
        for index, monster in self.monsters.items():
            valid_options = self._get_valid_options(monster)
            #print(valid_options)
            #iterate until you get the minimum value(s)
            minimum_distance = float('inf') #set minimum distance to the max value
            minimum_values = []
            for option in valid_options:
                potential_move = tuple(sum(values) for values in zip(monster.current_position, monster.movement_translator[option]))
                act_man_distance = euclidean_distance(potential_move, self.act_man.current_position)
                if act_man_distance < minimum_distance:
                    minimum_values = [option]
                elif act_man_distance == minimum_distance:
                    minimum_values.append(option)
            
            selected_move = None
            #if there is a tie, then get the minimum values
            
            #basic assertion protection (check that value(s) were selected, monster type is ogre or demon)
            assert minimum_values, f"No valid moves for monster {monster}"
            assert monster.monster_type in ['G', 'D'], f"{monster} isn't a demon or ogre"
            if 8 in minimum_values: selected_move = 8
            #since the minimum values should be ordered clockwise (with no 8s)
            #all we have to do is the first (ogre), or the last (demon)
            elif monster.monster_type == 'G':
                selected_move = minimum_values[0]
            elif monster.monster_type == 'D':
                selected_move = minimum_values[-1]
            #print(selected_move)
            #print(monster.current_position)
            #move monster to new selected position
            monster.current_position = tuple(sum(values) for values in zip(monster.current_position, monster.movement_translator[selected_move]))
            
            #check if any monsters, corpses or actman are in the new position
            #moved into act man
            if self.act_man.current_position == monster.current_position: self._kill_actman()
            #moved into corpse
            #because I can't delete the monster
            elif self.grid[monster.current_position[0]][monster.current_position[1]] == '@': monsters_to_remove.append(index)
            
        #delete all monsters that hit a corpse
        if monsters_to_remove: print(monsters_to_remove)
        [self._kill_monster(index) for index in monsters_to_remove]
        monsters_to_remove = []
        
        
        #once you finished moving the monsters, check if they've finished in the same place
        #moved into another monster
        #sinces self.monsters is a dictionary, each item in the dictionary has a constant index
        for index, monster in self.monsters.items():
            for check_index, check_monster in self.monsters.items():
                if monster.current_position == check_monster.current_position and check_index != index:
                    if index not in monsters_to_remove:
                        monsters_to_remove.append(index)
                    if check_index not in monsters_to_remove:
                        monsters_to_remove.append(check_index)
        
        #delete all monsters that are in the same collision space
        [self._kill_monster(index) for index in monsters_to_remove]