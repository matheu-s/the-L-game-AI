import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/images/background.png")


def get_font(size):
    return pygame.font.Font("assets/fonts/menu.otf", size)

def play():
    while True:
        POS_MOUSE = pygame.mouse.get_pos()
        SCREEN.fill("black")

        BTN_PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "White")
        BTN_PLAY_RECT = BTN_PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(BTN_PLAY_TEXT, BTN_PLAY_RECT)

        BTN_PLAY_BACK = Button(image=None, pos=(640, 460),
                            text_input="BACK", font=get_font(75), base_color="White", hovering_color="Green")

        BTN_PLAY_BACK.changeColor(POS_MOUSE)
        BTN_PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_PLAY_BACK.checkForInput(POS_MOUSE):
                    main_menu()

        pygame.display.update()
    
def options():
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("black")

        BTN_OPTIONS_TEXT = get_font(50).render("This is the OPTIONS screen.", True, "White")
        BTN_OPTIONS_RECT = BTN_OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(BTN_OPTIONS_TEXT, BTN_OPTIONS_RECT)

        BTN_OPTIONS_BACK = Button(image=None, pos=(640, 470),
                            text_input="BACK", font=get_font(80), base_color="White", hovering_color="Green")

        BTN_OPTIONS_BACK.changeColor(MOUSE_POS)
        BTN_OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BTN_OPTIONS_BACK.checkForInput(MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.fill("black")
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/images/play.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/images/options.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/images/quit.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()