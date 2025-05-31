import pygame
import sys
import random
import os

class Animation:
    def __init__(self, frames, pos, duration=5):
        self.frames = frames
        self.index = 0
        self.counter = 0
        self.duration = duration
        self.pos = list(pos)
        self.finished = False

    def update(self, screen):
        if self.finished:
            return

        screen.blit(self.frames[self.index], self.pos)
        self.counter += 1

        if self.counter >= self.duration:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.finished = True


width, height = 800, 800
player_width, player_height = 50, 50
platform_x, platform_y = 375, 750
platform_width, platform_height = 75, 20
player_vel_y = 0
player_vel_x = 10
player_speed_x = 0
acceleration = 3
friction = 0.5
jump_strength = 20
gravity = 1
scroll = 0
scroll_y = 0
score = 0
jetpack_active = False
jetpack_timer = 0
JETPACK_DURATION = 60
JETPACK_FORCE = 60
FPS = 60
platforms = []
record_file = "data/best_score.txt"
y = platform_y-((jump_strength/2)*jump_strength/gravity)
platforms.append({"rect": pygame.Rect(platform_x, platform_y, platform_width, platform_height), "type": "normal", "move_type": "stay", "velocity": 0})
enemies = []
size_of_enemy = 40
enemy_spawn_chance = 0.01
game_state = "menu"
max_delta=(((jump_strength*2)/gravity)*player_vel_x)
running = True
animations = []
jet_anim = []
heroside = 1

def image_scaling_height(height):
    return height/cloud_sample.get_height()*platform_height

pygame.init()
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("Sound/jump.mp3")
jetpack_sound = pygame.mixer.Sound("Sound/jet.mp3")
game_over_sound = pygame.mixer.Sound("Sound/lose.mp3")
spring_sound = pygame.mixer.Sound("Sound/spring.mp3")
break_sound = pygame.mixer.Sound("Sound/break.mp3")
font = pygame.font.Font("Font/PixelGame.otf", 36)
font_logo = pygame.font.Font("Font/PixelGame.otf", 72)
pause_text = font.render("PAUSED", True, (255, 0, 0))
screen = pygame.display.set_mode((width, height))
heronoj = pygame.image.load("assets/heronoj.png").convert_alpha()
heronoj = pygame.transform.scale(heronoj, (player_height, player_height))
heronoj_flipped = pygame.transform.flip(heronoj, True, False)
background = pygame.image.load("assets/background.png").convert()
background = pygame.transform.scale(background, (1420, 800))
cloud_sample = pygame.image.load("assets/cloud.png").convert_alpha()
cloud = pygame.image.load("assets/cloud.png").convert_alpha()
cloud = pygame.transform.scale(cloud, (platform_width, platform_height))
jetsprite = pygame.image.load("assets/noflame.png").convert_alpha()
jetsprite = pygame.transform.scale(jetsprite, (platform_width, image_scaling_height(jetsprite.get_height())))
flamejetsprite = pygame.image.load("assets/jet.png").convert_alpha()
flamejetsprite = pygame.transform.scale(flamejetsprite, (platform_width, image_scaling_height(flamejetsprite.get_height())))
enemysprite = pygame.image.load("assets/enemy.png").convert_alpha()
enemysprite = pygame.transform.scale(enemysprite, (size_of_enemy, size_of_enemy))
springsprite = pygame.image.load("assets/springhat.png").convert_alpha()
springsprite = pygame.transform.smoothscale(springsprite, (platform_width, image_scaling_height(springsprite.get_height())))
springsprite2 = pygame.image.load("assets/spring.png").convert_alpha()
springsprite2 = pygame.transform.scale(springsprite2, (platform_width, image_scaling_height(springsprite2.get_height())))
broken = pygame.image.load("assets/broken.png").convert_alpha()
broken = pygame.transform.scale(broken, (platform_width, platform_height))
broken2 = pygame.image.load("assets/unlucky.png").convert_alpha()
broken2 = pygame.transform.scale(broken2, (platform_width, platform_height))
pygame.display.set_caption("Jump Game")
player = pygame.Rect((platform_x*2+platform_width)/2-player_width/2, platform_y-player_height, player_width, player_height)
platform = pygame.Rect(platform_x, platform_y, platform_width, platform_height)
clock = pygame.time.Clock()
spring_frames = [springsprite2]
break_frames = [broken2]


def scale_by_width(image, target_height):
    rect = image.get_rect()
    width = rect.width
    height = rect.height
    scale_factor = target_height / height
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return pygame.transform.scale(image, new_size)

def reset_game():
    global player, player_speed_x, player_vel_y, score, scroll_y, platforms, enemies, jetpack_active, jetpack_timer, platform_x, platform_y, scroll, best_score_y
    platform_x, platform_y = 375, 750
    player.x = (platform_x * 2 + platform_width) / 2 - player_width / 2
    player.y = platform_y - player_height
    player_speed_x = 0
    player_vel_y = 0
    score = 0
    scroll = 0
    scroll_y = 0
    jetpack_active = False
    jetpack_timer = 0
    platforms.clear()
    enemies.clear()
    animations.clear()
    best_score_y = height // 2 - (best_score - scroll_y)
    platforms.append({"rect": pygame.Rect(platform_x, platform_y, platform_width, platform_height), "type": "normal", "move_type": "stay", "velocity": 0})
    for _ in range(60):
        add_new_platforms()

def draw_game_over():
    screen.blit(background, (0, 0))
    title_text = font_logo.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
    best_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    restart_text = font.render("Press [SPACE] to Restart", True, (255, 255, 255))
    quit_text = font.render("Press [ESC] to Quit", True, (255, 255, 255))

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 200))
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 300))
    screen.blit(best_text, (width // 2 - best_text.get_width() // 2, 350))
    screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, 450))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 500))
    pygame.display.flip()

def draw_main_menu():
    screen.blit(background, (0, 0))
    title_text = font_logo.render("Jump Game", True, (255, 255, 255))
    best_text = font.render(f"Best Score: {best_score}", True, (255, 255, 255))
    play_text = font.render("Press [SPACE] to Start", True, (255, 255, 255))
    quit_text = font.render("Press [ESC] to Quit", True, (255, 255, 255))
    pause_tip = font.render("Press [P] to Pause", True, (255, 255, 255))
    movement_tip = font.render("Press [A][D] or [RIGHT][LEFT] to Move", True, (255, 255, 255))
    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 200))
    screen.blit(best_text, (width // 2 - best_text.get_width() // 2, 300))
    screen.blit(play_text, (width // 2 - play_text.get_width() // 2, 400))
    screen.blit(quit_text, (width // 2 - quit_text.get_width() // 2, 450))
    screen.blit(pause_tip, (width // 2 - pause_tip.get_width() // 2, 500))
    screen.blit(movement_tip, (width // 2 - movement_tip.get_width() // 2, 550))
    pygame.display.flip()

def spawn_enemy():
    x = random.randint(0, width - size_of_enemy)
    y = random.randint(-height, 0)
    velocity = random.choice([-3, 3])
    enemies.append({"rect": pygame.Rect(x, y, size_of_enemy, size_of_enemy), "velocity": velocity})

def load_best_score():
    if os.path.exists(record_file):
        with open(record_file, "r") as f:
            return int(f.read())
    return 0

def save_best_score(score):
    os.makedirs(os.path.dirname(record_file), exist_ok=True)
    with open(record_file, "w") as f:
        f.write(str(score))

def create_platform(x, y):
    return {
        "rect": pygame.Rect(x, y, platform_width, platform_height),
        "type": get_platform_type(),
        "move_type": get_platform_move_type(),
        "velocity": get_platform_velocity()
    }

def get_platform_type():
    return random.choices(
        ["normal", "spring", "jetpack", "breakable"],
        weights=[75, 7.5, 2.5, 15],
        k=1
    )[0]

def get_platform_move_type():
    return random.choices(
        ["move", "stay"],
        weights=[25, 75],
        k=1
    )[0]

def get_platform_velocity():
    return random.randint(-5, 5)

def add_new_platforms():
    global platform_x, max_delta
    top = min(p["rect"].y for p in platforms)
    y = top - ((jump_strength / 2) * jump_strength / gravity) - random.randint(-10, 10)

    max_attempts = 1

    def try_create_platform(x, y):
        new_platform = create_platform(x, y)
        for p in platforms:
            if new_platform["rect"].colliderect(p["rect"]):
                return None  # пересекается — не подходит
        return new_platform

    def bounded_x(x):
        return max(10, min(x, width - platform_width-10))

    for _ in range(1):  # до 3 платформ максимум за вызов
        platform_x = generate_platform_x(platform_x)
        platform_x = bounded_x(platform_x)
        for _ in range(max_attempts):
            main_platform = try_create_platform(platform_x, y)
            if main_platform:
                platforms.append(main_platform)
                break

        number_of_side_platforms = random.randint(1, 3)

        if number_of_side_platforms == 1:
            side_offsets = [-(random.uniform(100, max_delta))]
        elif number_of_side_platforms == 2:
            side_offsets = [(random.uniform(-100, max_delta))]
        else:
            side_offsets = [-(random.uniform(100, max_delta)), (random.uniform(-100, max_delta))]

        for offset in side_offsets:
            bonus_x = bounded_x(platform_x + offset)
            for _ in range(max_attempts):
                bonus_platform = try_create_platform(bonus_x, y)
                if bonus_platform:
                    platforms.append(bonus_platform)
                    break


def generate_platform_x(platform_x, min_value=0, max_value=width-platform_width):
    global max_delta
    low = max(min_value, platform_x - max_delta)
    high = min(max_value, platform_x + max_delta)
    return random.uniform(low, high)

best_score = load_best_score()

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_state = "playing"
                    paused = False
                    reset_game()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        elif game_state == "game_over":
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                        game_state = "playing"
                        paused = False
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        elif game_state == "playing":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

    if game_state == "menu":
        draw_main_menu()
        pygame.display.flip()
        continue

    if game_state == "game_over":
        draw_game_over()
        pygame.display.flip()
        continue








    #PAUSE
    if paused:
        if jetpack_active:
            player_vel_y = -JETPACK_FORCE
            jetpack_timer -= 1
            for jet in jet_anim:
                screen.blit(flamejetsprite, jet["rect"])
                jet["rect"].x = player.x - player.width / 4
                jet["rect"].y = player.y + player.height - 12
            if jetpack_timer <= 0:
                jetpack_active = False
                jet_anim.clear()

        for anim in animations:
            anim.update(screen)
        animations = [a for a in animations if not a.finished]

        if best_score > 0:
            record_text = font.render("Best Score", True, (255, 255, 255))
            screen.blit(record_text, (10, best_score_y))
            pygame.draw.line(screen, "white", (0, best_score_y), (width, best_score_y), 2)

        for enemy in enemies:
            screen.blit(enemysprite, enemy["rect"])

        for p in platforms:
            color = "green"
            if p["type"] == "spring":
                screen.blit(springsprite, p["rect"])
            elif p["type"] == "jetpack":
                screen.blit(jetsprite, p["rect"])
            elif p["type"] == "breakable":
                screen.blit(broken, p["rect"])
            else:
                screen.blit(cloud, p["rect"])

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            heroside = 1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            heroside = 2

        if heroside == 1:
            screen.blit(heronoj_flipped, player)
        elif heroside == 2:
            screen.blit(heronoj, player)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        screen.blit(pause_text, (width // 2 - 50, height // 2 - 20))

        pygame.display.flip()
        continue










    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    player_vel_y += gravity
    player.y += player_vel_y



    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_speed_x -= acceleration
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_speed_x += acceleration
    else:
        if player_speed_x > 0:
            player_speed_x -= friction
            if player_speed_x < 0:
                player_speed_x = 0
        elif player_speed_x < 0:
            player_speed_x += friction
            if player_speed_x > 0:
                player_speed_x = 0
    player_speed_x = max(-player_vel_x, min(player_speed_x, player_vel_x))
    player.x += player_speed_x

    for p in platforms:
        rect = p["rect"]
        p_type = p["type"]
        p_vel = p["velocity"]
        p_move = p["move_type"]

        if p["move_type"] == "move":
            p["rect"].x += p["velocity"]
            if p["rect"].x <= 0 or p["rect"].x + platform_width >= width:
                p["velocity"] *= -1

        if player.colliderect(rect) and player_vel_y > 0:

            if p_type == "breakable":
                animations.append(Animation(break_frames, (rect.x, rect.y)))
                player_vel_y = -jump_strength
                break_sound.play()
                platforms.remove(p)
            elif p_type == "spring":
                platforms.remove(p)
                animations.append(Animation(spring_frames, (rect.x, rect.y-13.3491686461)))
                player_vel_y = -jump_strength * 1.5
                spring_sound.play()
            elif p_type == "jetpack":
                platforms.remove(p)
                jet_anim.append(p)
                jetpack_active = True
                jetpack_timer = JETPACK_DURATION
                jetpack_sound.play()
            else:
                jump_sound.play()
                player_vel_y = -jump_strength

            player.y = rect.y - player_height

    if player.y < height // 2:
        scroll = height // 2 - player.y
        player.y = height // 2
        scroll_y += scroll
        score += scroll
        platforms = [p for p in platforms if p["rect"].y <= height]
        best_score_y += scroll
        if random.random() < enemy_spawn_chance:
            spawn_enemy()

        for platform in platforms:
            platform["rect"].y += scroll

        for anim in animations:
            anim.pos[1] += scroll


    while len(platforms) < 30:
        add_new_platforms()

    if player.y + player_height > height:
        game_state = "game_over"
        game_over_sound.play()

    if running is False or game_state == "game_over":
        if score > best_score:
            best_score = score
            save_best_score(best_score)

    if player.x + player_width < 0:
        player.x = width
    elif player.x > width:
        player.x = -player_width

    for enemy in enemies:
        enemy["rect"].x += enemy["velocity"]
        if enemy["rect"].left <= 0 or enemy["rect"].right >= width:
            enemy["velocity"] *= -1  # отражение от стен

    for enemy in enemies:
        if player.colliderect(enemy["rect"]) and jetpack_active == False:
            game_over_sound.play()
            game_state = "game_over"

    for enemy in enemies:
        enemy["rect"].y += scroll

    enemies = [e for e in enemies if e["rect"].y < height]

#ОТРИСОВКА
    if jetpack_active:
        player_vel_y = -JETPACK_FORCE
        jetpack_timer -= 1
        for jet in jet_anim:
            screen.blit(flamejetsprite, jet["rect"])
            jet["rect"].x = player.x-player.width/4
            jet["rect"].y = player.y+player.height-12
        if jetpack_timer <= 0:
            jetpack_active = False
            jet_anim.clear()

    for anim in animations:
        anim.update(screen)
    animations = [a for a in animations if not a.finished]

    if best_score > 0:
        record_text = font.render("Best Score", True, (255, 255, 255))
        screen.blit(record_text, (10, best_score_y))
        pygame.draw.line(screen, "white", (0, best_score_y), (width, best_score_y), 2)

    for enemy in enemies:
        screen.blit(enemysprite, enemy["rect"])

    for p in platforms:
        color = "green"
        if p["type"] == "spring":
            screen.blit(springsprite, p["rect"])
        elif p["type"] == "jetpack":
            screen.blit(jetsprite, p["rect"])
        elif p["type"] == "breakable":
            screen.blit(broken, p["rect"])
        else:
            screen.blit(cloud, p["rect"])

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        heroside = 1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        heroside = 2

    if heroside == 1:
        screen.blit(heronoj_flipped, player)
    elif heroside == 2:
        screen.blit(heronoj, player)

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()