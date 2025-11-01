import pygame, math
import draw_graph as dg

# couleur cercle centre : #99CCFF
# couleur cercle exterieur : #FF6633
# couleur lignes : #00CCCC
COULEUR_CERCLE_CENTRE = (153, 204, 255)
COULEUR_CERCLE_EXTERIEUR = (255, 102, 51)
COULEUR_LIGNES = (0, 204, 204)

CIRCLE_SIZE = 15
WIDTH = 5

# def draw_line(surface, color, start_pos, end_pos, name=None, width=1, oriented=False):
    
#     if oriented:
#         v = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
#         l = (v[0]**2 + v[1]**2)**0.5
#         u = (v[0]/l, v[1]/l) if l != 0 else (0, 0)
#         pfin = (end_pos[0]-CIRCLE_SIZE*(end_pos[0]-start_pos[0])/l, end_pos[1]-CIRCLE_SIZE*(end_pos[1]-start_pos[1])/l)
#         pendline = (pfin[0]-u[0]*5, pfin[1]-u[1]*5)
#         v_angle = math.atan2(v[1], v[0])
#         angle1 = v_angle + math.radians(150)
#         angle2 = v_angle - math.radians(150)
#         p1 = (pfin[0] + 15*math.cos(angle1), pfin[1] + 15*math.sin(angle1))
#         p2 = (pfin[0] + 15*math.cos(angle2), pfin[1] + 15*math.sin(angle2))
#         pygame.draw.polygon(surface, color, [pfin, p1, p2])
#         pygame.draw.line(surface, color, start_pos, pendline, width)
#     else:
#         pygame.draw.line(surface, color, start_pos, end_pos, width)
#     if name is not None:
#         font = pygame.font.Font(None, 24)
#         text = font.render(str(name), True, (0, 0, 0))
#         text_rect = text.get_rect(center=((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2))
#         surface.blit(text, text_rect)



pygame.init()
FONT = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((400, 300), pygame.RESIZABLE)
pygame.display.set_caption('Graphes')
horloge = pygame.time.Clock()
FPS = 60
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
    screen.fill((255, 255, 255))
    pos1 = (screen.get_width() // 4, screen.get_height() // 4)
    pos2 = (screen.get_width() // 2, 1.5*screen.get_height() // 2)
    pos3 = (3 * screen.get_width() // 4, screen.get_height() // 4)
    dg.draw_circle(screen, FONT, COULEUR_CERCLE_EXTERIEUR, COULEUR_CERCLE_CENTRE, pos1, CIRCLE_SIZE, 1)
    dg.draw_circle(screen, FONT, COULEUR_CERCLE_EXTERIEUR, COULEUR_CERCLE_CENTRE, pos2, CIRCLE_SIZE, 2)
    dg.draw_circle(screen, FONT, COULEUR_CERCLE_EXTERIEUR, COULEUR_CERCLE_CENTRE, pos3, CIRCLE_SIZE, 3)
    dg.draw_line(screen, FONT, COULEUR_LIGNES, pos1, pos2, label="1-2", offset_end=CIRCLE_SIZE, offset_start=CIRCLE_SIZE)
    dg.draw_line(screen, FONT, COULEUR_LIGNES, pos2, pos3, label="2-3", offset_end=CIRCLE_SIZE, offset_start=CIRCLE_SIZE)
    dg.draw_line(screen, FONT, COULEUR_LIGNES, pos3, pos1, label="3-1", offset_end=CIRCLE_SIZE, offset_start=CIRCLE_SIZE)
    pygame.display.flip()
    horloge.tick(FPS)
pygame.quit()