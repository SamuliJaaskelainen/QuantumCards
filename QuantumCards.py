import pygame as pg

pg.init()
pg.display.set_caption('Quantum Cards')
pg.display.set_icon(pg.image.load('Icon.png'))
screen = pg.display.set_mode((1280, 720))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
COLOR_BLACK = pg.Color('black')
FONT = pg.font.Font(None, 32)
BG = pg.image.load("Bg.png")
BG_RECT = BG.get_rect()
BUTTON = pg.image.load("Button.png")
BUTTON_PRESSED = pg.image.load("ButtonPressed.png")

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

    def __init__(self, x, y, w, h, img_not_pressed, img_pressed):
        self.rect = pg.Rect(x, y, w, h);
        self.not_pressed = img_not_pressed
        self.img_pressed = img_pressed

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print('Button pressed')

    def draw(self, screen):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            screen.blit(self.img_pressed, self.rect)
        else:
            screen.blit(self.not_pressed, self.rect)

def main():
    clock = pg.time.Clock()
    
    game1 = InputBox(150, 500, 1000, 32)
    game2 = InputBox(150, 540, 1000, 32)
    input_boxes = [game1, game2]
    
    button1 = ButtonBox(30,500,100,32, BUTTON, BUTTON_PRESSED)
    button2 = ButtonBox(30,540,100,32, BUTTON, BUTTON_PRESSED)
    buttons = [button1,button2]
    
    running = True

    while running:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            for box in input_boxes:
                box.handle_event(event)
                
            for button in buttons:
                button.handle_event(event)

        for box in input_boxes:
            box.update()

        screen.fill(COLOR_BLACK)
        screen.blit(BG, BG_RECT)

        for box in input_boxes:
            box.draw(screen)
            
        for button in buttons:
            button.draw(screen)

        pg.display.flip()
        clock.tick(30)

if __name__ == '__main__':
    main()
    pg.quit()