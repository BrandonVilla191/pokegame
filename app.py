import pygame

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

player = pygame.Rect(screen_width // 2, screen_height // 2, 40, 40)
player_speed = .8
npc_colors = ['red', 'blue', 'green', 'yellow']
npc_dialogues = {
    "npc1": "bruh",
    "npc2": "go away ",
    "npc3": "lmaoo",
    "npc4": "Hi"
}

background = pygame.image.load('background.jpg')


npcs = [
    pygame.Rect(10, screen_height // 2, 30, 30),
    pygame.Rect(screen_width - 40, screen_height // 2, 30, 30),
    pygame.Rect(screen_width // 2, 10, 30, 30),
    pygame.Rect(screen_width // 2, screen_height - 40, 30, 30),
]

font = pygame.font.Font(None, 36)
current_dialogue = None

running = True
while running:
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= player_speed
        if player.y < 0:
            player.y = 0
    if keys[pygame.K_s]:
        player.y += player_speed
        if player.y > screen_height - player.height: 
            player.y = screen_height - player.height
    if keys[pygame.K_a]:
        player.x -= player_speed
        if player.x < 0:
            player.x = 0
    if keys[pygame.K_d]:
        player.x += player_speed
        if player.x > screen_width - player.width: 
            player.x = screen_width - player.width 

    for i, npc in enumerate(npcs):
        if player.colliderect(npc):
            current_dialogue = npc_dialogues[f'npc{i+1}']
            break
    else:
        current_dialogue = None


    pygame.draw.rect(screen, 'blue', player)
    for i, npc in enumerate(npcs):
        pygame.draw.rect(screen, npc_colors[i], npc)

    if current_dialogue:
        text = font.render(current_dialogue, True, (0, 0, 0))
        screen.blit(text, (20, 20))

    pygame.display.flip()

pygame.quit()