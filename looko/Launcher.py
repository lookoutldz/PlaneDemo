import pygame
import looko.Sprites as sp


class PlaneGame():

    def __init__(self):
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

    def __create_sprites(self):
        bg1 = sp.BGSprite()
        bg2 = sp.BGSprite(True)
        self.bg_group = pygame.sprite.Group(bg1,bg2)

    def __update_sprites(self):
        for group in [self.bg_group]:
            group.update()
            group.draw(self.screen)

    def __event_handler(self):
        pass

    def __check_collide(self):
        pass

    @classmethod
    def __create_user_events(cls):
        pass

    def launch(self):
        """开始游戏"""
        while True:
            # 1. 设置刷新帧率
            self.clock.tick(60)
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
    game.launch()
