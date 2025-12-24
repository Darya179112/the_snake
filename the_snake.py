import random
import pygame
from pygame.locals import K_DOWN, K_LEFT, K_RIGHT, K_UP, KEYDOWN, QUIT

# Константы игры
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


class GameObject:
    """
    Базовый класс для всех игровых объектов.
    
    Атрибуты:
        position: кортеж (x, y) с координатами объекта
        body_color: кортеж (R, G, B) с цветом объекта
    """

    def __init__(self, position=None, body_color=None):
        """Инициализирует игровой объект."""
        self.position = position if position else (
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод для отрисовки объекта."""
        pass


class Apple(GameObject):
    """
    Класс для представления яблока в игре.
    
    Атрибуты:
        position: кортеж (x, y) с координатами яблока
        body_color: цвет яблока (красный)
    """

    def __init__(self):
        """Инициализирует яблоко со случайной позицией."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию для яблока."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    """
    Класс для представления змейки в игре.
    
    Атрибуты:
        positions: список позиций всех сегментов змейки
        direction: текущее направление движения
        next_direction: следующее направление движения
        body_color: цвет змейки (зеленый)
        length: текущая длина змейки
        last: позиция последнего удаленного сегмента
    """

    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на одну клетку в текущем направлении."""
        head_x, head_y = self.get_head_position()

        # Вычисляем новую позицию головы
        dx, dy = self.direction
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_position = (new_x, new_y)

        # Проверяем столкновение с собой
        if new_position in self.positions[1:]:
            self.reset()
            return

        # Сохраняем последнюю позицию для стирания
        self.last = self.positions[-1] if len(self.positions) > 0 else None

        # Добавляем новую голову
        self.positions.insert(0, new_position)

        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на игровой поверхности."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)

        # Стираем последний удаленный сегмент
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления движения змейки.
    
    Аргументы:
        snake: экземпляр класса Snake
    """
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция игры, содержащая главный игровой цикл."""
    pygame.init()

    # Создание игрового окна
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')

    # Создание игровых объектов
    snake = Snake()
    apple = Apple()

    # Создание часов для контроля FPS
    clock = pygame.time.Clock()

    # Главный игровой цикл
    while True:
        # Обработка событий
        handle_keys(snake)

        # Обновление направления змейки
        snake.update_direction()

        # Перемещение змейки
        snake.move()

        # Проверка, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убеждаемся, что яблоко не появилось на змейке
            while apple.position in snake.positions:
                apple.randomize_position()

        # Отрисовка игрового поля
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Отрисовка игровых объектов
        snake.draw(screen)
        apple.draw(screen)

        # Обновление экрана
        pygame.display.update()

        # Контроль FPS
        clock.tick(10)


if __name__ == '__main__':
    main()
    