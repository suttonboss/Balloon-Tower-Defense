import pygame
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Balloon Tower Defense")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
LIGHTBLUE = (173, 216, 230)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

# Balloon types: (name, color, health, speed, reward)
BALLOON_TYPES = {
    'red': {'name': 'Red', 'color': RED, 'health': 3, 'speed': 1.5, 'reward': 10},
    'blue': {'name': 'Blue', 'color': BLUE, 'health': 5, 'speed': 2.0, 'reward': 15},
    'green': {'name': 'Green', 'color': GREEN, 'health': 7, 'speed': 1.0, 'reward': 20},
    'yellow': {'name': 'Yellow', 'color': YELLOW, 'health': 10, 'speed': 2.5, 'reward': 30},
    'purple': {'name': 'Purple', 'color': PURPLE, 'health': 15, 'speed': 1.2, 'reward': 40},
}

# Tower types: (name, cost, range, damage, cooldown, color)
TOWER_TYPES = {
    'basic': {'name': 'Basic', 'cost': 50, 'range': 150, 'damage': 1, 'cooldown': 30, 'color': ORANGE},
    'fast': {'name': 'Fast', 'cost': 100, 'range': 120, 'damage': 1, 'cooldown': 10, 'color': CYAN},
    'strong': {'name': 'Strong', 'cost': 150, 'range': 180, 'damage': 3, 'cooldown': 45, 'color': PURPLE},
    'sniper': {'name': 'Sniper', 'cost': 200, 'range': 300, 'damage': 5, 'cooldown': 60, 'color': GREEN},
}

# Game constants
BALLOON_REWARD = 10
STARTING_LIVES = 10
STARTING_MONEY = 100

# Wave definitions: list of (balloon_type, count, spawn_delay)
WAVES = [
    [('red', 5, 60)],
    [('red', 8, 50)],
    [('red', 5, 50), ('blue', 3, 60)],
    [('blue', 5, 50), ('red', 5, 40)],
    [('green', 5, 70)],
    [('blue', 8, 45), ('green', 3, 60)],
    [('yellow', 5, 50)],
    [('red', 10, 30), ('yellow', 5, 50)],
    [('purple', 3, 80), ('green', 5, 50)],
    [('purple', 5, 60), ('yellow', 8, 40), ('green', 10, 45)],
]

# Balloon path points (winding path from left to right)
PATH_POINTS = [
    (50, 100), (150, 100), (150, 200), (250, 200),
    (250, 100), (350, 100), (350, 200), (450, 200),
    (450, 100), (550, 100), (550, 200), (650, 200),
    (650, 300), (750, 300), (750, 400), (750, 500)
]

# Game variables
lives = STARTING_LIVES
money = STARTING_MONEY
wave = 1
balloons = []
towers = []
projectiles = []
path_color = (192, 192, 192)
path_width = 20

# Balloon class
class Balloon:
    def __init__(self, path_points, balloon_type='red'):
        self.path_points = path_points
        self.path_index = 0
        self.x = self.path_points[0][0]
        self.y = self.path_points[0][1]
        self.radius = 15

        # Calculate direction to next point
        self.next_point_index = 1
        self.target_x, self.target_y = self.path_points[self.next_point_index]
        
        # Set balloon properties based on type
        self.balloon_type = balloon_type
        type_data = BALLOON_TYPES.get(balloon_type, BALLOON_TYPES['red'])
        self.speed = type_data['speed']
        self.health = type_data['health']
        self.max_health = type_data['health']
        self.color = type_data['color']
        self.reward = type_data['reward']
        self.reached_end = False

    def move(self):
        if self.path_index >= len(self.path_points) - 1:
            self.reached_end = True
            return

        # Get current target point
        self.target_x, self.target_y = self.path_points[self.next_point_index]

        # Calculate direction
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < self.speed:
            self.x = self.target_x
            self.y = self.target_y
            self.path_index = self.next_point_index
            self.next_point_index += 1
            if self.next_point_index >= len(self.path_points):
                self.next_point_index = len(self.path_points) - 1
        else:
            # Move toward target
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, surface):
        # Draw balloon (circle)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        # Draw balloon outline
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)
        # Draw health text
        font = pygame.font.SysFont(None, 16)
        health_text = font.render(str(self.health), True, WHITE)
        surface.blit(health_text, (self.x - 5, self.y - 5))

    def take_damage(self, damage):
        self.health -= damage

# Tower class
class Tower:
    def __init__(self, x, y, tower_type='basic'):
        self.x = x
        self.y = y
        self.tower_type = tower_type
        
        # Set tower properties based on type
        type_data = TOWER_TYPES.get(tower_type, TOWER_TYPES['basic'])
        self.range = type_data['range']
        self.damage = type_data['damage']
        self.cooldown = 0
        self.max_cooldown = type_data['cooldown']
        self.color = type_data['color']
        self.cost = type_data['cost']

    def draw(self, surface):
        # Draw tower base (color based on type)
        pygame.draw.rect(surface, self.color, (self.x - 15, self.y - 15, 30, 30))
        # Draw tower outline
        pygame.draw.rect(surface, BLACK, (self.x - 15, self.y - 15, 30, 30), 2)
        # Draw tower top (different shape for different types)
        if self.tower_type == 'fast':
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 3)
            pygame.draw.circle(surface, BLACK, (int(self.x)-5, int(self.y)), 3)
            pygame.draw.circle(surface, BLACK, (int(self.x)+5, int(self.y)), 3)
        elif self.tower_type == 'strong':
            pygame.draw.polygon(surface, BLACK, [
                (self.x, self.y - 8),
                (self.x + 8, self.y + 8),
                (self.x - 8, self.y + 8)
            ])
        elif self.tower_type == 'sniper':
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 6)
            pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)
        else:
            pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 5)

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def shoot(self, balloons_list):
        if self.cooldown > 0:
            return None

        # Find nearest balloon in range
        nearest = None
        min_dist = float('inf')
        for balloon in balloons_list:
            dx = balloon.x - self.x
            dy = balloon.y - self.y
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < min_dist and dist <= self.range:
                min_dist = dist
                nearest = balloon

        if nearest:
            self.cooldown = self.max_cooldown
            return Projectile(self.x, self.y, nearest)
        return None

# Projectile class
class Projectile:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 8
        self.damage = 1
        self.active = True

    def update(self):
        if not self.active:
            return

        # Calculate direction to target
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        distance = math.sqrt(dx*dx + dy*dy)

        if distance < 5:
            self.active = False
            self.target.take_damage(self.damage)
        else:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def draw(self, surface):
        if not self.active:
            return
        # Draw projectile (small circle)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), 3)

# Game functions
def draw_path(surface):
    if len(PATH_POINTS) > 1:
        pygame.draw.lines(surface, path_color, False, PATH_POINTS, path_width)

def draw_ui(surface):
    font = pygame.font.SysFont(None, 24)
    lives_text = font.render(f"Lives: {lives}", True, BLACK)
    money_text = font.render(f"Money: {money}", True, BLACK)
    wave_text = font.render(f"Wave: {wave}", True, BLACK)
    cost_text = font.render(f"Tower Cost: {TOWER_COST}", True, BLACK)
    surface.blit(lives_text, (10, 10))
    surface.blit(money_text, (10, 30))
    surface.blit(wave_text, (10, 50))
    surface.blit(cost_text, (10, 70))

def check_game_over():
    global lives
    if lives <= 0:
        return True
    return False

def check_wave_complete():
    global wave, balloons
    if len(balloons) == 0:
        return True
    return False

# Wave Manager class
class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.wave_active = False
        self.wave_complete = False
        self.spawn_queue = []
        self.spawn_timer = 0
        self.wave_delay = 180  # 3 seconds between waves
        self.delay_timer = 0
        self.all_waves_complete = False
        
    def start_next_wave(self):
        global wave
        if self.current_wave >= len(WAVES):
            self.all_waves_complete = True
            return False
        
        self.current_wave += 1
        wave = self.current_wave
        self.wave_active = True
        self.wave_complete = False
        
        # Build spawn queue from wave definition
        self.spawn_queue = []
        for balloon_type, count, delay in WAVES[self.current_wave - 1]:
            for i in range(count):
                self.spawn_queue.append((balloon_type, delay))
        self.spawn_timer = 0
        return True
        
    def update(self):
        if self.all_waves_complete:
            return None
            
        if not self.wave_active:
            self.delay_timer += 1
            if self.delay_timer >= self.wave_delay:
                self.delay_timer = 0
                self.start_next_wave()
            return None
        
        if len(self.spawn_queue) == 0:
            return None
        
        self.spawn_timer += 1
        balloon_type, delay = self.spawn_queue[0]
        
        if self.spawn_timer >= delay:
            self.spawn_timer = 0
            self.spawn_queue.pop(0)
            return balloon_type
        
        return None
    
    def check_wave_complete(self, balloons_count):
        if self.wave_active and len(self.spawn_queue) == 0 and balloons_count == 0:
            self.wave_active = False
            self.wave_complete = True
            if self.current_wave >= len(WAVES):
                self.all_waves_complete = True
            return True
        return False

# Game states
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"

def draw_game_over(surface):
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))
    
    # Draw Game Over text
    game_over_text = font_large.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(game_over_text, text_rect)
    
    # Draw restart instruction
    restart_text = font_small.render("Press R to Restart", True, WHITE)
    text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(restart_text, text_rect)
    
    # Draw quit instruction
    quit_text = font_small.render("Press Q to Quit", True, WHITE)
    text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    surface.blit(quit_text, text_rect)

def draw_win_screen(surface):
    font_large = pygame.font.SysFont(None, 72)
    font_small = pygame.font.SysFont(None, 36)
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))
    
    # Draw Victory text
    win_text = font_large.render("VICTORY!", True, GREEN)
    text_rect = win_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(win_text, text_rect)
    
    # Draw message
    message_text = font_small.render("All waves completed!", True, WHITE)
    text_rect = message_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    surface.blit(message_text, text_rect)
    
    # Draw restart instruction
    restart_text = font_small.render("Press R to Restart", True, WHITE)
    text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(restart_text, text_rect)
    
    # Draw quit instruction
    quit_text = font_small.render("Press Q to Quit", True, WHITE)
    text_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90))
    surface.blit(quit_text, text_rect)

def draw_tower_selection(surface, selected_tower):
    font = pygame.font.SysFont(None, 24)
    
    title = font.render("Select Tower (keys 1-4):", True, BLACK)
    surface.blit(title, (SCREEN_WIDTH - 250, 10))
    
    for i, (tower_type, data) in enumerate(TOWER_TYPES.items()):
        color = data['color'] if selected_tower == tower_type else (150, 150, 150)
        x = SCREEN_WIDTH - 240 + i * 60
        pygame.draw.rect(surface, color, (x, 40, 50, 50))
        pygame.draw.rect(surface, BLACK, (x, 40, 50, 50), 2)
        
        # Draw tower type number
        num_text = font.render(str(i + 1), True, BLACK)
        surface.blit(num_text, (x + 20, 55))
        
        # Draw cost below
        cost_text = font.render(f"${data['cost']}", True, BLACK)
        surface.blit(cost_text, (x + 5, 95))

def reset_game():
    global lives, money, wave, balloons, towers, projectiles
    lives = STARTING_LIVES
    money = STARTING_MONEY
    wave = 1
    balloons = []
    towers = []
    projectiles = []
    return WaveManager()

# Main game loop
def main():
    global lives, money, wave, balloons, towers, projectiles
    clock = pygame.time.Clock()
    spawn_timer = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    # Check if clicked on path
                    on_path = False
                    for i in range(len(PATH_POINTS) - 1):
                        p1 = PATH_POINTS[i]
                        p2 = PATH_POINTS[i + 1]
                        # Simple line segment collision
                        if min(p1[0], p2[0]) <= mouse_x <= max(p1[1], p2[1]):
                            on_path = True
                            break
                    if not on_path:
                        if money >= TOWER_COST:
                            towers.append(Tower(mouse_x, mouse_y))
                            money -= TOWER_COST

        if not game_over:
            # Update game logic
            spawn_timer += 1
            if spawn_timer > 60:  # Spawn balloon every 1 second
                if len(balloons) < 10:  # Max balloons on screen
                    balloons.append(Balloon(PATH_POINTS))
                    spawn_timer = 0

            # Update balloons
            for balloon in balloons[:]:
                balloon.move()
                if balloon.reached_end:
                    lives -= 1
                    balloons.remove(balloon)
                elif balloon.health <= 0:
                    money += BALLOON_REWARD
                    balloons.remove(balloon)

            # Update towers
            for tower in towers:
                tower.update()
                projectile = tower.shoot(balloons)
                if projectile:
                    projectiles.append(projectile)

            # Update projectiles
            for projectile in projectiles[:]:
                projectile.update()
                if not projectile.active:
                    projectiles.remove(projectile)

            # Check game over
            if lives <= 0:
                game_over = True

            # Clear screen
            screen.fill(WHITE)

            # Draw path
            draw_path(screen)

            # Draw towers
            for tower in towers:
                tower.draw(screen)

            # Draw balloons
            for balloon in balloons:
                balloon.draw(screen)

            # Draw projectiles
            for projectile in projectiles:
                projectile.draw(screen)

            # Draw UI
            draw_ui(screen)

            # Update display
            pygame.display.flip()
            clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
