from DecisionMaking import decisionmaking
import pygame
from pygame.locals import *
import sys
import math

pygame.init()

# Screen
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Vision")
running = True
mode = ""


#Obstacle
class Obstacle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)

    def move(self, x, y):
        self.x += x
        self.y += y
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)


#End
class End:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def draw(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.r)


#Robot vision:
rbx = 500
rby = 500


def distance(obx, oby, rbx, rby):
    return math.sqrt(math.pow(obx-rbx, 2) + math.pow(oby-rby, 2))


def angle(obx, oby, rbx, rby):
    return math.atan2(math.fabs(rbx - obx), rby - oby)


draw = 0
t = 0.01
while running:
    screen.fill((255, 255, 255))

    pygame.draw.circle(screen, (0, 0, 0), (rbx, rby), 500, 2)
    pygame.draw.circle(screen, (0, 255, 0), (rbx, rby), 25)

    res_rect = pygame.draw.rect(screen, (0, 0, 0), (850, 0, 150, 75), 4)

    font = pygame.font.SysFont(None, 30)
    start_goal_rect = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 100, 50), 4)
    start_goal_text = font.render("Start", 1, (0, 0, 0))
    start_goal_text_rect = start_goal_text.get_rect(center=start_goal_rect.center)
    screen.blit(start_goal_text, start_goal_text_rect)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            if 0 <= mouse_x <= 100 and 0 <= mouse_y <= 50:
                draw = 5
            else:
                if event.button == 1:
                    if draw == 0:
                        obstacle1 = Obstacle(mouse_x, mouse_y, 10)
                        draw = 1
                    else:
                        obstacle2 = Obstacle(mouse_x, mouse_y, 10)
                        draw = 3
                if event.button == 3:
                    if draw == 1:
                        end1 = End(mouse_x, mouse_y, 5)
                        move_x1 = (end1.x - obstacle1.x)/4000
                        move_y1 = (end1.y - obstacle1.y)/4000
                        draw = 2
                    else:
                        end2 = End(mouse_x, mouse_y, 5)
                        move_x2 = (end2.x - obstacle2.x)/4000
                        move_y2 = (end2.y - obstacle2.y)/4000
                        draw = 4

    if draw == 1:
        obstacle1.draw()
    elif draw == 2:
        obstacle1.draw()
        end1.draw()
    elif draw == 3:
        obstacle1.draw()
        obstacle2.draw()
        end1.draw()
    elif draw == 4:
        obstacle1.draw()
        obstacle2.draw()
        end1.draw()
        end2.draw()
    elif draw == 5:
        end1.draw()
        end2.draw()
        obstacle1.move(move_x1, move_y1)
        obstacle2.move(move_x2, move_y2)
        if distance(obstacle1.x, obstacle1.y, end1.x, end1.y) < 2 and distance(obstacle2.x, obstacle2.y, end2.x, end2.y) < 2:
            draw = 4

    if draw == 5 and (distance(obstacle1.x, obstacle1.y, rbx, rby) <= 500 or distance(obstacle2.x, obstacle2.y, rbx, rby) <= 500):
        if distance(obstacle1.x, obstacle1.y, rbx, rby) <= 500:
            d1 = distance(obstacle1.x, obstacle1.y, rbx, rby)
            d_next1 = distance(obstacle1.x + move_x1, obstacle1.y + move_y1, rbx, rby)
            ang1 = angle(obstacle1.x, obstacle1.y, rbx, rby)/math.pi*180
            ang_next1 = angle(obstacle1.x + move_x1, obstacle1.y + move_y1, rbx, rby)/math.pi*180
            res1 = decisionmaking(ang1, ang_next1, d1, d_next1)

        else:
            res1 = "No"

        if distance(obstacle2.x, obstacle2.y, rbx, rby) <= 500:
            d2 = distance(obstacle2.x, obstacle2.y, rbx, rby)
            d_next2 = distance(obstacle2.x + move_x2, obstacle2.y + move_y2, rbx, rby)
            ang2 = angle(obstacle2.x, obstacle2.y, rbx, rby)/math.pi*180
            ang_next2 = angle(obstacle2.x + move_x2, obstacle2.y + move_y2, rbx, rby)/math.pi*180
            res2 = decisionmaking(ang2, ang_next2, d2, d_next2)
        else:
            res2 = "No"
        print(res1 + " " + res2)
        if res1 == "Replan" or res2 == "Replan":
            res = "Replan"
        elif res1 == "Stop" or res2 == "Stop":
            res = "Stop"
        else:
            res = "No"

        result = font.render(res, 1, (0, 0, 0))
        res_text_rect = result.get_rect(center=res_rect.center)
        screen.blit(result, res_text_rect)

    pygame.display.flip()