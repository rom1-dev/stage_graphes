import pygame, math
from enum import Enum

class ArrowType(Enum):
    """
    Types de flèches pour les lignes.
    """
    NONE = 0
    SINGLE = 1  # Flèche sur end_pos
    DOUBLE = 2  # Flèche sur start_pos et end_pos

def draw_line(surface:pygame.Surface, FONT:pygame.font.Font, color:tuple, 
                    start_pos:tuple, end_pos:tuple, thickness:int=6,
                    arrow_type:ArrowType=ArrowType.SINGLE, arrow_size:int=18,
                    offset_start:int=0, offset_end:int=0,
                    label:str=None, label_color:tuple=(0, 0, 0),
                    label_offset_x:int=0, label_offset_y:int=0) -> None:
    """
    Dessine une ligne entre deux points avec éventuellement des flèches et un label.

    Args:
        surface (pygame.Surface): Surface sur laquelle dessiner la ligne.
        FONT (pygame.font.Font): Police utilisée pour le label.
        color (tuple): Couleur de la ligne et des flèches (R, G, B).
        start_pos (tuple): Coordonnées (x, y) du point de départ.
        end_pos (tuple): Coordonnées (x, y) du point d'arrivée.
        thickness (int, optional): Épaisseur de la ligne. Défaut 6.
        arrow_type (ArrowType, optional): Type de flèche (aucune, simple, double). Défaut ArrowType.SINGLE.
        arrow_size (int, optional): Taille des têtes de flèche. Défaut 18.
        offset_start (int, optional): Décalage depuis le point de départ. Défaut 0.
        offset_end (int, optional): Décalage depuis le point d'arrivée. Défaut 0.
        label (str, optional): Texte à afficher au centre de la ligne. Défaut None.
        label_color (tuple, optional): Couleur du texte du label (R, G, B). Défaut (0, 0, 0).
        label_offset_x (int, optional): Décalage horizontal du label. Défaut 0.
        label_offset_y (int, optional): Décalage vertical du label. Défaut 0.
    
    Returns:
        None

    Note:
        - Les offsets permettent d'éviter que la ligne ne touche les cercles aux extrémités.
        - Les flèches sont dessinées en utilisant des polygones triangulaires.
        - Le label est centré sur la ligne, avec des options de décalage.
    
    Examples:
        >>> draw_line(screen, FONT, (0, 0, 0), (50, 50), (150, 150))
        >>> draw_line(screen, FONT, (255, 0, 0), (200, 50), (200, 250), arrow_type=ArrowType.DOUBLE, label="A-B")
        >>> draw_line(screen, FONT, (0, 0, 255), (300, 50), (300, 250), arrow_type=ArrowType.NONE, label="No Arrow", label_offset_y=-10)
    """

    # 1. Calculs des points et application des offsets
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    length = math.hypot(dx, dy)

    if length == 0: 
        return

    # Vecteur unitaire (direction de la ligne)
    unit_vx, unit_vy = dx / length, dy / length
    
    # Points où la POINTE de la flèche (ou la fin de la ligne) doit se trouver
    # Ces points sont basés sur les offsets fournis.
    final_point_end = (
        end_pos[0] - unit_vx * offset_end,
        end_pos[1] - unit_vy * offset_end
    )
    final_point_start = (
        start_pos[0] + unit_vx * offset_start,
        start_pos[1] + unit_vy * offset_start
    )
    
    # 2. Détermination des points de fin de la TIGE de la ligne
    
    # Si une flèche est présente, la tige doit s'arrêter AVANT le final_point.
    # On ajoute donc arrow_size*0.8 à l'offset (pour éviter que la ligne soit trop courte).
    
    offset_line_end = offset_end
    if arrow_type == ArrowType.SINGLE or arrow_type == ArrowType.DOUBLE:
        offset_line_end += arrow_size*0.8
        
    offset_line_start = offset_start
    if arrow_type == ArrowType.DOUBLE:
        offset_line_start += arrow_size*0.8

    # Points d'extrémité de la tige
    line_start = (
        start_pos[0] + unit_vx * offset_line_start,
        start_pos[1] + unit_vy * offset_line_start
    )
    line_end = (
        end_pos[0] - unit_vx * offset_line_end,
        end_pos[1] - unit_vy * offset_line_end
    )
    
    # Vérification de la longueur après décalage
    new_length = math.hypot(line_end[0] - line_start[0], line_end[1] - line_start[1])
    if new_length < thickness: 
        return

    # 3. Dessin de la tige
    pygame.draw.line(surface, color, line_start, line_end, thickness)

    # 4. Fonction auxiliaire pour dessiner une tête de flèche
    def draw_arrow_head(pos, angle_rad, size):
        point1 = (
            pos[0] - size * math.cos(angle_rad - math.pi / 6),
            pos[1] - size * math.sin(angle_rad - math.pi / 6)
        )
        point2 = (
            pos[0] - size * math.cos(angle_rad + math.pi / 6),
            pos[1] - size * math.sin(angle_rad + math.pi / 6)
        )
        pygame.draw.polygon(surface, color, [pos, point1, point2])

    # Angle de la ligne
    angle = math.atan2(unit_vy, unit_vx)

    # 5. Dessin des têtes de flèche
    if arrow_type == ArrowType.SINGLE or arrow_type == ArrowType.DOUBLE:
        # Tête sur le point d'arrivée (final_point_end)
        draw_arrow_head(final_point_end, angle, arrow_size)

    if arrow_type == ArrowType.DOUBLE:
        # Tête sur le point de départ (final_point_start)
        # Angle inversé (angle + pi)
        draw_arrow_head(final_point_start, angle + math.pi, arrow_size)
        
    # 6. Dessin du Nom
    if label and FONT:
        try:
            label = str(label)
        except Exception:
            label = "?"
        # Le centre est calculé sur la tige de la ligne
        center_x = (line_start[0] + line_end[0]) / 2
        center_y = (line_start[1] + line_end[1]) / 2
        
        text_surface = FONT.render(label, True, label_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (int(center_x) + label_offset_x, int(center_y) + label_offset_y)
        
        surface.blit(text_surface, text_rect)