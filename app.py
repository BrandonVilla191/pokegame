from enum import Enum
import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1000
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class GameState(Enum):
    HOME = 1
    MAIN = 2
    QUESTION = 3

player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 40, 40)
PLAYER_SPEED = 10
NPC_SIZE = (60, 60)
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 90
clock = pygame.time.Clock()

npc_dialogues = {
    "npc1": ["hi what's your name", "aditya", "adithya"],
    "npc2": ["hi what's your name", "yo", "rishabh"],
    "npc3": ["hi what's your name", "brandon", "cida"],
    "npc4": ["hi what's your name", "kingboo", "kekw"]
}

instructions_font = pygame.font.Font(None, 36)
instructions_text = [
    "Welcome to [name of game]!",
    "Use the arrow keys to move your character.",
    "The goal is to select the correct dialogue option for each NPC.",
    "Press ENTER to continue."
]

main_backgroundImage = pygame.image.load('background.jpg')
main_background = pygame.transform.scale(main_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
home_backgroundImage = pygame.image.load('back.jpg') ## TODO: CHANGE THIS TO A DIFFERENT PICTURE (or different for the actual game)
home_background = pygame.transform.scale(home_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
question_backgroundImage = pygame.image.load('question_background.png')
question_background = pygame.transform.scale(question_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = GameState.HOME

# Calculate the center of the screen
screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

player_sprite = pygame.image.load('sprite.png').convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT), "sprite": player_sprite}


npcs = [
    {"rect": pygame.Rect(10, SCREEN_HEIGHT // 2, *NPC_SIZE), "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE)},
    {"rect": pygame.Rect(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2, *NPC_SIZE), "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE)},
    {"rect": pygame.Rect(SCREEN_WIDTH // 2, 10, *NPC_SIZE), "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE)},
    {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 70, *NPC_SIZE), "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE)},
]


font = pygame.font.Font(None, 36)
current_dialogue = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == GameState.HOME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = GameState.MAIN


    
    if game_state == GameState.HOME:
        screen.blit(home_background, (0, 0))
        for i, line in enumerate(instructions_text):
            text = instructions_font.render(line, True, BLACK)
            screen.blit(text, (50, 50 + 40 * i))
    
    elif game_state == GameState.QUESTION:
        screen.blit(question_background, (0, 0))
        question = font.render(current_dialogue[0], True, (0, 0, 0))
        answer1 = font.render(current_dialogue[1], True, (0, 0, 0))
        answer2 = font.render(current_dialogue[2], True, (0, 0, 0))
        screen.blit(question, (650, 75))
        screen.blit(answer1, (650, 300))
        screen.blit(answer2, (650, 425))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            print("pressed a")
            game_state = GameState.MAIN
            player['rect'].update(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
        elif keys[pygame.K_b]:
            print("pressed b")
            game_state = GameState.MAIN
            player['rect'].update(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)


    elif game_state == GameState.MAIN:
        screen.blit(main_background, (0, 0))
        screen.blit(player["sprite"], player["rect"])
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player['rect'].left > 0:
            player['rect'].move_ip(-1 * PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and player['rect'].right < SCREEN_WIDTH:
            player['rect'].move_ip(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] and player['rect'].top > 0:
            player['rect'].move_ip(0, -1 * PLAYER_SPEED)
        if keys[pygame.K_DOWN] and player['rect'].bottom < SCREEN_HEIGHT:
            player['rect'].move_ip(0, PLAYER_SPEED)

        for i, npc in enumerate(npcs):
            if player["rect"].colliderect(npc["rect"]):
                
                player_mask = pygame.mask.from_surface(player["sprite"])
                npc_mask = pygame.mask.from_surface(npc["sprite"])

                offset_x = npc["rect"].x - player["rect"].x
                offset_y = npc["rect"].y - player["rect"].y

                if player_mask.overlap(npc_mask, (offset_x, offset_y)):
                    current_dialogue = npc_dialogues[f'npc{i+1}']
                    game_state = GameState.QUESTION
                    break
            else:
                current_dialogue = None


        for i, npc in enumerate(npcs):
            screen.blit(npc["sprite"], npc["rect"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()