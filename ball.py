import pygame
import sys
import math
import random

pygame.init()
WIDTH, HEIGHT, TAB = 800, 600, 300
FPS = 60

BG = '#1e1e1e'
TEXT = '#c4c4c4'
LIGHTBLUE = '#b0b5ff'
BLUE = '#8AB4F7'
GREEN = '#8af7b4'
RED = '#f7918a'
YELLOW = '#f6f78a'
PINK = '#f5b2f1'

MAIN_MENU = 'main menu'
UPGRADES_SCREEN = 'upgrades screen'
XY_CANVAS = 'xy canvas'

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GUI")

font_large = pygame.font.SysFont(None, 64)
font_medium = pygame.font.SysFont(None, 36)
font_small = pygame.font.SysFont(None, 18)

clock = pygame.time.Clock()
current_state = MAIN_MENU
class Stats:
    def __init__(self, money, duration, speed, size, broke, quantity, wall_gain, star_quantity, star_value, star_size, final_multiplier):
        self.money = money
        self.duration = duration
        self.speed = speed
        self.size = size
        self.broke = broke
        self.quantity = quantity
        self.wall_gain = wall_gain
        self.star_quantity = star_quantity
        self.star_value = star_value
        self.star_size = star_size
        self.final_multiplier = final_multiplier

stats = Stats(
    0,
    5000,
    3,
    3,
    False,
    1,
    1,
    3,
    50,
    5,
    1
)

circle_y = HEIGHT // 2 - 100
circle_direction = 1

def main_menu():
    global circle_y, circle_direction

    screen.fill(BG)
    
    if circle_y <= 50 or circle_y >= HEIGHT // 2 - 100:
        circle_direction *= -1
    circle_y += circle_direction * 2
    pygame.draw.circle(screen, random.choice([BLUE, PINK]), (WIDTH // 2, circle_y), 10)
    menu_text = font_large.render('Welcome to Bounce', True, BLUE)
    screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, 
                            HEIGHT // 2 - menu_text.get_height() // 2))

    start_text = font_medium.render('(Press Any Key to Continue..)', True, TEXT)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, 
                             HEIGHT // 2 - start_text.get_height() // 2 + menu_text.get_height()))

    author_text = font_small.render('Created by Yours Truly: Nicholas Soliman', True, TEXT)
    screen.blit(author_text, (WIDTH // 2 - author_text.get_width() // 2, HEIGHT - 50))

    pygame.display.flip()

class Node:
    def __init__(self, x, y, costs, name, desc, rank=0):
        self.x = x
        self.y = y
        self.costs = costs
        self.name = name
        self.rank = rank
        self.desc = desc
        self.neighbors = []

    def draw(self):
        color = TEXT if self.rank > 0 else (100, 100, 100)
        pygame.draw.rect(screen, color, (self.x, self.y, 50, 50), 2)
        if self.rank > 0:
            rank_text = font_small.render(str(self.rank), True, TEXT)
            screen.blit(rank_text, (self.x + 25 - rank_text.get_width() // 2, self.y + 25 - rank_text.get_height() // 2))

nodes = [
    Node(WIDTH // 2 - 25 - TAB // 2, HEIGHT // 2 - 25, [round(pow(1.25, i)) for i in range(1, 100)], 'Speed', 'Adds 1px/sec', rank=1),
    Node(WIDTH // 2 - 25 - TAB // 2, HEIGHT // 2 - 85, [round(pow(2, i)) for i in range(1, 100)], 'Duration', 'Adds 1 Second', rank=0),
    Node(WIDTH // 2 - 85 - TAB // 2, HEIGHT // 2 - 25, [round(pow(4, i)) for i in range(1, 100)], 'Quantity', 'Adds 1 Extra Blue Ball', rank=0),
    Node(WIDTH // 2 + 35 - TAB // 2, HEIGHT // 2 - 25, [round(pow(3, i)) for i in range(1, 100)], 'Wall Gain', 'Increase profits per hit + $1', rank=0),
    Node(WIDTH // 2 - 85 - TAB // 2, HEIGHT // 2 - 85, [round(pow(2, i)) for i in range(1, 100)], 'Size', 'Adds 0.5px Radius', rank=0),
    Node(WIDTH // 2 - 25 - TAB // 2, HEIGHT // 2 + 35, [round(pow(2.25, i)) for i in range(1, 100)], 'Star Size', 'Adds 0.5px Radius', rank=0),
    Node(WIDTH // 2 - 85 - TAB // 2, HEIGHT // 2 + 35, [round(pow(3, i)) for i in range(1, 100)], 'Star Value', 'Adds $200', rank=0),
    Node(WIDTH // 2 + 35 - TAB // 2, HEIGHT // 2 + 35, [round(pow(3, i)) for i in range(1, 100)], 'Star Quantity', 'Adds 1 Star', rank=0),
    Node(WIDTH // 2 + 35 - TAB // 2, HEIGHT // 2 - 85, [10000, 50000, 10**5, 10**6, 10**7, 10**8], 'Double Income', 'Doubles Final Income After Run', rank=0)
]
# list(range(10, 10001, 1000))
selected_node = nodes[0]

def reveal_neighbors(node):
    if node.rank > 0:
        for neighbor in node.neighbors:
            neighbor.rank = 1

def upgrades_screen():
    global text_bottom, stats, selected_node, double_or_nothing
    screen.fill(BG)

    # Left Portion
    title = font_large.render('Upgrades', True, TEXT)
    screen.blit(title, ((WIDTH - TAB) // 2 - title.get_width() // 2, 50))
    if stats.money >= 1000000:
        title = font_small.render('You Won!', True, GREEN)
        screen.blit(title, ((WIDTH - TAB) // 2 - title.get_width() // 2, 120))
    else:
        title = font_small.render('Obtain $1m to Win the Game', True, TEXT)
        screen.blit(title, ((WIDTH - TAB) // 2 - title.get_width() // 2, 120))
    for node in nodes:
        node.draw()
    start_button = font_small.render('Begin', True, LIGHTBLUE)
    pygame.draw.rect(screen, LIGHTBLUE, (50 - 5, HEIGHT - 50 - start_button.get_height() - 5, start_button.get_width() + 10, start_button.get_height() + 10), 2)
    screen.blit(start_button, (50, HEIGHT - 50 - start_button.get_height()))
    money_label = font_medium.render(f'$ {stats.money:,}', True, LIGHTBLUE)
    # make this int have commas, like 1000000 should be 1,000,000 and 10000 should be 10,000. write only code dont explain
    screen.blit(money_label, (WIDTH - TAB - 50 - money_label.get_width(), 50 - money_label.get_height()))

    double_or_nothing = font_small.render('Double or Nothing', True, PINK)
    pygame.draw.rect(screen, PINK, (WIDTH - TAB - 120 - 5, HEIGHT - 50 - double_or_nothing.get_height() - 5, double_or_nothing.get_width() + 10, double_or_nothing.get_height() + 10), 2)
    screen.blit(double_or_nothing, (WIDTH - TAB - 120, HEIGHT - 50 - double_or_nothing.get_height()))

    # Right Portion
    pygame.draw.rect(screen, LIGHTBLUE, (WIDTH - TAB, 0, TAB, HEIGHT))
    update_sidebar(selected_node)

def update_sidebar(node):
    global text_top, text_middle, text_bottom, stats
    text_top = font_medium.render(f'Upgrade {node.name}', True, BG)
    screen.blit(text_top, (WIDTH - TAB // 2 - text_top.get_width() // 2, 50))
    text_middle = font_small.render(f'Rank {node.rank}', True, BG)
    screen.blit(text_middle, (WIDTH - TAB // 2 - text_middle.get_width() // 2, 100))
    text_desc = font_small.render(f'{node.desc}', True, BG)
    screen.blit(text_desc, (WIDTH - TAB // 2 - text_desc.get_width() // 2, 150))
    text_bottom = font_small.render(f'Cost: ${node.costs[node.rank]:,}', True, BG)
    pygame.draw.rect(screen, BG, (WIDTH - TAB // 2 - text_bottom.get_width() // 2 - 5, HEIGHT - 50 - text_bottom.get_height() - 5, text_bottom.get_width() + 10, text_bottom.get_height() + 10), 2)
    screen.blit(text_bottom, (WIDTH - TAB // 2 - text_bottom.get_width() // 2, HEIGHT - 50 - text_bottom.get_height()))
    if stats.broke:
        broke_label = font_small.render(f'Too Poor', True, BG)
        screen.blit(broke_label, (WIDTH - TAB // 2 - broke_label.get_width() // 2, HEIGHT - 20 - broke_label.get_height()))
    if stats.money >= node.costs[node.rank]:
        broke_label = font_small.render(f'', True, BG)
        screen.blit(broke_label, (WIDTH - TAB // 2 - broke_label.get_width() // 2, HEIGHT - 20 - broke_label.get_height()))
        stats.broke = False
    pygame.display.update()

def handle_events():
    global current_state, stats, text_bottom, selected_node, double_or_nothing
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if current_state == MAIN_MENU:
                current_state = UPGRADES_SCREEN
            elif current_state == UPGRADES_SCREEN:
                pass
            elif current_state == XY_CANVAS:
                pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MAIN_MENU:
                current_state = UPGRADES_SCREEN
            elif current_state == UPGRADES_SCREEN:
                if WIDTH - TAB - 120 - 5 <= mouse_x <= WIDTH - TAB - 120 - 5 + double_or_nothing.get_width() + 10 and HEIGHT - 50 - double_or_nothing.get_height() - 5 <= mouse_y <= HEIGHT - 50 - double_or_nothing.get_height() - 5 + double_or_nothing.get_height() + 10:
                    if random.choice([0, 1]):
                        stats.money *= 2 
                    else:
                        stats.money = 0
                for node in nodes:
                    if node.x <= mouse_x <= node.x + 50 and node.y <= mouse_y <= node.y + 50:
                        selected_node = node
                if selected_node and WIDTH - TAB // 2 - text_bottom.get_width() // 2 <= mouse_x <= WIDTH - TAB // 2 + text_bottom.get_width() // 2 and HEIGHT - 50 - text_bottom.get_height() <= mouse_y <= HEIGHT - 50:
                    if stats.money >= selected_node.costs[selected_node.rank]:
                        stats.money -= selected_node.costs[selected_node.rank]
                        selected_node.rank += 1
                        reveal_neighbors(selected_node)
                        if selected_node.name == 'Speed':
                            stats.speed += 1
                        elif selected_node.name == 'Size':
                            stats.size += 0.5
                        elif selected_node.name == 'Duration':
                            stats.duration += 1000
                        elif selected_node.name == 'Quantity':
                            stats.quantity += 1
                        elif selected_node.name == 'Wall Gain':
                            stats.wall_gain += selected_node.rank
                            selected_node.desc = f'Increase profits per hit + ${selected_node.rank}'
                        elif selected_node.name == 'Star Size':
                            stats.star_size += 0.5
                        elif selected_node.name == 'Star Quantity':
                            stats.star_quantity += 1
                        elif selected_node.name == 'Star Value':
                            stats.star_value += selected_node.rank * 200
                            selected_node.desc = f'Adds Value + ${selected_node.rank * 200}'
                        elif selected_node.name == 'Double Income':
                            stats.final_multiplier += 1
                    else:
                        stats.broke = True
                if mouse_x <= 100 and mouse_y >= HEIGHT-100:
                   current_state = XY_CANVAS

class Ball:
    def __init__(self, x, y, speed, size, wall_gain):
        self.x = x
        self.y = y
        self.direction = math.radians(random.uniform(0, 360))
        self.speed = speed
        self.size = size
        self.wall_gain = wall_gain
        self.dollars = 0

    def update_position(self, width, height):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)

        if self.x - self.size < 0 or self.x + self.size > width:
            self.direction = math.radians(180) - self.direction
            self.dollars += 1 * self.wall_gain
        if self.y - self.size < 0 or self.y + self.size > height:
            self.direction = -self.direction
            self.dollars += 1 * self.wall_gain

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

class Star:
    def __init__(self, x, y, size, value):
        self.x = x
        self.y = y
        self.size = size
        self.value = value

    def draw(self, screen, color):
        pygame.draw.circle(screen, BG, (self.x, self.y), self.size + 1)
        pygame.draw.circle(screen, color, (self.x, self.y), self.size)

def xy_canvas():
    initial_money = stats.money
    start_time = pygame.time.get_ticks()
    balls = [Ball(WIDTH // 2, HEIGHT // 2, stats.speed, stats.size, stats.wall_gain) for _ in range(stats.quantity)]
    stars = [Star(random.randint(0, WIDTH), random.randint(0, HEIGHT), stats.star_size, stats.star_value) for _ in range(stats.star_quantity)]
    star_money = 0

    while True:
        elapsed_time = pygame.time.get_ticks() - start_time
        if elapsed_time > stats.duration:
            stats.money = ((total_dollars + star_money) * stats.final_multiplier) + initial_money
            return UPGRADES_SCREEN

        handle_events()
        screen.fill(BG)
        total_dollars = 0

        for ball in balls:
            ball.update_position(WIDTH, HEIGHT)
            ball.draw(screen, BLUE)
            total_dollars += ball.dollars

            for star in stars[:]:
                if math.hypot(star.x - ball.x, star.y - ball.y) < ball.size + star.size:
                    stars.remove(star)
                    star_money += stats.star_value

        for star in stars:
            star.draw(screen, YELLOW)

        stats.money = total_dollars + initial_money + star_money
        dollars_text = font_large.render(f"${stats.money:,}", True, TEXT)
        screen.blit(dollars_text, (WIDTH // 2 - dollars_text.get_width() // 2, 50))

        gauge_width = 100
        gauge_height = 20
        remaining_duration = stats.duration - elapsed_time
        gauge_fill = int((remaining_duration / stats.duration) * gauge_width)
        pygame.draw.rect(screen, TEXT, (10, 10, gauge_width, gauge_height), 2)
        
        color = RED if gauge_fill < 20 else YELLOW if gauge_fill < 45 else GREEN
        pygame.draw.rect(screen, color, (10, 10, gauge_fill, gauge_height))

        pygame.display.flip()
        clock.tick(FPS)

def main():
    global current_state

    while True:
        handle_events()

        if current_state == MAIN_MENU:
            main_menu()
        elif current_state == UPGRADES_SCREEN:
            upgrades_screen()
        elif current_state == XY_CANVAS:
            current_state = xy_canvas()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()