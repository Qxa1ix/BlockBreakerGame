import pygame,random
pygame.init()


we,le=1200,700
w=pygame.display.set_mode((we,le))
fps=60
time=pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self,player_grup):
        super().__init__()
        self.image=pygame.image.load('player.png')
        self.rect=self.image.get_rect()
        self.rect.centerx=600
        self.rect.centery =670
        self.player_grup = player_grup
        self.hiz=20
    def update(self):
        tus=pygame.key.get_pressed()
        if tus[pygame.K_a] and self.rect.left>-20:
            self.rect.x-=self.hiz
        if tus[pygame.K_d] and self.rect.right<1200:
            self.rect.x+=self.hiz


class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,ball_grup):
        super().__init__()
        self.image=pygame.image.load('ball.png')
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        self.ball_grup=ball_grup
        self.ycol=1
        self.xcol=1
        self.hiz=6

    def update(self):
        self.rect.x+=self.hiz*self.xcol
        self.rect.y+= self.hiz * self.ycol
        if self.rect.left<=0 or self.rect.right>=1200:
            self.xcol*=-1
        if self.rect.top<=0 or self.rect.bottom>=700:
            self.ycol*=-1


class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,block_grup,select):
        super().__init__()
        self.block_grup=block_grup
        self.image=pygame.image.load(select)
        self.rect=self.image.get_rect()
        self.rect.centerx=x
        self.rect.centery=y
        block_grup.add(self)
    def update(self):
        pass
class Game(Player,Ball,Block):
    def __init__(self):
        self.Player=Player
        self.Ball=Ball
        self.Block=Block
        self.level()
        self.level_no=1
        self.can=3

        self.background1=pygame.image.load('background1.jpg')
        self.background2 = pygame.image.load('background2.jpg')
        self.background3 = pygame.image.load('background3.jpg')
        self.background4 = pygame.image.load('background4.jpg')
        self.endphoto=pygame.image.load('endphoto.jpg')


        self.playercollide=pygame.mixer.Sound('playercollide.mp3')
        self.deathsound=pygame.mixer.Sound('deathsound.mp3')
        self.collidesound=pygame.mixer.Sound('collidesound.mp3')

        self.letertype=pygame.font.Font('EduVICWANTHandPre-Regular.ttf',40)
        self.cal=True




    def update(self):
        self.collide()
        self.playercol()
        if self.cal:
            if self.level_no==1:
                pygame.mixer.music.load('backsound1.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.9)
                self.cal=False
            if self.level_no==2:
                pygame.mixer.music.load('backsound2.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.9)
                self.cal=False

            if self.level_no==3:
                pygame.mixer.music.load('backsound2.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.9)
                self.cal=False
            if self.level_no==4:
                pygame.mixer.music.load('backsound3.mp3')
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.9)
                self.cal=False
    def draw(self):
        if self.level_no==1:
            w.blit(self.background1,(0,0))
        if self.level_no==2:
            w.blit(self.background2,(0,0))
            for top in ball_grup.sprites():
                top.hiz=8
        elif self.level_no==3:
            w.blit(self.background3,(0,0))
            for top in ball_grup.sprites():
                top.hiz=10
        elif self.level_no==4:
            w.blit(self.background4,(0,0))
            for top in ball_grup.sprites():
                top.hiz=12

    def collide(self):
        for top in ball_grup.sprites():
            collided_blocks = pygame.sprite.spritecollide(top, block_grup, False)

            if collided_blocks:
                self.collidesound.play()

                # Sadece ilk blok ile çarpışmayı ele al
                blok = collided_blocks[0]

                # X yönünde çarpışma
                if abs(top.rect.right - blok.rect.left) < 10 and top.xcol > 0:
                    top.xcol *= -1
                elif abs(top.rect.left - blok.rect.right) < 10 and top.xcol < 0:
                    top.xcol *= -1

                # Y yönünde çarpışma
                elif abs(top.rect.bottom - blok.rect.top) < 10 and top.ycol > 0:
                    top.ycol *= -1
                elif abs(top.rect.top - blok.rect.bottom) < 10 and top.ycol < 0:
                    top.ycol *= -1

                block_grup.remove(blok)  # sadece bir blok sil
                if len(block_grup)==0:
                    self.level_no+=1
                    self.level()
                    self.cal=True
                    if self.level_no>4:
                        self.end()
        for top in ball_grup.sprites():
            if top.rect.bottom>670:
                self.deathsound.play()

                self.can-=1
                ball_grup.empty()
                ball = Ball(player.rect.x, player.rect.y-20, ball_grup)
                ball_grup.add(ball)


    def playercol(self):
        for top in ball_grup.sprites():

            carpısma=pygame.sprite.spritecollide(player,ball_grup,False)
            if carpısma:
                top.ycol*=-1
                self.playercollide.play()
                self.playercollide.set_volume(0.1)


    def level(self):
        block_grup.empty()
        list=['block1.jpg','block2.jpg','block3.jpg']
        for e in range(4):
            for g in range(10):
                Block(130+101*g,40+50*e,block_grup,random.choice(list))
        ball_grup.empty()
        ball=Ball(600, 600, ball_grup)
        ball_grup.add(ball)
    def skore(self):
        pass
    def block(self):
        pass
    def reset(self):
        self.level_no=1
        pygame.mixer.music.stop()
        self.level()
        self.cal=True

    def end(self):
        edn=True
        global d
        w.blit(self.endphoto,(0,0))
        pygame.display.update()
        while edn:
            for e in pygame.event.get():
                if e.type==pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        edn=False
                        self.reset()
                if e.type==pygame.QUIT:
                    d=False
                    edn=False


player_grup=pygame.sprite.Group()
player=Player(player_grup)
player_grup.add(player)

ball_grup=pygame.sprite.Group()
ball=Ball(600,600,ball_grup)
ball_grup.add(ball)

block_grup=pygame.sprite.Group()
game=Game()
d=True
while d:
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            d=False
    game.draw()
    player_grup.update()
    player_grup.draw(w)
    ball_grup.update()
    ball_grup.draw(w)
    block_grup.update()
    block_grup.draw(w)
    game.update()

    pygame.display.update()
    time.tick(fps)


pygame.quit()