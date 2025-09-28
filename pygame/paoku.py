
import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -18
OBSTACLE_SPEED = 8
OBSTACLE_SPAWN_RATE = 1500  # 毫秒

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("跑酷游戏")
clock = pygame.time.Clock()

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50  # 初始位置
        self.velocity_y = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self):
        # 应用重力
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # 确保玩家不会掉出屏幕底部
        if self.rect.bottom >= SCREEN_HEIGHT - 50:  # 50是地面高度
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.on_ground = True

# 障碍物类
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 随机生成不同大小的障碍物
        width = random.randint(30, 60)
        height = random.randint(40, 80)
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - height - 50  # 放在地面上

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        # 如果障碍物移出屏幕左侧，则删除
        if self.rect.right < 0:
            self.kill()

# 地面类
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SCREEN_WIDTH, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - 50

# 创建精灵组
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# 创建玩家和地面
player = Player()
ground = Ground()

all_sprites.add(player)
all_sprites.add(ground)

# 游戏变量
score = 0
last_obstacle_time = pygame.time.get_ticks()
font = pygame.font.Font(None, 36)
game_over = False

# 游戏主循环
running = True
while running:
    current_time = pygame.time.get_ticks()
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
            if event.key == pygame.K_r and game_over:
                # 重置游戏
                game_over = False
                score = 0
                player.rect.y = SCREEN_HEIGHT - player.rect.height - 50
                player.velocity_y = 0
                player.on_ground = True
                # 清除所有障碍物
                for obstacle in obstacles:
                    obstacle.kill()
                last_obstacle_time = current_time

    if not game_over:
        # 增加分数
        score += 0.01
        
        # 随机生成障碍物
        if current_time - last_obstacle_time > OBSTACLE_SPAWN_RATE:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)
            last_obstacle_time = current_time
            # 随着分数增加，障碍物生成速度加快
            OBSTACLE_SPAWN_RATE = max(500, 1500 - int(score) * 5)
        
        # 更新精灵
        all_sprites.update()
        
        # 碰撞检测
        if pygame.sprite.spritecollide(player, obstacles, False):
            game_over = True
    
    # 绘制
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    # 显示分数
    score_text = font.render(f"分数: {int(score)}", True, BLACK)
    screen.blit(score_text, (10, 10))
    
    # 游戏结束显示
    if game_over:
        game_over_text = font.render("游戏结束! 按R键重新开始", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2))
    
    # 更新屏幕
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()