import pygame
from pygame.locals import *
import math
import random
from datetime import datetime
from datetime import timedelta


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
object_tablefilament = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/tablefilament/tablefilament5.png'), (128,128))



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
prusa1 = Objects('Prusa1',pygame.transform.scale(pygame.image.load('assets/sprites/printers/prusa.png'), (112, 112)),pygame.Rect(365,282,16,64))
prusa2 = Objects('Prusa2',pygame.transform.scale(pygame.image.load('assets/sprites/printers/prusa.png'), (112, 112)),pygame.Rect(490,282,16,64))
prusa3 = Objects('Prusa3',pygame.transform.scale(pygame.image.load('assets/sprites/printers/prusa.png'), (112, 112)),pygame.Rect(608,282,16,64))
ender = Objects('Ender',pygame.transform.scale(pygame.image.load('assets/sprites/printers/ender.png'), (128, 128)),pygame.Rect(745,295,16,64))
ultimaker = Objects('Ultimaker',pygame.transform.scale(pygame.image.load('assets/sprites/printers/ultimaker.png'), (120, 120)),pygame.Rect(870,295,16,64))
tablefilament = Objects('Table Filament',pygame.transform.scale(pygame.image.load('assets/sprites/items/tablefilament/tablefilament5.png'), (128, 128)),pygame.Rect(650,630,128,128))
laptop = Objects('Laptop',pygame.transform.scale(pygame.image.load('assets/sprites/items/laptop.png'), (128,128)),pygame.Rect(0,450,128,128))
sell_rect = Objects('sell_rect','assets/sprites/items/laptop.png',pygame.Rect(175,350,64,64))
student = Objects('Student',pygame.transform.scale(pygame.image.load(f'assets/sprites/students/studentl/student1.png'), (256,256)),pygame.Rect(175,720,64,64))
student2 = Objects('Student2',pygame.transform.scale(pygame.image.load('assets/sprites/students/studentr/student1.png'), (256,256)),pygame.Rect(860,720,64,64))
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
        self.laptopround = math.floor(self.laptop)
        self.sale = 1
        self.saletype = 0
        self.doorquote = random.randint(1,4)
        self.student1 = 0
        self.student1outfit = random.randint(1,5)
        self.student1quote = random.randint(1,4)
        self.student2 = 0
        self.student2outfit = random.randint(1,5)
        self.student2quote = random.randint(1,4)
        
        self.recharge = False
count = Counter()

student = Objects('Student',pygame.transform.scale(pygame.image.load(f'assets/sprites/students/studentl/student{count.student1outfit}.png'), (256,256)),pygame.Rect(175,720,64,64))
student2 = Objects('Student2',pygame.transform.scale(pygame.image.load(f'assets/sprites/students/studentr/student{count.student2outfit}.png'), (256,256)),pygame.Rect(860,720,64,64))
teacherspeak = Objects('TeacherSpeak',pygame.transform.scale(pygame.image.load(f'assets/sprites/speech/speech{count.doorquote}.png'), (256,256)),pygame.Rect(860,720,64,64))



class Printers():
    def __init__(self):
        self.prusa1 = False
        self.prusa2 = False
        self.prusa3 = False
        self.prusacount = 1
        self.prusacount2 = 1
        self.prusacount3 = 1
        self.ender = False
        self.endercount = 1
        self.ultimaker = False
        self.ultimakercount = 1
        self.bench = 1
        self.benchimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/benchy/benchy{self.bench}.png'), (40,40))
        self.octo = 1
        self.octoimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{self.octo}.png'), (40,40))
        self.octo2 = 1
        self.octoimage2 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{self.octo2}.png'), (40,40))
        self.octo3 = 1
        self.octoimage3 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{self.octo3}.png'), (40,40))
        self.drago = 1
        self.dragoimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/dragon/dragon{self.drago}.png'), (64,64))


printers = Printers()


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


player_coords = (player.x,player.y)
coordinates = str(player_coords)

def check_student():
    if pygame.sprite.collide_rect(player,student):
        if count.student1 >= 500 and invent.laptop >0:
            
            count.student1 = random.randint(-500,0)
            invent.laptop -=1
            invent.points +=2500
    
    if pygame.sprite.collide_rect(player,student2):
        if count.student2 >= 350 and invent.hall_pass >0:
            count.student2outfit = random.randint (1,5)
            count.student2quote = random.randint(1,4)
            
            count.student2 = random.randint(-500,0)
            invent.hall_pass -=1
            invent.points +=1000


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
            tablefilament.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/tablefilament/tablefilament{count.filamentround}.png'), (128,128))
    if count.filamentround == 0:
        count.recharge = True 
def check_laptop():
    #count.laptopround = math.floor(count.laptop)
    if count.laptopcollide and invent.money >=100 and count.use == 8:
        if count.laptop == 1:
            count.laptop = 0
            invent.laptop +=1
            invent.money -=100  
            #count.laptopround = math.floor(count.laptop)

def check_sales():
    if pygame.sprite.collide_rect(player,sell_rect):
        if count.sale >= 250:
            if count.saletype == 1:
                if invent.octopus > 0:
                    invent.octopus -=1
                    invent.money += 40
                    invent.points +=200
                    count.sale = random.randint(0,100)
                    count.saletype = random.randint(0,3)           

            if count.saletype == 2:
                if invent.benchy > 0:
                    invent.benchy -=1
                    invent.money += 20
                    invent.points += 100
                    count.sale = random.randint(0,100)
                    count.saletype = random.randint(0,3)
                    
            if count.saletype == 3:
                if invent.dragon > 0:
                    invent.dragon -=1
                    invent.money += 75
                    invent.points += 500
                    count.sale = random.randint(0,100)
                    count.saletype = random.randint(0,3)
                    
            if count.saletype == 0:
                invent.points +=1
                count.doorquote = random.randint(1,4)
                count.sale = random.randint(0,100)
                count.saletype = random.randint(0,3)
  
        
        
            

def check_printers():
    
    if pygame.sprite.collide_rect(player,prusa1):
        if printers.prusa1 == False and invent.filament > 0 and printers.octo != 200:
            printers.prusa1 = True            
            sound.printer1.play().set_volume(0.5)
            invent.filament -=1
        elif printers.prusa1 == False and printers.octo == 200:
            printers.octo=1
            invent.octopus +=1
            printers.octoimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo}.png'), (40,40))
        else:
            printers.prusa1 = False
            
        
            
    if pygame.sprite.collide_rect(player,prusa2):
        if printers.prusa2 == False and invent.filament > 0 and printers.octo2 != 200:
            printers.prusa2 = True            
            sound.printer2.play()
            invent.filament -=1
        elif printers.prusa2 == False and printers.octo2 == 200:
            printers.octo2=1
            invent.octopus +=1
            printers.octoimage2 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo2}.png'), (40,40))
        else:
            printers.prusa2 = False
            

    if pygame.sprite.collide_rect(player,prusa3):
        if printers.prusa3 == False and invent.filament > 0 and printers.octo3 != 200:
            printers.prusa3 = True           
            sound.printer3.play()          
            invent.filament -=1
        elif printers.prusa3 == False and printers.octo3 == 200:
            printers.octo3=1
            invent.octopus +=1
            printers.octoimage3 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo3}.png'), (40,40))
        else:
            printers.prusa3 = False
            
    

    if pygame.sprite.collide_rect(player,ender):
        if printers.ender == False and invent.filament > 0 and printers.bench != 120:
            printers.ender = True
            sound.printer4.play()
            invent.filament -=1
        elif printers.ender == False and printers.bench == 120:
            printers.bench=1
            invent.benchy +=1
            printers.benchimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/benchy/benchy{printers.bench}.png'), (40,40))
        else:
            printers.ender = False 

    if pygame.sprite.collide_rect(player,ultimaker):
        if printers.ultimaker == False and invent.filament > 0 and printers.drago != 400:
            printers.ultimaker = True
            sound.printer5.play()
            invent.filament -=1
        elif printers.ultimaker == False and printers.drago == 400:
            printers.drago=1
            invent.dragon +=1
            printers.dragoimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/dragon/dragon{printers.drago}.png'), (64,64))
        else:
            printers.ultimaker = False 
    
        
            
def print_anims():
    


    
    if printers.prusa1:
        printers.prusacount += 1
        if printers.prusacount >=20:
            printers.prusacount =1 
        prusa1.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/printers/prusa/prusa{printers.prusacount}.png'), (112, 112))
        printers.octo += 1
        if printers.octo >= 200:
            printers.octo = 200
            sound.printer1.stop()
            printers.prusa1 = False            
            
        printers.octoimage = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo}.png'), (40,40))
    
    if printers.prusa2:
        printers.prusacount2 += 1
        if printers.prusacount2 >=20:
            printers.prusacount2 =1 
        prusa2.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/printers/prusa/prusa{printers.prusacount2}.png'), (112, 112))
        printers.octo2 += 1
        if printers.octo2 >= 200:
            printers.octo2 = 200
            sound.printer2.stop()
            printers.prusa2 = False
        printers.octoimage2 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo2}.png'), (40,40))
    
    if printers.prusa3:
        printers.prusacount3 += 1
        if printers.prusacount3 >=20:
            printers.prusacount3 =1 
        prusa3.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/printers/prusa/prusa{printers.prusacount3}.png'), (112, 112))
        printers.octo3 += 1
        if printers.octo3 >= 200:
            printers.octo3 = 200
            sound.printer3.stop()
            printers.prusa3 = False
        printers.octoimage3 = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/octopus/octopus{printers.octo3}.png'), (40,40))

    if printers.ender:
        printers.endercount += 1
        if printers.endercount >=20:
            printers.endercount =1 
        ender.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/printers/ender/ender{printers.endercount}.png'), (128, 128))
        printers.bench += 1
        if printers.bench >= 120:
            printers.bench = 120
            sound.printer4.stop()
            printers.ender = False
        printers.benchimage= pygame.transform.scale(pygame.image.load(f'assets/sprites/items/benchy/benchy{printers.bench}.png'), (40,40))

    if printers.ultimaker:
        printers.ultimakercount += 1
        if printers.ultimakercount >=20:
            printers.ultimakercount =1 
        ultimaker.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/printers/ultimaker/ultimaker{printers.ultimakercount}.png'), (120, 120))
        printers.drago += 1
        if printers.drago >= 400:
            printers.drago = 400
            sound.printer5.stop()
            printers.ultimaker = False
        printers.dragoimage= pygame.transform.scale(pygame.image.load(f'assets/sprites/items/dragon/dragon{printers.drago}.png'), (64,64))    
    if count.recharge:
            count.tablefilament += 0.005
            count.filamentround = math.floor(count.tablefilament)
            tablefilament.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/tablefilament/tablefilament{count.filamentround}.png'), (128,128))
                               
    if count.tablefilament >=5:
        count.tablefilament = 5
        count.recharge = False
    tablefilament.image = pygame.transform.scale(pygame.image.load(f'assets/sprites/items/tablefilament/tablefilament{count.filamentround}.png'), (128,128))
    
    count.laptop +=0.002
    if count.laptop >=1:
        count.laptop = 1

    count.sale +=1    
    if count.sale >=625 and count.saletype != 0:
        pygame.mixer.Sound(sound.fail).play()
        count.sale = random.randint(0,100)
    
    
    
    count.student1 +=1
    if count.student1 >=1100:
        pygame.mixer.Sound(sound.fail).play()
        
        count.student1outfit = random.randint (1,5)
        count.student1quote = random.randint(1,4)
        count.student1 = random.randint(-200,0)
    count.student2 +=1
    if count.student2 >=850:
        pygame.mixer.Sound(sound.fail).play()
        
        count.student2outfit = random.randint (1,5)
        count.student2quote = random.randint(1,4)
        count.student2 = random.randint(-200,0)
    count.tablepass +=0.005
    if count.tablepass >=3:
        count.tablepass = 3
    
    #if player.idle == False:
        #walking = pygame.mixer.Channel(5)
        #if walking.get_busy():
            #pass
        #else:
            #walking.play(sound.walk)
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

def player_handle_movement(keys_pressed,player,event): 
    
    count.collide = pygame.sprite.collide_rect(player,table) or pygame.sprite.collide_rect(player,cart)
    count.printcollide = pygame.sprite.collide_rect(player,prusa1) or pygame.sprite.collide_rect(player,prusa2) or pygame.sprite.collide_rect(player,prusa3) or pygame.sprite.collide_rect(player,ender) or pygame.sprite.collide_rect(player,ultimaker)
    count.filamentcollide = pygame.sprite.collide_rect(player,tablefilament)
    count.laptopcollide = pygame.sprite.collide_rect(player,laptop)
    count.passcollide = pygame.sprite.collide_rect(player,hallpass)
    print_anims()
    count.VEL = 10
    if Player().stamina <= 0:
        Player().stamina = 0 
        Player().sprint = False

    
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
            player_left = pygame.transform.scale(pygame.image.load(f'assets/sprites//player/Walk/left/SidewalkL{count.walk}.png'), (256, 256))
            player.sprite = player_left
   

    elif keys_pressed[pygame.K_d]:
        player.direction = 'right'
        if player.x + count.VEL < 850:  # RIGHT
            player.idle = False     
            player.x += count.VEL
            player.rect.move_ip(+count.VEL,0)
            count.walk +=1
            if count.walk >= 8:
                count.walk = 1
            player_right = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/Walk/right/SidewalkR{count.walk //1}.png'), (256, 256))
            player.sprite = player_right
    

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
        player_back = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/Walk/back/BookerBackWalk{count.walk //1}.png'), (256, 256))
        player.sprite = player_back

        
            
        
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
        player_front = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/Walk/front/BookerFrontWalk{count.walk //1}.png'), (256, 256))
        player.sprite = player_front
            
    

    
    
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
            player_use = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/use/back/BookerBackUse{count.use //1}.png'), (256, 256))
        elif player.direction == 'down' or player.direction =='filde':
            player_use = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/use/front/BookerFrontUse{count.use //1}.png'), (256, 256))
        elif player.direction == 'left':
            player_use = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/use/left/sideusel{count.use //1}.png'), (256, 256))
        else:
            player.direction == 'right'
            player_use = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/use/right/sideuser{count.use //1}.png'), (256, 256))
        player.sprite = player_use
   
    elif keys_pressed[pygame.K_c]: #showcoords
        if count.randt == False:
            count.randt = True
        else:
            count.randt = False
        
    else: # IDLE  
        player.idle = True      
        count.idle +=1
        if player.direction == 'up':
            if count.idle >= 15:
                count.idle = 1
            player_idle = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/idle/back/BookerBackIdle{count.idle //1}.png'), (256, 256))
        elif player.direction == 'down':
            if count.idle >= 60:
                count.idle = 1
            player_idle = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/idle/front/BookerFrontIdle{count.idle //1}.png'), (256, 256))
        elif player.direction == 'left':
            if count.idle >= 60:
                count.idle = 1
            player_idle = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/idle/left/sideidlel{count.idle //1}.png'), (256, 256))
        elif player.direction == 'right':
            if count.idle >= 60:
                count.idle = 1
            player_idle = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/idle/right/sideidler{count.idle //1}.png'), (256, 256))
        else:
            if count.idle >= 60:
                count.idle = 1
            player_idle = pygame.transform.scale(pygame.image.load(f'assets/sprites/player/idle/front/BookerFrontIdle{count.idle //1}.png'), (256, 256))
        player.sprite = player_idle

    
    
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
        maintitle = pygame.transform.scale((pygame.image.load(f'assets/menu/main/mainmenu{count.title}.png')),(1024,768))
        screen.blit(maintitle, (0, 0))
              
        count.title +=1
        if count.title >64: #change back to
            count.title = 49    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                count.run = False
    
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        
                        pygame.mixer.Sound.play(sound.start)
                        pygame.mixer.music.stop()
                        pygame.time.wait(1500)
                        count.menu = False
                        count.loading = True
            if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        pygame.mixer.Sound.play(sound.start)
                        pygame.mixer.music.stop()
                        pygame.time.wait(1500)
                        count.menu = False
                        count.loading = True

                         
        pygame.display.update()

def loading(): 
    while count.loading: 

        clock.tick(FPS) 
        maintitle = pygame.transform.scale((pygame.image.load(f'assets/menu/loading/loading{count.load}.png')),(1024,768))
        screen.blit(maintitle, (0, 0))
        if count.gameovering:
            game.stop()
        count.load +=1
        if count.load >=12:
            count.load = 1    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                count.run = False
    
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
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
        player_handle_movement(keys_pressed,player,event)
        if count.readycount <10:
            getready = pygame.transform.scale(pygame.image.load('assets/menu/ready/getready.png'),(1024,768))
            screen.blit(getready,(0,0))
            pygame.display.flip()
        
        if count.readycount >=10 and count.readycount <20:
            getready3 = pygame.transform.scale(pygame.image.load('assets/menu/ready/getready3.png'),(1024,768))
            
            screen.blit(getready3,(0,0))
            pygame.display.flip()
        
        if count.readycount >=20 and count.readycount <30:
            getready2 = pygame.transform.scale(pygame.image.load('assets/menu/ready/getready2.png'),(1024,768))
            
            screen.blit(getready2,(0,0))
            pygame.display.flip()
        
        elif count.readycount >=30 and count.readycount <40:
            getready1 = pygame.transform.scale(pygame.image.load('assets/menu/ready/getready1.png'),(1024,768))
            
            screen.blit(getready1,(0,0))
            pygame.display.flip()
        
        elif count.readycount >=40 and count.readycount <50:
            getready0 = pygame.transform.scale(pygame.image.load('assets/menu/ready/getready0.png'),(1024,768))
            
            screen.blit(getready0,(0,0))
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
        timeup = pygame.transform.scale((pygame.image.load(f'assets/menu/timeup.png')),(1024,768)) 
        screen.blit(timeup,(0,0))
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
        game_over = pygame.transform.scale((pygame.image.load(f'assets/menu/gameover/gameover{count.gameover}.png')),(1024,768)) 
        screen.blit(game_over,(0,0))
        count.gameover +=1             
            
        if count.gameover >=60:
            count.gameover = 25
        if count.gameover >=25:
            levelcleared = game_over = pygame.transform.scale((pygame.image.load(f'assets/menu/levelcleared.png')),(1024,768)) 
            screen.blit(levelcleared,(0,0))
            draw_text('YOU EARNED',invent_font,WHITE,85,305)
            draw_text('POINTS',invent_font,WHITE,125,455)
            if invent.points < 10:
                draw_text('00000'+str(invent.points),pixel_font,YELLOW,40,350)
            if invent.points >= 10 and invent.points < 100:
                draw_text('0000'+str(invent.points),pixel_font,YELLOW,40,350)
            if invent.points >= 100 and invent.points < 1000:
                draw_text('000'+str(invent.points),pixel_font,YELLOW,40,350)
            if invent.points >= 1000 and invent.points < 10000:
                draw_text('00'+str(invent.points),pixel_font,YELLOW,40,350)
            if invent.points >= 10000 and invent.points < 100000:
                draw_text('0'+str(invent.points),pixel_font,YELLOW,40,350)
            if invent.points >= 100000 and invent.points < 1000000:
                draw_text(str(invent.points),pixel_font,YELLOW,40,350)
            draw_text('YOU BANKED',invent_font,WHITE,715,305)
            if invent.money < 10:
                draw_text('00000'+str(invent.money),pixel_font,GREEN,670,350)
            if invent.money >= 10 and invent.money < 100:
                draw_text('0000'+str(invent.money),pixel_font,GREEN,670,350)
            if invent.money >= 100 and invent.money < 1000:
                draw_text('000'+str(invent.money),pixel_font,GREEN,670,350)
            if invent.money >= 1000 and invent.money < 10000:
                draw_text('00'+str(invent.money),pixel_font,GREEN,670,350)
            if invent.money >= 10000 and invent.money < 100000:
                draw_text('0'+str(invent.money),pixel_font,GREEN,670,350)
            if invent.money >= 100000 and invent.money < 1000000:
                draw_text(str(invent.money),pixel_font,GREEN,670,350)
            money = pygame.transform.scale(pygame.image.load('assets/sprites/items/coin.png'),(80,80))
            screen.blit(money, (780,440))
            buttons = pygame.transform.scale(pygame.image.load('assets/menu/gameover/gameoverbuttons.png'),(1024,768))
            screen.blit(buttons,(0,0))
            
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
        sell_image = pygame.transform.scale(pygame.image.load(f'assets/sprites/sales/sellimage{count.saletype}.png'), (286,286))
        screen.blit(sell_image,(0,240))
    
    draw_text('STAMINA',invent_font,WHITE,815,10)
    draw_text('POINTS:',invent_font,WHITE,230,10)
    if invent.points < 10:
        draw_text('00000'+str(invent.points),invent_font,WHITE,230,55)
    if invent.points >= 10 and invent.points < 100:
        draw_text('0000'+str(invent.points),invent_font,WHITE,230,55)
    if invent.points >= 100 and invent.points < 1000:
        draw_text('000'+str(invent.points),invent_font,WHITE,230,55)
    if invent.points >= 1000 and invent.points < 10000:
        draw_text('00'+str(invent.points),invent_font,WHITE,230,55)
    if invent.points >= 10000 and invent.points < 100000:
        draw_text('0'+str(invent.points),invent_font,WHITE,230,55)
    if invent.points >= 100000 and invent.points < 1000000:
        draw_text(str(invent.points),invent_font,WHITE,230,55)
    
    
    time_minutes = count.gametime//600
    time_seconds = (count.gametime - ((count.gametime//600)*600))//10
    draw_text('TIME:',invent_font,WHITE,630,10)
    if time_seconds >9:
        draw_text(str(time_minutes)+":"+str(time_seconds),invent_font,WHITE,640,55)
    else:
        draw_text(str(time_minutes)+":0"+str(time_seconds),invent_font,WHITE,640,55)

    #draw_text('PRINTCOLLIDE ='+str(count.printcollide),invent_font,BLACK,300,50)
    #draw_text('SALE ='+str(count.sale)+' STUDENT1 = '+str(count.student1)+' STUDENT2 = '+str(count.student2),count_font,BLACK,230,108)
    #draw_text('Dq'+str(count.doorquote)+'St1 '+str(count.student1)+' St1q '+str(count.student1quote)+' St1o '+str(count.student1outfit)+' St2 '+str(count.student2)+' St2q '+str(count.student2quote)+' St2o '+str(count.student2outfit),count_font,BLACK,230,108)
    stamina_bar = pygame.transform.scale2x(pygame.image.load(f'assets/sprites/stamina/stamina{player.stamina}.png'))
    screen.blit(stamina_bar,(768,10))
    money = pygame.transform.scale2x(pygame.image.load('assets/sprites/items/coin.png'))
    draw_text(str(invent.money),invent_font,WHITE,75,32)
    screen.blit(money, (15,20))
    screen.blit(prusa1.image,(320,310))
    screen.blit(prusa2.image,(445,310))
    screen.blit(prusa3.image,(563,310))
    screen.blit(printers.octoimage,(360,355))
    screen.blit(printers.octoimage2,(485,355))
    screen.blit(printers.octoimage3,(602,355))
    screen.blit(ender.image,(686,280))
    screen.blit(printers.benchimage,(732,345))
    screen.blit(ultimaker.image,(817,284))
    screen.blit(printers.dragoimage,(848,315))
    
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
        
        teacherspeak = (pygame.transform.scale2x(pygame.image.load(f'assets/sprites/speech/speech{count.doorquote}.png')))
        screen.blit(teacherspeak,(player.x-55,player.y-25))
        
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
    if count.student1 >= 500:
        
        speech_l = (pygame.transform.scale2x(pygame.image.load(f'assets/sprites/speech/speechl{count.student1quote}.png')))
        screen.blit(speech_l,(270,550))
        
        student_l = pygame.transform.scale(pygame.image.load(f'assets/sprites/students/studentl/student{count.student1outfit}.png'), (256,256))
        screen.blit(student_l,(85,520))
    if count.student2 >= 350:
       
        
        speech_r = (pygame.transform.scale2x(pygame.image.load(f'assets/sprites/speech/speechr{count.student2quote}.png')))
        screen.blit(speech_r,(720,550))
         
        student_r = pygame.transform.scale(pygame.image.load(f'assets/sprites/students/studentr/student{count.student2outfit}.png'), (256,256))
        screen.blit(student_r,(780,520))
    #######RECTS
    rects = False
    if rects == True:
        #pygame.draw.rect(screen,BLACK,table.rect)
        #pygame.draw.rect(screen,BLACK,cart.rect)
        #pygame.draw.rect(screen,BLACK,prusa1.rect)
        #pygame.draw.rect(screen,BLACK,prusa2.rect)
        #pygame.draw.rect(screen,BLACK,prusa3.rect)
        #pygame.draw.rect(screen,BLACK,ender.rect)
        #pygame.draw.rect(screen,BLACK,ultimaker.rect)
        pygame.draw.rect(screen,BLACK,player.rect)
        #pygame.draw.rect(screen,BLACK,tablefilament.rect)
        #pygame.draw.rect(screen,BLACK,laptop.rect)
        #pygame.draw.rect(screen,BLACK,sell_rect)
        pygame.draw.rect(screen,BLACK,student.rect)
        pygame.draw.rect(screen,BLACK,student2.rect)
    
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
    count.student1 = 1
    count.student2 = 1
    


       

count.run = True
while count.run:
    clock.tick(FPS)
    
    
    
    
    if count.gametime <=0:
        count.gametime = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            count.run = False
    
    
                                    
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
    
    
    
                
     
    
    
    player_handle_movement(keys_pressed,player,event)  
    pygame.display.update()
    
pygame.quit()

