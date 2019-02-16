import pygame as pg
import random
#import QuantumEngine as qe

pg.init()
pg.display.set_caption('Quantum Cards')
pg.display.set_icon(pg.image.load('Icon.png'))
screen = pg.display.set_mode((1280, 720))
COLOR_INACTIVE = pg.Color('gray')
COLOR_ACTIVE = pg.Color('pink')
COLOR_BLACK = pg.Color('black')
FONT = pg.font.Font(None, 32)
BG = pg.image.load("Bg.png")
BG_RECT = BG.get_rect()
BUTTON = pg.image.load("Button.png")
BUTTON_HOVER = pg.image.load("ButtonHover.png")
BUTTON_PRESSED = pg.image.load("ButtonPressed.png")
number_of_players=3
buttons_players=[]
pg.mixer.music.load('Music.ogg')
pg.mixer.music.play(-1)
BUTTON_SOUNDS = [pg.mixer.Sound('ButtonSound1.ogg'), pg.mixer.Sound('ButtonSound2.ogg'), pg.mixer.Sound('ButtonSound3.ogg')]
ui_state=0 #0=game, 1=score, 2=help
run_score=0#0=none, 1=simulation, 2=simulation with noise, 3=quantum computer

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
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
            if self.active:
                if event.key == pg.K_RETURN:
                    self.active = not self.active
                elif event.key == pg.K_DELETE:
                    self.text = ""
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)
                
        self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    def update(self):
        width = max(1000, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pg.draw.rect(screen, self.color, self.rect, 2)

class ButtonBox:
    global BUTTON_SOUNDS

    def __init__(self, x, y, w, h, img_not_pressed, img_hover, img_pressed, toggle, button_event):
        self.rect = pg.Rect(x, y, w, h);
        self.not_pressed = img_not_pressed
        self.img_hover = img_hover
        self.img_pressed = img_pressed
        self.button_event = button_event;
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
                    self.pressed = not self.pressed;

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
    global buttons_players
    print('Set player number to two')
    for button in buttons_players:
        button.reset()
    number_of_players=2;
    GetStartingPlayer()
            
def SetPlayerToThree():
    global buttons_players
    print('Set player number to three')
    for button in buttons_players:
        button.reset()
    number_of_players=3;
    GetStartingPlayer()
    
def SetPlayerToFour():
    global buttons_players
    print('Set player number to four')
    for button in buttons_players:
        button.reset()
    number_of_players=4;
    GetStartingPlayer()
    
def SetPlayerToFive():
    global buttons_players
    print('Set player number to five')
    for button in buttons_players:
        button.reset()
    number_of_players=5;
    GetStartingPlayer()
    
def GetStartingPlayer():
    starting_player = random.randint(0, number_of_players) + 1

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

def main():
    global run_score
    clock = pg.time.Clock()
    
    game1 = InputBox(150, 500, 1000, 32)
    game2 = InputBox(150, 540, 1000, 32)
    game3 = InputBox(150, 580, 1000, 32)
    input_boxes = [game1, game2, game3]
    
    button_two_p = ButtonBox(30,50,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, True, SetPlayerToTwo)
    button_three_p = ButtonBox(30,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, True, SetPlayerToThree)
    button_four_p = ButtonBox(160,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, True, SetPlayerToFour)
    button_five_p = ButtonBox(290,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, True, SetPlayerToFive)
    button_random_p = ButtonBox(500,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, GetStartingPlayer)
    button_simulate = ButtonBox(200,680,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, Simulate)
    button_simulate_noisy = ButtonBox(350,680,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, SimulateWithNoise)
    button_calculate = ButtonBox(500,680,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, Calculate)
    button_help = ButtonBox(1000,20,100,32, BUTTON, BUTTON_HOVER, BUTTON_PRESSED, False, ShowHelp)
    buttons_players.append(button_two_p)
    buttons_players.append(button_three_p)
    buttons_players.append(button_four_p)
    buttons_players.append(button_five_p)
    buttons = [button_random_p, button_simulate, button_simulate_noisy, button_calculate, button_help]
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
                
        elif ui_state is 1:
            button_exit_score.draw(screen)
        elif ui_state is 2:
            button_exit_help.draw(screen)
            
        if ui_state is 1:
            if run_score is 1:
                print('RUN SIMULATION')
                run_score = 0
            elif run_score is 2:
                print('RUN SIMULATION WITH NOISE')
                run_score = 0
            elif run_score is 3:
                print('RUN QUANTUM COMPUTER')
                run_score = 0

        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
    pg.quit()