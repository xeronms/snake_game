import pygame
import sys, random, time

pygame.init()
clock = pygame.time.Clock()
#        green, blue, red, purple, yellow, pink
colors = [(100, 250, 10), (87, 248, 249), (249, 0, 25), (197, 76, 245), (249, 244, 25), (228, 11, 133)]
pygame.mixer.music.load("v5.wav")
crash_sound = pygame.mixer.Sound("puf.wav")
eat_sound = pygame.mixer.Sound("pop.wav")

myfont = pygame.font.SysFont("Impact", 35)


def init():
    screen = pygame.display.set_mode((500, 500))
    return screen


def draw(screen, snake, food, i, score):
    # clear screen, make it all black
    screen.fill((0, 0, 0))
    for part in snake:
        bit = pygame.Rect(part[0], part[1], 49, 49)
        pygame.draw.rect(screen, colors[i], bit)

    pygame.draw.rect(screen, colors[(i+1) % 6], food)

    text = myfont.render("score " + str(score), True, colors[(i+1) % 6])
    screen.blit(text, [370, 450])

    # change old screen with new
    pygame.display.flip()


def choose_dir(a):
    dirX, dirY = 0,0
    if a == pygame.K_RIGHT:
        dirX, dirY = 1, 0
    elif a == pygame.K_LEFT:
        dirX, dirY = -1, 0
    elif a == pygame.K_DOWN:
        dirX, dirY = 0, 1
    elif a == pygame.K_UP:
        dirX, dirY = 0, -1
    return [dirX, dirY]


def eat(snake):
    hungry = True
    while hungry:
        x = random.randrange(10)*50
        y = random.randrange(10)*50
        if [x, y] not in snake:
            food = pygame.Rect(x+5, y+5, 40, 40)
            hungry = False

    return food


def move(snake, hungry, directory, prev_directory):
    snake_head = [0, 0]

    if not hungry:
        snake.append(snake[-1].copy())
        snake.pop(0)
    else:
        snake.append(snake[-1].copy())

    snake_head[0] = snake[-1][0] + directory[0] * 50
    snake_head[1] = snake[-1][1] + directory[1] * 50
    if (snake_head[0] != snake[-3][0]) or (snake_head[1] != snake[-3][1]):
        snake[-1] = snake_head.copy()
    else:
        directory[0] = prev_directory[0]
        directory[1] = prev_directory[1]
        snake[-1][0] += prev_directory[0] * 50
        snake[-1][1] += prev_directory[1] * 50


def crash(snake):
    crashed = False

    if snake[-1][0] < 0 or snake[-1][0] > 450 or snake[-1][1] < 0 or snake[-1][1] > 450:
        crashed = True

    for elem in snake[:-1]:
        if (elem[0] == snake[-1][0]) and (elem[1] == snake[-1][1]):
            crashed = True

    return crashed


# def scoring(score):
#     file = shelve.open('score.txt')
#     highscore = file['score']
#     if highscore:
#         if highscore < score:
#             file['score'] = score
#     file.close()


def main():
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    score = 0

    while True:
        snake = [[50, 250], [100, 250], [150, 250], [200, 250]]
        directory = [0, 0]
        hungry = False
        i = 0
        init()
        food = pygame.Rect(0, 0, 0, 0)
        draw(init(), snake, food, i, score)
        score = 0
        food = eat(snake)
        interval = 0.25

        while True:
            time.sleep(interval)
            # delta = 0
            prev_directory = directory.copy()

            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    if choose_dir(event.key) != [0, 0]:
                        directory = choose_dir(event.key)

            if directory != [0, 0]:

                # wydłużenie, zjedzenie
                if food.x-5 == snake[-1][0] and food.y-5 == snake[-1][1]:
                    hungry = True
                    i = (i+1) % 6
                    pygame.mixer.Sound.play(eat_sound)
                    score += 1
                    if interval > 0.15:
                        interval -= 0.008

                move(snake, hungry, directory, prev_directory)
                if hungry:
                    food = eat(snake)
                    hungry = False
                draw(init(), snake, food, i, score)

                if crash(snake):
                    pygame.mixer.music.stop()
                    pygame.mixer.Sound.play(crash_sound)
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.2)

                    break


main()
