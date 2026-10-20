import pygame
import random
from logic import GameLogic

# ================= CONFIGURATION =================
START_BALLS_COUNT = 15
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
# =================================================

def get_random_color():
    """Генерирует случайный яркий цвет."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    # Инициализация Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Ball Mixing Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # Инициализация логики
    game = GameLogic(WINDOW_WIDTH, WINDOW_HEIGHT)

    # Создание стартовых шариков
    for _ in range(START_BALLS_COUNT):
        game.add_ball(
            x=random.randint(20, WINDOW_WIDTH - 20),
            y=random.randint(20, WINDOW_HEIGHT - 20),
            vx=random.uniform(-3, 3),
            vy=random.uniform(-3, 3),
            color=get_random_color()
        )

    running = True
    while running:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if event.button == 1: # ЛКМ - всасывание
                    game.absorb_ball(mx, my)
                elif event.button == 3: # ПКМ - выплевывание
                    game.spit_ball(mx, my)

        # 2. Обновление логики
        game.update()

        # 3. Отрисовка
        screen.fill((255, 255, 255)) # Белый фон

        # Отрисовка зоны удаления (полупрозрачный красный прямоугольник)
        trash_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        trash_surf.fill((255, 0, 0, 80)) # Красный с прозрачностью
        screen.blit(trash_surf, (game.trash_zone['x_start'], game.trash_zone['y_start']))

        trash_text = font.render("УДАЛЕНИЕ", True, (150, 0, 0))
        screen.blit(trash_text, (game.trash_zone['x_start'] + 10, game.trash_zone['y_start'] + 40))

        # Отрисовка шариков на экране
        for ball in game.balls:
            pygame.draw.circle(screen, ball.color, (int(ball.x), int(ball.y)), ball.radius)
            # Добавим легкую обводку для красоты
            pygame.draw.circle(screen, (50, 50, 50), (int(ball.x), int(ball.y)), ball.radius, 1)

        # Отрисовка инвентаря (в верхней части экрана)
        inventory_text = font.render(f"Инвентарь: {len(game.inventory)}", True, (0, 0, 0))
        screen.blit(inventory_text, (10, 10))

        # Рисуем маленькие превью шариков в инвентаре
        for i, ball in enumerate(game.inventory):
            # Рисуем в ряд с отступом
            pygame.draw.circle(screen, ball.color, (60 + i*25, 20), 8)
            pygame.draw.circle(screen, (50, 50, 50), (60 + i*25, 20), 8, 1)

        # Подсказка по управлению
        controls_text = font.render("ЛКМ: Всосать | ПКМ: Выплюнуть", True, (100, 100, 100))
        screen.blit(controls_text, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
