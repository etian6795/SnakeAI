from Snake import Snake
from HamiltonianCycle import HamiltonianCycle

class SnakeAI:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        # create game board and Hamiltonian Cycle
        self.snake = Snake(m, n)
        self.ham_cyc = HamiltonianCycle(m, n).cycle
        # start game
        self.snake.runGame(self, self.ham_cyc)

    def get_move(self):
        # get positions of head and tail of snake
        head_x = self.snake.head[0]
        head_y = self.snake.head[1]
        head_val = self.ham_cyc[head_y][head_x]
        tail_x = self.snake.tails[0][0]
        tail_y = self.snake.tails[0][1]
        tail_val = self.ham_cyc[tail_y][tail_x]
        fruit_val = self.ham_cyc[self.snake.fruit_pos//self.n][self.snake.fruit_pos%self.n]
        len = self.snake.length
        dir = [0, 1, 0, -1, 0]
        dir_res = ['R', 'D', 'L', 'U']
        if len >= 3*(self.m*self.n)//4:
            for i in range(4):
                if head_y+dir[i] >= 0 and head_y+dir[i] < self.m and head_x+dir[i+1] >= 0 and head_x+dir[i+1] < self.n and self.ham_cyc[head_y+dir[i]][head_x+dir[i+1]] == (head_val+1)%(self.m*self.n):
                    return dir_res[i]
        else:
            best_dist = 1000000000
            best_dir = ' '
            for i in range(4):
                if head_y+dir[i] >= 0 and head_y+dir[i] < self.m and head_x+dir[i+1] >= 0 and head_x+dir[i+1] < self.n and self.ham_cyc[head_y+dir[i]][head_x+dir[i+1]] == (head_val+1)%(self.m*self.n):
                    best_dir = dir_res[i]
            if head_val > tail_val:
                if fruit_val < tail_val:
                    fruit_val += self.m*self.n
                for i in range(4):
                    next_y = head_y + dir[i]
                    next_x = head_x + dir[i+1]
                    if next_y >= 0 and next_y < self.m and next_x >= 0 and next_x < self.n: 
                        next_val = self.ham_cyc[next_y][next_x]
                        if next_val < tail_val:
                            next_val += self.m*self.n
                        if next_val > head_val and next_val <= fruit_val and next_val <= tail_val+self.m*self.n:
                            if fruit_val - next_val < best_dist:
                                best_dist = fruit_val - next_val
                                best_dir = dir_res[i]
            else:
                for i in range(4):
                    next_y = head_y + dir[i]
                    next_x = head_x + dir[i+1]
                    if next_y >= 0 and next_y < self.m and next_x >= 0 and next_x < self.n:  
                        next_val = self.ham_cyc[next_y][next_x]
                        if next_val > head_val and next_val <= tail_val and next_val <= fruit_val:
                            if fruit_val - next_val < best_dist:
                                best_dist = fruit_val - next_val
                                best_dir = dir_res[i]
            return best_dir
                  
ai = SnakeAI(10, 10)