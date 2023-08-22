import pygame as pg
import numpy as np
import random
import string
import sys
pg.mixer.pre_init(44100, -16, 1, 512) # for sound
pg.init()

sw,sh = 1280, 760 # ScreenWidth, ScreenHeight
sc = (sw/2, sh/2) # align center
screen = pg.display.set_mode((sw,sh))
pg.display.set_caption("CRAMMAN")
default_font = pg.font.SysFont(None, 40)


# Colors
colors = {"black":(0,0,0),"gray":(128,128,128), "white":(255,255,255),"darkred":(128,0,0),"darkgreen":(0,128,0),"lavender":(230,230,250)}

# Images
images = {"logo":pg.image.load("image/logo1.png"),0:pg.image.load("image/I1.png"), 1:pg.image.load("image/I2.png"), 2:pg.image.load("image/I3.png"),
          3:pg.image.load("image/I4.png"),4:pg.image.load("image/I5.png"),5:pg.image.load("image/I6.png"),6:pg.image.load("image/I7.png")}

# Audio
sounds = {"win":pg.mixer.Sound("audio/win.wav"), "lose":pg.mixer.Sound("audio/lose.wav"),"click":pg.mixer.Sound("audio/click.wav")}

alphabet = list(string.ascii_uppercase) # Uppercase Letters


class Button(object): # A GENERAL CLASS FOR ALL THE BUTTONS ON THE SCREEN (LETTERS & LANGUAGE BUTTONS)
    def __init__(self, color, pos, width, height, letter, active = False, type = 1, size = 40):
        self.type = type #TYPE 1 IS A LETTER, TYPE 2 IS A LANGUAGE BUTTON
        self.active = active    # A VARIABLE ONLY FOR TYPE 2
        self.clicked = False    # A VARIABLE ONLY FOR TYPE 1
        self.rollOver = False   # A VARIABLE ONLY FOR TYPE 1
        self.size = size
        self.font = pg.font.SysFont(None, self.size)
        self.color = color
        self.letter = letter
        self.pos = pos
        self.width = width
        self.height = height
        self.subsurface = pg.Surface((self.width, self.height))         # CREATING A SUBSURFACE TO
        self.subsurface.fill(self.color)                                # GET A RECT (FOR COLLISION)
        self.text = self.font.render(self.letter, True, colors["white"])

    def Draw(self, surface):
        if self.type == 1:
            if self.rollOver:                   # IF A TYPE 1 BUTTON IS UNDER
                self.subsurface.set_alpha(200)  # THE MOUSE, MAKE IT LESS VIBRANT
            else:
                self.subsurface.set_alpha(255)
            if not self.clicked:
                surface.blit(self.subsurface, self.pos)
                self.subsurface.blit(self.text, (self.width/4,self.height/5))
        if self.type == 2:
            if self.active:                     # IF A TYPE 2 BUTTON IS ACTIVE
                self.subsurface.set_alpha(255)  # MAKE IT'S COLOR MORE VIBRANT
            else:
                self.subsurface.set_alpha(100)
            surface.blit(self.subsurface, self.pos)
            self.subsurface.blit(self.text, (self.width / 4, self.height / 5))



notesArea = pg.Surface((sw,700))        # CREATING TWO
notesArea.fill(colors["white"])         # AREAS WITH DIFFERENT
                                        # COLORS
buttonArea = pg.Surface((sw, 100))
buttonArea.fill(colors["lavender"])

letters = []
j = 0   # TO ALIGN THE LETTERS ON THE SCREEN ( VERTICALLY )
for number, letter in enumerate(alphabet):
    if number > 12: # TO ALIGN THE LETTERS ON THE SCREEN ( HORIZONTALLY )
        number = number - 13
        j = 1
    letters.append(Button(colors["gray"], (70+number*90,140+j*60), 50, 50, letter))

languageButtons = []
languageButtons.append(Button(colors["gray"], (30, 400), 80,40, "English", False, 2, 20))
languageButtons.append(Button(colors["gray"], (120, 400), 80,40, "Tagalog", True, 2, 20))

errorCount = 0

#WORDS
English=["BRIDGE", "BONE","GRAPES","BELL" ,"JELLYFISH","BUNNY","TRUCK" ,"GRASS"
        ,"DOOR","MONKEY", "SPIDER" ,"BREAD","EARS","BOWL","BRACELET","ALLIGATOR"
        ,"BAT","CLOCK","LOLLIPOP","MOON","DOLL","ORANGE","EAR","BASKETBALL"
        ,"BIKE","AIRPLANE","PEN","INCHWORM" ,"SEASHELL" ,"ROCKET","CLOUD","BEAR"
        ,"CORN","CHICKEN","PURSE","GLASSES","BLOCKS" ,"CARROT","TURTLE","PENCIL"
        ,"HORSE","DINOSAUR","HEAD","LAMP","SNOWMAN","ANT","GIRAFFE" ,"CUPCAKE"
        ,"CHAIR","LEAF","BUNK","BED","SNAIL","BABY","BALLOON","BUS" ,"CHERRY"
        ,"CRAB","FOOTBALL","BRANCH" ,"ROBOT"]
Tagalog=["LINGGO","TAON","BUKAS","KAHAPON" ,"KALENDARYO" ,"SEGUNDO" ,"ORAS" ,"MINUTO"
         ,"ORASAN" ,"MAGANDA" ,"PANGIT" ,"DALAWA","MABIGAT","MAKAPAL","MALAPAD","MAHABA"
         ,"MALAKI","LALAKI","BABAE","MANIPIS","MAIKLI","MALIIT","MAKITID","ISDA","ASAWA"
         ,"HAYOP","IBON","GUBAT","BULAKLAK","PRUTAS","BALAHIBO","PAKPAK","NGIPIN","BITUKA"
         ,"BITUIN","ALIKABOK","BUHANGIN","LANGIT","NIYEBE","BUNDOK"]

languageChoice=1 
if languageChoice == 1:
    currentLanguage = Tagalog
else:
    currentLanguage = English
currentWord = random.randrange(0, len(currentLanguage))

guessed = []

lw = 40 # WIDTH OF THE LINE FOR THE LETTERS
ls = 10 # SPACE BETWEEN THE LINES

needRestart = False # FOR CONDITIONS IN WHICH YOU NEED TO RESTART THE GAME, LIKE CHANGING THE LANGUAGE
winCount = 0
pointCount = 0
spaceCount = 0  # COUNTING HOW MANY SPACES A WORD HAS, IT'LL BE IMPORTANT WHEN CHECKING-
for letter in currentLanguage[currentWord]: # - IF YOU GUESSED THE WORD COMPLETELY.
    if letter == " ":
        spaceCount += 1
print(len(English))
print(len(Tagalog))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEMOTION:
            for button in letters: # CHECK IF MOUSE IS ON ANY BUTTONS, BUTTON POS GOT BY CALLING GET_RECT()
                currentRect = button.subsurface.get_rect(topleft = (button.pos[0], button.pos[1]))
                if currentRect.collidepoint(pg.mouse.get_pos()): # IF COLLIDING WITH MOUSE CURSOR
                    button.rollOver = True      # ONLY HIGHLIGHT A BUTTON IF YOU ARE
                else:                           # ON IT AND IF YOU AREN'T, STOP HIGHLIGHTING
                    button.rollOver = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1: # LEFT MOUSE BUTTON / LEFT CLICK
                for button in letters:
                    if button.rollOver == True and button.clicked == False: # IF YOU ARE ON THE BUTTON AND IF
                        sounds["click"].play()                              # THE BUTTON ISN'T CLICKED STILL,
                        button.clicked = True                               # ONLY THEN IT'S CLICKABLE.
                        guessed.append(button.letter)
                        noError = False
                        for letter in currentLanguage[currentWord]:
                            if button.letter == letter:
                                noError = True
                        if errorCount < 6 and not noError: # IF THAT LETTER ISN'T IN THE WORD, IF NOERROR == FALSE,
                            errorCount += 1                # UP THE ERROR COUNT BY ONE
                for button in languageButtons:
                    currentRectLang = button.subsurface.get_rect(topleft = (button.pos[0], button.pos[1]))
                    if currentRectLang.collidepoint(pg.mouse.get_pos()):    # SAME PROCESS WITH THE LANG. BUTTONS
                        button.active = True
                        sounds["click"].play()
                        if button.letter == "English":
                            currentLanguage = English
                        else:
                            currentLanguage = Tagalog
                        currentIndex = languageButtons.index(button)            # IF YOU ACTIVATE A LANG. BUTTON
                        for subbutton in languageButtons:                       # THE OTHERS GET DEACTIVATED.
                            if languageButtons.index(subbutton) == currentIndex:
                                pass
                            else:
                                subbutton.active = False
                                needRestart = True          # NEED TO RESTART THE GAME


    screen.fill(colors["white"])        # BG COLOR THAT WE WON'T SEE
    screen.blit(notesArea, (0,0))       # TOP PART
    screen.blit(buttonArea, (0, 700))   # BOTTOM PART
    screen.blit(images["logo"], (sc[0]-images["logo"].get_rect().width/2, 10)) # LOGO

    screen.blit(images[errorCount], (sc[0]-images[errorCount].get_rect().width/2, sc[1]-images[errorCount].get_rect().height/2+70))
    # ^^ THE HANGMAN PICTURES

    for letter in letters:              # DRAWING
        letter.Draw(screen)             # THE BUTTONS
                                        # TO THE
    for langbut in languageButtons:     # SCREEN
        langbut.Draw(screen)

    stats_font = pg.font.SysFont(None, 25, False, True)  # A FONT FOR THE STATS
    winCountText = stats_font.render("TOTAL GUESSED WORDS       : " + str(winCount), True, colors["black"])
    pointCountText = stats_font.render("TOTAL POINTS   : " + str(pointCount), True, colors["black"])
    screen.blit(winCountText, (30, 300))
    screen.blit(pointCountText, (30, 330))

    totalShown = 0  # TOTAL LETTERS SHOWN AT THE BOTTOM PART
    if not needRestart:
        for i,letter in enumerate(currentLanguage[currentWord]):
            text = default_font.render(letter, True, colors["black"])
            posX = (1280 - len(currentLanguage[currentWord]) * (lw + ls))/2 + i * (lw + ls)
            posY = 740
            if letter != " ":
                pg.draw.rect(screen, colors["black"], (posX, posY, lw, 3))
            else:
                pg.draw.rect(screen, colors["lavender"], (posX, posY, lw, 3))
            if letter in guessed:
                totalShown += 1
                screen.blit(text, (posX+lw/3, posY-30))

    pg.display.update() # UPDATING THE SCREEN AT THIS POINT, ANYTHIGN AFTER THIS WON'T BE SEEN UNTIL
                        # A NEW FRAME STARTS OR I MANUALLY UPDATE IT AGAIN, WHICH I DO AT LINE 239 AND 258

    final_font = pg.font.SysFont(None, 80)
    final_font1 = pg.font.SysFont(None, 50)
    lose_text = final_font.render("YOU LOSE!", True, colors["darkred"])
    lose_text1 = final_font1.render ("The Word is",True,colors["black"])
    lose_text2= final_font1.render ("{}".format(currentLanguage[currentWord]),True,colors["darkred"])
    win_text = final_font.render("YOU GUESSED IT", True, colors["darkgreen"])


    if errorCount >= 6 or needRestart:  # IF A RESTART CONDITION IS MET
        if not needRestart:    # But if that condition is not by changing languages: lose.
            sounds["lose"].play()
            screen.blit(lose_text, (500,380))
            screen.blit(lose_text1,(500,580))
            screen.blit(lose_text2,(500,610))
            pg.display.update()
            pg.time.wait(1000)
        guessed.clear() #       RESETTING EVERYTHING            #
        pointCount = 0                                          #
        errorCount = 0                                          #
        winCount = 0                                            #
        for letter in letters:                                  #
            letter.clicked = False                              #
        currentWord = random.randrange(0, len(currentLanguage)) #
        spaceCount = 0                                          #
        for letter in currentLanguage[currentWord]:             #
            if letter == " ":                                   #
                spaceCount += 1                                 #
        needRestart = False                                     #
        pg.time.wait(1000)                                      #

    if totalShown == len(currentLanguage[currentWord]) - spaceCount: # IF IT'S A WIN CONDITION
        sounds["win"].play()
        screen.blit(win_text, (380, 380))
        pg.display.update()
        pg.time.wait(1000)
        guessed.clear()
        pointCount += 600 + winCount*10 - errorCount * 100 # POINTS SYSTEM, GAIN FEWER POINTS IF YOU HAD MORE ERRORS
        errorCount = 0
        winCount+=1

        for letter in letters:
            letter.clicked = False
        currentWord = random.randrange(0, len(currentLanguage))
        spaceCount = 0
        for letter in currentLanguage[currentWord]:
            if letter == " ":
                spaceCount += 1
        pg.time.wait(1000)
