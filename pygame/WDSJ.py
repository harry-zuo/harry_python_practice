import pygame
import random
import sys

# 初始化pygame
pygame.init()

# 游戏常量
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

# 颜色定义
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (34, 139, 34)  # 草地颜色
DIRT_COLOR = (139, 69, 19)    # 泥土颜色
STONE_COLOR = (169, 169, 169) # 石头颜色
WOOD_COLOR = (139, 69, 19)    # 木头颜色
LEAF_COLOR = (34, 139, 34)    # 树叶颜色

# 方块类型
AIR = 0
GRASS = 1
DIRT = 2
STONE = 3
WOOD = 4
LEAVES = 5

# 创建屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Minecraft")

# 时钟
clock = pygame.time.Clock()

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = (255, 0, 0)  # 红色玩家
        self.speed = 5
        self.jumping = False
        self.jump_vel = 0
        self.gravity = 0.5
        
    def draw(self, surface, offset_x, offset_y):
        # 绘制玩家（相对于屏幕的位置）
        pygame.draw.rect(surface, self.color, 
                         (self.x + offset_x, self.y + offset_y, 
                          self.width, self.height))
    
    def move(self, dx, dy, world):
        # 水平移动
        self.x += dx
        
        # 水平碰撞检测
        if self.collide(world):
            self.x -= dx
            
        # 应用重力
        self.jump_vel += self.gravity
        self.y += self.jump_vel
        
        # 如果正在跳跃且达到最高点，停止跳跃
        if self.jump_vel > 0:
            self.jumping = False
            
        # 垂直碰撞检测
        if self.collide(world):
            self.y -= self.jump_vel
            self.jump_vel = 0
            self.jumping = False
    
    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_vel = -12  # 负值表示向上
    
    def collide(self, world):
        # 检查玩家是否与世界中的方块碰撞
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        # 只检查玩家周围的方块以提高性能
        start_x = max(0, int(self.x // TILE_SIZE) - 1)
        end_x = min(len(world[0]), int((self.x + self.width) // TILE_SIZE) + 1)
        start_y = max(0, int(self.y // TILE_SIZE) - 1)
        end_y = min(len(world), int((self.y + self.height) // TILE_SIZE) + 1)
        
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if world[y][x] != AIR:
                    tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, 
                                           TILE_SIZE, TILE_SIZE)
                    if player_rect.colliderect(tile_rect):
                        return True
        return False

def generate_world(width, height):
    """生成随机世界"""
    world = [[AIR for _ in range(width)] for _ in range(height)]
    
    # 基本地形
    ground_level = height - 10
    
    for x in range(width):
        # 随机地形高度变化
        if x > 0:
            ground_level += random.randint(-1, 1)
            ground_level = max(height - 20, min(ground_level, height - 5))
        
        # 放置草方块
        world[ground_level][x] = GRASS
        
        # 放置泥土
        for y in range(ground_level + 1, ground_level + 4):
            if y < height:
                world[y][x] = DIRT
        
        # 放置石头
        for y in range(ground_level + 4, height):
            if y < height:
                # 偶尔有石头
                if random.random() < 0.7:
                    world[y][x] = STONE
                else:
                    world[y][x] = DIRT
    
    # 添加一些树
    for _ in range(20):
        tree_x = random.randint(0, width - 1)
        # 找到地面位置
        tree_y = 0
        for y in range(height):
            if world[y][tree_x] != AIR:
                tree_y = y - 1
                break
        
        # 树干
        trunk_height = random.randint(3, 5)
        for y in range(tree_y - trunk_height, tree_y):
            if 0 <= y < height:
                world[y][tree_x] = WOOD
        
        # 树叶
        leaf_radius = 2
        for dy in range(-leaf_radius, leaf_radius + 1):
            for dx in range(-leaf_radius, leaf_radius + 1):
                if abs(dx) + abs(dy) <= leaf_radius + 1:  # 粗略的圆形
                    leaf_x = tree_x + dx
                    leaf_y = tree_y - trunk_height - 1 + dy
                    if 0 <= leaf_x < width and 0 <= leaf_y < height:
                        if random.random() < 0.8:  # 一些随机性
                            world[leaf_y][leaf_x] = LEAVES
    
    return world

def draw_world(surface, world, offset_x, offset_y):
    """绘制世界（只绘制可见部分）"""
    # 填充天空
    surface.fill(SKY_BLUE)
    
    # 计算可见的方块范围
    start_x = max(0, int(-offset_x // TILE_SIZE) - 1)
    end_x = min(len(world[0]), int((-offset_x + SCREEN_WIDTH) // TILE_SIZE) + 1)
    start_y = max(0, int(-offset_y // TILE_SIZE) - 1)
    end_y = min(len(world), int((-offset_y + SCREEN_HEIGHT) // TILE_SIZE) + 1)
    
    # 绘制方块
    for y in range(start_y, end_y):
        for x in range(start_x, end_x):
            tile_type = world[y][x]
            if tile_type != AIR:
                # 选择方块颜色
                if tile_type == GRASS:
                    color = GROUND_COLOR
                elif tile_type == DIRT:
                    color = DIRT_COLOR
                elif tile_type == STONE:
                    color = STONE_COLOR
                elif tile_type == WOOD:
                    color = WOOD_COLOR
                elif tile_type == LEAVES:
                    color = LEAF_COLOR
                else:
                    color = (255, 255, 255)  # 白色（默认）
                
                # 绘制方块
                rect = (x * TILE_SIZE + offset_x, 
                        y * TILE_SIZE + offset_y, 
                        TILE_SIZE - 1,  # -1 是为了显示网格线
                        TILE_SIZE - 1)
                pygame.draw.rect(surface, color, rect)

def get_block_at_cursor(world, mouse_pos, offset_x, offset_y):
    """获取鼠标指向的方块坐标"""
    mx, my = mouse_pos
    # 转换屏幕坐标到世界坐标
    world_x = (mx - offset_x) // TILE_SIZE
    world_y = (my - offset_y) // TILE_SIZE
    
    # 检查是否在世界范围内
    if 0 <= world_x < len(world[0]) and 0 <= world_y < len(world):
        return world_x, world_y
    return None

def main():
    # 世界大小（以方块为单位）
    WORLD_WIDTH = 100
    WORLD_HEIGHT = 50
    
    # 生成世界
    world = generate_world(WORLD_WIDTH, WORLD_HEIGHT)
    
    # 创建玩家（放置在世界中间）
    player = Player(WORLD_WIDTH * TILE_SIZE // 2, WORLD_HEIGHT * TILE_SIZE // 2)
    
    # 相机偏移
    offset_x = SCREEN_WIDTH // 2 - player.width // 2 - player.x
    offset_y = SCREEN_HEIGHT // 2 - player.height // 2 - player.y
    
    # 当前选中的方块类型
    selected_block = GRASS
    
    running = True
    while running:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 左键破坏方块
                if event.button == 1:
                    block_pos = get_block_at_cursor(world, pygame.mouse.get_pos(), 
                                                  offset_x, offset_y)
                    if block_pos:
                        x, y = block_pos
                        world[y][x] = AIR
                # 右键放置方块
                elif event.button == 3:
                    block_pos = get_block_at_cursor(world, pygame.mouse.get_pos(), 
                                                  offset_x, offset_y)
                    if block_pos:
                        x, y = block_pos
                        world[y][x] = selected_block
            elif event.type == pygame.KEYDOWN:
                # 数字键切换方块类型
                if event.key == pygame.K_1:
                    selected_block = GRASS
                elif event.key == pygame.K_2:
                    selected_block = DIRT
                elif event.key == pygame.K_3:
                    selected_block = STONE
                elif event.key == pygame.K_4:
                    selected_block = WOOD
                elif event.key == pygame.K_5:
                    selected_block = LEAVES
                elif event.key == pygame.K_SPACE:
                    player.jump()
        
        # 玩家移动
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -player.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = player.speed
        
        player.move(dx, 0, world)
        
        # 更新相机位置（跟随玩家）
        target_offset_x = SCREEN_WIDTH // 2 - player.width // 2 - player.x
        target_offset_y = SCREEN_HEIGHT // 2 - player.height // 2 - player.y
        
        # 平滑相机移动
        offset_x += (target_offset_x - offset_x) * 0.1
        offset_y += (target_offset_y - offset_y) * 0.1
        
        # 绘制
        draw_world(screen, world, offset_x, offset_y)
        player.draw(screen, offset_x, offset_y)
        
        # 显示选中的方块类型
        font = pygame.font.SysFont(None, 24)
        block_names = ["Air", "Grass", "Dirt", "Stone", "Wood", "Leaves"]
        text = font.render(f"Selected: {block_names[selected_block]} (1-5 to change)", 
                         True, (255, 255, 255))
        screen.blit(text, (10, 10))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
