import pygame
import math
import random

pygame.init()

sw = 800
sh = 800

bg = pygame.image.load('asteroidsPics/starbg.png')
alienImg = pygame.image.load('asteroidsPics/alienShip.png')
playerShip = pygame.image.load('asteroidsPics/spaceRocket.png')
star = pygame.image.load('asteroidsPics/star.png')
asteroid50 = pygame.image.load('asteroidsPics/asteroid50.png')
asteroid100 = pygame.image.load('asteroidsPics/asteroid100.png')
asteroid150 = pygame.image.load('asteroidsPics/asteroid150.png')

pygame.display.set_caption('Asteroids')
screen = pygame.display.set_mode((sw, sh))

clock = pygame.time.Clock()

gameover = False
lives = 3
score= 0
tries_count = 0

class Player(object):
    def __init__(self):
        self.img = playerShip
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw//2
        self.y = sh//2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle) #Метод отвечающий за поворот
        self.rotatedRect = self.rotatedSurf.get_rect() #Получение координат после поворота
        self.rotatedRect.center = (self.x, self.y) #Располагает корабль в центре поля
        self.cosine = math.cos(math.radians(self.angle + 90)) #Расположение 0 направо
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2) #Координаты головы корабля

    def draw(self, screen):
        # screen.blit(self.img, [self.x, self.y, self.h, self.w])
        screen.blit(self.rotatedSurf, self.rotatedRect) #Обновляемость положения

    def turnLeft(self):
        self.angle += 5 #Каждый поворот с шагом 5
        self.rotatedSurf = pygame.transform.rotate(self. img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def turnRight(self):
        self.angle -= 5
        self.rotatedSurf = pygame.transform.rotate(self. img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 6
        self.y -= self.sine * 6
        self.rotatedSurf = pygame.transform.rotate(self. img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def Location(self):
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0



class Bullet(object):
    def __init__(self):
        self.point = player.head
        self.x, self.y = self.point
        self.w = 4
        self.h = 4
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self): #Скорость движения пули
        self.x += self.xv
        self.y -= self.yv

    def draw(self, screen): #Рисует пулю
        pygame.draw.rect(screen, (255, 255, 255), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self): #Проверка вылета пули за пределы экрана
        if self.x < -50 or self.x > sw or self.y > sh or self.y < -50:
            return True


class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        else:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw-self.w), #Слева
                                        random.choice([-1*self.h - 5, sh + 5])), #
                                       (random.choice([-1*self.w - 5, sw + 5]), #
                                        random.randrange(0, sh - self.h)) #
                                       ])
        self.x, self.y = self.ranPoint #Траектории полета
        if self.x < sw//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, screen): #Отрисовка астероидов
        screen.blit(self.image, (self.x, self.y))


def redrawGameWindow(): # Стилизация окна
    screen.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial', 30)
    livesText = font.render('Lives: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('Press Space to Play Again', 1, (255, 255, 255))
    playAgainText1 = font.render('Press Space to Play', 1, (255, 255, 255))
    scoreText = font.render('Score: ' + str(score), 1, (255, 255, 255))

    player.draw(screen)
    for a in asteroids:
        a.draw(screen)
    for b in playerBullets:
        b.draw(screen)
    if gameover:
        screen.blit(playAgainText, (sw//2-playAgainText.get_width()//2, sh//2-playAgainText.get_height()//2))
    screen.blit(livesText, (25, 25))
    screen.blit(scoreText, (sw - scoreText.get_width() - 25, 25))
    pygame.display.update()


player = Player()
playerBullets = []
asteroids = []
count = 0

run = True
while run:
    clock.tick(60)
    count +=1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroids.append(Asteroid(ran))
        player.Location()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b))

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv
            if (a.x >= player.x - player.w//2 and a.x <= player.x + player.w//2) or (a.x + a.w <= player.x + player.w//2 and a.x + a.w >= player.x - player.w//2):
                if(a.y >= player.y - player.h//2 and a.y <= player.y + player.h//2) or (a.y  +a.h >= player.y - player.h//2 and a.y + a.h <= player.y + player.h//2):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break


            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or (b.x >= a.x and b.x + b.w <= a.x + a.w):
                    if (b.y >= a.y and b.y <= a.y + a.h) or (b.y >= a.y and b.y + b.h <= a.y + a.h):
                        if a.rank == 3:
                            score += 10
                            na1 = Asteroid(2)
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score +=30
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))

        if lives <= 0:
            gameover = True
            tries_count +=1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not gameover:
                    playerBullets.append(Bullet())
                else:
                    gameover = False
                    lives = 3
                    asteroids.clear()
                    score = 0

    redrawGameWindow()
pygame.quit()

