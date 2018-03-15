import random
import math
import pygame


# 游戏屏幕大小
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)


class GameSprite(pygame.sprite.Sprite):
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

    @staticmethod
    def image_names(prefix, count):
        names = []
        for i in range(1, count + 1):
            names.append("./images/" + prefix + str(i) + ".png")
        return names

    def update(self, *args):
        # 默认在垂直方向移动
        self.rect.top += self.speed


class BGSprite(GameSprite):
    """背景精灵"""
    def __init__(self, is_alt=False):
        image_name = "./images/background.png"
        super().__init__(image_name)
        self.speed = 2
        # 判断是否交替图片，如果是，将图片设置到屏幕顶部
        if is_alt:
            self.rect.bottom = 0

    def update(self, *args):
        # 调用父类方法
        super().update(args)
        # 判断是否超出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            self.rect.bottom = 0


class PlaneSprite(GameSprite):
    """飞机精灵，包括敌机和英雄"""

    def __init__(self, image_names, destroy_names, life, speed):
        image_name = image_names[0]
        super().__init__(image_name, speed)
        # 生命值
        self.life = life
        # 正常图像列表
        self.__life_images = []
        for file_name in image_names:
            image = pygame.image.load(file_name)
            self.__life_images.append(image)
        # 被摧毁图像列表
        self.__destroy_images = []
        for file_name in destroy_names:
            image = pygame.image.load(file_name)
            self.__destroy_images.append(image)
        # 默认播放生存图片
        self.images = self.__life_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = True
        # 是否可以被删除
        self.can_destroied = False

    def destroied(self):
        """飞机被摧毁"""
        # 默认播放生存图片
        self.images = self.__destroy_images
        # 显示图像索引
        self.show_image_index = 0
        # 是否循环播放
        self.is_loop_show = False

    def update_images(self):
        """更新图像"""
        pre_index = int(self.show_image_index)
        self.show_image_index += 0.05
        count = len(self.images)
        # 判断是否循环播放
        if self.is_loop_show:
            self.show_image_index %= len(self.images)
        elif self.show_image_index > count - 1:
            self.show_image_index = count - 1
            self.can_destroied = True
        current_index = int(self.show_image_index)
        if pre_index != current_index:
            self.image = self.images[current_index]

    def update(self, *args):
        self.update_images()
        super().update(args)


class EnemySprite(PlaneSprite):
    """敌机精灵"""

    def __init__(self):
        image_names = ["./images/enemy1.png"]
        destroy_names = GameSprite.image_names("enemy1_down", 4)
        super().__init__(image_names, destroy_names, 2, 1)
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
            self.kill()
            print("敌人已安突破防线，GG...")
            pygame.quit()
            exit()
        # 判断敌机是否已经被销毁
        if self.can_destroied:
            self.kill()


class StrongEnemySprite(PlaneSprite):
    """敌机精灵"""

    def __init__(self):
        image_names = ["./images/enemy2.png"]
        destroy_names = GameSprite.image_names("enemy2_down", 4)
        super().__init__(image_names, destroy_names, 25, 1)
        # 随机敌机出现位置
        width = SCREEN_RECT.width - self.rect.width
        self.rect.left = random.randint(0, width)
        self.rect.bottom = 0
        self.speed = 1

    def update(self, *args):
        super().update(args)
        # 判断敌机是否移出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            self.kill()
            print("敌人已安突破防线，GG...")
            pygame.quit()
            exit()
        # 判断敌机是否已经被销毁
        if self.can_destroied:
            self.kill()


class BossSprite(PlaneSprite):
    """敌机精灵"""

    def __init__(self):
        image_names = ["./images/enemy3_n1.png"]
        destroy_names = GameSprite.image_names("enemy3_down", 4)
        super().__init__(image_names, destroy_names, 80, 1)
        # 随机敌机出现位置
        width = SCREEN_RECT.width - self.rect.width
        self.rect.left = random.randint(0, width)
        self.rect.bottom = 0
        self.speed = 1

    def update(self, *args):
        super().update(args)
        # 判断敌机是否移出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            self.kill()
            print("敌人已安突破防线，GG...")
            pygame.quit()
            exit()
        # 判断敌机是否已经被销毁
        if self.can_destroied:
            self.kill()


class HeroSprite(GameSprite):
    """英雄精灵"""

    def __init__(self):
        image_name = "./images/life.png"
        super().__init__(image_name, 0)
        self.has_bombs = 0
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
        # bullet_count = len(self.bullets.sprites())
        # print("子弹数量 %d" % bullet_count)
        for i in range(0, 3):
            # 创建子弹精灵
            bullet = BulletSprite()
            # 设置子弹位置
            bullet.rect.bottom = self.rect.top - i * 20
            bullet.rect.centerx = self.rect.centerx

            # 将子弹添加到精灵组
            self.bullets.add(bullet)


class BulletSprite(GameSprite):
    """子弹精灵"""

    def __init__(self):
        image_name = "./images/bullet1.png"
        super().__init__(image_name, -10)
        self.speed = -10

    def update(self, *args):
        super().update(args)
        # 判断是否超出屏幕
        if self.rect.bottom < 0:
            self.kill()


class BombSprite(GameSprite):
    """炸弹精灵"""
    def __init__(self):
        image_name = "./images/bomb_supply.png"
        super().__init__(image_name)
        # 随机补给出现位置
        self.speed = 1
        self.life = 1
        width = SCREEN_RECT.width - self.rect.width
        self.rect.left = random.randint(0, width)
        self.rect.bottom = 0

    def update(self, *args):
        super().update(args)
        # 判断补给是否移出屏幕
        if self.rect.top >= SCREEN_RECT.height:
            # 将精灵从所有组中删除
            self.kill()
        if self.life <= 0:
            self.kill()