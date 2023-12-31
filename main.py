import pygame

pygame.init()

window_size = (800, 800)
game_window = pygame.display.set_mode(window_size)

resolution = (200, 200)
pixel_size = (window_size[0] // resolution[0], window_size[1] // resolution[1])

clock = pygame.time.Clock()
fps = 150

# creates layer 1 and draws every square
layers = [{}, {}, {}]
for y in range(resolution[1]):
    for x in range(resolution[0]):
        layers[0][(x, y)] = {"rect": pygame.Rect((x * pixel_size[0], y * pixel_size[1]), pixel_size), "colour": (255, 255, 255)}
        pygame.draw.rect(game_window, layers[0][(x, y)]["colour"], layers[0][(x, y)]["rect"])
pygame.display.update()

draw_list = []
last_mouse_pos = None


def draw(layer_num, coord, color):
    coord = (min(resolution[0] - 1, max(0, coord[0])), min(resolution[1] - 1, max(0, coord[1])))

    square = layers[layer_num][coord]
    square['colour'] = color

    draw_list.append(square["rect"])
    pygame.draw.rect(game_window, color, square['rect'])


def draw_line(start, end, color, thickness=1):
    # Calculate differences
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    x_sign = 1 if dx > 0 else -1
    y_sign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    # Ensure thickness is at least 1
    thickness = max(1, thickness)

    # Draw the central line
    def draw_line_single(xx, yy):
        draw(0, (xx, yy), color)

    if dx > dy:
        yy_range = [int(round(start[1] + (dy / dx) * y_sign * step)) if dx != 0 else start[1] for step in range(dx + 1)]
        for offset in range(-(thickness // 2), (thickness // 2) + 1):
            for idx, xx in enumerate(range(start[0], end[0] + x_sign, x_sign)):
                yy = yy_range[min(idx, len(yy_range) - 1)] + offset
                draw_line_single(xx, yy)

    else:
        xx_range = [int(round(start[0] + (dx / dy) * x_sign * step)) if dy != 0 else start[0] for step in range(dy + 1)]
        for offset in range(-(thickness // 2), (thickness // 2) + 1):
            for idx, yy in enumerate(range(start[1], end[1] + y_sign, y_sign)):
                xx = xx_range[min(idx, len(xx_range) - 1)] + offset
                draw_line_single(xx, yy)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEMOTION:
            if event.buttons[0] == 1:
                mouse_coord = (event.pos[0] // pixel_size[0], event.pos[1] // pixel_size[1])
                if last_mouse_pos:
                    draw_line(last_mouse_pos, mouse_coord, (0, 255, 0), 5)
                else:
                    draw(0, mouse_coord, (0, 255, 0))
                last_mouse_pos = mouse_coord
            else:
                last_mouse_pos = None

    pygame.display.update(draw_list)
    draw_list.clear()

    clock.tick(fps)
    real_fps = clock.get_fps()
    pygame.display.set_caption(f'FPS: {real_fps:.2f}')
