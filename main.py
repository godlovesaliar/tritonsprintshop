import pygame
from pygame.locals import *
import math
import random


FPS = 10
RED = (255, 0, 0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)

pygame.init()
screen_width = 1024
screen_height = 768
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Tritons Print Shop: The Game")
pygame.mixer.init()
pygame.mixer.set_num_channels(8)
clock = pygame.time.Clock()



intro = pygame.mixer.Channel(1)
soundss = pygame.mixer.Sound("assets/sound/intro.mp3")
game = pygame.mixer.Channel(2)
soundsss = pygame.mixer.Sound("assets/sound/game.mp3")


#title images
maintitle1 = pygame.image.load('assets/menu/main/mainmenu1.png')
maintitle2 = pygame.image.load('assets/menu/main/mainmenu2.png')
invent_bg = pygame.image.load('assets/menu/inventorybase.png')


#level image
level_bg = pygame.transform.scale(pygame.image.load('assets/level/level.png'), (screen_width, screen_height))
sell_image = pygame.transform.scale(pygame.image.load('assets/sprites/sales/sellimage0.png'), (286,286))

tables = pygame.transform.scale(pygame.image.load('assets/level/tables.png'), (screen_width, screen_height)).convert_alpha()


#image objects

pixel_font = pygame.font.Font('assets/pixel_font.ttf',80)
invent_font = pygame.font.Font('assets/pixel_font.ttf',35)
count_font = pygame.font.Font('assets/pixel_font.ttf',15)
object_filament = pygame.transform.scale(pygame.image.load('assets/sprites/items/printerfilament.png'), (128,128))
object_filament0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/printerfilament0.png'), (128,128))
object_octopus = pygame.transform.scale(pygame.image.load('assets/sprites/items/octopus/octopus.png'), (128,128))
object_octopus0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/octopus/octopus0.png'), (128,128))
object_benchy = pygame.transform.scale(pygame.image.load('assets/sprites/items/benchy/benchy.png'), (128,128))
object_benchy0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/benchy/benchy0.png'), (128,128))
object_laptop = pygame.transform.scale(pygame.image.load('assets/sprites/items/laptop.png'), (128,128))
object_laptop0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/laptop0.png'), (128,128))
object_hall_pass = pygame.transform.scale(pygame.image.load('assets/sprites/items/hall_pass.png'), (128,128))
object_hall_pass0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/hall_pass0.png'), (128,128))
object_dragon = pygame.transform.scale(pygame.image.load('assets/sprites/items/dragon/dragon.png'), (128,128))
object_dragon0 = pygame.transform.scale(pygame.image.load('assets/sprites/items/dragon/dragon0.png'), (128,128))
object_tablefilament = pygame.transform.scale(pygame.image.load('assets/sprites/items/tablefilament/tablefilament5.png'), (128,128))


#ASSET-LOADING HELPERS
#
# Everything below loads and scales each sprite frame exactly once, at
# startup, into a cached Surface. Gameplay code then just indexes into
# these caches instead of hitting the disk every frame.

def load_scaled(path, size):
    return pygame.transform.scale(pygame.image.load(path), size)

def load_2x(path):
    return pygame.transform.scale2x(pygame.image.load(path))

def load_frame_seq(path_fmt, count, size, start=1):
    return [load_scaled(path_fmt.format(i), size) for i in range(start, count + 1)]


#CLASSES


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def init(self):
        """Initialize the joystick components"""

        pygame.init()
        joystick_count = pygame.joystick.get_count()
        pygame.joystick.init()
        for i in range(joystick_count):
            self.controller = pygame.joystick.Joystick(i)
            self.controller.init()





ps4 = PS4Controller()
ps4.init()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 100
        self.y = 400
        self.direction = 'fidle'
        self.stamina = 100
        self.sprite = pygame.transform.scale(pygame.image.load('assets/sprites/player/BookerBase.png'), (256, 256)).convert_alpha()
        self.mask = pygame.mask.from_surface(self.sprite)
        #self.rect = self.sprite.get_rect()
        self.rect = pygame.Rect(self.x+81,self.y+20,95,215)
        self.idle = True
        self.sprint = False

player = Player()

class Objects:
    def __init__(self,name,image,rect):
        self.name = name
        self.image = image
        self.rect = rect


table = Objects('Table',pygame.transform.scale(pygame.image.load('assets/level/tables.png'), (screen_width, screen_height)).convert_alpha(),pygame.Rect(400,650,350,450))
cart = Objects('Cart',pygame.transform.scale(pygame.image.load('assets/level/cart.png'), (256, 256)),pygame.Rect(-75,640,195,100))
tablefilament = Objects('Table Filament',pygame.transform.scale(pygame.image.load('assets/sprites/items/tablefilament/tablefilament5.png'), (128, 128)),pygame.Rect(650,630,128,128))
laptop = Objects('Laptop',pygame.transform.scale(pygame.image.load('assets/sprites/items/laptop.png'), (128,128)),pygame.Rect(0,450,128,128))
sell_rect = Objects('sell_rect','assets/sprites/items/laptop.png',pygame.Rect(175,350,64,64))
hallpass = Objects('Hall Pass',pygame.transform.scale(pygame.image.load('assets/sprites/items/hall_pass.png'), (64,64)),pygame.Rect(400,600,64,64))

class Inventory():
    def __init__(self):
        self.active = False
        self.filament = 5
        self.octopus = 0
        self.benchy = 0
        self.laptop = 0
        self.hall_pass = 0
        self.dragon = 0
        self.money = 0
        self.points = 0
invent = Inventory()


def show():
    if invent.active:
        screen.blit(invent_bg, (0,0))
        if invent.filament > 0:
            screen.blit(object_filament,(215,210))
        else:
            screen.blit(object_filament0,(215,210))
        filament = str(invent.filament)
        draw_text((filament+"x"),invent_font,WHITE,315,300)
        if invent.benchy > 0:
            screen.blit(object_benchy,(450,210))
        else:
            screen.blit(object_benchy0,(450,210))
        benchy = str(invent.benchy)
        draw_text((benchy+"x"),invent_font,WHITE,545,300)
        if invent.octopus > 0:
            screen.blit(object_octopus,(680,210))
        else:
            screen.blit(object_octopus0,(680,210))
        octopus = str(invent.octopus)
        draw_text((octopus+"x"),invent_font,WHITE,775,300)

        if invent.laptop > 0:
            screen.blit(object_laptop,(680,420))
        else:
            screen.blit(object_laptop0,(680,420))
        laptop = str(invent.laptop)
        draw_text((laptop+"x"),invent_font,WHITE,775,515)

        if invent.hall_pass > 0:
            screen.blit(object_hall_pass,(450,420))
        else:
            screen.blit(object_hall_pass0,(450,420))
        hall_pass = str(invent.hall_pass)
        draw_text((hall_pass+"x"),invent_font,WHITE,545,515)

        if invent.dragon > 0:
            screen.blit(object_dragon,(215,420))
        else:
            screen.blit(object_dragon0,(215,420))
        dragon = str(invent.dragon)
        draw_text((dragon+"x"),invent_font,WHITE,315,515)



class Counter():
    def __init__(self):
        self.run = True
        self.gamerun = False
        self.menu = True
        self.title = 1
        self.load = 1
        self.loading = False
        self.readying = False
        self.readycount = 1
        self.gameover = 1
        self.gameovering = False
        self.randt = False
        self.rando = 1

        self.gametime = 1800


        self.walk =1
        self.idle =3
        self.use =1
        self.showback = 2
        self.VEL = 10



        self.collide = False
        self.printcollide = False
        self.filamentcollide = False
        self.passcollide = False

        self.tablefilament = 5
        self.tablepass = 3
        self.filamentround = math.floor(self.tablefilament)
        self.laptop = 1
        self.laptopcollide = False
        self.sale = 1
        self.saletype = 0
        self.doorquote = random.randint(1,4)

        self.recharge = False
count = Counter()


#PRELOADED ANIMATION / UI FRAME CACHES

DIR_FOLDER = {'up': 'back', 'down': 'front', 'left': 'left', 'right': 'right'}

PLAYER_WALK_FRAMES = {
    'left':  load_frame_seq('assets/sprites/player/Walk/left/SidewalkL{}.png', 7, (256, 256)),
    'right': load_frame_seq('assets/sprites/player/Walk/right/SidewalkR{}.png', 7, (256, 256)),
    'up':    load_frame_seq('assets/sprites/player/Walk/back/BookerBackWalk{}.png', 7, (256, 256)),
    'down':  load_frame_seq('assets/sprites/player/Walk/front/BookerFrontWalk{}.png', 7, (256, 256)),
}
PLAYER_IDLE_FRAMES = {
    'up':    load_frame_seq('assets/sprites/player/Idle/back/BookerBackIdle{}.png', 14, (256, 256)),
    'down':  load_frame_seq('assets/sprites/player/Idle/front/BookerFrontIdle{}.png', 59, (256, 256)),
    'left':  load_frame_seq('assets/sprites/player/Idle/left/sideidlel{}.png', 59, (256, 256)),
    'right': load_frame_seq('assets/sprites/player/Idle/right/sideidler{}.png', 59, (256, 256)),
}
PLAYER_USE_FRAMES = {
    'up':    load_frame_seq('assets/sprites/player/use/back/BookerBackUse{}.png', 14, (256, 256)),
    'down':  load_frame_seq('assets/sprites/player/use/front/BookerFrontUse{}.png', 14, (256, 256)),
    'left':  load_frame_seq('assets/sprites/player/use/left/sideusel{}.png', 14, (256, 256)),
    'right': load_frame_seq('assets/sprites/player/use/right/sideuser{}.png', 14, (256, 256)),
}

MAIN_MENU_FRAMES = load_frame_seq('assets/menu/main/mainmenu{}.png', 64, (1024, 768))
LOADING_FRAMES = load_frame_seq('assets/menu/loading/loading{}.png', 12, (1024, 768))
GAMEOVER_FRAMES = load_frame_seq('assets/menu/gameover/gameover{}.png', 60, (1024, 768))
GETREADY_SEQUENCE = [
    load_scaled('assets/menu/ready/getready.png', (1024, 768)),
    load_scaled('assets/menu/ready/getready3.png', (1024, 768)),
    load_scaled('assets/menu/ready/getready2.png', (1024, 768)),
    load_scaled('assets/menu/ready/getready1.png', (1024, 768)),
    load_scaled('assets/menu/ready/getready0.png', (1024, 768)),
]
LEVEL_CLEARED_IMG = load_scaled('assets/menu/levelcleared.png', (1024, 768))
GAMEOVER_BUTTONS_IMG = load_scaled('assets/menu/gameover/gameoverbuttons.png', (1024, 768))
TIMEUP_IMG = load_scaled('assets/menu/timeup.png', (1024, 768))

COIN_SMALL = load_scaled('assets/sprites/items/coin.png', (80, 80))
COIN_HUD = load_2x('assets/sprites/items/coin.png')
STAMINA_FRAMES = [load_2x(f'assets/sprites/stamina/stamina{i}.png') for i in range(0, 101)]
SELL_IMAGE_FRAMES = load_frame_seq('assets/sprites/sales/sellimage{}.png', 3, (286, 286), start=0)
DOOR_SPEECH_FRAMES = [load_2x(f'assets/sprites/speech/speech{i}.png') for i in range(1, 5)]
LEFT_SPEECH_FRAMES = [load_2x(f'assets/sprites/speech/speechl{i}.png') for i in range(1, 5)]
RIGHT_SPEECH_FRAMES = [load_2x(f'assets/sprites/speech/speechr{i}.png') for i in range(1, 5)]
STUDENT_L_FRAMES = load_frame_seq('assets/sprites/students/studentl/student{}.png', 5, (256, 256))
STUDENT_R_FRAMES = load_frame_seq('assets/sprites/students/studentr/student{}.png', 5, (256, 256))

TABLEFILAMENT_FRAMES = load_frame_seq('assets/sprites/items/tablefilament/tablefilament{}.png', 5, (128, 128), start=0)

PRUSA_IDLE_IMAGE = load_scaled('assets/sprites/printers/prusa.png', (112, 112))
ENDER_IDLE_IMAGE = load_scaled('assets/sprites/printers/ender.png', (128, 128))
ULTIMAKER_IDLE_IMAGE = load_scaled('assets/sprites/printers/ultimaker.png', (120, 120))
PRUSA_ANIM_FRAMES = load_frame_seq('assets/sprites/printers/prusa/prusa{}.png', 19, (112, 112))
ENDER_ANIM_FRAMES = load_frame_seq('assets/sprites/printers/ender/ender{}.png', 19, (128, 128))
ULTIMAKER_ANIM_FRAMES = load_frame_seq('assets/sprites/printers/ultimaker/ultimaker{}.png', 19, (120, 120))
OCTOPUS_FRAMES = load_frame_seq('assets/sprites/items/octopus/octopus{}.png', 200, (40, 40))
BENCHY_FRAMES = load_frame_seq('assets/sprites/items/benchy/benchy{}.png', 120, (40, 40))
DRAGON_FRAMES = load_frame_seq('assets/sprites/items/dragon/dragon{}.png', 400, (64, 64))


class Printer():
    """A print station: idle -> prints (consumes filament, animates) -> ready
    to collect -> collected (adds one unit of its byproduct to inventory)."""

    def __init__(self, name, rect, screen_pos, idle_image, anim_frames, sound,
                 byproduct_name, byproduct_frames, byproduct_max, byproduct_pos, volume=1.0):
        self.name = name
        self.rect = rect
        self.screen_pos = screen_pos
        self.image = idle_image
        self.anim_frames = anim_frames
        self.anim_index = 1
        self.active = False
        self.sound = sound
        self.volume = volume
        self.byproduct_name = byproduct_name
        self.byproduct_frames = byproduct_frames
        self.byproduct_max = byproduct_max
        self.byproduct_progress = 1
        self.byproduct_image = byproduct_frames[0]
        self.byproduct_pos = byproduct_pos

    def interact(self):
        if not self.active and invent.filament > 0 and self.byproduct_progress != self.byproduct_max:
            self.active = True
            self.sound.play().set_volume(self.volume)
            invent.filament -= 1
        elif not self.active and self.byproduct_progress == self.byproduct_max:
            self.byproduct_progress = 1
            setattr(invent, self.byproduct_name, getattr(invent, self.byproduct_name) + 1)
            self.byproduct_image = self.byproduct_frames[0]
        else:
            self.active = False

    def update(self):
        if not self.active:
            return
        self.anim_index += 1
        if self.anim_index >= len(self.anim_frames) + 1:
            self.anim_index = 1
        self.image = self.anim_frames[self.anim_index - 1]

        self.byproduct_progress += 1
        if self.byproduct_progress >= self.byproduct_max:
            self.byproduct_progress = self.byproduct_max
            self.sound.stop()
            self.active = False
        self.byproduct_image = self.byproduct_frames[self.byproduct_progress - 1]


class Student():
    """A student at the door: idles, occasionally wants an item in exchange
    for points, and gives up (rerolling their ask) if kept waiting too long."""

    def __init__(self, rect, outfit_frames, speech_frames, positions, reward_attr,
                 reward_points, active_threshold, fail_threshold, sound_fail, reroll_on_success):
        self.rect = rect
        self.outfit_frames = outfit_frames
        self.speech_frames = speech_frames
        self.speech_pos, self.outfit_pos = positions
        self.reward_attr = reward_attr
        self.reward_points = reward_points
        self.active_threshold = active_threshold
        self.fail_threshold = fail_threshold
        self.sound_fail = sound_fail
        self.reroll_on_success = reroll_on_success
        self.outfit = random.randint(0, len(outfit_frames) - 1)
        self.quote = random.randint(0, len(speech_frames) - 1)
        self.timer = 0

    def reroll(self):
        self.outfit = random.randint(0, len(self.outfit_frames) - 1)
        self.quote = random.randint(0, len(self.speech_frames) - 1)

    def interact(self):
        if self.timer >= self.active_threshold and getattr(invent, self.reward_attr) > 0:
            if self.reroll_on_success:
                self.reroll()
            setattr(invent, self.reward_attr, getattr(invent, self.reward_attr) - 1)
            invent.points += self.reward_points
            self.timer = random.randint(-500, 0)

    def update(self):
        self.timer += 1
        if self.timer >= self.fail_threshold:
            self.sound_fail.play()
            self.reroll()
            self.timer = random.randint(-200, 0)

    def draw(self, screen):
        if self.timer >= self.active_threshold:
            screen.blit(self.speech_frames[self.quote], self.speech_pos)
            screen.blit(self.outfit_frames[self.outfit], self.outfit_pos)


class Sound():
    def __init__(self) -> None:
        self.intro = pygame.mixer.Sound('assets/sound/intro.mp3')
        self.start = pygame.mixer.Sound("assets/sound/start.wav")
        self.fail = pygame.mixer.Sound('assets/sound/fail.wav')
        self.walk =  pygame.mixer.Sound('assets/sound/walk.wav')
        self.bell = pygame.mixer.Sound('assets/sound/classbell.wav')
        self.printer1 = pygame.mixer.Sound('assets/sound/print.wav')
        self.printer2 = pygame.mixer.Sound('assets/sound/print.wav')
        self.printer3 = pygame.mixer.Sound('assets/sound/print.wav')
        self.printer4 = pygame.mixer.Sound('assets/sound/print.wav')
        self.printer5 = pygame.mixer.Sound('assets/sound/print.wav')




sound = Sound()

printers = [
    Printer('Prusa1', pygame.Rect(365,282,16,64), (320,310), PRUSA_IDLE_IMAGE, PRUSA_ANIM_FRAMES,
            sound.printer1, 'octopus', OCTOPUS_FRAMES, 200, (360,355), volume=0.5),
    Printer('Prusa2', pygame.Rect(490,282,16,64), (445,310), PRUSA_IDLE_IMAGE, PRUSA_ANIM_FRAMES,
            sound.printer2, 'octopus', OCTOPUS_FRAMES, 200, (485,355)),
    Printer('Prusa3', pygame.Rect(608,282,16,64), (563,310), PRUSA_IDLE_IMAGE, PRUSA_ANIM_FRAMES,
            sound.printer3, 'octopus', OCTOPUS_FRAMES, 200, (602,355)),
    Printer('Ender', pygame.Rect(745,295,16,64), (686,280), ENDER_IDLE_IMAGE, ENDER_ANIM_FRAMES,
            sound.printer4, 'benchy', BENCHY_FRAMES, 120, (732,345)),
    Printer('Ultimaker', pygame.Rect(870,295,16,64), (817,284), ULTIMAKER_IDLE_IMAGE, ULTIMAKER_ANIM_FRAMES,
            sound.printer5, 'dragon', DRAGON_FRAMES, 400, (848,315)),
]

students = [
    Student(pygame.Rect(175,720,64,64), STUDENT_L_FRAMES, LEFT_SPEECH_FRAMES, ((270,550),(85,520)),
            'laptop', 2500, active_threshold=500, fail_threshold=1100, sound_fail=sound.fail, reroll_on_success=False),
    Student(pygame.Rect(860,720,64,64), STUDENT_R_FRAMES, RIGHT_SPEECH_FRAMES, ((720,550),(780,520)),
            'hall_pass', 1000, active_threshold=350, fail_threshold=850, sound_fail=sound.fail, reroll_on_success=True),
]

SALE_ITEMS = {1: ('octopus', 40, 200), 2: ('benchy', 20, 100), 3: ('dragon', 75, 500)}


def format_score(value):
    return f"{value:06d}"


def check_student():
    for s in students:
        if pygame.sprite.collide_rect(player, s):
            s.interact()


def check_pass():
    if count.passcollide and invent.money >=5 and count.use == 8:
        if count.tablepass >=1:
            count.tablepass -=1
            invent.hall_pass +=1
            invent.money -=5

def check_filament():
    count.filamentround = math.floor(count.tablefilament)
    if count.filamentcollide and invent.money >=10 and count.use == 8:
        if count.tablefilament >=1:
            count.tablefilament -=1
            invent.filament +=1
            invent.money -=10
            count.filamentround = math.floor(count.tablefilament)
            tablefilament.image = TABLEFILAMENT_FRAMES[count.filamentround]
    if count.filamentround == 0:
        count.recharge = True
def check_laptop():
    if count.laptopcollide and invent.money >=100 and count.use == 8:
        if count.laptop == 1:
            count.laptop = 0
            invent.laptop +=1
            invent.money -=100

def check_sales():
    if not pygame.sprite.collide_rect(player, sell_rect):
        return
    if count.sale < 250:
        return
    if count.saletype == 0:
        invent.points += 1
        count.doorquote = random.randint(1, 4)
        count.sale = random.randint(0, 100)
        count.saletype = random.randint(0, 3)
        return
    item_attr, money_gain, points_gain = SALE_ITEMS[count.saletype]
    if getattr(invent, item_attr) > 0:
        setattr(invent, item_attr, getattr(invent, item_attr) - 1)
        invent.money += money_gain
        invent.points += points_gain
        count.sale = random.randint(0, 100)
        count.saletype = random.randint(0, 3)


def check_printers():
    for p in printers:
        if pygame.sprite.collide_rect(player, p):
            p.interact()

def print_anims():
    for p in printers:
        p.update()

    if count.recharge:
        count.tablefilament += 0.005
        count.filamentround = math.floor(count.tablefilament)
    if count.tablefilament >=5:
        count.tablefilament = 5
        count.recharge = False
    tablefilament.image = TABLEFILAMENT_FRAMES[count.filamentround]

    count.laptop +=0.002
    if count.laptop >=1:
        count.laptop = 1

    count.sale +=1
    if count.sale >=625 and count.saletype != 0:
        sound.fail.play()
        count.sale = random.randint(0,100)

    for s in students:
        s.update()

    count.tablepass +=0.005
    if count.tablepass >=3:
        count.tablepass = 3

    if player.idle:
            walking = pygame.mixer.Channel(5)
            walking.stop()
    if count.randt:
        count.rando +=1
    else:
        count.rando = 0





def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def player_handle_movement(keys_pressed,player):

    count.collide = pygame.sprite.collide_rect(player,table) or pygame.sprite.collide_rect(player,cart)
    count.printcollide = any(pygame.sprite.collide_rect(player, p) for p in printers)
    count.filamentcollide = pygame.sprite.collide_rect(player,tablefilament)
    count.laptopcollide = pygame.sprite.collide_rect(player,laptop)
    count.passcollide = pygame.sprite.collide_rect(player,hallpass)
    print_anims()
    count.VEL = 10
    if player.stamina <= 0:
        player.stamina = 0
        player.sprint = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            count.run = False

    if keys_pressed[pygame.K_LSHIFT]:  # SPRINT

        if player.idle == False:
            if player.stamina > 0:
                player.sprint = True
                player.stamina -= 5
        if player.sprint == True and player.stamina >0:
            count.VEL = 25
        else:
            count.VEL = 10




    if keys_pressed[pygame.K_a]:
        player.direction = 'left'
        if player.x - count.VEL > -90:  # LEFT
            player.idle = False
            player.x -= count.VEL
            player.rect.move_ip(-count.VEL,0)
            count.walk +=1

            if count.walk >= 8:
                count.walk = 1
        player.sprite = PLAYER_WALK_FRAMES['left'][count.walk - 1]


    elif keys_pressed[pygame.K_d]:
        player.direction = 'right'
        if player.x + count.VEL < 850:  # RIGHT
            player.idle = False
            player.x += count.VEL
            player.rect.move_ip(+count.VEL,0)
            count.walk +=1
            if count.walk >= 8:
                count.walk = 1
        player.sprite = PLAYER_WALK_FRAMES['right'][count.walk - 1]


    elif keys_pressed[pygame.K_w]:
        player.direction = 'up'

        if player.y - count.VEL > 310:  # UP
            player.idle = False
            player.y -= count.VEL
            player.rect.move_ip(0,-count.VEL)
            count.walk +=1
            if count.walk >= 8:
                count.walk = 1
        count.showback=1
        player.sprite = PLAYER_WALK_FRAMES['up'][count.walk - 1]




    elif keys_pressed[pygame.K_s]:
        player.direction = 'down'

        if player.y + count.VEL < 600:  # DOWN
            player.idle = False
            player.y += count.VEL
            player.rect.move_ip(0,+count.VEL)
            count.walk +=1
            if count.walk >= 8:
                count.walk = 1
        count.showback = 0
        player.sprite = PLAYER_WALK_FRAMES['down'][count.walk - 1]





    elif keys_pressed[pygame.K_SPACE]: #INTERACT
        count.use +=1
        if count.use >= 15:
            count.use = 1
        if count.use == 8:
            check_filament()
            if player.direction == 'up' or player.direction == 'bidle':
                check_printers()
                check_sales()
            if player.direction == 'left' or player.direction == 'down':
                check_laptop()
            if player.direction == 'down' or player.direction == 'fidle':
                check_student()
            if player.direction == 'right' or player.direction == 'down' or player.direction == 'fidle':
                check_pass()

        if player.direction == 'up' or player.direction == 'bidle':
            use_frames = PLAYER_USE_FRAMES['up']
        elif player.direction == 'down':
            use_frames = PLAYER_USE_FRAMES['down']
        elif player.direction == 'left':
            use_frames = PLAYER_USE_FRAMES['left']
        else:
            use_frames = PLAYER_USE_FRAMES['right']
        player.sprite = use_frames[count.use - 1]

    elif keys_pressed[pygame.K_c]: #showcoords
        if count.randt == False:
            count.randt = True
        else:
            count.randt = False

    else: # IDLE
        player.idle = True
        count.idle +=1
        idle_threshold = 15 if player.direction == 'up' else 60
        if count.idle >= idle_threshold:
            count.idle = 1
        idle_frames = PLAYER_IDLE_FRAMES.get(player.direction, PLAYER_IDLE_FRAMES['down'])
        player.sprite = idle_frames[count.idle - 1]



    if keys_pressed[pygame.K_TAB]:  #INVENTORY
        if invent.active == False:
            invent.active = True
        else:
            invent.active = False

def colliders():
    if count.collide:
        if player.rect.bottom > cart.rect.top:
            player.y = cart.rect.top -235
            player.rect.bottom = cart.rect.top
        elif player.rect.left < cart.rect.right:
            player.x = cart.rect.right -81
            player.rect.left = cart.rect.right



        elif player.rect.bottom > table.rect.top and player.rect.left > table.rect.left and player.rect.right < table.rect.right:
            player.y = table.rect.top-235
            player.rect.bottom = table.rect.top

        elif player.rect.right > table.rect.left and player.x <450 and player.rect.bottom > table.rect.top:
            player.x = table.rect.left-176
            player.rect.right = table.rect.left

        elif player.rect.left < table.rect.right and player.x >450 and player.rect.bottom > table.rect.top:
            player.x = table.rect.right-81
            player.rect.left = table.rect.right

def stamina():
    if player.stamina > 100:
            player.stamina = 100
    elif player.stamina < 100:
        player.stamina +=1
    if player.stamina <= 0:
        player.stamina=0
        player.sprint = False

def main_title():
    while count.menu:

        clock.tick(8)
        screen.blit(MAIN_MENU_FRAMES[count.title - 1], (0, 0))

        count.title +=1
        if count.title >64: #change back to
            count.title = 49
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                count.run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pygame.mixer.Sound.play(sound.start)
                pygame.mixer.music.stop()
                pygame.time.wait(1500)
                count.menu = False
                count.loading = True
            if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                pygame.mixer.Sound.play(sound.start)
                pygame.mixer.music.stop()
                pygame.time.wait(1500)
                count.menu = False
                count.loading = True


        pygame.display.update()

def loading():
    while count.loading:

        clock.tick(FPS)
        screen.blit(LOADING_FRAMES[count.load - 1], (0, 0))
        if count.gameovering:
            game.stop()
        count.load +=1
        if count.load >=12:
            count.load = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                count.run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                intro.stop()
                pygame.mixer.Sound.play(sound.start)
                pygame.mixer.music.stop()
                pygame.time.wait(1500)
                count.loading = False
                count.readying = True


        pygame.display.update()


def get_ready():
    if count.readycount ==1:
            game.set_volume(1)
            game.play(soundsss)

    while count.readying:
        clock.tick(FPS)
        graphics()
        player_handle_movement(keys_pressed,player)
        getready_idx = min(count.readycount // 10, 4)
        screen.blit(GETREADY_SEQUENCE[getready_idx],(0,0))
        pygame.display.flip()

        if count.readycount>50:
            count.readying = False
            count.gamerun=True
            count.readycount = 1
        count.readycount+=1
        pygame.display.flip()


def gameover():

    if count.gametime == 0:

        game.stop()
        screen.blit(TIMEUP_IMG,(0,0))
        pygame.display.update()
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(sound.bell)

        pygame.time.wait(3800)

        intro.set_volume(1)
        intro.play(soundss)
        count.gamerun = False
        count.gameovering = True
    while count.gameovering:

        clock.tick(FPS)
        screen.blit(GAMEOVER_FRAMES[count.gameover - 1], (0, 0))
        count.gameover +=1

        if count.gameover >=60:
            count.gameover = 25
        if count.gameover >=25:
            screen.blit(LEVEL_CLEARED_IMG, (0, 0))
            draw_text('YOU EARNED',invent_font,WHITE,85,305)
            draw_text('POINTS',invent_font,WHITE,125,455)
            draw_text(format_score(invent.points),pixel_font,YELLOW,40,350)
            draw_text('YOU BANKED',invent_font,WHITE,715,305)
            draw_text(format_score(invent.money),pixel_font,GREEN,670,350)
            screen.blit(COIN_SMALL, (780,440))
            screen.blit(GAMEOVER_BUTTONS_IMG,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                count.run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(sound.start)
                    intro.stop()
                    pygame.time.wait(1500)

                    count.gameovering = False
                    count.gamerun = False
                    count.readying = True
                    game.set_volume(1)
                    game.play(soundsss)
                    reset()

                    #get_ready()

                elif event.key == pygame.K_ESCAPE:
                    count.run = False
                    count.gameovering = False

        pygame.display.update()



def graphics():
    screen.blit(level_bg, (0, 0))
    if count.sale >= 250:
        screen.blit(SELL_IMAGE_FRAMES[count.saletype], (0, 240))

    draw_text('STAMINA',invent_font,WHITE,815,10)
    draw_text('POINTS:',invent_font,WHITE,230,10)
    draw_text(format_score(invent.points),invent_font,WHITE,230,55)

    time_minutes = count.gametime//600
    time_seconds = (count.gametime - ((count.gametime//600)*600))//10
    draw_text('TIME:',invent_font,WHITE,630,10)
    if time_seconds >9:
        draw_text(str(time_minutes)+":"+str(time_seconds),invent_font,WHITE,640,55)
    else:
        draw_text(str(time_minutes)+":0"+str(time_seconds),invent_font,WHITE,640,55)

    screen.blit(STAMINA_FRAMES[player.stamina], (768, 10))
    draw_text(str(invent.money),invent_font,WHITE,75,32)
    screen.blit(COIN_HUD, (15, 20))
    for p in printers:
        screen.blit(p.image, p.screen_pos)
        screen.blit(p.byproduct_image, p.byproduct_pos)

    if player.y > 480:
        screen.blit(tables,(100,0))
        screen.blit(tablefilament.image,(590,600))
        if count.tablepass >=1:
            screen.blit(hallpass.image,(400,600))
        if count.tablepass >=2:
            screen.blit(hallpass.image,(410,625))
        if count.tablepass >=3:
            screen.blit(hallpass.image,(420,613))
    else:
        screen.blit(tables,(-5000,768))
        screen.blit(tablefilament.image,(5900,600))
    if player.rect.bottom > cart.rect.top:
        screen.blit(cart.image,(-75,500))
    else:
        screen.blit(cart.image,(-750,500))
    screen.blit(player.sprite,(player.x,player.y))
    if count.sale >= 250 and count.saletype == 0:
        screen.blit(DOOR_SPEECH_FRAMES[count.doorquote - 1], (player.x - 55, player.y - 25))

    if player.y <=480:
        screen.blit(tables,(100,0))
        screen.blit(tablefilament.image,(590,600))
        if count.tablepass >=1:
            screen.blit(hallpass.image,(400,600))
        if count.tablepass >=2:
            screen.blit(hallpass.image,(410,625))
        if count.tablepass >=3:
            screen.blit(hallpass.image,(420,613))
    else:
        screen.blit(tables,(0,7680))
        screen.blit(tablefilament.image,(590,6000))
    if player.rect.bottom <= cart.rect.top+25:
        screen.blit(cart.image,(-75,500))
    else:
        screen.blit(cart.image,(-750,500))
    if count.laptop == 1:
        screen.blit(laptop.image,(0,450))
    for s in students:
        s.draw(screen)

def reset():
    invent.benchy = 0
    invent.dragon = 0
    invent.filament = 5
    invent.octopus = 0
    invent.points = 0
    count.gametime = 1800
    count.gameover = 1
    count.laptop = 1
    count.sale = 1
    students[0].timer = 1
    students[1].timer = 1





count.run = True
while count.run:
    clock.tick(FPS)

    if count.gametime <=0:
        count.gametime = 0

    keys_pressed = pygame.key.get_pressed()

    if count.menu:
        intro.set_volume(1)
        intro.play(soundss)

    main_title()
    loading()
    get_ready()
    stamina()
    graphics()
    colliders()
    print_anims()
    show()
    gameover()

    if count.gamerun:
        count.gametime -=1
    if count.readying:
        count.readycount +=1
    pygame.display.update()

    player_handle_movement(keys_pressed,player)
    pygame.display.update()

pygame.quit()
