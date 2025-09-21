from pygame import *
from random import randint
import random
from random import choice
# музика для фона
mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()
volume = 0.4
mixer.music.set_volume(volume)

# шрифти та написи
font.init()
font1 = font.Font('Bender_Black.otf', 40)
font2 = font.Font('Bender_Black.otf', 25)

# картинки
game_background = 'background1.png'
menu_background = 'menu_background.png'
img_player = "player_cars/car_1.png"
imgs_enemy_reversed = ["enemy cars/enemy_car_1_reversed.png", "enemy cars/enemy_car_2_reversed.png", "enemy cars/enemy_car_3_reversed.png", 'enemy cars/enemy_car_4_reversed.png', 'enemy cars/enemy_car_5_reversed.png', 'enemy cars/enemy_car_6_reversed.png', 'enemy cars/enemy_car_7_reversed.png']
imgs_enemy = ["enemy cars/enemy_car_1.png", "enemy cars/enemy_car_2.png", "enemy cars/enemy_car_3.png", 'enemy cars/enemy_car_4.png', 'enemy cars/enemy_car_5.png', 'enemy cars/enemy_car_6.png', 'enemy cars/enemy_car_7.png']
menu_car = 'menu_car.png'
####################################
score = 0


with open('doc.txt', 'r', encoding='utf-8') as file:
    a = file.readlines(1)
    a = a[0].split("=")
    a = a[1]
    a.replace('\n', '')
    max_score = int(a)

# створення батьківського класу для інших спрайтів
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# клас гравця, управління
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 145:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 260:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 170:
            self.rect.y += self.speed

# клас ворога
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global score
        if self.rect.y > win_height:
            self.kill()
            score += 1

win_width = 1000
win_height = 700
display.set_caption("traffic racer")
window = display.set_mode((win_width, win_height))



# створюємо фон
background = transform.scale(image.load(game_background), (win_width, win_height))
bg_rect = background.get_rect()

# декор для меню
car_in_menu = transform.scale(image.load(menu_car), (400, 200))

y1 = 0 #координата y для першого фону 
y2 = -bg_rect.height # координата y для другого фону
bg_speed = 15 # швидкість фону

#створення спрайтів
car = Player(img_player, 520, 500, 120, 180, 5)

enemy_cars = sprite.Group()

spawn_event_for_left_side = USEREVENT + 1
spawn_event_for_right_side = USEREVENT + 2

def restart_timers(): # перезапускаем таймеры по истечению которых срабатывают функции спавна врагов
    if not pause:
        time.set_timer(spawn_event_for_left_side, randint(1000, 2000)) # для спавна врагов слева
        time.set_timer(spawn_event_for_right_side, randint(1500, 2000)) # для спавна врагов справа

def stop_timers(pause): #если игра ставиться на паузу таймеры сбрасываються
    if pause:
        time.set_timer(spawn_event_for_left_side, 0)
        time.set_timer(spawn_event_for_right_side, 0)
    else:
        restart_timers() # когда игра продолжаеться таймеры перезапускаються

left_enemy_pos_x = [210, 360] # координати спавну ворогів на лівій стороні дороги
right_enemy_pos_x = [520, 670] # координати спавну ворогів на правій стороні

blur = transform.scale(image.load("blur.png"), (win_width, win_height)) # блюр для паузы
# Кнопки для меню и паузы
plus_button = GameSprite('plus_button.png', 520, 250, 50, 50, 0)
minus_button = GameSprite('minus_button.png', 450, 250, 50, 50, 0)
back_button = GameSprite('back_button.png', 75, 15, 65, 65, 0)
play_button = GameSprite('play_button.png', 400, 300, 200, 100, 0)
shop_button = GameSprite("shop_button.png", 400, 450, 200, 100, 0)
settings_button = GameSprite("settings_button.png", 20, 20, 50, 50, 0)
menu_car = GameSprite('menu_car.png', 250, 40, 500, 250, 0)

text1 = font1.render('Звук:', True, (0, 0, 0))
text2 = font1.render(str(volume * 100)+'%', True, (0, 0, 0))

tovar1 = GameSprite('owned_tovar.png', 250, 100, 100, 150, 0)
tovar1_image = GameSprite('player_cars/car_1.png', 273, 115, 50, 75, 0 )
tovar2 = GameSprite('owned_tovar.png', 450, 100, 100, 150, 0)
tovar2_image = GameSprite('player_cars/car_2.png', 474, 115, 50, 75, 0)
tovar3 = GameSprite('owned_tovar.png', 650, 100, 100, 150, 0)
tovar3_image = GameSprite('player_cars/car_3.png', 675, 115, 50, 75, 0)
tovar4 = GameSprite('owned_tovar.png', 250, 300, 100, 150, 0)
tovar4_image = GameSprite('player_cars/car_4.png', 273, 315, 50, 75, 0)
tovar5 = GameSprite('owned_tovar.png', 450, 300, 100, 150, 0)
tovar5_image = GameSprite('player_cars/car_5.png', 475, 315, 50, 75, 0)
tovar6 = GameSprite('owned_tovar.png', 650, 300, 100, 150 ,0)
tovar6_image = GameSprite('player_cars/car_6.png', 675, 315, 50, 75, 0)
tovar_text1 = font2.render('OWNED', True, (0, 0, 0))
tovar_text2 = font2.render('OWNED', True, (0, 0, 0))
tovar_text3 = font2.render('OWNED', True, (0, 0, 0))
tovar_text4 = font2.render('OWNED', True, (0, 0, 0))
tovar_text5 = font2.render('OWNED', True, (0, 0, 0))
tovar_text6 = font2.render('OWNED', True, (0, 0, 0))

def reset_game():
    global score
    score = 0
    car.rect.x = 520
    car.rect.y = 500
    for e in enemy_cars:
        e.kill()
    
stan = 0

pause = False
finish = True
# основний цикл гри
run = True
while run:
    for e in event.get():
        if e.type == QUIT: # выход из игры, закрытие окна
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE: # пауза
                if pause == False and finish == False:
                    stan = 0
                    pause = True
                    stop_timers(pause)
                    window.blit(blur, (0, 0)) #отрисовать картинку при паузе
                else:
                    pause = False
                    restart_timers()

        elif e.type == MOUSEBUTTONDOWN:
            if finish == True or pause == True:
                if stan == 0:
                    if play_button.rect.collidepoint(e.pos):
                        if pause == True:
                            pause = False
                            restart_timers()
                        if finish == True:
                            finish = False
                            restart_timers()
                            reset_game()
                    if settings_button.rect.collidepoint(e.pos):
                        stan = 1
                    if shop_button.rect.collidepoint(e.pos):
                        stan = 2
                if back_button.rect.collidepoint(e.pos):
                    if stan == 1 or stan == 2:
                        stan = 0

        elif e.type == spawn_event_for_left_side: # когда таймер истек 
            if not pause and not finish:
                new_enemy_left = Enemy(random.choice(imgs_enemy_reversed), random.choice(left_enemy_pos_x), -200, 120, 190, 10) # создаем нового врага
                enemy_cars.add(new_enemy_left)

        elif e.type == spawn_event_for_right_side: # когда таймер истек
            if not finish and not pause:
                new_enemy_right = Enemy(random.choice(imgs_enemy), random.choice(right_enemy_pos_x), -200, 120, 190, 5)
                enemy_cars.add(new_enemy_right)

    if pause == True:
        if stan == 0:
            window.blit(background, (0, 0))
            window.blit(blur, (0, 0))
            play_button.reset()
            settings_button.reset()
            shop_button.reset()
            menu_car.reset()
        elif stan == 1:
            window.blit(background, (0, 0))
            back_button.reset()
            plus_button.reset()
            minus_button.reset()

            window.blit(text1, (400, 200))
            window.blit(text2, (520, 200))
            for e in event.get():
                if e.type == MOUSEBUTTONDOWN:
                    if plus_button.rect.collidepoint(e.pos):
                        volume += 0.1
                        if volume > 1:
                            volume = 1
                    if minus_button.rect.collidepoint(e.pos):
                        volume -= 0.1
                        if volume < 0:
                            volume = 0
                    
                    mixer.music.set_volume(volume)
                    text2 = font1.render(str(int(volume * 100))+'%', True, (0, 0, 0))

        elif stan == 2:
            window.blit(background, (0, 0))
            back_button.reset()
            tovar1.reset()
            tovar1_image.reset()
            tovar2.reset()
            tovar2_image.reset()
            tovar3.reset()
            tovar3_image.reset()
            tovar4.reset()
            tovar4_image.reset()
            tovar5.reset()
            tovar5_image.reset()
            tovar6.reset()
            tovar6_image.reset()
            window.blit(tovar_text1, (256, 210))
            window.blit(tovar_text2, (456, 210))
            window.blit(tovar_text3, (656, 210))
            window.blit(tovar_text4, (256, 410))
            window.blit(tovar_text5, (456, 410))
            window.blit(tovar_text6, (656, 410))
            for e in event.get():
                if e.type == MOUSEBUTTONDOWN:
                    if tovar1.rect.collidepoint(e.pos):
                        img_player = 'player_cars/car_1.png'
                        car = Player(img_player, 520, 500, 120, 180, 5)
                    elif tovar2.rect.collidepoint(e.pos):
                        img_player = "player_cars/car_2.png"
                        car = Player(img_player, 520, 500, 120, 180, 5)
                    elif tovar3.rect.collidepoint(e.pos):
                        img_player = "player_cars/car_3.png"
                        car = Player(img_player, 520, 500, 120, 180, 5)
                    elif tovar4.rect.collidepoint(e.pos):
                        img_player = "player_cars/car_4.png"
                        car = Player(img_player, 520, 500, 120, 180, 5)
                    elif tovar5.rect.collidepoint(e.pos):
                        img_player = "player_cars/car_5.png"
                        car = Player(img_player, 520, 500, 120, 180, 5)
                    elif tovar6.rect.collidepoint(e.pos):
                        img_player = "player_cars/car_6.png"
                        car = Player(img_player, 520, 500, 120, 180, 5)

    else:

        # сама гра дії спрайтів, перевірка правил гри, перемальовка
        if not finish:

            # координати обох фонів збільшуються тим самим картинки постійно спускаються вниз зі швидкістю bg_speed
            y1 += bg_speed
            y2 += bg_speed

            # перевірка якщо фон виходить за єкран він відмальовується зверху й знову спускається
            if y1 >= bg_rect.height:
                y1 = -bg_rect.height
            if y2 >= bg_rect.height:
                y2 = -bg_rect.height
            
            #відмальовка фонів на екрані
            window.blit(background, (0, y1))
            window.blit(background, (0, y2))

            text = font1.render("Score:"+ str(score), True, (0, 0, 0))
            window.blit(text, (10, 20))

            #рухи спрайтів
            car.update()
            enemy_cars.update()

            # оновлюємо їх у новому місці при кожній ітерації циклу
            car.reset()
            enemy_cars.draw(window)

            if sprite.spritecollide(car, enemy_cars, False):
                finish = True

        if finish == True:
            if stan == 0:
                window.blit(background, (0, 0))
                play_button.reset()
                settings_button.reset()
                shop_button.reset()
                menu_car.reset()
            elif stan == 1:
                window.blit(background, (0, 0))
                back_button.reset()
                plus_button.reset()
                minus_button.reset()
                window.blit(text1, (400, 200))
                window.blit(text2, (520, 200))

                for e in event.get():
                    if e.type == MOUSEBUTTONDOWN:
                        if plus_button.rect.collidepoint(e.pos):
                            volume += 0.1
                            if volume > 1:
                                volume = 1
                        if minus_button.rect.collidepoint(e.pos):
                            volume -= 0.1
                            if volume < 0:
                                volume = 0
                    
                    mixer.music.set_volume(volume)
                    text2 = font1.render(str(int(volume * 100))+'%', True, (0, 0, 0))

            elif stan == 2:
                window.blit(background, (0, 0))
                back_button.reset()   
                tovar1.reset() 
                tovar1_image.reset()
                tovar2.reset()
                tovar2_image.reset() 
                tovar3.reset()
                tovar3_image.reset()
                tovar4.reset()
                tovar4_image.reset()
                tovar5.reset()
                tovar5_image.reset()
                tovar6.reset()
                tovar6_image.reset()
                window.blit(tovar_text1, (256, 210))
                window.blit(tovar_text2, (456, 210))
                window.blit(tovar_text3, (656, 210))
                window.blit(tovar_text4, (256, 410))
                window.blit(tovar_text5, (456, 410))
                window.blit(tovar_text6, (656, 410))

                for e in event.get():
                    if e.type == MOUSEBUTTONDOWN:
                        if tovar1.rect.collidepoint(e.pos):
                            img_player = 'player_cars/car_1.png'
                            car = Player(img_player, 520, 500, 120, 180, 5)
                        elif tovar2.rect.collidepoint(e.pos):
                            img_player = "player_cars/car_2.png"
                            car = Player(img_player, 520, 500, 120, 180, 5)
                        elif tovar3.rect.collidepoint(e.pos):
                            img_player = "player_cars/car_3.png"
                            car = Player(img_player, 520, 500, 120, 180, 5)
                        elif tovar4.rect.collidepoint(e.pos):
                            img_player = "player_cars/car_4.png"
                            car = Player(img_player, 520, 500, 120, 180, 5)
                        elif tovar5.rect.collidepoint(e.pos):
                            img_player = "player_cars/car_5.png"
                            car = Player(img_player, 520, 500, 120, 180, 5)
                        elif tovar6.rect.collidepoint(e.pos):
                            img_player = "player_cars/car_6.png"
                            car = Player(img_player, 520, 500, 120, 180, 5)

    display.update()
    #цикл спрацьовує кожні 0.01 секунд
    time.delay(10)


