import pygame
import os
pygame.font.init()
pygame.mixer.init()

#WINDOWS/ BACKGROUND
WEIDTH,HIEGHT = 900,500
WIN = pygame.display.set_mode((WEIDTH,HIEGHT))
pygame.display.set_caption("Space Battle Showdown!")
WHITE = (255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)

BORDER = pygame.Rect(WEIDTH//2-5,0,10,HIEGHT)
#bullet sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets","Grenade+1.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets","Gun+Silencer.mp3"))

#game mechanism
HEALTH_TXT = pygame.font.SysFont("comicsans",40)
WINNER_TXT = pygame.font.SysFont("comicsans",100)

FPS = 40
VELOSITY = 4
BULLET_VELOSITY = 8
MAX_BULLET = 5
YELLOW_HIT = pygame.USEREVENT +1
RED_HIT = pygame.USEREVENT+2 

#spaceship config
SPACESHIP_WIDTH,SPACESHIP_HIGHT = 50,38


YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
        (YELLOW_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HIGHT)),90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join("Assets","spaceship_red.png"))

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
        (RED_SPACESHIP_IMAGE,(SPACESHIP_WIDTH,SPACESHIP_HIGHT)),270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),(WEIDTH,HIEGHT) )

#all things draw in windows/background
def draw_window(red,yellow,yellow_bullet,red_bullet, red_health, yellow_health):
    WIN.blit(SPACE,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)
    red_health_txt = HEALTH_TXT.render("Health: " + str(red_health),1 ,WHITE)
    yellow_health_txt = HEALTH_TXT.render("Health: " + str(yellow_health),1 ,WHITE)
    
    WIN.blit(red_health_txt,(WEIDTH - red_health_txt.get_width()-10,10 ))
    WIN.blit(yellow_health_txt,(10,10 ))
    WIN.blit(YELLOW_SPACESHIP,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP,(red.x,red.y))
    
    for bullet in red_bullet:
        pygame.draw.rect(WIN,RED,bullet)
        
    for bullet in yellow_bullet:
        pygame.draw.rect(WIN,YELLOW,bullet)
    pygame.display.update()
    
#yellow spaceship movement program
def yellow_movement(key_pressed,yellow):
    if key_pressed[pygame.K_a]and yellow.x - VELOSITY > 0 :#left    
        yellow.x -= VELOSITY
    if key_pressed[pygame.K_d] and yellow.x + VELOSITY + yellow.width  < BORDER.x: #right
        yellow.x += VELOSITY
    if key_pressed[pygame.K_s]and yellow.y + VELOSITY + yellow.height  < HIEGHT - 15 : #down   
        yellow.y += VELOSITY
    if key_pressed[pygame.K_w]and yellow.y - VELOSITY > 0: #up
        yellow.y -= VELOSITY

#red spaceship movement program
def red_movement(key_pressed,red):
    if key_pressed[pygame.K_LEFT]and red.x - VELOSITY > BORDER.x + BORDER.width :#left    
        red.x -= VELOSITY
    if key_pressed[pygame.K_RIGHT] and red.x + VELOSITY + red.width  < WEIDTH: #right
        red.x += VELOSITY
    if key_pressed[pygame.K_DOWN]and red.y + VELOSITY + red.height  < HIEGHT - 15: #down   
        red.y += VELOSITY
    if key_pressed[pygame.K_UP]and red.y - VELOSITY > 0: #up
        red.y -= VELOSITY


#bullet fire mechanism
def handle_bullet(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOSITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WEIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOSITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0 :
            red_bullets.remove(bullet)

#endscreen winner text
def draw_winner(text):
    draw_txt=WINNER_TXT.render(text,1,WHITE)
    WIN.blit(draw_txt,(WEIDTH/2-draw_txt.get_width()/2,HIEGHT/2 - draw_txt.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():#main funct of the game 
    red = pygame.Rect(700,200,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
    yellow = pygame.Rect(100,200,SPACESHIP_WIDTH,SPACESHIP_HIGHT)
    red_bullets=[]
    yellow_bullets=[]
    
    yellow_health = 15 # spaceship health
    red_health = 15
    
        
    clock = pygame.time.Clock()
    run = True
    while run: #game starting to end loop
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN: #bullet fire from spaceship mechanism
                if event.key== pygame.K_f and len(yellow_bullets) < MAX_BULLET:
                    bullets =pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2+2, 10,5)
                    yellow_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                    bullets =pygame.Rect(red.x, red.y + red.height//2+2, 10,5)
                    red_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()
                    
            if event.type== RED_HIT: #bullet hit to spaceship
                red_health -= 1
                BULLET_HIT_SOUND.play()
                
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                
        winner_txt = "" #winner text config
        if  red_health <=0:
            winner_txt = "Yellow Win!"   
        
        if yellow_health <= 0:
            winner_txt = "Red Win!"        
                
        if winner_txt != "":
            draw_winner(winner_txt) 
            break
        
            
            
        key_pressed = pygame.key.get_pressed() #all key and move ment passed down
        yellow_movement(key_pressed,yellow)
        red_movement(key_pressed,red)
        handle_bullet(yellow_bullets, red_bullets, yellow, red)
        draw_window(red,yellow,yellow_bullets,red_bullets,red_health,yellow_health)

    main()
    
if __name__ == "__main__":
    main()
