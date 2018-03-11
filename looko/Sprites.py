import random
import math
import pygame


# 游戏屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)

class GameSprites(pygame.sprite.Sprite):
    """游戏精灵基类"""

    def __init__(self, image_name, h_speed=5, v_speed=5):
        # 调用父类的初始化方法
        super().__init__()
        # 加载图像
        self.image = pygame.image.load(image_name)
        # 设置尺寸
        self.rect = self.image.get_rect()
        # 记录速度
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.speed = math.sqrt((h_speed*h_speed)+(v_speed*v_speed))

    def update(self, *args):
        # 默认在垂直方向移动
        self.rect.top += self.speed


class BGSprite(GameSprites):
    """背景精灵"""

    def __init__(self, is_alt = False):
        image_name = "./images/background.png"
        super().__init__(image_name)
        # 判断是否交替图片，如果是，将图片设置到屏幕顶部
        if is_alt:
            self.rect.bottom = 0

    def update(self, *args):
        # 调用父类方法
        super().update(args)
        # 判断是否超出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            self.rect.bottom = 0


class EnemySprite(GameSprites):
    """敌机精灵"""

    def __init__(self):
        image_name = "./images/enemy1.png"
        super().__init__(image_name)
        # 随机敌机出现位置
        width = SCREEN_RECT.width - self.rect.width
        self.rect.left = random.randint(0, width)
        self.rect.bottom = 0
        # 随机速度
        self.speed = random.randint(1, 2)

    def update(self, *args):
        super().update(args)
        # 判断敌机是否移出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            # 将精灵从所有组中删除
            self.kill()


class HeroSprite(GameSprites):
    """英雄精灵"""

    def __init__(self):
        image_name = "../images/me1.png"
        super().__init__(image_name, 0, 0)
        # 设置初始位置
        self.rect.centerx = SCREEN_RECT.centerx
        self.rect.bottom = SCREEN_RECT.bottom - 20
        # 创建子弹组
        self.bullets = pygame.sprite.Group()

    def update(self, *args):
        # 飞机水平移动
        self.rect.left += self.h_speed
        # 超出屏幕检测
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_RECT.right:
            self.rect.right = SCREEN_RECT.right

        # 飞机垂直移动
        self.rect.top += self.v_speed
        # 超出屏幕检测
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_RECT.bottom:
            self.rect.bottom = SCREEN_RECT.bottom

    def fire(self):
        pass