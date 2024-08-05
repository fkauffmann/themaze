import pygame
import random
from wall import Wall
from item import Item

class Labyrinth():
    def __init__(self, laby_struct, cell_width, cell_height, max_items, player, monster):
        self.labyrinth = laby_struct
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.max_items = max_items
        self.player = player
        self.monster = monster

    # generate items randomly in the maze
    def randomize(self):
        bonus_spawned = False

        free_cells = 0
        for x in range(len(self.labyrinth[0])):
            for y in range(len(self.labyrinth)):
                if self.labyrinth[y][x] == 0:
                    free_cells = free_cells + 1
        print(f"Free cells: {free_cells}")

        if self.max_items >= (free_cells - 2):
            self.max_items = free_cells - 2

        for x in range(len(self.labyrinth[0])):
            for y in range(len(self.labyrinth)):
                if self.labyrinth[y][x] > 1:
                    self.labyrinth[y][x] = 0
        maxItems = self.max_items
        while maxItems>0:
            x = random.randint(0,len(self.labyrinth[0])-1)
            y = random.randint(0,len(self.labyrinth)-1)
            if self.labyrinth[y][x] == 0:
                item_type = random.randint(2,4)

                if bonus_spawned:
                    item_type = random.randint(2,3)

                maxItems = maxItems - 1;
                if item_type == 4:
                    bonus_spawned = True
                self.labyrinth[y][x] = item_type 

        # spawn the player on an empty spot
        player_spawn = False
        while not player_spawn:
            x = random.randint(0,len(self.labyrinth[0])-1)
            y = random.randint(0,len(self.labyrinth)-1)
            if self.labyrinth[y][x] == 0:
                self.player.rect.x = x * self.cell_width
                self.player.rect.y = y * self.cell_height
                player_spawn = True

        # spawn the monster
        monster_spawn = False
        while not monster_spawn:
            x = random.randint(0,len(self.labyrinth[0])-1)
            y = random.randint(0,len(self.labyrinth)-1)
            if self.labyrinth[y][x] == 0:
                self.monster.rect.x = x * self.cell_width
                self.monster.rect.y = y * self.cell_height
                if self.player.rect.x!=self.monster.rect.x and self.player.rect.y!=self.monster.rect.y:
                    monster_spawn = True

    def read_and_display(self, wall_sprite_group, item_sprite_group):
        x_pos = 0
        y_pos = 0
        for y in range(len(self.labyrinth)):
            x_pos = 0
            for x in range(len(self.labyrinth[0])):
                if self.labyrinth[y][x] == 1:
                    wall = Wall()
                    wall.rect.x = x_pos
                    wall.rect.y = y_pos
                    wall_sprite_group.add(wall)
                elif self.labyrinth[y][x] == 2:
                    diamond = Item("./assets/diamond.png")
                    diamond.rect.x = x_pos
                    diamond.rect.y = y_pos
                    item_sprite_group.add(diamond)
                elif self.labyrinth[y][x] == 3:
                    round = Item("./assets/round.png")
                    round.rect.x = x_pos
                    round.rect.y = y_pos
                    item_sprite_group.add(round)                     
                elif self.labyrinth[y][x] == 4:
                    triangle = Item("./assets/triangle.png")
                    triangle.rect.x = x_pos
                    triangle.rect.y = y_pos
                    item_sprite_group.add(triangle)
                x_pos += self.cell_width
            y_pos += self.cell_height