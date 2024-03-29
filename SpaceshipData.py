import pygame
import random
from spaceship import Spaceship
from baddie import Baddie

class SpaceshipData:

    def __init__(self,width,height,frame_rate):
        self.font = pygame.font.SysFont("Times New Roman",36)
        self.font2 = pygame.font.SysFont("Castellar",20)
        self.frame_rate = frame_rate
        self.text_color = (255,0,0)
        self.width  = width
        self.height = height
        self.upper_limit = self.width/3
        self.spaceship_width = 20
        self.spaceship_height = 10
        self.spaceship = Spaceship(self.spaceship_width,self.spaceship_height,0,(self.height / 2) - 10, (255,255,255))
        self.spaceship_speed = 5
        self.bullets = []
        self.bullet_width = 10
        self.bullet_height = 5
        self.bullet_color = (255,255,255)
        self.baddies = []
        self.baddie_width = 20
        self.baddie_height = 20
        self.baddie_color = (255,0,0)
        #SCORE
        self.kills = 0
        self.score_color = (0, 212, 83)
        self.score_x = 10
        self.score_y = 30
        #/SCORE
        
        return

    def evolve(self, keys, newkeys, buttons, newbuttons, mouse_position):
        if pygame.K_LEFT in keys:
            self.spaceship.moveLeft(self.spaceship_speed)
        if pygame.K_RIGHT in keys:
            self.spaceship.moveRight(self.spaceship_speed,self.upper_limit)
        if pygame.K_UP in keys:
            self.spaceship.moveUp(self.spaceship_speed)
        if pygame.K_DOWN in keys:
            self.spaceship.moveDown(self.spaceship_speed,self.height)

        if pygame.K_SPACE in newkeys:
            self.bullets.append(self.spaceship.fire(self.bullet_width,self.bullet_height,self.bullet_color))

        if random.randint(1, self.frame_rate/2) == 1:
            self.addBaddie()

        for bullet in self.bullets:
            bullet.moveBullet()
            bullet.checkBackWall(self.width)
                
        for baddie in self.baddies:
            baddie.tick(0,0,self.height)

        for bullet in self.bullets:
            if not bullet.alive:
                continue
            for baddie in self.baddies:
                if not baddie.alive:
                    continue
                x,y,w,h = baddie.getDimensions()
                bullet.checkHitBaddie(x,y,w,h)
                if bullet.getHit():
                    bullet.setAlive(False)
                    baddie.setAlive(False)
                    #SCORE
                    self.kills = self.kills + 1
                    #/SCORE
                    bullet.hit = False


        live_bullets = []
        live_baddies = []
        for bullet in self.bullets:
            if bullet.alive:
                live_bullets.append(bullet)
        for baddie in self.baddies:
            if baddie.alive:
                live_baddies.append(baddie)
      
        self.bullets = live_bullets
        self.baddies = live_baddies
            
        return

    def addBaddie(self):
        new_baddie = Baddie( self.baddie_width, self.baddie_height, self.width, random.randint(0,(self.height-self.baddie_height)), self.baddie_color )
        self.baddies.append( new_baddie )
                   
        return

    def draw(self,surface):
        rect = pygame.Rect(0,0,self.width,self.height)
        surface.fill((0,0,0),rect )
        self.spaceship.draw(surface)
        for bullet in self.bullets:
            bullet.draw(surface)
        for baddie in self.baddies:
            baddie.draw(surface)
            #SCORE
            score_str = "Score: " + str(self.kills)
            self.drawTextLeft(surface, score_str, self.score_color, self.score_x, self.score_y, self.font2)
            #/SCORE
        return

    
    def drawTextLeft(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomleft = (x, y)
        surface.blit(textobj, textrect)
        return

    def drawTextRight(self, surface, text, color, x, y,font):
        textobj = font.render(text, False, color)
        textrect = textobj.get_rect()
        textrect.bottomright = (x, y)
        surface.blit(textobj, textrect)
        return
