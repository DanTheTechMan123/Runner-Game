import pygame
import tkinter as tk


start = tk.Tk()
start.title("Runner game")
start.configure(width=500, height=500)


def starts():
    start.destroy()


def ins():
    def back():
        instructions.destroy()
    instructions = tk.Tk()
    instructions.title("Instructions")
    instructions.configure(width=200,height=200)
    ins_title = tk.Label(instructions, text="Instructions")
    ins_title.pack(side="top", pady=10, padx=10)
    ins_1 = tk.Label(instructions, text="Use the up button to jump!")
    ins_1.pack(side="top", pady=10, padx=10)
    ins_2 = tk.Label(instructions, text="Use the down button to slide!")
    ins_2.pack(side="top", pady=10, padx=10)
    ins_3 = tk.Label(instructions, text="Avoid obstacles and survive for as long as possible!")
    ins_3.pack(side="top", pady=10, padx=10)
    back = tk.Button(instructions, text="Back", command=back)
    back.pack(side="top", pady=10, padx=10)
    instructions.mainloop()


title = tk.Label(start, text="Runner game")
title.pack(side="top", pady=10, padx=10)

start_button = tk.Button(start, text="Press to start", command=starts)
start_button.pack(side="top", pady=10, padx=10)

ins_button = tk.Button(start, text="Press for instructions", command=ins)
ins_button.pack(side="top", pady=10, padx=10)

start.mainloop()

pygame.init()
pygame.font.init()
pygame.mixer.init()


pygame.mixer.music.load("Audio/Song.mp3")
pygame.mixer.music.play(-1)

sprite = pygame.image.load("Images/meme.png")
obs = pygame.image.load("Images/obs.png")
obs2 = pygame.image.load("Images/obs2.png")

bg = pygame.image.load("Images/background.png")
bgx = 0

sprites = [pygame.image.load("Images/s1.png"), pygame.image.load("Images/s2.png"), pygame.image.load("Images/s3.png"),
           pygame.image.load("Images/s4.png"), pygame.image.load("Images/s5.png"), pygame.image.load("Images/s6.png"),
           pygame.image.load("Images/s7.png")]
slide_img = pygame.image.load("Images/slide.png")
jump_img = pygame.image.load("Images/jump.png")
scount = 0
myfont = pygame.font.SysFont('Comic Sans MS', 20)
window = pygame.display.set_mode((750, 450))
pygame.display.set_caption("Runner")
run = True


score = 0

class player():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.isSlide = False
        self.jumpCount = 10
        self.hitbox = [self.x, self.y, self.x + self.width, self.y + self.height]


class obstacle():
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = [self.x, self.y, self.x + self.width, self.y + self.height]
        self.vel = vel


def contact(a, b):
    if b.y + b.width > a.y > b.y or b.y + b.width > a.y + a.height > b.y:
        if b.x + b.width > a.x > b.x or b.x + b.width > a.x + a.width > b.x:
            pygame.quit()
            ending()


def redrawgamewindow():
    window.blit(bg, (bgx, -700))
    if runner.isJump:
        window.blit(jump_img, (runner.x, runner.y))
    elif runner.isSlide:
        window.blit(slide_img, (runner.x, runner.y))
    else:
        window.blit(sprites[scount % 5], (runner.x, runner.y))
    textsurface = myfont.render("Score: " + str(score), False, (0,0,0))
    window.blit(textsurface, (0, 0))
    window.blit(obs2, (arrow.x, arrow.y))
    window.blit(obs, (boulder.x, boulder.y))
    pygame.display.update()

def ending():
    end = tk.Tk()
    end.title("Game Over")
    end.configure(width=500, height=500)
    end_title = tk.Label(end, text="GAME OVER")
    end_title.pack(side="top", pady=10, padx=10)
    scores = tk.Label(end, text="Your score was: " + str(score))
    scores.pack(side="top", pady=10, padx=10)
    end.mainloop()


runner = player(50, 380, 70, 60)
boulder = obstacle(750, 350, 100, 100, 15)
arrow = obstacle(750, 350, 150, 50, 50)
slide_count = 0
boulder_count = 0
arrow_count = 0
score_lim = 1000

while run:
    pygame.time.delay(50)
    slide_count += 50
    boulder_count += 50
    arrow_count += 50
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    if not runner.isJump:
        if keys[pygame.K_UP]:
            runner.isJump = True
    else:
        if runner.jumpCount >= -10:
            neg = 0.75
            if runner.jumpCount < 0:
                neg = -0.75
            runner.y -= (runner.jumpCount ** 2) * 0.5 * neg
            runner.jumpCount -= 1
        else:
            runner.isJump = False
            runner.jumpCount = 10
    if not runner.isSlide:
        if keys[pygame.K_DOWN]:
            runner.isSlide = True
            slide_count = 0
    else:
        if slide_count < 500:
            runner.isJump = False
            runner.height = 40
            runner.y = 400
        else:
            runner.isSlide = False
            runner.height = 60
            runner.y = 380
            slide_count = 0
    if boulder.x >= -100:
        pass
    else:
        if boulder_count <= 3000:
            pass
        else:
            boulder.x = 1000
            boulder_count = 0
    boulder.x -= boulder.vel
    if arrow_count <= 3000:
        pass
    else:
        arrow.x -= arrow.vel
    contact(runner, boulder)
    contact(arrow, runner)
    if arrow.x >= - 512:
        pass
    else:
        if arrow_count <= 11000:
            pass
        else:
            arrow.x = 1000
            arrow_count = 0
    scount += 1
    if bgx < - 1298:
        bgx = 0
    bgx -= 10
    score += 1
    if score >= score_lim:
        arrow.vel += 5
        boulder.vel += 5
        score_lim += 500

    redrawgamewindow()
