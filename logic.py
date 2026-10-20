import random
import math

class Ball:
    """Представляет один игровой шарик."""
    def __init__(self, x, y, vx, vy, color, radius=20):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        # Цвет представлен как список [R, G, B]
        self.color = list(color)
        self.radius = radius

    def update_position(self, width, height):
        """Обновляет координаты и обрабатывает отскоки от границ."""
        self.x += self.vx
        self.y += self.vy

        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.vy *= -1

    def mix_color(self, other_ball):
        """Смешивает цвета двух шариков."""
        # Вычисляем среднее значение для каждого канала RGB
        new_color = [
            int((self.color[0] + other_ball.color[0]) / 2),
            int((self.color[1] + other_ball.color[1]) / 2),
            int((self.color[2] + other_ball.color[2]) / 2)
        ]

        # Чтобы избежать быстрого превращения в серый/белый,
        # добавляем небольшую случайную вариативность (насыщенность)
        for i in range(3):
            new_color[i] = max(0, min(255, new_color[i] + random.randint(-10, 10)))

        self.color = new_color
        other_ball.color = list(new_color)

    def get_distance(self, other_x, other_y):
        """Вычисляет расстояние до заданной точки."""
        return math.sqrt((self.x - other_x)**2 + (self.y - other_y)**2)


class GameLogic:
    """Управляет всей игровой логикой взаимодействия."""
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.balls = []       # Шарики на экране
        self.inventory = []   # Шарики в инвентаре

        # Зона удаления: прямоугольник в правом нижнем углу
        self.trash_zone = {
            'x_start': width - 100,
            'y_start': height - 100,
            'x_end': width,
            'y_end': height
        }

    def add_ball(self, x, y, vx, vy, color):
        """Добавляет новый шарик в игру."""
        self.balls.append(Ball(x, y, vx, vy, color))

    def update(self):
        """Основной цикл обновления состояния мира."""
        # 1. Движение
        for ball in self.balls:
            ball.update_position(self.width, self.height)

        # 2. Смешивание цветов при касании
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                b1 = self.balls[i]
                b2 = self.balls[j]
                if b1.get_distance(b2.x, b2.y) <= (b1.radius + b2.radius):
                    b1.mix_color(b2)

        # 3. Удаление шариков в зоне удаления
        self.balls = [
            ball for ball in self.balls
            if not (self.trash_zone['x_start'] < ball.x < self.trash_zone['x_end'] and
                    self.trash_zone['y_start'] < ball.y < self.trash_zone['y_end'])
        ]

    def absorb_ball(self, mouse_x, mouse_y, radius=30):
        """'Всасывание' ближайшего шарика в инвентарь."""
        closest_ball = None
        min_dist = radius

        for ball in self.balls:
            dist = ball.get_distance(mouse_x, mouse_y)
            if dist < min_dist:
                min_dist = dist
                closest_ball = ball

        if closest_ball:
            self.balls.remove(closest_ball)
            self.inventory.append(closest_ball)
            return True
        return False

    def spit_ball(self, mouse_x, mouse_y):
        """'Выплевывание' шарика из инвентаря обратно на экран."""
        if self.inventory:
            ball = self.inventory.pop()
            ball.x = mouse_x
            ball.y = mouse_y
            # При выплевывании даем случайный небольшой импульс
            ball.vx = random.uniform(-2, 2)
            ball.vy = random.uniform(-2, 2)
            self.balls.append(ball)
            return True
        return False
