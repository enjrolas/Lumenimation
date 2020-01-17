import pygame
import sys
pygame.init()

def blit_alpha(dest, source, pos, opacity):
    """Hack: blit per-pixel alpha source onto dest with surface opacity."""
    # http://www.nerdparadise.com/tech/python/pygame/blitopacity/
    (x, y) = pos
    temp = pygame.Surface((source.get_width(),
                           source.get_height())).convert()
    temp.blit(dest, (-x, -y))
    temp.blit(source, (0, 0))
    temp.set_alpha(opacity)
    dest.blit(temp, pos)

def color_mask(surface, color):
    if isinstance(color, kurt.Color):
        color = color.value
    surface = surface.convert()
    surface.set_colorkey(color)
    color_mask = pygame.mask.from_surface(surface)
    color_mask.invert()
    return color_mask


screen = pygame.display.set_mode((1920,1080),0)
mask=pygame.image.load("simpleMask.png)"
frame=pygame.image.load("frame.jpg")
mask = pygame.transform.scale(mask,(400,300))
mask.set_colorkey([255,255,255])
copy=frame
copy.blit(mask,(0,0))
copy.set_colorkey([0,0,0])
frame = pygame.transform.scale(frame,(400,300))
surf=pygame.Surface((400,300))
surf.blit(frame, (0,0))
blit_alpha(surf, frame,(0,0), 0)
#blit_alpha(surf, mask,(0,0), 0)

while True:
    screen.fill([0,0,0])
    screen.blit(mask,(0,0)) 
    screen.blit(frame,(0,300))
    screen.blit(surf,(400,0))
    screen.blit(copy,(400,300))
    pygame.display.update()    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
