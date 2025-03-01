import pygame

# initializes all imported pygame modules
pygame.init()

'''Initial setup'''

#font that is used to render the text
font20 = pygame.font.Font('freesansbold.ttf', 20)

#RGB values of standard colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#Basic parameters of the screen
WIDTH, HEIGHT, = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pong")
#used to adjust frame rate
clock = pygame.time.Clock()
FPS = 30

'''stricker: the stricker class has the following method
- init() used to initialize the class variables
- display() used to render the object on the screen
- update() used to change the state of the object
- displayScore() used to render the score of the player on the screen in text format
- getRect() used to get the rect object
'''

#Player Class
class Stricker:
    #take the initial position
    # dimensions, speed and color of the object
    def __init__ (self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        #rect that is used to control the position and collisions of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        #object that is blit on the screen
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)
        

    #used to update the state of the object
    # yFac represents the direction of the stricker movement
    # if yFac == -1 ==> the object is moving upwards
    # if yFac == 1 ==> the object is moving downwards
    # if yFac == 0 ==> the object is not moving

    #used to diaply an object to the screen
    def display(self):
         self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed*yFac

        #Restricting the stricker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # restricting the stricker to be above
        # the botton surface on the screen
        elif self.posy +  self.height >= HEIGHT:
                self.posy = HEIGHT-self.height

        #updating the rect with new values        
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    #used to render the score on the screen
    # first, create a text objer using the font.render() method
    # then, get the rect of that text using the get_rect() method
    # finally blit the text on the screen
    def displayScore(self, text, score, x, y, color):
         text = font20.render(text+str(score), True, color)
         textRect = text.get_rect()
         textRect.center = (x,y)

         screen.blit(text, textRect)
    def getRect(self):
         return self.geekRect     

'''ball: the ball class has the following methods: 
- init() used to initialize the class variables
- display() used to render the object onto the screen
- update() used to change the state of the object
- getRect() used to get the rect object
'''    
# ball class
class Ball:
     def __init__(self, posx, posy, radius, speed, color):
          self.posx = posx
          self.posy = posy
          self.radius = radius
          self.speed = speed
          self.color = color
          self.xFac = 1
          self.yFac = -1
          self.ball = pygame.draw.circle(
               screen, self.color, (self.posx, self.posy), self.radius
          ) 
          self.firstTime = 1
     def display(self):
            self.ball = pygame.draw.circle(
                screen, self.color, (self.posx, self.posy), self.radius
            )

     def update(self):
          self.posx += self.speed*self.xFac
          self.posy += self.speed*self.yFac

          #if the ball hits the top or bottom surfaces, then the sign of yFac is changed and it results in a reflection
          if self.posy <= 0 or self.posy >=HEIGHT:
               self.yFac *= -1

          #is the ball touches the left wall for the first time, the firstTime is set to 0 and we return 1 indicating that Geek2 has scored.
          # firstTime is set to 0 and so that the condition if met only once and we can avoid giving multiple points to the player
          if self.posx <=0 and self.firstTime:
               self.firstTime = 0
               return 1
          elif self.posx >= WIDTH and self.firstTime:
               self.firsTime = 0
               return -1
          else: 
               return 0

    #used to reset the position of the ball to the center of the screen
     def reset(self):
          self.posx = WIDTH//2
          self.posy= HEIGHT//2
          self.xFac *= -1
          self.firstTime =1
    #used to reflect the ball along the x-axis
     def hit(self):
          self.xFac *= -1

     def getRect(self):
          return self.ball
     
#Game Manager
def main():
    running = True
    #defining the object
    geek1 = Stricker(20,0,10,100,10, GREEN)
    geek2 = Stricker(WIDTH-30,0,10,100,10,GREEN)
    ball = Ball(WIDTH//2, HEIGHT//2, 7,7,WHITE)

    listOfGeeks = [geek1, geek2]
    #initial parameters of the players
    geek1Score, geek2Score = 0,0
    geek1YFac, geek2YFac = 0,0

    while running:
        screen.fill(BLACK)

        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0
        
        # collosion detection
        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
        #updating the objects
        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()

        #-1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        # 0 -> none of them scored
        if point == -1:
            geek1Score +=1
        elif point == 1:
            geek2Score +=1
        
        #someone has scored a point and the ball is out of bounds, so, we reset its position
        if point:
            ball.reset()

        # displaying the object on the screen
        geek1.display()
        geek2.display()
        ball.display()

        #displaying the scores of the players
        geek1.displayScore("Player 1 : ", geek1Score, 100, 20, WHITE)
        geek2.displayScore("Player 2: ", geek2Score, WIDTH-100, 20, WHITE)

        pygame.display.update()
        #adjust the frame rate
        clock.tick(FPS)            

if __name__ == "__main__":
     main()
     pygame.quit()





                 