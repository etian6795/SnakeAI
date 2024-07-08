import pygame
import time
import random

class Snake:
    def __init__(self, game_width, game_height):
        # set game dimensions and tile size
        self.tile_size = 25
        self.game_width = game_width
        self.game_height = game_height
        # initialize some properties
        self.head = [game_width//2, game_height//2]
        self.tails = []
        self.vel = [1, 0]
        self.length = 4
        self.open_tiles = set([])
        # set of open tiles for places to put apple
        for i in range(0, self.game_width):
            for j in range(0, self.game_height):
                self.open_tiles.add(i+j*self.game_width)
        # start with length of 4
        for i in range(3):
            self.tails.append([self.head[0] - (3-i), self.head[1]])
            self.open_tiles.remove(self.head[0] - (3-i) + self.head[1]*self.game_width)
        self.open_tiles.remove(self.head[0] + self.head[1]*self.game_width)

    def runGame(self, ai, ham_cyc):
        # start pygame screen
        pygame.init()
        pygame.display.set_caption('snake')
        self.screen = pygame.display.set_mode((self.game_width * self.tile_size, self.game_height * self.tile_size))
        self.fps = pygame.time.Clock()
        # place fruit
        self.fruit_pos = random.choice(list(self.open_tiles))
        self.open_tiles.remove(self.fruit_pos)
        # start game logic
        while True:
            # check for a key input
            event = ai.get_move()
            if event == 'U' and self.vel != [0, 1]:
                self.vel = [0, -1]
            elif event == 'D' and self.vel != [0, -1]:
                self.vel = [0, 1]
            elif event == 'L' and self.vel != [1, 0]:
                self.vel = [-1, 0]
            elif event == 'R' and self.vel != [-1, 0]:
                self.vel = [1, 0]
            # move snake
            self.move()
            # check bounds for game over
            if self.head[0] < 0 or self.head[1] < 0 or self.head[0] >= self.game_width or self.head[1] >= self.game_height or self.head in self.tails:
                pygame.quit()
                return
            # draw game state
            self.screen.fill((15, 15, 15)) # black color for background
            self.draw_path(ham_cyc)
            self.draw_snake()

            pygame.display.update()
            self.fps.tick(10)

    def draw_snake(self):
        # green color for snake
        pygame.draw.rect(self.screen, (43, 140, 24), pygame.Rect(self.head[0] * self.tile_size, self.head[1] * self.tile_size, self.tile_size-1, self.tile_size-1))
        # draw eyes
        if self.vel == [1, 0]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [-1, 0]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [0, 1]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + 3 * self.tile_size//5, self.tile_size//5, self.tile_size//5))
        elif self.vel == [0, -1]:
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
            pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(self.head[0] * self.tile_size + 3 * self.tile_size//5, self.head[1] * self.tile_size + self.tile_size//5, self.tile_size//5, self.tile_size//5))
        prev_x = self.head[0]
        prev_y = self.head[1]
        idx = len(self.tails)-1
        while idx >= 0:
            pygame.draw.rect(self.screen, (43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, self.tails[idx][1] * self.tile_size, self.tile_size-1, self.tile_size-1))  # green color for snake
            from_dir = self.dir(prev_x, prev_y, self.tails[idx][0], self.tails[idx][1])
            # based on where the previous segment is, make the current segment connect with it
            if from_dir == 'U':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, self.tails[idx][1] * self.tile_size -1, self.tile_size-1, 1))
            if from_dir == 'D':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size, (self.tails[idx][1]+1) * self.tile_size -1, self.tile_size-1, 1))
            if from_dir == 'L':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect(self.tails[idx][0] * self.tile_size -1, self.tails[idx][1] * self.tile_size, 1, self.tile_size-1))
            if from_dir == 'R':
                pygame.draw.rect(self.screen,(43, 140, 24), pygame.Rect((self.tails[idx][0]+1) * self.tile_size -1, self.tails[idx][1] * self.tile_size, 1, self.tile_size-1))
            prev_x = self.tails[idx][0]
            prev_y = self.tails[idx][1]
            idx-=1
        # red color for apple
        pygame.draw.rect(self.screen, (198, 41, 41), pygame.Rect((self.fruit_pos%self.game_width) * self.tile_size, (self.fruit_pos//self.game_width) * self.tile_size, self.tile_size, self.tile_size)) #red color for apple

    def dir(self, x1, y1, x2, y2):
        if x1 == x2:
            if y1 < y2:
                return 'U'
            else:
                return 'D'
        elif y1 == y2:
            if x1 < x2:
                return 'L'
            else:
                return 'R'

    def draw_path(self, ham_cyc):
        dir = [0, 1, 0, -1, 0]
        for i in range(self.game_height):
            for j in range(self.game_width):
                for k in range(4):
                    ni = i+dir[k]
                    nj = j + dir[k+1]
                    if ni >= 0 and ni < self.game_height and nj >= 0 and nj < self.game_width and ham_cyc[ni][nj] == (ham_cyc[i][j]+1)%(self.game_height*self.game_width):
                        pygame.draw.line(self.screen, (221, 213, 213), [j*self.tile_size + self.tile_size//2, i*self.tile_size + self.tile_size//2], [nj*self.tile_size + self.tile_size//2, ni*self.tile_size + self.tile_size//2])

    def move(self):
        self.tails.append([self.head[0], self.head[1]])
        self.head[0] += self.vel[0]
        self.head[1] += self.vel[1]
        if self.fruit_pos != self.head[0] + self.head[1]*self.game_width:
            self.open_tiles.add(self.tails[0][0] + self.tails[0][1]*self.game_width)
            del self.tails[0]
            if self.head[0] + self.head[1]*self.game_width in self.open_tiles:
                self.open_tiles.remove(self.head[0] + self.head[1]*self.game_width)
        else:
            self.length += 1
            if len(self.open_tiles) == 0:
                self.game_over()
                return
            self.fruit_pos = random.choice(list(self.open_tiles))
            self.open_tiles.remove(self.fruit_pos)

    def game_over(self):
        # creating font object
        my_font = pygame.font.SysFont('times new roman', 50)
        # creating a text surface to draw text
        game_over_surface = my_font.render('You Won!', True, 'blue')
        # create a rectangular object for the text surface object
        game_over_rect = game_over_surface.get_rect()
        # setting position of the text
        game_over_rect.midtop = (self.game_width/2, self.game_height/4)
        # blit will draw the text on screen
        self.screen.blit(game_over_surface, game_over_rect)
        pygame.display.flip()
        # quit after 2 seconds
        time.sleep(2)
        pygame.quit()
