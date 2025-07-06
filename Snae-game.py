

import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# ------------ CONFIGURATION ------------
BLOCK = 20  # size of one square block (pixels)
GRID_W, GRID_H = 32, 24  # grid size → window will be BLOCK * GRID_W/H
WIDTH, HEIGHT = BLOCK * GRID_W, BLOCK * GRID_H
FPS = 10  # frames per second (increase for faster snake)

# Colors (R, G, B)
BG_COLOR = (30, 30, 30)
SNAKE_COLOR = (50, 205, 50)
FOOD_COLOR = (220, 20, 60)
GRID_COLOR = (40, 40, 40)
TEXT_COLOR = (200, 200, 200)

# Directions (dx, dy)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake — Simple Pygame Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)

def draw_grid():
    """Optional: draw subtle grid lines for reference."""
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_rect(color, pos):
    pygame.draw.rect(
        screen,
        color,
        pygame.Rect(pos[0] * BLOCK, pos[1] * BLOCK, BLOCK, BLOCK),
    )

def spawn_food(snake):
    """Return a random position not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_W - 1), random.randint(0, GRID_H - 1))
        if pos not in snake:
            return pos

def show_text(text, center):
    surface = font.render(text, True, TEXT_COLOR)
    rect = surface.get_rect(center=center)
    screen.blit(surface, rect)


def main():
    snake = [(GRID_W // 2, GRID_H // 2)]  # list of (x, y) tuples; head at index 0
    direction = RIGHT
    food = spawn_food(snake)
    score = 0
    game_over = False

    while True:
        # ---------- Event Handling ----------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key in (pygame.K_UP, pygame.K_w) and direction != DOWN:
                    direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s) and direction != UP:
                    direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a) and direction != RIGHT:
                    direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and direction != LEFT:
                    direction = RIGHT
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN and game_over:
                # Restart on any key after game over
                main()
                return

        if not game_over:
            # ---------- Move Snake ----------
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            # Check collisions with walls
            if (
                new_head[0] < 0
                or new_head[0] >= GRID_W
                or new_head[1] < 0
                or new_head[1] >= GRID_H
                or new_head in snake
            ):
                game_over = True
            else:
                snake.insert(0, new_head)  # add new head
                # Eat food
                if new_head == food:
                    score += 1
                    food = spawn_food(snake)
                else:
                    snake.pop()  # remove tail if no food eaten

        # ---------- Drawing ----------
        screen.fill(BG_COLOR)
        draw_grid()
        draw_rect(FOOD_COLOR, food)
        for pos in snake:
            draw_rect(SNAKE_COLOR, pos)

        show_text(f"Score: {score}", (70, 20))

        if game_over:
            show_text("GAME OVER — press any key to restart", (WIDTH // 2, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
