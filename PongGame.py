import pygame
import tkinter as tk

pygame.init()

'''Initial setup'''
font20 = pygame.font.Font('freesansbold.ttf', 20)

# RGB values of standard colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Basic parameters of the screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
FPS = 30

# Initialize Tkinter window
window = tk.Tk()
window.title("Winner Display")
winner_label = tk.Label(window, text="", font=("Arial", 14))
winner_label.pack()

class Stricker:
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.geekRect = pygame.Rect(posx, posy, width, height)
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy += self.speed * yFac
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)
        screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac
        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    def hit(self):
        self.xFac *= -1

    def getRect(self):
        return self.ball


def display_winner(winner):
    """Updates the Tkinter window with the winner's name."""
    winner_label.config(text=f"The winner is: {winner}")
    window.update()


def main():
    running = True
    geek1 = Stricker(20, 250, 10, 100, 10, GREEN)
    geek2 = Stricker(WIDTH - 30, 250, 10, 100, 10, GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, WHITE)

    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0

    while running:
        screen.fill(BLACK)
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
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    geek2YFac = 0
                if event.key in (pygame.K_w, pygame.K_s):
                    geek1YFac = 0

        for geek in [geek1, geek2]:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()

        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()

        if point == -1:
            geek1Score += 1
        elif point == 1:
            geek2Score += 1

        if point:
            ball.reset()

        geek1.display()
        geek2.display()
        ball.display()
        geek1.displayScore("Player 1: ", geek1Score, 100, 20, WHITE)
        geek2.displayScore("Player 2: ", geek2Score, WIDTH - 100, 20, WHITE)

        pygame.display.update()
        clock.tick(FPS)

        # Check for a winner and stop the game
        if geek1Score == 10:
            print("Player 1 is the winner")
            display_winner("Player 1")
            pygame.time.delay(2000)  # Pause for 2 seconds
            running = False
        elif geek2Score == 10:
            print("Player 2 is the winner")
            display_winner("Player 2")
            pygame.time.delay(2000)  # Pause for 2 seconds
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()
