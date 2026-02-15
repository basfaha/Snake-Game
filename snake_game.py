import random
import time
import os
import msvcrt
from collections import deque

# Game settings
WIDTH = 40
HEIGHT = 20
SNAKE_CHAR = '█'
FOOD_CHAR = '●'
EMPTY_CHAR = ' '

class SnakeGame:
    def __init__(self):
        self.snake = deque([(HEIGHT//2, WIDTH//2)])
        self.direction = (0, 1)  # (row, col) - start moving right
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        
    def spawn_food(self):
        while True:
            food = (random.randint(1, HEIGHT-2), random.randint(1, WIDTH-2))
            if food not in self.snake:
                return food
    
    def get_input(self):
        if msvcrt.kbhit():
            try:
                key = msvcrt.getch()
                
                # Handle special keys (arrow keys start with 0xe0 or 0x00)
                if key in (b'\xe0', b'\x00'):
                    # Read the second byte for arrow keys
                    key = msvcrt.getch()
                    if key == b'H' and self.direction != (1, 0):  # Up arrow
                        self.direction = (-1, 0)
                    elif key == b'P' and self.direction != (-1, 0):  # Down arrow
                        self.direction = (1, 0)
                    elif key == b'K' and self.direction != (0, 1):  # Left arrow
                        self.direction = (0, -1)
                    elif key == b'M' and self.direction != (0, -1):  # Right arrow
                        self.direction = (0, 1)
                else:
                    # Handle regular keys (WASD)
                    key = key.decode('utf-8').lower()
                    if key == 'w' and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif key == 's' and self.direction != (-1, 0):
                        self.direction = (1, 0)
                    elif key == 'a' and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif key == 'd' and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif key == 'q':
                        self.game_over = True
            except:
                pass  # Ignore any other problematic keys
    
    def update(self):
        # Calculate new head position
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Check collisions
        if (new_head[0] <= 0 or new_head[0] >= HEIGHT-1 or
            new_head[1] <= 0 or new_head[1] >= WIDTH-1 or
            new_head in self.snake):
            self.game_over = True
            return
        
        # Add new head
        self.snake.appendleft(new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()  # Remove tail
    
    def draw(self):
        os.system('cls')
        
        # Create board
        board = [[EMPTY_CHAR for _ in range(WIDTH)] for _ in range(HEIGHT)]
        
        # Draw borders
        for i in range(HEIGHT):
            board[i][0] = board[i][WIDTH-1] = '|'
        for j in range(WIDTH):
            board[0][j] = board[HEIGHT-1][j] = '-'
        board[0][0] = '+'
        board[0][WIDTH-1] = '+'
        board[HEIGHT-1][0] = '+'
        board[HEIGHT-1][WIDTH-1] = '+'
        
        # Draw food
        board[self.food[0]][self.food[1]] = FOOD_CHAR
        
        # Draw snake
        for i, segment in enumerate(self.snake):
            if i == 0:
                board[segment[0]][segment[1]] = 'O'  # Head
            else:
                board[segment[0]][segment[1]] = SNAKE_CHAR
        
        # Print board
        for row in board:
            print(''.join(row))
        
        print(f"\nScore: {self.score} | Controls: WASD or Arrow Keys, Q to quit")
        
    def run(self):
        while not self.game_over:
            self.draw()
            self.get_input()
            self.update()
            time.sleep(0.15)  # Game speed
        
        # Game over screen
        self.draw()
        print(f"\nGAME OVER! Final Score: {self.score}")

if __name__ == "__main__":
    print("Terminal Snake Game")
    print("Use WASD or Arrow Keys to move, Q to quit")
    print("Press Enter to start...")
    input()
    
    game = SnakeGame()

    game.run()
