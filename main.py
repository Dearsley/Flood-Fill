import pygame as pg

# Настройки размеров
WIDTH, HEIGHT = 1280, 720
CELL_SIZE = 20
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE

# Цвета
COLORS = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GRAY": (200, 200, 200)
}

# Инициализация
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Flood Fill")
clock = pg.time.Clock()

grid = [[COLORS["WHITE"] for _ in range(COLS)] for _ in range(ROWS)]


def draw_grid():
    for rw in range(ROWS):
        for col in range(COLS):
            rect = pg.Rect(col * CELL_SIZE, rw * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, grid[rw][col], rect)
            pg.draw.rect(screen, COLORS["GRAY"], rect, 1)


def flood_fill(col, rw, target_color, fill_color):
    if target_color == fill_color or grid[rw][col] != target_color:
        return

    queue = [(col, rw)]
    while queue:
        cur_column, cur_row = queue.pop(0)

        if grid[cur_row][cur_column] == target_color:
            grid[cur_row][cur_column] = fill_color

            if cur_column > 0:
                queue.append((cur_column - 1, cur_row))
            if cur_column < COLS - 1:
                queue.append((cur_column + 1, cur_row))
            if cur_row > 0:
                queue.append((cur_column, cur_row - 1))
            if cur_row < ROWS - 1:
                queue.append((cur_column, cur_row + 1))


# === Main ===
running = True
mouse_down = False
while running:
    screen.fill(COLORS["WHITE"])
    draw_grid()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        elif event.type == pg.KEYDOWN and event.key == pg.K_c:
            grid = [[COLORS["WHITE"]] * COLS for _ in range(ROWS)]  # Очистка

        elif event.type == pg.MOUSEBUTTONDOWN:
            column, row = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE

            if event.button == 1:
                mouse_down = True
                grid[row][column] = COLORS["BLACK"]

            elif event.button == 3:
                flood_fill(column, row, grid[row][column], COLORS["BLACK"])

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            mouse_down = False

    if mouse_down:
        column, row = pg.mouse.get_pos()
        column //= CELL_SIZE
        row //= CELL_SIZE
        
        if 0 <= column < COLS and 0 <= row < ROWS:
            grid[row][column] = COLORS["BLACK"]

    pg.display.flip()
    clock.tick(300)

pg.quit()
