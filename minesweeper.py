import pygame
import random

def run_minesweeper(shared_game_over):
    pygame.init()
    WIDTH, HEIGHT = 400, 400
    ROWS, COLS = 10, 10
    CELL_SIZE = WIDTH // COLS
    MINES = 15

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")
    font = pygame.font.Font(None, 30)

    # Colors
    BG_COLOR = (200, 200, 200)
    HIDDEN_COLOR = (160, 160, 160)
    REVEALED_COLOR = (220, 220, 220)
    MINE_COLOR = (255, 0, 0)
    FLAG_COLOR = (0, 0, 255)
    TEXT_COLOR = (0, 0, 0)

    # Grid setup
    def create_grid():
        grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        mines = set()
        while len(mines) < MINES:
            r = random.randrange(ROWS)
            c = random.randrange(COLS)
            mines.add((r, c))
        for r, c in mines:
            grid[r][c] = -1
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == -1:
                    continue
                count = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < ROWS and 0 <= nc < COLS:
                            if grid[nr][nc] == -1:
                                count += 1
                grid[r][c] = count
        return grid

    grid = create_grid()
    revealed = [[False]*COLS for _ in range(ROWS)]
    flags = [[False]*COLS for _ in range(ROWS)]
    game_over = False
    won = False

    def reveal(r, c):
        if revealed[r][c] or flags[r][c]:
            return
        revealed[r][c] = True
        if grid[r][c] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        reveal(nr, nc)

    def check_win():
        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] != -1 and not revealed[r][c]:
                    return False
        return True

    while not shared_game_over.value:
        screen.fill(BG_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shared_game_over.value = True
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                r, c = y // CELL_SIZE, x // CELL_SIZE
                if event.button == 1:
                    if grid[r][c] == -1:
                        shared_game_over.value = True
                        game_over = True
                    else:
                        reveal(r, c)
                        if check_win():
                            won = True
                            game_over = True
                elif event.button == 3:
                    flags[r][c] = not flags[r][c]

        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if revealed[r][c]:
                    pygame.draw.rect(screen, REVEALED_COLOR, rect)
                    if grid[r][c] > 0:
                        text = font.render(str(grid[r][c]), True, TEXT_COLOR)
                        screen.blit(text, (c*CELL_SIZE+10, r*CELL_SIZE+5))
                else:
                    pygame.draw.rect(screen, HIDDEN_COLOR, rect)
                    if flags[r][c]:
                        pygame.draw.circle(screen, FLAG_COLOR, rect.center, CELL_SIZE//4)
                pygame.draw.rect(screen, (0,0,0), rect, 1)
                if game_over and grid[r][c] == -1:
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, CELL_SIZE//3)

        if game_over:
            msg = "You Win!" if won else "Game Over!"
            text = font.render(msg, True, (0,0,0))
            screen.blit(text, (WIDTH//2-50, HEIGHT//2-10))

        pygame.display.flip()

    pygame.quit()
