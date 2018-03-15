import pygame
import time
import Sprites as sp

# 敌机出现事件
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 精英敌机出现事件
CREATE_STRONG_ENEMY_EVENT = pygame.USEREVENT + 3
# boss敌机出现事件
CREATE_BOSS_EVENT = pygame.USEREVENT + 4
# 炸弹出现事件
CREATE_BOMB_EVENT = pygame.USEREVENT + 2
# 发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class PlaneGame():

    def __init__(self):
        self.start_time = time.clock()
        # 1. pygame 初始化
        pygame.init()
        # 2. 创建游戏屏幕
        self.screen = pygame.display.set_mode(sp.SCREEN_RECT.size)
        # 3. 创建游戏时钟
        self.clock = pygame.time.Clock()
        # 4. 创建精灵组
        self.__create_sprites()
        # 5. 创建用户事件
        PlaneGame.__create_user_events()


    # 创建精灵组
    def __create_sprites(self):
        """创建精灵组"""
        # 背景组
        bg1 = sp.BGSprite()
        bg2 = sp.BGSprite(True)
        self.back_group = pygame.sprite.Group(bg1, bg2)
        # 敌机组
        enemy = sp.EnemySprite()
        self.enemy_group = pygame.sprite.Group(enemy)
        # 英雄组
        self.hero = sp.HeroSprite()
        self.hero_group = pygame.sprite.Group(self.hero)
        # 补给组
        self.bomb = sp.BombSprite()
        self.bomb_group = pygame.sprite.Group(self.bomb)

        self.destroy_group = pygame.sprite.Group()

    def __event_handler(self):
        """事件监听"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("退出游戏...")
                pygame.quit()
                exit()
            if event.type == CREATE_ENEMY_EVENT:
                # 创建敌机，并且添加到敌机组
                self.enemy_group.add(sp.EnemySprite())
                # 测试敌机精灵数量
                # enemy_count = len(self.enemy_group.sprites())
                # print("敌机精灵数量 %d" % enemy_count)
            if event.type == CREATE_STRONG_ENEMY_EVENT:
                # 创建敌机，并且添加到敌机组
                self.enemy_group.add(sp.StrongEnemySprite())
            if event.type == CREATE_BOSS_EVENT:
                # 创建敌机，并且添加到敌机组
                self.enemy_group.add(sp.BossSprite())
            if event.type == CREATE_BOMB_EVENT:
                # 创建bomb，并且添加到bomb组
                self.bomb_group.add(sp.BombSprite())
            if event.type == HERO_FIRE_EVENT:
                # 英雄发射子弹
                self.hero.fire()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                print("gaga, bombs left : %d" % self.hero.has_bombs)
                if self.hero.has_bombs > 0:
                    self.hero.has_bombs -= 1
                    enemies = pygame.sprite.groupcollide(self.enemy_group, self.enemy_group, False, True )
                    for enemy in enemies:
                        enemy.life -= 1
                        if enemy.life <= 0:
                            enemy.add(self.destroy_group)
                            enemy.remove(self.enemy_group)

        # 通过 pygame.key 获取用户按键
        keys_pressed = pygame.key.get_pressed()
        hdir = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
        vdir = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]
        # 根据移动方向设置英雄的速度
        self.hero.h_speed = hdir * 5
        self.hero.v_speed = vdir * 5


    def __update_sprites(self):
        """更新精灵组"""
        for group in [self.back_group, self.enemy_group, self.destroy_group,
                      self.hero_group, self.hero.bullets, self.bomb_group]:
            group.update()
            group.draw(self.screen)


    def __check_collide(self):
        """碰撞检测"""
        # 1. 子弹摧毁敌机
        enemies = pygame.sprite.groupcollide(self.enemy_group, self.hero.bullets, False, True)
        for enemy in enemies:
            enemy.life -= 1
            if enemy.life <= 0:
                enemy.add(self.destroy_group)
                enemy.remove(self.enemy_group)
                enemy.destroied()
        # 2. 英雄被撞毁
        collide_list = pygame.sprite.spritecollide(self.hero, self.enemy_group, False)
        if len(collide_list) > 0:
            self.hero.is_alive = False
            print("英雄牺牲...")
            end_time = time.clock()
            print("游戏时长 ： %.2f s" % (end_time - self.start_time))
            pygame.quit()
            exit()
        # 3.炸弹砸脸
        collide_list = pygame.sprite.spritecollide(self.hero, self.bomb_group, True)
        if len(collide_list) > 0:
            self.bomb.life -= 1
            self.hero.has_bombs += 1
            print("英雄被砸...")

    # 创建用户事件
    @classmethod
    def __create_user_events(cls):
        """创建用户事件"""
        # 每秒添加2架敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 500)
        # 每10秒添加一架敌机
        pygame.time.set_timer(CREATE_STRONG_ENEMY_EVENT, 7000)
        # 每20秒添加一架boss
        pygame.time.set_timer(CREATE_BOSS_EVENT, 17000)
        # 每30秒添加一个bomb
        pygame.time.set_timer(CREATE_BOMB_EVENT, 30000)
        # 每秒发射10次子弹
        pygame.time.set_timer(HERO_FIRE_EVENT, 100)


    def launch_game(self):
        """开始游戏"""
        while True:
            # 1. 设置刷新帧率
            self.clock.tick(240)
            # 2. 事件监听
            self.__event_handler()
            # 3. 更新精灵组
            self.__update_sprites()
            # 碰撞检测
            self.__check_collide()
            # 4. 更新屏幕显示
            pygame.display.update()

if __name__ == '__main__':

    game = PlaneGame()
    game.launch_game()