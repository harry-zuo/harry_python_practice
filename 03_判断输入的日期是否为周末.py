# 编写程序，判断今天是否为周末
"""
a = 5
b = [1,2,3,4]
print(a in b) # False
"""

'''
a = "lydia"
b = "i'm lydia"
print(a in b) # True
'''
"""
a = input(f"请输入今天周几:")
b = ["周六","周天","6","7"]
c = a in b

if c == True:
    msg = "今天是周末"
else:
    msg = "今天不是周末"

print(msg)
"""
"""
import pygame
import random
import sys
import math

# 初始化pygame
pygame.init()

# 游戏窗口设置
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("枪战游戏")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 玩家类
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.health = 100
        self.shoot_delay = 250  # 射击延迟（毫秒）
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        
        # 键盘控制
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -8
        if keys[pygame.K_RIGHT]:
            self.speed_x = 8
        if keys[pygame.K_UP]:
            self.speed_y = -8
        if keys[pygame.K_DOWN]:
            self.speed_y = 8
            
        # 边界检测
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
        self.rect.y += self.speed_y
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

# 敌人类
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # 当敌人移出屏幕底部时重新放置到顶部
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)

# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # 当子弹移出屏幕顶部时删除
        if self.rect.bottom < 0:
            self.kill()

# 创建精灵组
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# 创建玩家
player = Player()
all_sprites.add(player)

# 创建敌人
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# 游戏时钟
clock = pygame.time.Clock()

# 分数
score = 0

# 游戏字体
font_name = pygame.font.match_font('simsun')  # 使用系统中的宋体

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (health / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

# 游戏主循环
running = True
while running:
    # 保持30fps
    clock.tick(60)
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    # 更新精灵
    all_sprites.update()

    # 碰撞检测：子弹击中敌人
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # 碰撞检测：敌人击中玩家
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 25
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
        if player.health <= 0:
            running = False

    # 绘制
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # 绘制分数
    draw_text(screen, f"分数: {score}", 18, WIDTH // 2, 10)
    
    # 绘制生命值
    draw_health(screen, 5, 5, player.health)
    
    # 更新屏幕
    pygame.display.flip()

# 游戏结束画面
screen.fill(BLACK)
draw_text(screen, "游戏结束", 64, WIDTH // 2, HEIGHT // 4)
draw_text(screen, f"最终分数: {score}", 22, WIDTH // 2, HEIGHT // 2)
draw_text(screen, "按任意键退出", 18, WIDTH // 2, HEIGHT * 3 // 4)
pygame.display.flip()

# 等待用户按键退出
waiting = True
while waiting:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        if event.type == pygame.KEYUP:
            waiting = False

pygame.quit()
sys.exit()
"""
"""
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
"""
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import time

# 游戏常量
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
MOVE_SPEED = 0.15
ROT_SPEED = 0.3
BULLET_SPEED = 0.5
BULLET_LIFETIME = 60  # 子弹存在的帧数
ENEMY_SPEED = 0.05
ENEMY_SPAWN_RATE = 120  # 每多少帧生成一个敌人
PLAYER_HEALTH = 100

class Bullet:
    def __init__(self, x, y, z, dir_x, dir_z, rot_y):
        self.x = x
        self.y = y
        self.z = z
        self.dir_x = dir_x
        self.dir_z = dir_z
        self.rot_y = rot_y
        self.lifetime = BULLET_LIFETIME
        
    def update(self):
        self.x += self.dir_x * BULLET_SPEED
        self.z += self.dir_z * BULLET_SPEED
        self.lifetime -= 1
        return self.lifetime > 0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot_y, 0, 1, 0)
        glColor3f(1.0, 0.8, 0.2)  # 子弹为金色
        
        # 绘制子弹（小圆柱）
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.05, 0.05, 0.3, 10, 1)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glPopMatrix()

class Enemy:
    def __init__(self):
        # 随机生成在玩家周围较远的位置
        angle = random.uniform(0, math.pi * 2)
        distance = random.uniform(15, 25)
        self.x = math.sin(angle) * distance
        self.z = math.cos(angle) * distance
        self.y = 1.0  # 高度
        self.health = 30
        self.color = (0.8, 0.2, 0.2)  # 红色
        
    def update(self, player_x, player_z):
        # 敌人向玩家移动
        dx = player_x - self.x
        dz = player_z - self.z
        dist = math.sqrt(dx*dx + dz*dz)
        
        if dist > 1.0:  # 保持一定距离
            self.x += (dx / dist) * ENEMY_SPEED
            self.z += (dz / dist) * ENEMY_SPEED
            
        return dist < 1.5  # 敌人是否碰到玩家
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # 绘制敌人身体（立方体）
        glColor3f(*self.color)
        draw_cube(0, 0, 0, 0.8, 1.8, 0.8)
        
        # 绘制敌人头部（球体）
        glPushMatrix()
        glTranslatef(0, 1.2, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.5, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glPopMatrix()
        
    def hit(self, damage):
        self.health -= damage
        return self.health <= 0

class Player:
    def __init__(self):
        self.x = 0.0
        self.z = 0.0
        self.y = 0.0  # 高度
        self.rot_x = 0.0  # 上下旋转
        self.rot_y = 0.0  # 左右旋转
        self.health = PLAYER_HEALTH
        self.score = 0
        
    def update(self, keys):
        # 处理旋转
        rad = math.radians(self.rot_y)
        
        # 处理移动
        if keys[pygame.K_w]:  # 前进
            self.x -= math.sin(rad) * MOVE_SPEED
            self.z -= math.cos(rad) * MOVE_SPEED
        if keys[pygame.K_s]:  # 后退
            self.x += math.sin(rad) * MOVE_SPEED
            self.z += math.cos(rad) * MOVE_SPEED
        if keys[pygame.K_a]:  # 左移
            self.x -= math.sin(rad + math.pi/2) * MOVE_SPEED
            self.z -= math.cos(rad + math.pi/2) * MOVE_SPEED
        if keys[pygame.K_d]:  # 右移
            self.x += math.sin(rad + math.pi/2) * MOVE_SPEED
            self.z += math.cos(rad + math.pi/2) * MOVE_SPEED
            
        # 限制上下视角
        if self.rot_x > 90:
            self.rot_x = 90
        if self.rot_x < -90:
            self.rot_x = -90
            
    def shoot(self):
        # 根据玩家视角计算子弹方向
        rad = math.radians(self.rot_y)
        dir_x = -math.sin(rad)
        dir_z = -math.cos(rad)
        return Bullet(self.x + dir_x * 0.5, self.y + 0.8, self.z + dir_z * 0.5, dir_x, dir_z, self.rot_y)
        
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0

def draw_cube(x, y, z, width, height, depth):
    # 绘制立方体的辅助函数
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # 前面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glEnd()
    
    # 后面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    glEnd()
    
    # 左面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    glEnd()
    
    # 右面
    glBegin(GL_QUADS)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glEnd()
    
    # 顶面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glEnd()
    
    # 底面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glEnd()
    
    glPopMatrix()

def draw_scene(player, bullets, enemies):
    # 清除缓冲区
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # 重置模型视图矩阵
    glLoadIdentity()
    
    # 设置相机位置和角度（第一人称）
    gluLookAt(
        player.x, player.y + 1.7, player.z,  # 相机位置（眼睛高度）
        player.x - math.sin(math.radians(player.rot_y)), 
        player.y + 1.7 + math.sin(math.radians(player.rot_x)), 
        player.z - math.cos(math.radians(player.rot_y)),  # 看向的点
        0, 1, 0  # 上方向
    )
    
    # 绘制地面
    glBegin(GL_QUADS)
    glColor3f(0.3, 0.3, 0.3)  # 灰色地面
    glVertex3f(-50, 0, -50)
    glVertex3f(50, 0, -50)
    glVertex3f(50, 0, 50)
    glVertex3f(-50, 0, 50)
    glEnd()
    
    # 绘制一些障碍物
    glColor3f(0.5, 0.5, 0.5)  # 灰色障碍物
    draw_cube(-10, 0, 5, 3, 2, 3)
    draw_cube(7, 0, -3, 2, 3, 2)
    draw_cube(0, 0, 10, 4, 1, 4)
    draw_cube(-5, 0, -8, 2, 2, 5)
    
    # 绘制子弹
    for bullet in bullets:
        bullet.draw()
    
    # 绘制敌人
    for enemy in enemies:
        enemy.draw()

def draw_hud(player):
    # 在2D屏幕上绘制HUD（平视显示器）
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # 禁用深度测试以确保HUD在最前面
    glDisable(GL_DEPTH_TEST)
    
    # 绘制准星
    glColor3f(1.0, 0.0, 0.0)  # 红色准星
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(SCREEN_WIDTH//2 - 10, SCREEN_HEIGHT//2)
    glVertex2f(SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT//2)
    glVertex2f(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 10)
    glVertex2f(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10)
    glEnd()
    
    # 绘制生命值
    glColor3f(0.0, 1.0, 0.0)  # 绿色生命值条
    glBegin(GL_QUADS)
    glVertex2f(20, SCREEN_HEIGHT - 40)
    glVertex2f(20 + player.health * 2, SCREEN_HEIGHT - 40)
    glVertex2f(20 + player.health * 2, SCREEN_HEIGHT - 20)
    glVertex2f(20, SCREEN_HEIGHT - 20)
    glEnd()
    
    # 绘制生命值边框
    glColor3f(1.0, 1.0, 1.0)  # 白色边框
    glLineWidth(1.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(20, SCREEN_HEIGHT - 40)
    glVertex2f(20 + PLAYER_HEALTH * 2, SCREEN_HEIGHT - 40)
    glVertex2f(20 + PLAYER_HEALTH * 2, SCREEN_HEIGHT - 20)
    glVertex2f(20, SCREEN_HEIGHT - 20)
    glEnd()
    
    # 绘制分数
    font = pygame.font.SysFont(None, 36)
    text_surface = font.render(f"Score: {player.score}", True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glRasterPos2f(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 40)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # 恢复状态
    glEnable(GL_DEPTH_TEST)
    glLineWidth(1.0)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def init():
    # 初始化游戏
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Shooter")
    
    # 设置视角
    gluPerspective(75, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 100.0)
    
    # 启用深度测试和光照
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # 设置光源
    light_pos = [10.0, 20.0, 10.0, 1.0]
    light_ambient = [0.2, 0.2, 0.2, 1.0]
    light_diffuse = [0.8, 0.8, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    # 设置鼠标
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)  # 捕获鼠标

def main():
    init()
    
    player = Player()
    bullets = []
    enemies = []
    frame_count = 0
    last_shot_time = 0
    shoot_cooldown = 20  # 射击冷却帧数
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        frame_count += 1
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # 生成敌人
        if frame_count % ENEMY_SPAWN_RATE == 0:
            enemies.append(Enemy())
        
        # 处理输入
        keys = pygame.key.get_pressed()
        player.update(keys)
        
        # 处理鼠标移动
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        player.rot_y += mouse_dx * ROT_SPEED
        player.rot_x -= mouse_dy * ROT_SPEED  # 负号因为鼠标上移应该看向下方
        
        # 处理射击
        if keys[pygame.K_SPACE] and frame_count - last_shot_time > shoot_cooldown:
            bullets.append(player.shoot())
            last_shot_time = frame_count
        
        # 更新子弹
        bullets = [bullet for bullet in bullets if bullet.update()]
        
        # 检测子弹与敌人碰撞
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                dx = enemy.x - bullet.x
                dz = enemy.z - bullet.z
                distance = math.sqrt(dx*dx + dz*dz)
                
                if distance < 0.8:  # 碰撞检测
                    bullets.remove(bullet)
                    if enemy.hit(10):  # 敌人受10点伤害
                        enemies.remove(enemy)
                        player.score += 100
                    break
        
        # 更新敌人并检测与玩家的碰撞
        for enemy in enemies[:]:
            if enemy.update(player.x, player.z):
                # 敌人碰到玩家，玩家受伤
                if player.take_damage(5):
                    print(f"游戏结束！你的分数是: {player.score}")
                    running = False
                enemies.remove(enemy)
        
        # 绘制场景
        draw_scene(player, bullets, enemies)
        draw_hud(player)
        
        # 更新屏幕
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
"""
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from collections import defaultdict
import time

# 游戏常量
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
MOVE_SPEED = 0.13
CROUCH_SPEED = 0.07
SPRINT_SPEED = 0.22
ROT_SPEED = 0.3
BULLET_SPEED = 0.7
EVAC_TIME = 60  # 撤离倒计时（秒）

class Player:
    def __init__(self):
        self.x = 0.0
        self.z = 0.0
        self.y = 0.0  # 高度
        self.rot_x = 0.0  # 上下视角
        self.rot_y = 0.0  # 左右视角
        self.health = 100
        self.stamina = 100  # 耐力，影响冲刺
        self.inventory = defaultdict(int)
        self.equipped_weapon = "pistol"
        self.ammo = {"pistol": 15, "rifle": 30, "shotgun": 8}
        self.loot_value = 0  # 收集的战利品总价值
        self.crouching = False
        self.sprinting = False
        
    def move(self, keys, dt):
        # 根据状态调整移动速度
        current_speed = MOVE_SPEED
        if self.crouching:
            current_speed = CROUCH_SPEED
        elif self.sprinting and self.stamina > 0:
            current_speed = SPRINT_SPEED
            self.stamina = max(0, self.stamina - 0.5)
        else:
            # 恢复耐力
            self.stamina = min(100, self.stamina + 0.1)
        
        rad = math.radians(self.rot_y)
        
        # WASD移动
        if keys[pygame.K_w]:
            self.x -= math.sin(rad) * current_speed
            self.z -= math.cos(rad) * current_speed
        if keys[pygame.K_s]:
            self.x += math.sin(rad) * current_speed
            self.z += math.cos(rad) * current_speed
        if keys[pygame.K_a]:
            self.x -= math.sin(rad + math.pi/2) * current_speed
            self.z -= math.cos(rad + math.pi/2) * current_speed
        if keys[pygame.K_d]:
            self.x += math.sin(rad + math.pi/2) * current_speed
            self.z += math.cos(rad + math.pi/2) * current_speed
            
        # 蹲伏控制
        if keys[pygame.K_LCTRL]:
            self.crouching = True
            self.y = -0.5  # 降低高度
        else:
            self.crouching = False
            self.y = 0.0
            
        # 冲刺控制
        self.sprinting = keys[pygame.K_LSHIFT]
            
        # 限制上下视角
        self.rot_x = max(-90, min(90, self.rot_x))
            
    def shoot(self):
        if self.ammo[self.equipped_weapon] <= 0:
            return None
            
        self.ammo[self.equipped_weapon] -= 1
        rad = math.radians(self.rot_y)
        dir_x = -math.sin(rad)
        dir_z = -math.cos(rad)
        
        # 根据武器类型返回不同子弹
        damage = 15 if self.equipped_weapon == "pistol" else 25 if self.equipped_weapon == "rifle" else 35
        return Bullet(
            self.x + dir_x * 0.5, 
            self.y + 0.8, 
            self.z + dir_z * 0.5, 
            dir_x, dir_z, 
            self.rot_y,
            damage
        )
        
    def pick_up_item(self, item):
        if item.type == "weapon":
            self.equipped_weapon = item.name
            self.ammo[self.equipped_weapon] = 30 if item.name == "rifle" else 15 if item.name == "pistol" else 8
            return True
        elif item.type == "ammo":
            add_amount = 15 if item.weapon_type == "pistol" else 30 if item.weapon_type == "rifle" else 8
            self.ammo[item.weapon_type] += add_amount
            return True
        elif item.type == "health":
            self.health = min(100, self.health + 40)
            return True
        elif item.type == "loot":
            self.loot_value += item.value
            return True
        return False

class Bullet:
    def __init__(self, x, y, z, dir_x, dir_z, rot_y, damage):
        self.x = x
        self.y = y
        self.z = z
        self.dir_x = dir_x
        self.dir_z = dir_z
        self.rot_y = rot_y
        self.damage = damage
        self.lifetime = 50  # 存在帧数
        
    def update(self):
        self.x += self.dir_x * BULLET_SPEED
        self.z += self.dir_z * BULLET_SPEED
        self.lifetime -= 1
        return self.lifetime > 0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glRotatef(self.rot_y, 0, 1, 0)
        glColor3f(1.0, 0.9, 0.7)
        
        # 绘制子弹
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.04, 0.04, 0.25, 8, 1)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glPopMatrix()

class Enemy:
    def __init__(self, x, z, difficulty=1):
        self.x = x
        self.z = z
        self.y = 0.0
        self.health = 40 * difficulty
        self.speed = 0.06 + (difficulty * 0.02)
        self.aggro_range = 12.0
        self.attack_range = 2.0
        self.attack_cooldown = 60 - (difficulty * 10)
        self.last_attack = 0
        self.difficulty = difficulty
        self.looted = False
        
    def update(self, player, frame_count):
        dx = player.x - self.x
        dz = player.z - self.z
        distance = math.sqrt(dx*dx + dz*dz)
        
        # 追击玩家
        if distance < self.aggro_range:
            self.x += (dx / distance) * self.speed
            self.z += (dz / distance) * self.speed
            
            # 攻击玩家
            if distance < self.attack_range and frame_count - self.last_attack > self.attack_cooldown:
                self.last_attack = frame_count
                return True  # 攻击成功
        return False
        
    def hit(self, damage):
        self.health -= damage
        return self.health <= 0
        
    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y + 1, self.z)
        
        # 敌人身体
        color_intensity = 0.8 - (self.difficulty * 0.2)
        glColor3f(0.9, color_intensity, color_intensity)
        draw_cube(0, 0, 0, 0.7, 1.6, 0.7)
        
        # 敌人头部
        glPushMatrix()
        glTranslatef(0, 1, 0)
        quad = gluNewQuadric()
        gluSphere(quad, 0.4, 16, 16)
        gluDeleteQuadric(quad)
        glPopMatrix()
        
        glPopMatrix()

class Item:
    def __init__(self, x, z, item_type, name=None, value=0, weapon_type=None):
        self.x = x
        self.z = z
        self.y = 0.2  # 稍微高于地面
        self.type = item_type  # weapon, ammo, health, loot
        self.name = name
        self.value = value
        self.weapon_type = weapon_type
        self.respawn_timer = 0
        
    def draw(self):
        if self.respawn_timer > 0:
            return
            
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        
        # 旋转效果让物品更明显
        glRotatef(pygame.time.get_ticks() * 0.1, 0, 1, 0)
        
        if self.type == "weapon":
            glColor3f(0.5, 0.5, 0.5)
            draw_cube(0, 0, 0, 0.6, 0.2, 0.2)
        elif self.type == "ammo":
            glColor3f(0.8, 0.6, 0.2)
            draw_cube(0, 0, 0, 0.3, 0.1, 0.3)
        elif self.type == "health":
            glColor3f(0.2, 0.8, 0.2)
            quad = gluNewQuadric()
            gluSphere(quad, 0.25, 16, 16)
            gluDeleteQuadric(quad)
        elif self.type == "loot":
            glColor3f(1.0, 0.8, 0.0)
            draw_cube(0, 0, 0, 0.2, 0.05, 0.2)
            
        glPopMatrix()

class EvacPoint:
    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.active = False
        self.activation_time = 0
        self.radius = 3.0
        
    def update(self, current_time):
        if self.active:
            return self.activation_time > current_time
            
    def draw(self, current_time):
        glPushMatrix()
        glTranslatef(self.x, 0.1, self.z)
        
        # 绘制撤离点平台
        glColor3f(0.3, 0.5, 0.8)
        glBegin(GL_QUADS)
        glVertex3f(-self.radius, 0, -self.radius)
        glVertex3f(self.radius, 0, -self.radius)
        glVertex3f(self.radius, 0, self.radius)
        glVertex3f(-self.radius, 0, self.radius)
        glEnd()
        
        # 激活状态下绘制光圈
        if self.active:
            remaining = max(0, (self.activation_time - current_time) / EVAC_TIME)
            glColor3f(0.3, 0.8, 0.5, 0.3)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0, 0.1, 0)
            for i in range(37):
                angle = i * 10 * math.pi / 180
                r = self.radius * (1 - (remaining * 0.3))
                glVertex3f(math.sin(angle) * r, 0.1, math.cos(angle) * r)
            glEnd()
            
        glPopMatrix()

class Map:
    def __init__(self):
        self.walls = []
        self.rooms = []
        self.spawn_points = []
        self.items = []
        self.evac_points = []
        self.generate_map()
        
    def generate_map(self):
        # 生成多层建筑风格地图
        self.generate_rooms()
        self.generate_walls()
        
        # 生成敌人出生点
        self.spawn_points = [
            (-14, -14), (14, -14), (14, 14), (-14, 14),
            (-10, 0), (10, 0), (0, 10), (0, -10),
            (-5, 12), (5, -12), (12, 5), (-12, -5)
        ]
        
        # 生成物品
        item_types = [
            {"type": "weapon", "name": "pistol"},
            {"type": "weapon", "name": "rifle"},
            {"type": "weapon", "name": "shotgun"},
            {"type": "ammo", "weapon_type": "pistol"},
            {"type": "ammo", "weapon_type": "rifle"},
            {"type": "ammo", "weapon_type": "shotgun"},
            {"type": "health"},
            {"type": "loot", "value": random.randint(50, 200)}
        ]
        
        for _ in range(30):
            x = random.uniform(-14, 14)
            z = random.uniform(-14, 14)
            # 确保物品生成在房间内
            if any(room.contains_point(x, z) for room in self.rooms):
                item_data = random.choice(item_types)
                self.items.append(Item(x, z, item_data))
        
        # 生成撤离点
        self.evac_points = [
            EvacPoint(-12, 12),
            EvacPoint(12, -12),
            EvacPoint(0, 0)  # 中心撤离点
        ]
        
    def generate_rooms(self):
        # 生成多个房间
        room_sizes = [
            (8, 8, -15, -15),  # 宽、高、x、z
            (8, 8, 7, -15),
            (8, 8, 7, 7),
            (8, 8, -15, 7),
            (6, 6, -5, -5),
            (6, 6, 5, -5),
            (6, 6, 5, 5),
            (6, 6, -5, 5)
        ]
        
        for w, h, x, z in room_sizes:
            self.rooms.append(Room(x, z, x + w, z + h))
    
    def generate_walls(self):
        # 外墙
        self.walls.append((-15, -15, 15, -15))  # 下
        self.walls.append((15, -15, 15, 15))   # 右
        self.walls.append((15, 15, -15, 15))   # 上
        self.walls.append((-15, 15, -15, -15)) # 左
        
        # 房间之间的隔墙
        for room in self.rooms:
            # 房间墙壁
            self.walls.append((room.x1, room.z1, room.x2, room.z1))
            self.walls.append((room.x2, room.z1, room.x2, room.z2))
            self.walls.append((room.x2, room.z2, room.x1, room.z2))
            self.walls.append((room.x1, room.z2, room.x1, room.z1))
            
            # 添加门
            door_count = random.randint(1, 2)
            for _ in range(door_count):
                side = random.choice(["north", "south", "east", "west"])
                if side == "north" and room.z2 < 15:
                    door_pos = random.uniform(room.x1 + 2, room.x2 - 2)
                    # 移除一段墙作为门
                    if (room.x1, room.z2, room.x2, room.z2) in self.walls:
                        self.walls.remove((room.x1, room.z2, room.x2, room.z2))
                        # 添加门两侧的墙
                        self.walls.append((room.x1, room.z2, door_pos - 1, room.z2))
                        self.walls.append((door_pos + 1, room.z2, room.x2, room.z2))
                elif side == "south" and room.z1 > -15:
                    door_pos = random.uniform(room.x1 + 2, room.x2 - 2)
                    if (room.x1, room.z1, room.x2, room.z1) in self.walls:
                        self.walls.remove((room.x1, room.z1, room.x2, room.z1))
                        self.walls.append((room.x1, room.z1, door_pos - 1, room.z1))
                        self.walls.append((door_pos + 1, room.z1, room.x2, room.z1))
                elif side == "east" and room.x2 < 15:
                    door_pos = random.uniform(room.z1 + 2, room.z2 - 2)
                    if (room.x2, room.z1, room.x2, room.z2) in self.walls:
                        self.walls.remove((room.x2, room.z1, room.x2, room.z2))
                        self.walls.append((room.x2, room.z1, room.x2, door_pos - 1))
                        self.walls.append((room.x2, door_pos + 1, room.x2, room.z2))
                elif side == "west" and room.x1 > -15:
                    door_pos = random.uniform(room.z1 + 2, room.z2 - 2)
                    if (room.x1, room.z1, room.x1, room.z2) in self.walls:
                        self.walls.remove((room.x1, room.z1, room.x1, room.z2))
                        self.walls.append((room.x1, room.z1, room.x1, door_pos - 1))
                        self.walls.append((room.x1, door_pos + 1, room.x1, room.z2))
    
    def draw(self):
        # 绘制地面
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_QUADS)
        glVertex3f(-15, 0, -15)
        glVertex3f(15, 0, -15)
        glVertex3f(15, 0, 15)
        glVertex3f(-15, 0, 15)
        glEnd()
        
        # 绘制房间地板区分
        for i, room in enumerate(self.rooms):
            glColor3f(0.22, 0.22, 0.22 + (i % 3) * 0.03)
            glBegin(GL_QUADS)
            glVertex3f(room.x1, 0.01, room.z1)
            glVertex3f(room.x2, 0.01, room.z1)
            glVertex3f(room.x2, 0.01, room.z2)
            glVertex3f(room.x1, 0.01, room.z2)
            glEnd()
        
        # 绘制墙壁
        glColor3f(0.4, 0.4, 0.4)
        for (x1, z1, x2, z2) in self.walls:
            glBegin(GL_QUADS)
            # 墙的前面
            glVertex3f(x1, 0, z1)
            glVertex3f(x2, 0, z2)
            glVertex3f(x2, 3, z2)
            glVertex3f(x1, 3, z1)
            # 墙的顶部
            glVertex3f(x1, 3, z1)
            glVertex3f(x2, 3, z2)
            glVertex3f(x2, 3.1, z2)
            glVertex3f(x1, 3.1, z1)
            glEnd()

class Room:
    def __init__(self, x1, z1, x2, z2):
        self.x1 = x1
        self.z1 = z1
        self.x2 = x2
        self.z2 = z2
        
    def contains_point(self, x, z):
        return self.x1 < x < self.x2 and self.z1 < z < self.z2

def draw_cube(x, y, z, width, height, depth):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # 前面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glEnd()
    
    # 后面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    glEnd()
    
    # 左面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, -depth/2)
    glEnd()
    
    # 右面
    glBegin(GL_QUADS)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glEnd()
    
    # 顶面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, -depth/2)
    glVertex3f(width/2, height/2, depth/2)
    glVertex3f(-width/2, height/2, depth/2)
    glEnd()
    
    # 底面
    glBegin(GL_QUADS)
    glVertex3f(-width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, -depth/2)
    glVertex3f(width/2, -height/2, depth/2)
    glVertex3f(-width/2, -height/2, depth/2)
    glEnd()
    
    glPopMatrix()

def draw_hud(player, evac_active, evac_time_left):
    # 绘制HUD
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    
    # 准星
    glColor3f(1.0, 0.0, 0.0)
    glLineWidth(2.0)
    glBegin(GL_LINES)
    glVertex2f(SCREEN_WIDTH//2 - 8, SCREEN_HEIGHT//2)
    glVertex2f(SCREEN_WIDTH//2 + 8, SCREEN_HEIGHT//2)
    glVertex2f(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 8)
    glVertex2f(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 8)
    glEnd()
    
    # 生命值
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(20, SCREEN_HEIGHT - 30)
    glVertex2f(20 + player.health * 2, SCREEN_HEIGHT - 30)
    glVertex2f(20 + player.health * 2, SCREEN_HEIGHT - 15)
    glVertex2f(20, SCREEN_HEIGHT - 15)
    glEnd()
    
    # 耐力条
    glColor3f(0.0, 0.6, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(20, SCREEN_HEIGHT - 50)
    glVertex2f(20 + player.stamina * 2, SCREEN_HEIGHT - 50)
    glVertex2f(20 + player.stamina * 2, SCREEN_HEIGHT - 35)
    glVertex2f(20, SCREEN_HEIGHT - 35)
    glEnd()
    
    # 弹药
    ammo_text = f"Ammo: {player.ammo[player.equipped_weapon]}"
    font = pygame.font.SysFont(None, 24)
    text_surface = font.render(ammo_text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2f(20, SCREEN_HEIGHT - 70)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # 当前武器
    weapon_text = f"Weapon: {player.equipped_weapon.capitalize()}"
    text_surface = font.render(weapon_text, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2f(20, SCREEN_HEIGHT - 95)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # 战利品价值
    loot_text = f"Loot: ${player.loot_value}"
    text_surface = font.render(loot_text, True, (255, 215, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2f(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 30)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    # 撤离倒计时
    if evac_active and evac_time_left > 0:
        evac_text = f"Evacuating in: {int(evac_time_left)}s"
        text_surface = font.render(evac_text, True, (0, 255, 100))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        glRasterPos2f(SCREEN_WIDTH//2 - 80, 30)
        glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                    GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glEnable(GL_DEPTH_TEST)
    glLineWidth(1.0)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_message(message, y_pos=SCREEN_HEIGHT//2):
    # 绘制临时消息
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glDisable(GL_DEPTH_TEST)
    glColor3f(1.0, 1.0, 1.0)
    
    font = pygame.font.SysFont(None, 48)
    text_surface = font.render(message, True, (255, 255, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    x_pos = SCREEN_WIDTH//2 - text_surface.get_width()//2
    glRasterPos2f(x_pos, y_pos)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), 
                GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    
    glEnable(GL_DEPTH_TEST)
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def init():
    pygame.init()
    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("搜打撤游戏")
    
    gluPerspective(70, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 50.0)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
    # 设置光源
    light_pos = [5.0, 10.0, 5.0, 1.0]
    light_ambient = [0.3, 0.3, 0.3, 1.0]
    light_diffuse = [0.7, 0.7, 0.7, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

def main():
    init()
    
    player = Player()
    game_map = Map()
    bullets = []
    # 初始敌人
    enemies = [Enemy(x, z, random.randint(1, 2)) for x, z in random.sample(game_map.spawn_points, 5)]
    
    frame_count = 0
    last_shot = 0
    shoot_delay = 15  # 射击延迟帧数
    game_state = "playing"  # playing, success, failed
    evac_activated = False
    game_start_time = time.time()
    message_timer = 0
    message = ""
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        current_time = time.time()
        dt = clock.tick(60) / 1000.0
        frame_count += 1
        
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # 激活撤离点
                if event.key == pygame.K_f and game_state == "playing" and not evac_activated:
                    for evac in game_map.evac_points:
                        dx = evac.x - player.x
                        dz = evac.z - player.z
                        if math.sqrt(dx*dx + dz*dz) < evac.radius:
                            evac.active = True
                            evac.activation_time = current_time + EVAC_TIME
                            evac_activated = True
                            message = "撤离点已激活！保护好自己直到撤离！"
                            message_timer = 180  # 显示3秒
                            break
        
        if game_state != "playing":
            # 游戏结束状态
            if keys[pygame.K_r]:
                # 重新开始游戏
                return main()
            if keys[pygame.K_q]:
                running = False
        
        else:
            # 输入处理
            keys = pygame.key.get_pressed()
            player.move(keys, dt)
            
            # 鼠标控制
            mouse_dx, mouse_dy = pygame.mouse.get_rel()
            player.rot_y += mouse_dx * ROT_SPEED
            player.rot_x -= mouse_dy * ROT_SPEED
            
            # 射击
            if keys[pygame.K_SPACE] and frame_count - last_shot > shoot_delay:
                bullet = player.shoot()
                if bullet:
                    bullets.append(bullet)
                    last_shot = frame_count
            
            # 拾取物品
            if keys[pygame.K_e]:
                for item in game_map.items[:]:
                    if item.respawn_timer > 0:
                        continue
                    dx = item.x - player.x
                    dz = item.z - player.z
                    if math.sqrt(dx*dx + dz*dz) < 1.5:
                        if player.pick_up_item(item):
                            game_map.items.remove(item)
                            # 物品一段时间后重生
                            if item.type == "loot":
                                new_item = Item(item.x, item.z, "loot", value=random.randint(30, 180))
                                new_item.respawn_timer = 300  # 5秒后重生
                                game_map.items.append(new_item)
                            break
            
            # 更新子弹
            bullets = [b for b in bullets if b.update()]
            
            # 检测子弹击中敌人
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    dx = enemy.x - bullet.x
                    dz = enemy.z - bullet.z
                    if math.sqrt(dx*dx + dz*dz) < 0.7:
                        bullets.remove(bullet)
                        if enemy.hit(bullet.damage):
                            enemies.remove(enemy)
                            # 敌人掉落物品
                            if random.random() < 0.6:
                                loot_value = random.randint(50, 200) * enemy.difficulty
                                game_map.items.append(Item(enemy.x, enemy.z, "loot", value=loot_value))
                            # 有几率掉落武器或弹药
                            if random.random() < 0.2:
                                game_map.items.append(Item(enemy.x, enemy.z, "ammo", weapon_type=random.choice(["pistol", "rifle"])))
                        break
            
            # 更新敌人
            for enemy in enemies[:]:
                if enemy.update(player, frame_count):
                    player.health -= 10 + (enemy.difficulty * 5)
                    if player.health <= 0:
                        game_state = "failed"
                        message = f"任务失败！收集的战利品价值: ${player.loot_value}"
                        message_timer = float('inf')
            
            # 定期生成新敌人
            if frame_count % 400 == 0 and len(enemies) < 8:
                x, z = random.choice(game_map.spawn_points)
                difficulty = min(3, 1 + int((current_time - game_start_time) / 60))
                enemies.append(Enemy(x, z, difficulty))
            
            # 更新物品重生
            for item in game_map.items:
                if item.respawn_timer > 0:
                    item.respawn_timer -= 1
            
            # 检查撤离状态
            if evac_activated:
                evac_time_left = 0
                for evac in game_map.evac_points:
                    if evac.active:
                        evac_time_left = evac.activation_time - current_time
                        if evac_time_left <= 0:
                            # 成功撤离
                            game_state = "success"
                            message = f"成功撤离！获得战利品价值: ${player.loot_value}"
                            message_timer = float('inf')
                        break
                
                # 检查玩家是否在撤离点内
                player_in_evac = False
                for evac in game_map.evac_points:
                    if evac.active:
                        dx = evac.x - player.x
                        dz = evac.z - player.z
                        if math.sqrt(dx*dx + dz*dz) < evac.radius:
                            player_in_evac = True
                            break
                
                if not player_in_evac:
                    message = "返回撤离点！"
                    message_timer = 60
        
        # 绘制场景
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # 设置相机
        gluLookAt(
            player.x, player.y + 1.7, player.z,
            player.x - math.sin(math.radians(player.rot_y)),
            player.y + 1.7 + math.sin(math.radians(player.rot_x)),
            player.z - math.cos(math.radians(player.rot_y)),
            0, 1, 0
        )
        
        game_map.draw()
        
        # 绘制物品
        for item in game_map.items:
            item.draw()
        
        # 绘制敌人
        for enemy in enemies:
            enemy.draw()
        
        # 绘制子弹
        for bullet in bullets:
            bullet.draw()
        
        # 绘制撤离点
        for evac in game_map.evac_points:
            evac.draw(current_time)
        
        # 绘制HUD
        evac_time_left = max(0, game_map.evac_points[0].activation_time - current_time) if evac_activated else 0
        draw_hud(player, evac_activated, evac_time_left)
        
        # 绘制消息
        if message_timer > 0:
            draw_message(message)
            message_timer -= 1
        
        # 游戏结束画面
        if game_state != "playing":
            draw_message(message, SCREEN_HEIGHT//2 + 50)
            draw_message("按 R 重新开始，按 Q 退出", SCREEN_HEIGHT//2 - 50)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
    