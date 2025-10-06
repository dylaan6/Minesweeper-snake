import pygame
import random
import threading
import tkinter as tk
from multiprocessing import Process

def run_snake_game(shared_game_over):
    pygame.init()
    WIDTH, HEIGHT = 1000, 700
    CELL_SIZE = 20

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = [(WIDTH // 2, HEIGHT // 2)]
    snake_dir = (0, 0)

    food_amount = 5
    foods = [pygame.Rect(random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
                         random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE),
                         CELL_SIZE, CELL_SIZE)
             for _ in range(food_amount)]

    font = pygame.font.Font(None, 36)

    # Tkinter slider window
    def slider_window():
        nonlocal food_amount, foods
        root = tk.Tk()
        root.title("Food Amount Slider")
        slider = tk.Scale(root, from_=1, to=50, orient="horizontal", label="Food Amount")
        slider.set(food_amount)

        def update_value(val):
            nonlocal food_amount, foods
            food_amount = int(val)
            foods = [pygame.Rect(random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
                                 random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE),
                                 CELL_SIZE, CELL_SIZE)
                     for _ in range(food_amount)]

        slider.config(command=update_value)
        slider.pack(padx=20, pady=20)
        root.mainloop()

    threading.Thread(target=slider_window, daemon=True).start()

    while not shared_game_over.value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shared_game_over.value = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and snake_dir != (0, CELL_SIZE):
            snake_dir = (0, -CELL_SIZE)
        elif keys[pygame.K_DOWN] and snake_dir != (0, -CELL_SIZE):
            snake_dir = (0, CELL_SIZE)
        elif keys[pygame.K_LEFT] and snake_dir != (CELL_SIZE, 0):
            snake_dir = (-CELL_SIZE, 0)
        elif keys[pygame.K_RIGHT] and snake_dir != (-CELL_SIZE, 0):
            snake_dir = (CELL_SIZE, 0)

        if snake_dir != (0, 0):
            head = (snake[0][0] + snake_dir[0], snake[0][1] + snake_dir[1])
            head = (head[0] % WIDTH, head[1] % HEIGHT)
            snake.insert(0, head)

            # Self-collision
            if head in snake[1:]:
                shared_game_over.value = True
                break

            ate_food = False
            for f in foods:
                if pygame.Rect(head, (CELL_SIZE, CELL_SIZE)).colliderect(f):
                    ate_food = True
                    f.topleft = (random.randrange(0, WIDTH - CELL_SIZE, CELL_SIZE),
                                 random.randrange(0, HEIGHT - CELL_SIZE, CELL_SIZE))
                    break

            if not ate_food:
                snake.pop()

        # Drawing
        screen.fill((0, 0, 0))
        for pos in snake:
            pygame.draw.rect(screen, (0, 255, 0), (pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        for f in foods:
            pygame.draw.rect(screen, (255, 0, 0), f)
        score_text = font.render(f"Score: {len(snake)-1}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(15)

    pygame.quit()
