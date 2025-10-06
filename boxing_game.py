import pygame, sys

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🥊 Boxing Game")

# Colors
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
GREEN = (0,255,0)

# FPS & Clock
FPS = 60
clock = pygame.time.Clock()

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 60, 120
VEL = 5
PUNCH_REACH = 40
MAX_HEALTH = 100

font = pygame.font.SysFont("arial", 30)

# Player class
class Fighter:
    def __init__(self, x, color, left_keys, right_keys):
        self.rect = pygame.Rect(x, HEIGHT-PLAYER_HEIGHT-20, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.health = MAX_HEALTH
        self.is_punching = False
        self.left_keys, self.right_keys = left_keys, right_keys

    def move(self, keys):
        if keys[self.left_keys["left"]] and self.rect.left > 0:
            self.rect.x -= VEL
        if keys[self.left_keys["right"]] and self.rect.right < WIDTH:
            self.rect.x += VEL

    def punch(self, other):
        if not self.is_punching:
            self.is_punching = True
            punch_area = self.rect.copy()
            if self.color == RED:
                punch_area.width += PUNCH_REACH
            else:
                punch_area.x -= PUNCH_REACH
                punch_area.width += PUNCH_REACH
            if punch_area.colliderect(other.rect):
                other.health -= 10
                if other.health < 0:
                    other.health = 0

    def draw(self):
        pygame.draw.rect(WIN, self.color, self.rect)
        # Health bar
        bar_x = 50 if self.color == RED else WIDTH - 250
        pygame.draw.rect(WIN, BLACK, (bar_x, 20, 200, 20))
        pygame.draw.rect(WIN, GREEN, (bar_x, 20, 2*self.health, 20))
        name = "RED" if self.color == RED else "BLUE"
        WIN.blit(font.render(f"{name}: {self.health}", True, WHITE), (bar_x, 45))

# Initialize players
red_keys = {"left": pygame.K_a, "right": pygame.K_d, "punch": pygame.K_w}
blue_keys = {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "punch": pygame.K_UP}
red = Fighter(150, RED, red_keys, blue_keys)
blue = Fighter(700, BLUE, red_keys, blue_keys)

# Game loop
def main():
    run = True
    while run:
        clock.tick(FPS)
        WIN.fill((30,30,30))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == red.left_keys["punch"]:
                    red.punch(blue)
                if event.key == blue.right_keys["punch"]:
                    blue.punch(red)

        red.move(keys)
        blue.move(keys)

        red.draw()
        blue.draw()

        # Check win
        if red.health <= 0 or blue.health <= 0:
            winner = "Blue" if red.health <= 0 else "Red"
            text = font.render(f"{winner} Wins!", True, WHITE)
            WIN.blit(text, (WIDTH//2 - 80, HEIGHT//2))
            pygame.display.update()
            pygame.time.delay(3000)
            run = False
            continue

        pygame.display.update()
        red.is_punching = False
        blue.is_punching = False

if __name__ == "__main__":
    main()
