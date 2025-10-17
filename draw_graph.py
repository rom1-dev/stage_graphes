"""
draw_graph.py - Module pour le dessin d'arêtes orientées ou non avec Pygame.
------
Ce module fournit des utilitaires simples pour dessiner des arêtes (lignes) entre deux
points dans une surface Pygame, avec prise en charge optionnelle de têtes de flèche
(simple ou double), d'un label centré, et d'offsets pour éviter les collisions avec
des nœuds circulaires. Il est conçu pour être utilisé dans des visualisations de graphes
ou d'algorithmes sur des graphes (parcours, flot, etc.).
# Dépendances
-----------
- pygame
- math
- enum (Enum)
API publique
------------
- ArrowType (Enum)
    Enumération décrivant le placement des têtes de flèche :
      * NONE   : aucune tête de flèche
      * SINGLE : tête unique sur le point d'arrivée
      * DOUBLE : têtes sur le point de départ et d'arrivée
- draw_line(surface, FONT, color, start_pos, end_pos, thickness=6,
            arrow_type=ArrowType.SINGLE, arrow_size=18,
            offset_start=0, offset_end=0,
            label=None, label_color=(0,0,0),
            label_offset_x=0, label_offset_y=0)
    Dessine une "arête" entre deux points avec options pour flèches et texte.
# draw_line — Paramètres détaillés
--------------------------------
- surface : pygame.Surface
    Surface Pygame sur laquelle dessiner.
- FONT : pygame.font.Font
    Police utilisée pour le rendu du label. Si None, aucun label n'est dessiné.
- color : tuple[int, int, int]
    Couleur (R, G, B) utilisée pour la tige et les têtes de flèche.
- start_pos : tuple[float, float]
    Coordonnées (x, y) du point de départ.
- end_pos : tuple[float, float]
    Coordonnées (x, y) du point d'arrivée.
- thickness : int, optionnel (défaut 6)
    Épaisseur en pixels de la tige (ligne). La fonction évite de dessiner si la tige
    calculée devient trop courte (inférieure à thickness).
- arrow_type : ArrowType, optionnel (défaut ArrowType.SINGLE)
    Type de flèches à dessiner : NONE, SINGLE ou DOUBLE.
- arrow_size : int, optionnel (défaut 18)
    Taille approximative (longueur) des têtes de flèche en pixels. Les têtes sont
    dessinées comme des triangles centrés sur les points finaux.
- offset_start, offset_end : int, optionnel (défaut 0)
    Décalages le long de la direction de l'arête à appliquer respectivement au départ
    et à l'arrivée. Utiles pour que la tige ne recouvre pas les cercles représentant
    les nœuds (par exemple rayon du nœud).
- label : str | None, optionnel
    Texte à afficher centré sur la tige. Si None, aucun texte n'est rendu.
- label_color : tuple[int, int, int], optionnel (défaut (0, 0, 0))
    Couleur du texte du label (R, G, B).
- label_offset_x, label_offset_y : int, optionnel (défaut 0)
    Décalages en pixels appliqués à la position du label (horizontal, vertical).
# Comportement et remarques
-------------------------
- Les offsets sont appliqués à l'extrémité de la tige pour éviter que la ligne ne touche
  directement les formes représentant les nœuds. Si des têtes de flèche sont demandées,
  la tige s'arrête avant la pointe de la flèche (en tenant compte d'une marge relative
  à arrow_size) pour que la flèche ne chevauche pas la tige.
- Si la distance entre start_pos et end_pos est nulle (même point), la fonction
  retourne sans rien dessiner.
- La fonction vérifie également que la tige résultante ait une longueur suffisante
  (supérieure à thickness) avant le dessin, pour éviter des artefacts visuels.
- Les têtes de flèche sont dessinées comme des polygones triangulaires simples. Leur
  orientation est calculée à partir de l'angle de la ligne. Pour une tête au départ,
  l'angle est inversé (angle + pi).
- Le label est rendu via FONT.render et centré sur la tige entre line_start et line_end,
  puis décalé via label_offset_x / label_offset_y et blitté sur la surface.
Exemples d'utilisation
----------------------
- Dessiner une arête orientée simple :
    draw_line(screen, FONT, (0,0,0), (50,50), (150,150))
- Arête verticale avec flèches aux deux extrémités et label :
    draw_line(screen, FONT, (255,0,0), (200,50), (200,250),
              arrow_type=ArrowType.DOUBLE, label="A-B", arrow_size=16,
              offset_start=10, offset_end=10)
- Ligne sans flèche et label décalé vers le haut :
    draw_line(screen, FONT, (0,0,255), (300,50), (300,250),
              arrow_type=ArrowType.NONE, label="No Arrow", label_offset_y=-10)
# Compatibilité et bonnes pratiques
---------------------------------
- Conserver une police (FONT) initialisée via pygame.font.Font ou pygame.font.SysFont
  avant d'appeler draw_line si l'on souhaite afficher un label.
- Veiller à appeler pygame.init() et pygame.font.init() au préalable dans l'application
  et à mettre à jour l'affichage avec pygame.display.flip() ou pygame.display.update()
  après les opérations de dessin.
- Adapter offset_start / offset_end aux rayons des nœuds (ou autres formes) pour
  garantir une apparence nette et éviter les chevauchements.
# Licence et attribution
----------------------
Ce module est fourni sans garantie explicite. Peut être modifié pour répondre aux besoins
spécifiques d'une application de visualisation de graphes.
"""

import pygame, math
from enum import Enum

class ArrowType(Enum):
    """Énumération définissant le placement des têtes de flèche pour les arêtes du graphe.

    Valeurs:
        NONE (int): Aucune tête de flèche n'est dessinée pour l'arête.
        SINGLE (int): Une seule tête de flèche est dessinée à la position d'arrivée de l'arête.
        DOUBLE (int): Des têtes de flèche sont dessinées aux positions de départ et d'arrivée.

    Cette énumération est utilisée par les routines de dessin et de mise en page pour déterminer
    comment afficher les indicateurs de direction sur les arêtes (par exemple dans les graphes
    orientés ou lors de la visualisation de flux). Chaque membre possède une valeur entière et
    peut être utilisé dans la logique conditionnelle pour sélectionner le comportement de rendu
    approprié.
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
    # final_point_end est basé sur end_pos et offset_end
    # final_point_start est basé sur start_pos et offset_start
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