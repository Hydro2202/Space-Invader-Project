#Space Invader
#_________________________________________________Import modules__________________________________________________________________________________________________
import pygame
import os
import time
import random
pygame.font.init()
pygame.init()  # Initialize Pygame
pygame.mixer.init()  # Initialize Pygame's mixer

# _______________________________________Load Custom Laser Images__________________________________________________
CUSTOM_LASER_1 = pygame.image.load(os.path.join("SPACESS", "bullet.png"))
CUSTOM_LASER_2 = pygame.image.load(os.path.join("SPACESS", "bullet1.png"))
CUSTOM_LASER_3 = pygame.image.load(os.path.join("SPACESS", "burst.png"))

#________________________________________Size of screen____________________________________________________
WIDTH, HEIGHT = 1000, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invader")

#___________________________________Load Explosion Image_______________________________________________________________
EXPLOSION = pygame.image.load(os.path.join("SPACESS", "exp4.png"))

# ___________________________________Load Enemy Images____________________________________________________________________
RED_SPACE_SHIP = pygame.image.load(os.path.join("SPACESS", "ENEMY_SHIP2.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("SPACESS", "ufo.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("SPACESS", "alien3.png"))


# _________________________________Load Player Image____________________________________________________________________
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("SPACESS", "SPACESHIP4.png"))

# _______________________________________Load Laser______________________________________________________________
RED_LASER = pygame.image.load(os.path.join("SPACESS", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("SPACESS", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("SPACESS", "alien_bullet.png"))

#_________________________________Player Laser_______________________________________________________________________________
YELLOW_LASER = pygame.image.load(os.path.join("SPACESS", "pixel_laser_blue.png"))

#___________________________________________Background_____________________________________________________________________
BG = pygame.transform.scale(pygame.image.load(os.path.join("SPACESS", "bg.png")), (WIDTH, HEIGHT))

#____________________________________GAME BACKGROUND MUSIC__________________________________________________________________
background_music = pygame.mixer.Sound(os.path.join("SPACESS","Space.mp3"))
background_music.set_volume(0.20)
#________________________________________Sound effect______________________________________________________________________ 
pygame.mixer.init()
shoot_sounds = pygame.mixer.Sound(os.path.join("SPACESS","laser.wav"))
red_laser_sound = pygame.mixer.Sound(os.path.join("SPACESS", "laser.wav"))
green_laser_sound = pygame.mixer.Sound(os.path.join("SPACESS", "laser.wav"))
blue_laser_sound = pygame.mixer.Sound(os.path.join("SPACESS", "laser.wav"))
explosion_fx = pygame.mixer.Sound(os.path.join("SPACESS","explosion2.wav"))

#___________________________Sound effect adjustment_________________________________________
shoot_sounds.set_volume(0.2)
red_laser_sound.set_volume(0.2)
green_laser_sound.set_volume(0.2)
blue_laser_sound.set_volume(0.2)
explosion_fx.set_volume(1000)

#______________________________________Define class laser_______________________________________________________________________
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        shoot_sounds.play()

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

#_____________________________________________Definee class ship_______________________________________________________________________
class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):             
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        explosion = Explosion(obj.x, obj.y, 2)  # Adjust the size of explosion img
                        explosion_group.add(explosion)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 10 #Adjust the speed of laser

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

#_____________________________________Player Ship_______________________________________________________
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_index = 0
        self.laser_options = [YELLOW_LASER, CUSTOM_LASER_1, CUSTOM_LASER_2, CUSTOM_LASER_3]
        self.laser_img = self.laser_options[self.laser_index]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)
                        explosion = Explosion(obj.x, obj.y, 5)              # ---Adjust the size  of the explosion img-----
                        explosion_group.add(explosion)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 20              # -----------Adjust the speed of the laser---------------------------

    def cycle_laser(self):
#____________________________________________laser options_____________________________________________________________
        self.laser_index = (self.laser_index + 1) % len(self.laser_options)
        self.laser_img = self.laser_options[self.laser_index]


    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
#_________________________________________Health bar of player spaceship________________________________________________________________________
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

#______________________________________________ENEMY Spaceship______________________________________________________________________________________________
class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER, red_laser_sound, 0.3),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER, green_laser_sound, 0.3),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER, blue_laser_sound, 0.3),
        
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img, self.laser_sound, self.volume = self.COLOR_MAP[color]
        self.laser_sound.set_volume(self.volume)                            # -----------------Set the volume for the laser sound---------------------
        self.mask = pygame.mask.from_surface(self.ship_img)
        red_laser_sound.set_volume(0)
        green_laser_sound.set_volume(0)
        blue_laser_sound.set_volume(0)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.ship_img.get_width() // 2 - 5, self.y + self.ship_img.get_height(), self.laser_img)
            self.lasers.append(laser)
            self.laser_sound.play()                                          # --------Play the alien's laser sound-----------
            self.cool_down_counter = 0.1
            

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.laser_sound.play()                         # -----------Play the spaceship's laser sound-------------
            self.cool_down_counter = 0.1
            
    def move_lasers(self, vel, player):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                # You should pass a list containing the player object
                if laser.collision(player[0]):
                    player[0].health -= 10
                    self.lasers.remove(laser)
                    explosion = Explosion(player[0].x, player[0].y, 10)     # ------Adjust the size parameter of explosion img---------------
                    explosion_group.add(explosion)

#_____________________________________DEfExplosion__________________________________________

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(os.path.join("SPACESS", "exp3.png"))
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            elif size == 2:
                img = pygame.transform.scale(img, (40, 40))
            elif size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # ---------------add the image to the list-------------------------
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        explosion_fx.play()

    def update(self):
        explosion_speed = 2
        # -----------------update explosion animation-----------------------------
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        #----------------- if the animation is complete, delete explosion------------------------------
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


explosion_group = pygame.sprite.Group()       
#_________________________________________________________________________________________________________________________________________________
def update(self):
		explosion_speed = 3
		#------------------------update explosion animation-----------------------------------
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

#__________________________if the animation is complete it will delete explosion____________________________________________________________
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

#______________________________________________________________________________________
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None
#_____________________________________MAIN____________________________________
def main():
    run = True
    FPS = 120
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50) #-------------------Font and Size of Lives and Leve---------------------
    lost_font = pygame.font.SysFont("Viner Hand ITC", 90) #---------------Font and Size of Game Over---------------------

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 10
    laser_vel = 5

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

# ----------------------------------Play the background music-------------------------------
    background_music.play(loops=-1)  # ---------------------------loops=-1 means the music will loop indefinitely-------------------------------
    def redraw_window():
        WIN.blit(BG, (0,0))
#______________________________________draw text________________________________________________________________
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
#_________This will check the player health bar if it's > 0_________________________________________________
        if player.health > 0:
            player.draw(WIN)
            player.healthbar(WIN)

        for explosion in explosion_group:
            explosion.update()
        explosion_group.draw(WIN)
        

        if lost:
            lost_label = lost_font.render("GAME OVER", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()
        
#________________________________________________Game Loop_____________________________________________________________________
    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                quit()
#______________________This will be the control key of Player Spaceship________________________________________________________________
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0:  # -----left-----
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # -----right-----
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:  # ------up------
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT:  # -------down-----
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_TAB]:
            player.cycle_laser()


        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, [player])

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
                explosion = Explosion(enemy.x, enemy.y, 5)  # ----------------Adjust the size parameter of explosion img--------------------
                explosion_group.add(explosion)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)
        redraw_window()

    # ------------------Stop the background music when the game is over--------------------------------
background_music.stop() 
#_________________________________Starting Screeen___________________________________________________________________
def main_menu():
    title_font = pygame.font.SysFont("Magneto", 60)
    invader_font = pygame.font.SysFont("Magneto", 90)  # -------------------Adjusted font size for "Space Invader"----------------------------
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        
        # -----------------------Display "Space Invader" in the upper middle of the screen--------------------------
        invader_label = invader_font.render("Space Invader", 1, (255, 255, 255))
        WIN.blit(invader_label, (WIDTH/2 - invader_label.get_width()/2, HEIGHT/4))
        
        #-------------------below "Space Invader"-----------------------------------------------  
        title_label = title_font.render("Press the mouse to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, HEIGHT/2))

        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()
# ------------------Play the background music-------------------------------
background_music.play(loops=1)  # ---------------------------loops=-1 means the music will loop indefinitely-------------------------------

main_menu()