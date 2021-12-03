from random import randint, choice

import pygame
pygame.init()
# Configure the screen
screen = pygame.display.set_mode([500, 500])
# Creat the game loop
running = True

clock = pygame.time.Clock()

lanes = [93, 218, 343]

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super(GameObject, self).__init__()
        # self.surf = pygame.Surface((width, height))
        # self.surf.fill((255, 0, 255))
        self.surf = pygame.image.load(image)
        self.x = x
        self.y = y
        self.rect = self.surf.get_rect() # add 

    def render(self, screen):
        self.rect.x = self.x # add
        self.rect.y = self.y # add
        screen.blit(self.surf, (self.x, self.y))


class Apple(GameObject):
    def __init__(self):
        super(Apple, self).__init__(choice(lanes), 0, './images/apple.png')
        self.dx = 0
        self.dy = (randint(0, 200) / 100) + 1
        self.reset()  # call reset here!
        self.direction = choice([0, 1])

    def move(self):
        if self.direction == 0:
            self.x += self.dx
            self.y += self.dy
            # Check the y position of the apple
            if self.y > 500:
                self.reset()
        else: 
            self.x -= self.dx
            self.y -= self.dy
            if self.y < 0:
                self.reset()

    # add a new method
    def reset(self):
        self.x = choice(lanes)
        self.direction = choice([0, 1])
        if self.direction == 0:
            self.y = -64
        else:
            self.y = 564



class Strawberry(GameObject):
    def __init__(self):
        super(Strawberry, self).__init__(0, choice(lanes), './images/strawberry.png')
        self.dx = (randint(0, 200) / 100) + 1
        self.dy = 0
        self.reset()  # call reset here!
        self.direction = choice([0, 1])

    def move(self):
        if self.direction == 0:
            self.x += self.dx
            self.y += self.dy
            # Check the y position of the apple
            if self.x > 500:
                self.reset()
        else:
            self.x -= self.dx
            self.y -= self.dy
            # Check the y position of the apple
            if self.x < 0:
                self.reset()

    # add a new method
    def reset(self):
        self.x = -64
        self.y = choice(lanes)
        self.direction = choice([0, 1])
        if self.direction == 0:
            self.x = -64
        else:
            self.x = 565

class Player(GameObject):
    def __init__(self):
        super(Player, self).__init__(0, 0, './images/player.png')
        self.dx = 93
        self.dy = 93
        self.pos_x = 1
        self.pos_y = 1
        self.reset() 

    def left(self):
        if self.pos_x > 0:
            self.pos_x -= 1
            self.update_dx_dy()

    def right(self):
        if self.pos_x < len(lanes) - 1:
            self.pos_x += 1
            self.update_dx_dy()

    def up(self):
        if self.pos_y > 0:
            self.pos_y -= 1
            self.update_dx_dy()

    def down(self):
        if self.pos_y < len(lanes) - 1:
            self.pos_y += 1
            self.update_dx_dy()

    def move(self):
        self.x -= (self.x - self.dx) * 0.25
        self.y -= (self.y - self.dy) * 0.25

    def reset(self):
        self.x = lanes[self.pos_x]
        self.y = lanes[self.pos_y]
        self.update_dx_dy()

    def update_dx_dy(self):
        self.dx = lanes[self.pos_x]
        self.dy = lanes[self.pos_y]

class Bomb(GameObject):
    def __init__(self):
        super(Bomb, self).__init__(0, 0, './images/bomb.png')
        self.dx = 0
        self.dy = 0
        self.reset()
        self.direction = choice([0, 1])
        self.direction_y = choice([0, 1])
        self.direction_x = choice([0, 1])

    def move(self):
        # print(self.direction_x)
        if self.direction == 0:
            if self.direction_x == 0:
                self.x += self.dx 
                self.y += self.dy
                if self.x > 500:
                    print('x1 end')
                    self.reset()
            else:
                self.x -= self.dx 
                self.y -= self.dy 
                if self.x < 0:
                    print('x2 end')
                    self.reset()
        else: 
            if self.direction_y == 0:
                self.x += self.dx 
                self.y += self.dy 
                if self.y > 500:
                    print("y1 end")
                    self.reset()
            else:
                self.x -= self.dx 
                self.y -= self.dy 
                if self.y < 0:
                    print("y2 end")
                    self.reset()



    def reset(self):
        self.direction = choice([0, 1])
        if self.direction == 0:
            self.dx = (randint(0, 200) / 100) + 1
            self.dy = 0
            self.y = choice(lanes)
            self.x = -64
            self.direction_x = choice([0, 1])
            print("Direction: horizontal")
        else:
            self.dx = 0
            self.dy = (randint(0, 200) / 100) + 1
            self.x = choice(lanes)
            self.y = -64
            self.direction_y = choice([0, 1])
            print("Direction: vertical")



apple = Apple()
strawberry = Strawberry()
player = Player()
bomb = Bomb()

#group sprites
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(apple)
all_sprites.add(strawberry)
all_sprites.add(bomb)

#group fruits
fruit_sprites = pygame.sprite.Group()
fruit_sprites.add(apple)
fruit_sprites.add(strawberry)


while running:
    # Looks at events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()

    #reset screen
    screen.fill((255, 255, 255))

    for entity in all_sprites:
        entity.move()
        entity.render(screen)

    fruit = pygame.sprite.spritecollideany(player, fruit_sprites)
    if fruit:
	    fruit.reset()

    if pygame.sprite.collide_rect(player, bomb):
	    running = False
    # Update the window
    pygame.display.flip()
    clock.tick(60)
