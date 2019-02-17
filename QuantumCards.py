import pygame as pg
import random
#import QuantumEngine as qe

pg.init()
pg.display.set_caption('Quantum Cards')
pg.display.set_icon(pg.image.load('Icon.png'))
screen = pg.display.set_mode((1280, 720))
COLOR_INACTIVE = pg.Color('white')
COLOR_ACTIVE = pg.Color(211, 219, 221)
COLOR_TEXT = pg.Color(90, 120, 142)
COLOR_BLACK = pg.Color('black')
FONT = pg.font.Font("Font/Calibri.ttf", 32)
FONT_BOLD = pg.font.Font("Font/Calibrib.ttf", 26)
BG = pg.image.load("GameUI/BG.png")
BG_RECT = BG.get_rect()
BUTTON = pg.image.load("Button.png")
BUTTON_HOVER = pg.image.load("ButtonHover.png")
BUTTON_PRESSED = pg.image.load("ButtonPressed.png")
CORRECT_STRING = pg.image.load("GameUI/correct.png")
NOT_CORRECT_STRING = pg.image.load("GameUI/notcorrect.png")
GAME1_RECT = pg.Rect(1174, 288, 38, 39)
GAME2_RECT = pg.Rect(1174, 390, 38, 39)
GAME3_RECT = pg.Rect(1174, 490, 38, 39)
SPEECH_BUBBLE = pg.image.load("GameUI/Speachboubble.png")
SPEECH_BUBBLE_RECT = pg.Rect(692, 40, 240, 82)
SPEECH_BUBBLE_TEXT_RECT = pg.Rect(717, 70, 240, 82)
number_of_players=3
starting_player = 1
buttons_players=[]
pg.mixer.music.load('Audio/Music.ogg')
pg.mixer.music.play(-1)
BUTTON_SOUNDS = [pg.mixer.Sound('Audio/ButtonSound1.ogg'), pg.mixer.Sound('Audio/ButtonSound2.ogg'), pg.mixer.Sound('Audio/ButtonSound3.ogg')]
ui_state=0  #0=game, 1=score, 2=help
run_score=0 #0=none, 1=simulation, 2=simulation with noise, 3=quantum computer
check_strings=False
phase1_score = []
phase2_score = []
phase3_score = []

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text_color = COLOR_TEXT
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False

        if event.type == pg.KEYDOWN:
            global check_strings
            check_strings = True
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = not self.active
                elif event.key == pg.K_DELETE:
                    self.text = ""
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode.upper()
                self.txt_surface = FONT.render(self.text, True, self.text_color)
                
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def update(self):
        width = max(900, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)
        
    def get_text(self):
        return self.text

class ButtonBox:
    global BUTTON_SOUNDS

    def __init__(self, x, y, w, h, img_not_pressed, img_hover, img_pressed, toggle, button_event):
        self.rect = pg.Rect(x, y, w, h)
        self.not_pressed = img_not_pressed
        self.img_hover = img_hover
        self.img_pressed = img_pressed
        self.button_event = button_event
        self.toggle = toggle
        self.pressed = False

    def press_event(self):
        self.button_event()
        if(self.toggle):
            self.pressed = not self.pressed;

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.button_event()
                BUTTON_SOUNDS[random.randint(0, 2)].play()
                if(self.toggle):
                    self.pressed = not self.pressed

    def reset(self):
        self.pressed = False;

    def draw(self, screen):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if pg.mouse.get_pressed()[0]:
                screen.blit(self.img_pressed, self.rect)
            else:
                screen.blit(self.img_hover, self.rect)
        elif self.pressed:
            screen.blit(self.img_pressed, self.rect)
        else:
            screen.blit(self.not_pressed, self.rect)

def SetPlayerToTwo():
    global buttons_players, number_of_players
    print('Set player number to two')
    for button in buttons_players:
        button.reset()
    number_of_players=2;
    GetStartingPlayer()
            
def SetPlayerToThree():
    global buttons_players, number_of_players
    print('Set player number to three')
    for button in buttons_players:
        button.reset()
    number_of_players=3;
    GetStartingPlayer()
    
def SetPlayerToFour():
    global buttons_players, number_of_players
    print('Set player number to four')
    for button in buttons_players:
        button.reset()
    number_of_players=4;
    GetStartingPlayer()
    
def SetPlayerToFive():
    global buttons_players, number_of_players
    print('Set player number to five')
    for button in buttons_players:
        button.reset()
    number_of_players=5;
    GetStartingPlayer()
    
def GetStartingPlayer():
    global starting_player
    starting_player = random.randint(1, number_of_players)

def Simulate():
    global run_score
    print('Simulate result')
    ShowScore()
    run_score=1

def SimulateWithNoise():
    global run_score
    print('Simulate result with noise')
    ShowScore()
    run_score=2

def Calculate():
    global run_score
    print('Calculate result with quantum computer')
    ShowScore()
    run_score=3

def ShowGame():
    global ui_state
    ui_state=0
    print('Show game ui')

def ShowScore():
    global ui_state
    ui_state=1
    print('Show score ui')

def ShowHelp():
    global ui_state
    ui_state=2
    print('Show help ui')
    
def ToggleMusic():
    if pg.mixer.music.get_volume() > 0:
        pg.mixer.music.set_volume(0)
    else:
        pg.mixer.music.set_volume(1)
        
def main():
    global run_score, starting_player, check_strings
    clock = pg.time.Clock()
    
    game1 = InputBox(250, 292, 1000, 32)
    game2 = InputBox(250, 394, 1000, 32)
    game3 = InputBox(250, 496, 1000, 32)
    input_boxes = [game1, game2, game3]
    
    button_two_p = ButtonBox(62,57,110,27, pg.image.load("GameUI/2players.png"), pg.image.load("GameUI/2players_hover.png"), pg.image.load("GameUI/2players_select.png"), True, SetPlayerToTwo)
    button_three_p = ButtonBox(210,57,110,27, pg.image.load("GameUI/3players.png"), pg.image.load("GameUI/3players_hover.png"), pg.image.load("GameUI/3players_select.png"), True, SetPlayerToThree)
    button_four_p = ButtonBox(358,57,110,27, pg.image.load("GameUI/4players.png"), pg.image.load("GameUI/4players_hover.png"), pg.image.load("GameUI/4players_select.png"), True, SetPlayerToFour)
    button_five_p = ButtonBox(514,57,110,27, pg.image.load("GameUI/5player.png"), pg.image.load("GameUI/5player_hover.png"), pg.image.load("GameUI/5player_select.png"), True, SetPlayerToFive)
    button_random_p = ButtonBox(950,40,71,72, pg.image.load("GameUI/dice.png"), pg.image.load("GameUI/dice_hover.png"), pg.image.load("GameUI/dice.png"), False, GetStartingPlayer)
    button_simulate = ButtonBox(70,591,228,92, pg.image.load("GameUI/simulate.png"), pg.image.load("GameUI/simulate_hover.png"), pg.image.load("GameUI/simulate.png"), False, Simulate)
    button_simulate_noisy = ButtonBox(385,591,448,93, pg.image.load("GameUI/simulatewithnoise.png"), pg.image.load("GameUI/simulatewithnoise_hover.png"), pg.image.load("GameUI/simulatewithnoise.png"), False, SimulateWithNoise)
    button_calculate = ButtonBox(915,591,292,92, pg.image.load("GameUI/goquantum.png"), pg.image.load("GameUI/goquantum_hover.png"), pg.image.load("GameUI/goquantum.png"), False, Calculate)
    button_help = ButtonBox(1143,40,71,72, pg.image.load("GameUI/help.png"), pg.image.load("GameUI/help_hover.png"), pg.image.load("GameUI/help.png"), False, ShowHelp)
    button_mute = ButtonBox(1048,40,71,72, pg.image.load("GameUI/music_select.png"), pg.image.load("GameUI/music_hover.png"), pg.image.load("GameUI/music.png"), True, ToggleMusic)
    buttons_players.append(button_two_p)
    buttons_players.append(button_three_p)
    buttons_players.append(button_four_p)
    buttons_players.append(button_five_p)
    buttons = [button_random_p, button_simulate, button_simulate_noisy, button_calculate, button_help, button_mute]
    button_five_p.press_event()
    
    button_exit_help = ButtonBox(1000,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, ShowGame)
    
    button_exit_score = ButtonBox(1000,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, ShowGame)
    
    running = True
    while running:

        screen.fill(COLOR_BLACK)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                print('Goodbye! Thanks for playing.')
                running = False

            if ui_state is 0:
                for box in input_boxes:
                    box.handle_event(event)

                for button in buttons_players:
                    button.handle_event(event)

                for button in buttons:
                    button.handle_event(event)

            elif ui_state is 1:
                button_exit_score.handle_event(event)
            elif ui_state is 2:
                button_exit_help.handle_event(event)

        if(ui_state is 0):
        
            for box in input_boxes:
                box.update()

            screen.blit(BG, BG_RECT)

            for box in input_boxes:
                box.draw(screen)

            for button in buttons_players:
                button.draw(screen)

            for button in buttons:
                button.draw(screen)
                
            #if check_strings:
            #    if qe.check_game(game1.get_text(),number_of_players):
            #        print("OK1")
            #        screen.blit(CORRECT_STRING, GAME1_RECT)
            #    else:
            #        print("Not OK1")
            #        screen.blit(NOT_CORRECT_STRING, GAME1_RECT)
            #        
            #    if qe.check_game(game2.get_text(),number_of_players):
            #        print("OK2")
            #        screen.blit(CORRECT_STRING, GAME2_RECT)
            #    else:
            #        print("Not OK2")
            #        screen.blit(NOT_CORRECT_STRING, GAME2_RECT)
            #        
            #    if qe.check_game(game3.get_text(),number_of_players):
            #        print("OK3")
            #        screen.blit(CORRECT_STRING, GAME3_RECT)
            #    else:
            #        print("Not OK3")
            #        screen.blit(CORRECT_STRING, GAME3_RECT)
            #    check_strings = False
            #    
            # TODO: Delete 3 lines underneath
            screen.blit(CORRECT_STRING, GAME1_RECT)
            screen.blit(CORRECT_STRING, GAME2_RECT)
            screen.blit(CORRECT_STRING, GAME3_RECT)
            
            screen.blit(SPEECH_BUBBLE, SPEECH_BUBBLE_RECT)
            starting_player_surface = FONT_BOLD.render("PLAYER " + str(starting_player) + " STARTS", False, (255, 255, 255))
            screen.blit(starting_player_surface, SPEECH_BUBBLE_TEXT_RECT)
            
        elif ui_state is 1:
            button_exit_score.draw(screen)
        elif ui_state is 2:
            button_exit_help.draw(screen)
            
        if ui_state is 1:
            if run_score is 1:
                print('RUN SIMULATION')
                #phase1_score = qe.get_scores(game1.get_text(), number_of_players, True, False)
                #phase2_score = qe.get_scores(game2.get_text(), number_of_players, True, False)
                #phase3_score = qe.get_scores(game3.get_text(), number_of_players, True, False)
                run_score = 0
            elif run_score is 2:
                print('RUN SIMULATION WITH NOISE')
                #phase1_score = qe.get_scores(game1.get_text(), number_of_players, True, True)
                #phase2_score = qe.get_scores(game2.get_text(), number_of_players, True, True)
                #phase3_score = qe.get_scores(game3.get_text(), number_of_players, True, True)
                run_score = 0
            elif run_score is 3:
                print('RUN QUANTUM COMPUTER')
                #phase1_score = qe.get_scores(game1.get_text(), number_of_players, False)
                #phase2_score = qe.get_scores(game2.get_text(), number_of_players, False)
                #phase3_score = qe.get_scores(game3.get_text(), number_of_players, False)
                run_score = 0
            #print(phase1_score)
            #print(phase2_score)
            #print(phase3_score)

        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit()
