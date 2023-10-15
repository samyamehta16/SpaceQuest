#Pixel Py-oneers(Our teamname)
import pygame 
import random 
import sys

pygame.init()

screen_width = 1000
screen_height = 500

score = 0
spaceship_lives = 3
font = pygame.font.Font(None,36)
game_over_font = pygame.font.Font(None, 64)
spaceship_fires=[]
 
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Space Quest")

background_image = pygame.image.load("COMPETE/background.jpg")
background_image = pygame.transform.scale(background_image,(screen_width,screen_height))
bg_width = background_image.get_width() 
bg_x = 0
speed_increase_rate = 0
spaceship_fires=[]
stars = []
asteroids=[]
class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("COMPETE/spaceship.png")
        self.img = pygame.transform.scale(self.img ,(100,100))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.run_animation_count = 0
        
        self.is_jump = False
        self.img_list=["compete/spaceship.png","compete/spaceship.png","compete/spaceship.png","compete/spaceship.png"]
        self.jump_count = 15
        self.fire_img= "compete/fire.png"

    def run_animation_spaceship(self):
        if not self.is_jump:
            self.img = pygame.image.load(self.img_list[int(self.run_animation_count)])
            self.img = pygame.transform.scale(self.img,(300,300))
            self.rect = self.img.get_rect()
            self.rect.center = (self.x, self.y)
            self.run_animation_count+=0.5
            self.run_animation_count=self.run_animation_count%4            
        

    def draw(self):
        self.rect.center = (self.x , self.y)
        screen.blit(self.img , self.rect)

    def jump(self):
        if (self.jump_count>=-15):
            n= 1
            if(self.jump_count<0):
                n =-1
            self.y -= ((self.jump_count ** 2)/10 *n)
            self.jump_count-=1
        else:
            self.is_jump = False
            self.jump_count =20
            self.y=386
    def shoot(self):
        fire = Fire(self.x+5, self.y-18, self.fire_img)
        spaceship_fires.append(fire)

class Asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("compete/asteroid.png")
        self.img = pygame.transform.scale(self.img ,(100,100))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        self.run_animation_count = 0
        self.img_list=["compete/asteroid.png","compete/asteroid.png","compete/asteroid.png"]
    
       
        
    def draw(self):
        self.rect.center = (self.x , self.y)
        screen.blit(self.img , self.rect)

    def run_animation_asteroid(self):
        self.img = pygame.image.load(self.img_list[int(self.run_animation_count)])
        self.img = pygame.transform.scale(self.img,(75,75))
        self.run_animation_count+=0.5
        self.run_animation_count=self.run_animation_count%3 

class Star:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.img = pygame.image.load("compete/star.png")
        self.img = pygame.transform.scale(self.img,(150,150))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
        
    
    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img, self.rect)
   
    def move(self, vel):
        self.x +=vel

    def off_screen(self):
        return(self.x<=0 or self.x>=screen_width)
    
class Fire:
    def __init__(self,x,y,img):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img,(15,15))
        self.rect = self.img.get_rect()
        self.rect.center = (x,y)
    
    def draw(self):
        self.rect.center = (self.x,self.y)
        screen.blit(self.img, self.rect)
   
    def move(self, vel):
        self.x +=vel

    def off_screen(self):                    
        return(self.x<=0 or self.x>=screen_width)

spaceship = Character(100,386)

running = True
clock = pygame.time.Clock() 
last_star_spawn_time = pygame.time.get_ticks()

last_asteroid_spawn_time = pygame.time.get_ticks()

while running:
    score+=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not spaceship.is_jump:
                spaceship.is_jump = True
            if event.key == pygame.K_RIGHT:
                spaceship.shoot()
    speed_increase_rate+=0.006
    bg_x-=(10+ speed_increase_rate)
    if bg_x < -bg_width:
        bg_x = 0
    screen.blit(background_image,(bg_x,0))
    screen.blit(background_image,(bg_x+bg_width,0))

    spaceship.run_animation_spaceship()
    spaceship.draw()
    current_time = pygame.time.get_ticks()
    if (current_time - last_asteroid_spawn_time) >= 3000:
        if random.randint(0,100)<3:
            asteroid_x = screen_width + 900
            asteroid_y = 396
            asteroid = Asteroid(asteroid_x,asteroid_y)
            asteroids.append(asteroid)
            last_asteroid_spawn_time = current_time

    current_time = pygame.time.get_ticks()
    if (current_time - last_star_spawn_time) >= 3000:
        if random.randint(0,100)<3:
            star_x = screen_width + 900
            star_y = 100
            star = Star(star_x,star_y)
            stars.append(star)
            last_star_spawn_time = current_time
    
    for asteroid in asteroids:
        asteroid.x -=(15 + speed_increase_rate)
        asteroid.draw()
        asteroid.run_animation_asteroid()

        if asteroid.rect.colliderect(spaceship.rect):
            spaceship_lives -=1
            asteroids.remove(asteroid)

        for fire in spaceship_fires:
            if pygame.Rect.colliderect(asteroid.rect, fire.rect):
                spaceship_fires.remove(fire)
                asteroids.remove(asteroid)
                score-=10

    for star in stars:
         star.x -=(15 + speed_increase_rate)
         star.draw()

         if star.rect.colliderect(spaceship.rect):
               score+=100
               stars.remove(star)

    if spaceship_lives <=0:
        game_over_text = game_over_font.render("Game Over", True, (255,255,255))
        screen.blit(game_over_text,(screen_width//2 -120, screen_height//2))
        pygame.display.update()
        pygame.time.wait(1000)
        pygame.quit
        sys.exit
    
    live_text = font.render(f"Lives:{spaceship_lives}", True, (255,255,255))
    screen.blit(live_text,(screen_width-120,10))
    score_text = font.render(f"Score:{score}",True,(255,255,255))
    screen.blit(score_text,(20,10))
    if spaceship.is_jump:
        spaceship.jump()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
