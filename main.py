import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 500, 700

MAIN_FONT = pygame.font.SysFont('comicsans', 30)
WIN = pygame.display.set_mode((WIDTH, HEIGHT,))

FPS = 10
WHITE = (255, 255, 255)
BACKGROUND = (192, 192, 192)
TRADECENTER = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'tradecenter.jpg')), (WIDTH, 200))
PLANE = pygame.image.load(os.path.join('assets', 'b1.gif'))
TURRET = pygame.image.load(os.path.join('assets', 'torreta.gif'))
BULLET = pygame.image.load(os.path.join('assets', 'balota.gif'))
EXPLOSION = pygame.image.load(os.path.join('assets', 'explosion.gif'))
VEL = 40
PLANE_VEL_X = 30
PLANE_VEL_Y = 20
PLANE_HIT_WTC = pygame.USEREVENT + 1
BULLET_HIT_PLANE = pygame.USEREVENT + 2
RED = (255, 0, 0)
MAX_BULLETS = 2
LOSE_IMAGE = pygame.image.load(os.path.join('assets', 'binladen-win.gif'))
WIN_IMAGE = pygame.image.load(os.path.join('assets', 'binladen-lose.gif'))


def draw_window(plane, wtc, bullets_left, bullets_right):
    WIN.fill(BACKGROUND)
    WIN.blit(TRADECENTER, (wtc.x, wtc.y))
    WIN.blit(PLANE,  (plane.x, plane.y))
    WIN.blit(TURRET, (139, HEIGHT - TRADECENTER.get_height() -
             TURRET.get_height() + 10))
    WIN.blit(TURRET, (332, HEIGHT - TRADECENTER.get_height() -
             TURRET.get_height() + 10))
    for bullet in bullets_left:
        WIN.blit(BULLET, (bullet.x, bullet.y))
    for bullet in bullets_right:
        WIN.blit(BULLET, (bullet.x, bullet.y))
    pygame.display.update()


def handle_colisions(plane, wtc):
    if plane.colliderect(wtc):
        pygame.event.post(pygame.event.Event(PLANE_HIT_WTC))


def print_message(win):
    if win:
        message = "GANASTE!!!"
        WIN.blit(WIN_IMAGE, (WIDTH/2 - WIN_IMAGE.get_width() /
                 2, HEIGHT/2 - WIN_IMAGE.get_height()//2))
    else:
        message = "PERDISTE!!!"
        WIN.blit(LOSE_IMAGE, (WIDTH/2 - LOSE_IMAGE.get_width() //
                 2, HEIGHT/2 - LOSE_IMAGE.get_height()//2))
    display_message = MAIN_FONT.render(message, True, RED)
    WIN.blit(display_message, (WIDTH/2 - display_message.get_width() /
             2, HEIGHT/2 - display_message.get_height()/2))
    pygame.display.update()


def move_plane(plane: pygame.Rect, lr):
    plane.y += PLANE_VEL_Y
    if plane.x <= 0:
        lr = True
    elif (plane.x + plane.width) >= WIDTH:
        lr = False

    if lr:
        plane.x += PLANE_VEL_X
    else:
        plane.x -= PLANE_VEL_X

    return lr


def handle_bullets(plane: pygame.Rect, bullets_left, bullets_right):
    for bullet in bullets_left:
        bullet.y -= VEL
        if bullet.y <= 0:
            bullets_left.remove(bullet)
        if plane.colliderect(bullet):
            bullets_left.remove(bullet)
            pygame.event.post(pygame.event.Event(BULLET_HIT_PLANE))

    for bullet in bullets_right:
        bullet.y -= VEL
        if bullet.y <= 0:
            bullets_right.remove(bullet)
        if plane.colliderect(bullet):
            bullets_right.remove(bullet)
            pygame.event.post(pygame.event.Event(BULLET_HIT_PLANE))


def main():
    run = True
    clock = pygame.time.Clock()
    plane = pygame.Rect(0 + WIDTH/2 - PLANE.get_width()/2,
                        0, PLANE.get_width(), PLANE.get_height())
    wtc = pygame.Rect(0, HEIGHT - TRADECENTER.get_height(),
                      TRADECENTER.get_width(), TRADECENTER.get_height())
    bullets_left = list()
    bullets_right = list()
    lr = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(bullets_left) < MAX_BULLETS:
                    bullet = pygame.Rect(139, HEIGHT - TRADECENTER.get_height(
                    ) - TURRET.get_height() + 10, BULLET.get_width(), BULLET.get_height())
                    bullets_left.append(bullet)
                if event.key == pygame.K_RSHIFT and len(bullets_right) < MAX_BULLETS:
                    bullet = pygame.Rect(332, HEIGHT - TRADECENTER.get_height(
                    ) - TURRET.get_height() + 10, BULLET.get_width(), BULLET.get_height())
                    bullets_right.append(bullet)
            if event.type == PLANE_HIT_WTC:
                print_message(False)
                pygame.time.delay(2000)
                main()
            if event.type == BULLET_HIT_PLANE:
                WIN.blit(EXPLOSION, (plane.x + (plane.width / 4),
                         plane.y + plane.height/4))
                print_message(True)
                pygame.time.delay(2000)
                main()

        lr = move_plane(plane, lr)
        handle_bullets(plane, bullets_left, bullets_right)
        handle_colisions(plane, wtc)
        draw_window(plane, wtc, bullets_left, bullets_right)

    pygame.quit()


if __name__ == '__main__':
    main()
