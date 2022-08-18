import pygame, random


class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("laser.png").convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.yy = 2
        self.image = pygame.image.load('donas.png').convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.x += random.randint(-3,3)        

        if self.rect.y > 600 - self.rect.height or self.rect.y < 0:
            self.yy = -self.yy

        self.rect.y += self.yy


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('monstruo.png').convert()
        self.image.set_colorkey(negro)
        self.rect = self.image.get_rect()
    
    def  update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.x = mouse_pos[0]
        self.rect.y = mouse_pos[1]
        
    def draw_text(surface, text, size, x, y):  #Se llama a la función que imprimirá el score en pantalla
        font = pygame.font.SysFont("serif", size)
        text_surface = font.render(text, True, blanco)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)
        
negro = 0,0,0
blanco = 255,255,255

def draw_text(surface, text, size, x, y):  #Se llama a la función que imprimirá el score en pantalla
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, blanco)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode([900,600])

    clock = pygame.time.Clock()
    run = True
    score = 0

    width = 900
    height = 600
    i = 0
    
    #Textos
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render('Score: ', 0, (255, 255, 255))
    
    fuenteSistema = pygame.font.SysFont("Castellar", 50)
    fondo = pygame.image.load('fondo2.jpg')
    fondorect = fondo.get_rect();
    bg = pygame.transform.scale(fondo, (900,600) )


    all_sprite_list = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    laser_list = pygame.sprite.Group()

    for i in range(10):
        meteor = Meteor()
        meteor.rect.x = random.randrange(800)
        meteor.rect.y = random.randrange(400)

        meteor_list.add(meteor)
        all_sprite_list.add(meteor)

    player = Player()
    all_sprite_list.add(player)

    sound = pygame.mixer.Sound('laser5.ogg')
    pygame.mixer.music.load('sonidofondo.mp3')
    pygame.mixer.music.play(3) #el 3 es el número de veces que se reproduce el archivo

    while run:
        for event in pygame.event.get(): #se captura el evento que se produce
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                laser = Laser()
                laser.rect.x = player.rect.x + 50
                laser.rect.y = player.rect.y - 20

                all_sprite_list.add(laser)
                laser_list.add(laser)
                sound.play()
    
        all_sprite_list.update() #actualiza el movimiento de los sprite
        #se definen las colisiones
        for laser in laser_list:
            meteor_hit_list = pygame.sprite.spritecollide(laser, meteor_list, True) # el true es para que desaparezcan
            #para eliminar el laser en las colisiones
            for meteor in meteor_hit_list:
                all_sprite_list.remove(laser)
                laser_list.remove(laser)
                score += 1
                texto2 = fuenteSistema.render(str(score), True, (255, 255, 255))
                screen.blit(texto2, (700,550))
                print(score)
            if laser.rect.y < 0:
                all_sprite_list.remove(laser)
                laser_list.remove(laser)
        
   
        
        screen.fill((0,0,0))
        screen.blit(bg, (i,0))
        screen.blit(bg, (width+i,0))

        if i == -width:
            screen.blit(bg, (width+i, 0))
            i = 0

        i -= 1
        all_sprite_list.draw(screen) #se pintan todos los sprites
        
        ##Marcador
        draw_text(screen, str(score), 25, 830, 553)
        
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()



if __name__ == "__main__":
    main()
