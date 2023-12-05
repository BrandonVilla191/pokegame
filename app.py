from enum import Enum
import textwrap
import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1000
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class GameState(Enum):
    HOME = 1
    MAIN = 2
    QUESTION = 3
    ANSWER = 4

player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 40, 40)
PLAYER_SPEED = 10
NPC_SIZE = (90, 90)
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 200
clock = pygame.time.Clock()

npcs = {
    "npc_left": {
        "rect": pygame.Rect(10, SCREEN_HEIGHT // 2, *NPC_SIZE),
        "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE),
        "question": ["What's better to ask", "the health chatbot?"], 
        "answer1": ["I am sick, please help"], 
        "answer2": ["Explain the diagnosis", "my doctor provided", "in terms I can understand."],
        "correct": "answer2",
        "reason": ["Incorrect! Providing a detailed", "query will help the chatbot", "help you."],
    },
    "npc_right": {
        "rect": pygame.Rect(SCREEN_WIDTH - 90, SCREEN_HEIGHT // 2, *NPC_SIZE),
        "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE),
        "question": ["In the context of interacting with", "an AI health chatbot, what is the", "significance of understanding the", "limitations and capabilities of the", "technology?"], 
        "answer1": ["No limitations, it can handle", "all queries."], 
        "answer2": ["Knowing the limitations helps", "set realistic expectations and", "improves user experience."],
        "correct": "answer2",
        "reason": ["Incorrect! AI healthcare chatbots", "have limitations just like any", "other AI technology."],
    },
    "npc_top": {
        "rect": pygame.Rect(SCREEN_WIDTH // 2, 10, *NPC_SIZE),
        "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE),
        "question": ["Why is it important to", "verify information recieved from", "an AI healthcare chatbot with", "a qualified healthcare professional?"], 
        "answer1": ["Because they may not have", "the ability to consider complex,", "individualized medical contexts."], 
        "answer2": ["Not necessary because they", "have access to the latest", "medical databases"],
        "correct": "answer1",
        "reason": ["Incorrect! Medical databases alone", "are not enough to consider the", "important context of the", "patient's medical history."]
    },
    "npc_bot": {
        "rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 90, *NPC_SIZE),
        "sprite": pygame.transform.scale(pygame.image.load('squirtle.png').convert_alpha(), NPC_SIZE),
        "question": ["How should you responsibly interact", "with a medical chatbot when seeking", "medical advice?"], 
        "answer1": ["Ask it to cure your illness."], 
        "answer2": ["Share some information about", "your condition and ask for", "advice treating symptoms."],
        "correct": "answer2",
        "reason": ["Incorrect! Chatbots are not", "capable of diagnosing and", "curing illnesses."]
    }
}

instructions_font = pygame.font.Font(None, 36)
instructions_text = [
    "Welcome to AI for Bedside Patient Assistance - the Game!",
    "Use the arrow keys to move your character to a NPC.",
    "The goal is to select the correct dialogue option",
    "for each NPC by pressing either A or B.",
    "Press ENTER to continue."
]

main_backgroundImage = pygame.image.load('background.jpg')
main_background = pygame.transform.scale(main_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
home_backgroundImage = pygame.image.load('back.jpg')
home_background = pygame.transform.scale(home_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
question_backgroundImage = pygame.image.load('question_background.png')
question_background = pygame.transform.scale(question_backgroundImage, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_state = GameState.HOME

# Calculate the center of the screen
screen_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

player_sprite = pygame.image.load('player_sprite2.png').convert_alpha()
player_sprite = pygame.transform.scale(player_sprite, (PLAYER_WIDTH, PLAYER_HEIGHT))
player = {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT), "sprite": player_sprite}


big_font = pygame.font.Font(None, 36)
medium_font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 25)
current_npc = None
current_response = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == GameState.HOME:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = GameState.MAIN
    
    keys = pygame.key.get_pressed()

    if game_state == GameState.ANSWER:
        screen.blit(question_background, (0, 0))
        for i, line in enumerate(current_response):
            text = medium_font.render(line, True, BLACK)
            screen.blit(text, (650, 75 + i * 40))

        screen.blit(big_font.render("Press ENTER to continue.", True, BLACK), (650, 300))
        if keys[pygame.K_RETURN]:
            game_state = GameState.MAIN
            player['rect'].update(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT)
    
    if game_state == GameState.HOME:
        screen.blit(home_background, (0, 0))
        for i, line in enumerate(instructions_text):
            text = instructions_font.render(line, True, BLACK)
            screen.blit(text, (50, 50 + 40 * i))
    
    elif game_state == GameState.QUESTION:
        screen.blit(question_background, (0, 0))
        
        if keys[pygame.K_a]:
            if current_npc["correct"] == "answer1":
                current_response = ["Correct!"]
            else:
                current_response = current_npc["reason"]
            game_state = GameState.ANSWER
        elif keys[pygame.K_b]:
            if current_npc["correct"] == "answer2":
                current_response = ["Correct!"]
            else:
                current_response = current_npc["reason"]
            game_state = GameState.ANSWER
        
        text_width = 150
        line_height = big_font.get_linesize()
        x = 650
        for i, line in enumerate(current_npc["question"]):
            text = small_font.render(line, True, BLACK)
            screen.blit(text, (x, 75 + i * line_height))

        for i, line in enumerate(current_npc["answer1"]):
            text = medium_font.render(line, True, BLACK)
            screen.blit(text, (x, 290 + i * line_height))

        for i, line in enumerate(current_npc["answer2"]):
            text = medium_font.render(line, True, BLACK)
            screen.blit(text, (x, 425 + i * line_height))
        


    elif game_state == GameState.MAIN:
        screen.blit(main_background, (0, 0))
        screen.blit(player["sprite"], player["rect"])
        
        if keys[pygame.K_LEFT] and player['rect'].left > 0:
            player['rect'].move_ip(-1 * PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] and player['rect'].right < SCREEN_WIDTH:
            player['rect'].move_ip(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] and player['rect'].top > 0:
            player['rect'].move_ip(0, -1 * PLAYER_SPEED)
        if keys[pygame.K_DOWN] and player['rect'].bottom < SCREEN_HEIGHT:
            player['rect'].move_ip(0, PLAYER_SPEED)

        for key, npc in npcs.items():
            if player["rect"].colliderect(npc["rect"]):
                
                player_mask = pygame.mask.from_surface(player["sprite"])
                npc_mask = pygame.mask.from_surface(npc["sprite"])

                offset_x = npc["rect"].x - player["rect"].x
                offset_y = npc["rect"].y - player["rect"].y

                if player_mask.overlap(npc_mask, (offset_x, offset_y)):
                    current_npc = npc
                    game_state = GameState.QUESTION
                    break
            else:
                current_npc = None


        for key, npc in npcs.items():
            screen.blit(npc["sprite"], npc["rect"])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()