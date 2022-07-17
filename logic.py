import random

import pygame

from tiles import *

WIDTH = 800
HEIGHT = 1000
header = 200
padding = 50

pygame.font.init()
number_font = pygame.font.Font("fonts/Pixeltype.ttf", 50)


class Board:

    def __init__(self, screen, width=16, height=16):
        self.game_over = False
        self.won = False
        self.lost = False
        self.board = []
        self.cells = []
        self.width = width
        self.height = height
        self.display_surface = screen
        self.tiles = pygame.sprite.Group()
        self.tile_list = []
        self.flags = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.knowledge = []

        self.real_mines = set()
        self.explored_cells = set()
        self.marked_mines = set()
        width = WIDTH - (padding * 2)
        height = HEIGHT - header - (padding * 2)
        self.rect_width = int(width / self.width)
        self.rect_height = int(height / self.height)
        self.origin = (padding, header + padding)

        self.make_board()
        self.number_board()
        self.make_tiles()

    def make_board(self):
        """Make board comprised of Truth/False"""
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                if random.randint(0, 5) == 0:
                    row.append(True)
                    self.real_mines.add((i, j))
                else:
                    row.append(False)
            self.board.append(row)

    def define_cell(self, cell):
        """Return number of mines neighboring cell"""
        y = cell[0]
        x = cell[1]
        count = 0

        if not self.board[y][x]:
            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if 0 <= j < self.width and 0 <= i < self.height:
                        if (i, j) == (y, x):
                            continue
                        else:
                            if self.board[i][j]:
                                count += 1
            return count
        else:
            return "#"

    def number_board(self):
        """Turn self.board into board of numbers"""
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(str(self.define_cell((i, j))))
            board.append("".join(row))

        self.board = board

    def print(self):
        """Print board in text format"""
        print(f"+{'-'*self.width}+")
        for row in self.board:
            print(f'|{row}|')
        print(f"+{'-' * self.width}+")

    def draw_skeleton(self):
        """Draw skeleton board"""
        board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                # Skeleton cells
                x = self.origin[0] + (j * self.rect_width)
                y = self.origin[1] + (i * self.rect_height)
                rect = pygame.Rect(x, y, self.rect_width, self.rect_height)
                pygame.draw.rect(self.display_surface, (170, 170, 170), rect)
                pygame.draw.rect(self.display_surface, (130, 130, 130), rect, 3)
                row.append(rect)
                # Numbers
                if self.board[i][j] != "0":
                    number_text = number_font.render(f"{self.board[i][j]}", True, (0, 0, 0))
                    number_text_rect = number_text.get_rect()
                    number_text_rect.center = rect.center
                    self.display_surface.blit(number_text, number_text_rect)
            board.append(row)
        self.tile_list = board

    def make_tiles(self):
        """"Add tiles to self.tiles sprite group"""
        for i in range(self.height):
            for j in range(self.width):
                x = self.origin[0] + (j * self.rect_width)
                y = self.origin[1] + (i * self.rect_height)
                tile = Tile((x, y), (self.rect_width, self.rect_height))
                self.tiles.add(tile)

    def draw(self):
        """Draw tiles, mines, and flags"""
        self.tiles.draw(self.display_surface)
        self.flags.draw(self.display_surface)
        if self.game_over is True:
            self.mines.draw(self.display_surface)

    def click(self):
        """Explore or flag mine based on current cursor position"""
        pos = pygame.mouse.get_pos()
        for i in range(len(self.tile_list)):
            for j in range(len(self.tile_list[i])):
                if self.tile_list[i][j].collidepoint(pos):
                    if pygame.mouse.get_pressed()[0] is True:
                        self.explore((i, j))
                    elif pygame.mouse.get_pressed()[2] is True:
                        self.mark_mine((i, j))

        self.check_win()

    def mark_mine(self, cell):
        """Add cell to self.marked_mines and draw flag"""
        i = cell[0]
        j = cell[1]
        if (i, j) not in self.explored_cells:
            if (i, j) not in self.marked_mines:
                self.marked_mines.add((i, j))
                flag = Flag(self.tile_list[i][j].topleft, (self.rect_width, self.rect_height))
                self.flags.add(flag)

            else:
                self.marked_mines.remove((i, j))
                for mine in self.flags:
                    if mine.rect.collidepoint(pygame.mouse.get_pos()):
                        self.flags.remove(mine)

        self.check_win()
        self.update_ai()

    def center(self,cell):
        i = cell[0]
        j = cell[1]
        return self.tile_list[i][j].center

    def explore(self, cell):
        """Add cell to self.explored_cells and remove covering tile"""
        y = cell[0]
        x = cell[1]

        if (y, x) not in self.marked_mines:
            # Remove tile empty tile
            for tile in self.tiles:
                if tile.rect.colliderect(self.tile_list[y][x]):
                    self.tiles.remove(tile)
            self.explored_cells.add((y, x))

            # Clicked on bomb
            if self.board[y][x] == "#":
                self.lost = True
                self.game_over = True
                print("Game over.")
                end_bomb = Bomb(self.tile_list[y][x].topleft, (self.rect_width, self.rect_height), True)
                self.mines.add(end_bomb)
                for i in range(self.height):
                    for j in range(self.width):
                        if self.board[i][j] == "#":
                            bomb = Bomb((self.origin[0] + (j * self.rect_width),
                                         self.origin[1] + (i * self.rect_height)),
                                        (self.rect_width, self.rect_height), False)
                            self.mines.add(bomb)

            # Clicked on 0 cell
            elif self.board[y][x] == "0":
                # Automatically explore all neighboring cells, recursively explore all neighboring 0 cells
                for i in range(y - 1, y + 2):
                    for j in range(x - 1, x + 2):
                        if 0 <= j < self.width and 0 <= i < self.height:
                            if (i, j) == (y, x):
                                continue
                            else:
                                if (i, j) not in self.explored_cells:
                                    self.explore((i, j))

            else:
                sentence = Sentence(set(), self.board[y][x], (y, x))
                for i in range(y - 1, y + 2):
                    for j in range(x - 1, x + 2):
                        if 0 <= j < self.width and 0 <= i < self.height:
                            if (i, j) == (y, x):
                                continue
                            else:
                                if (i, j) not in self.explored_cells:
                                    sentence.add((i, j))
                self.knowledge.append(sentence)
            self.update_ai()

    def check_win(self):
        """Called every time an action has been taken to check if player has won"""
        if self.marked_mines == self.real_mines:
            self.won = True
            self.game_over = True

    def reset(self):
        """Reset tile map and all variables"""
        self.tiles = pygame.sprite.Group()
        self.tile_list = []
        self.flags = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.real_mines = set()
        self.explored_cells = set()
        self.marked_mines = set()
        self.knowledge = []
        self.make_board()
        self.number_board()
        self.make_tiles()
        self.game_over = False
        self.won = False
        self.lost = False

    # Ai part
    def update_ai(self):
        """Function called every time a cell is explored or mine flagged to update AI self.knowledge"""
        # Update all sentences with flags
        for mine in self.marked_mines:
            for knowledge in self.knowledge:
                knowledge.flag_mine(mine)

        for knowledge in self.knowledge:
            # Remove cells that have already been explored from sentence
            for cell in knowledge.cells.copy():
                if cell in self.explored_cells:
                    knowledge.cells.remove(cell)

        # Remove sentences that have no cells
        for knowledge in self.knowledge:
            if len(knowledge.cells) == 0:
                self.knowledge.remove(knowledge)

        # Debug stuff
        # print('--------------KNOWLEDGE---------------')
        # print(f'Marked mines: {self.marked_mines}')
        # print(f'Explored cells: {self.explored_cells}')
        # for knowledge in self.knowledge:
        #     print(knowledge)

    def inference(self):
        """Make inferences based on knowledge base if no safe moves are available"""
        for sentence1 in self.knowledge.copy():
            for sentence2 in self.knowledge.copy():
                if sentence2.cells != sentence1.cells:
                    if sentence1.cells.issubset(sentence2.cells):
                        sentence = Sentence(sentence2.cells.difference(sentence1.cells),
                                            sentence2.count - sentence1.count, None)
                        if sentence not in self.knowledge:
                            self.knowledge.append(sentence)

    def ai_move(self):
        """Return AI's move."""
        self.update_ai()
        for knowledge in self.knowledge:
            if len(knowledge.cells) == knowledge.count:
                # Mark mine
                for cell in knowledge.cells:
                    return cell, True
            elif knowledge.count == 0:
                # Explore cell
                for cell in knowledge.cells.copy():
                    return cell, False
            else:
                continue
            break
        else:
            return None

    def ai_random_move(self):
        """"Make random move because no moves are guaranteed"""

        while True:
            i = random.randrange(self.height)
            j = random.randrange(self.width)
            if (i, j) not in self.explored_cells:
                self.explore((i, j))
                return i, j
                break


class Sentence:
    def __init__(self, cells, count, cell):
        self.cells = cells
        self.count = int(count)
        self.cell = cell

    def __str__(self):
        return f"{self.cell}:{self.cells} = {self.count}"

    def add(self, cell):
        self.cells.add(cell)

    def flag_mine(self, mine):
        """Remove mine from sentence because it was flagged"""
        if mine in self.cells:
            self.cells.remove(mine)
            self.count -= 1


class Particle:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.color = 255
        self.radius = 0

    def render(self, screen):
        self.radius += 0.3
        self.color -= 1
        pygame.draw.circle(screen, (self.color, self.color, self.color), (self.x, self.y), self.radius, 1)
