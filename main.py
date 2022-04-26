#!/bin/python3

from cgitb import text
import datetime
import pygame
import sys
import subprocess
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))


pygame.init()
pygame.font.init()
pygame.joystick.init()
pygame.mixer.init()

pygame.display.set_caption("PyLaunch")

fullscreen = 1

pygame.mouse.set_visible(False)

res = (1920, 1080)
display_surface = pygame.display.set_mode(res,pygame.FULLSCREEN)

wav_select = pygame.mixer.Sound("select.wav")



os.system("/bin/bash ./autostart.sh")

category_list = []
current_category_num = 0

class CategoryList:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename


for file in os.listdir("."):
    if file.endswith(".list"):
        f = open(os.path.join(file),"r")
        aname = f.readline()
        f.close()
        category_list.append(CategoryList(aname,os.path.join(file)))
        
gamelist = []

category_name = "none"

imagetextures = []

# aspect ratio 13:18

imagesize = (250,346)
font = pygame.font.Font("font.ttf", 50)

textrenders = []
textrendersshadow = []

def load_game_list(filename):
    global category_name, current_choice, textrenders, gamelist, imagetextures, textrendersshadow

    current_choice = 0
    f = open(filename,"r")
    contents = f.readlines()

    gamelist = []
    i = 0
    class Gameitem:
        def __init__(self, name, command, cwd, boxart):
            self.name = name
            self.command = command
            self.cwd = cwd
            self.boxart = boxart

    category_name = contents[i].strip()
    i = i + 2

    while True:
        aname = contents[i].strip()
        i = i+1
        acommand = contents[i].strip()

        i = i+1
        acwd = contents[i].strip()

        i = i+1
        aboxart = contents[i].strip()

        newgameitem = Gameitem(aname, acommand, acwd, aboxart)
        gamelist.append(newgameitem)

        i = i+2

        if (i > len(contents)):
            break    

    f.close()

    imagetextures = []
    for x in range(len(gamelist)):
        imagetextures.append(pygame.image.load(gamelist[x].boxart))
        imagetextures[x] = pygame.transform.smoothscale(imagetextures[x],imagesize)

    textrenders = []
    textrendersshadow = []
    for x in range(len(gamelist)):
        textrenders.append(font.render(gamelist[x].name, True, (255,255,255)))
        textrendersshadow.append(font.render(gamelist[x].name, True, (0,0,0)))


load_game_list(category_list[current_category_num].filename)
category_name = category_list[current_category_num].name








clock = pygame.time.Clock()

current_choice = 0

bg = pygame.image.load("bg.jpg")
overlay = pygame.image.load("overlay.png")
overlay_btm = pygame.transform.flip(overlay,False,True)



loadingtext = font.render("LOADING GAME", True, (255,255,255))
categorytext = [] 
categorytextshadow = []

for i in range(len(category_list)):
    categorytext.append(font.render(category_list[i].name, True, (255,255,255)))
    categorytextshadow.append(font.render(category_list[i].name, True, (0,0,0)))

tc = 0

if pygame.joystick.get_count() > 0:
    joystick = pygame.joystick.Joystick(0)

pressed = 0

num_rows = 7

def run_app():
    display_surface.fill((0,0,0))
    display_surface.blit(bg, (0,0))

    text_rect = loadingtext.get_rect(center=(res[0]/2, res[1]/2))
    display_surface.blit(loadingtext, text_rect)

    pygame.display.update()

    process = subprocess.Popen(gamelist[current_choice].command, shell=True, stdout=subprocess.PIPE, cwd=gamelist[current_choice].cwd)
    process.wait()

    pygame.event.clear()

scroll = 0

def next_category():
    global current_category_num, category_list, current_choice
    current_category_num = current_category_num + 1

    if current_category_num > len(category_list)-1:
        current_category_num = 0
    
    load_game_list(category_list[current_category_num].filename)
    current_choice = 0



def previous_category():
    global current_category_num, category_list, current_choice
    current_category_num = current_category_num - 1

    if current_category_num < 0:
        current_category_num = len(category_list)-1
    
    load_game_list(category_list[current_category_num].filename)
    current_choice = 0    

def move_left():
    global current_choice, scroll
    if current_choice > 0:
        current_choice = current_choice - 1    

def move_right():
    global current_choice, scroll
    if current_choice < len(gamelist)-1:
        current_choice = current_choice + 1


def move_up():
    global current_choice, num_rows
    current_choice -= num_rows
    if (current_choice < 0):
        current_choice = 0

def move_down():
    global current_choice, num_rows
    current_choice += num_rows
    if (current_choice > (len(gamelist) - 1)):
        current_choice = len(gamelist) - 1

while True:
    display_surface.fill((0,0,0))
    display_surface.blit(bg, (0,0))

    if (len(gamelist) > num_rows *2):
        scroll = (current_choice // num_rows) * (imagesize[1]+20)
    else:
        scroll = 0

    for x in range(len(gamelist)): 
        if x != current_choice:
            imagetextures[x].set_alpha(150)
        else:
            imagetextures[x].set_alpha(255)
        
        pos = ((imagesize[0]+20)*(x%num_rows) + 20,170 - scroll)
        pos = (pos[0], pos[1]+ (x//num_rows) * (imagesize[1]+20))

        
        if (tc % 7 < 3 or current_choice != x):
            imagetextures[x].set_alpha(180)
        else:
            imagetextures[x].set_alpha(255)
        
        display_surface.blit(imagetextures[x], pos)

    
    display_surface.blit(overlay,(0,0))

    display_surface.blit(overlay_btm,(0,res[1]-120))    

    now = datetime.datetime.now()
    time_text = font.render(now.strftime("%H:%M"), True, (255,255,255))
    text_rect = time_text.get_rect()

    display_surface.blit(time_text, (res[0]-text_rect[2]-20,0))

    tc += 1

    pos = (20,10)

    for i in range(len(category_list)):
        #text_rect = categorytext[i].get_rect(center=(res[0]/2, 50))
        

        text_rect = categorytext[i].get_rect()
        text_rect = (categorytext[i].get_rect()[0] + pos[0], categorytext[i].get_rect()[1])

        

        if (i == current_category_num):
            #if (tc % 7 > 3):
            categorytext[i].set_alpha(255)
            categorytextshadow[i].set_alpha(255)
            display_surface.blit(categorytextshadow[i], (pos[0]+2,pos[1]+2))
            display_surface.blit(categorytext[i], pos)
        else:
            categorytext[i].set_alpha(68)
            categorytextshadow[i].set_alpha(68)
            display_surface.blit(categorytextshadow[i], (pos[0]+2,pos[1]+2))
            display_surface.blit(categorytext[i], pos)

        pos = (pos[0]+categorytext[i].get_rect()[2],10)



    text_rect = textrenders[current_choice].get_rect(center=(res[0]/2, res[1]-50))

    display_surface.blit(textrendersshadow[current_choice], (text_rect[0]+2,text_rect[1]+2))
    display_surface.blit(textrenders[current_choice], text_rect)

    pygame.display.update()
    clock.tick(20)


    for event in pygame.event.get():
        if pygame.joystick.get_count() > 0:
            if event.type == pygame.JOYHATMOTION or event.type == pygame.JOYBUTTONDOWN:
                #pygame.mixer.Sound.play(wav_select)
                if pressed == 0:
                    wav_select.play()
                if (joystick.get_hat(0)[1] == 1 and pressed == 0): #up
                    move_up()
                    pressed = 1
                elif (joystick.get_hat(0)[1] == -1 and pressed == 0): #down
                    move_down()
                    pressed = 1
                elif (joystick.get_hat(0)[0] == 1 and pressed == 0): #right
                    move_right()
                    pressed = 1            
                elif (joystick.get_hat(0)[0] == -1 and pressed == 0): #left
                    move_left()   
                    pressed = 1
                elif (joystick.get_button(0) == True and pressed == 0): #button 1
                    run_app()
                    pressed = 1

                elif (joystick.get_button(7) == True and pressed == 0):
                    next_category()
                    pressed = 1

                elif (joystick.get_button(6) == True and pressed == 0):
                    previous_category()
                    pressed = 1

                elif (joystick.get_button(13) == True and joystick.get_button(14) == True and pressed == 0):
                    pressed = 1
                    sys.exit()
                else:
                    pressed = 0                   


        if event.type == pygame.KEYUP:
            #pygame.mixer.Sound.play(wav_select)
            if event.key != pygame.K_LSHIFT and event.key != pygame.K_LALT:
                wav_select.play()
            if event.key == pygame.K_RETURN and pygame.key.get_mods() & pygame.KMOD_ALT:
                if fullscreen == 1:
                    fullscreen = 0
                    res = (1400,900)
                    display_surface = pygame.display.set_mode(res)
                    pass
                else:
                    res = (1920,1080)
                    display_surface = pygame.display.set_mode(res,pygame.FULLSCREEN)

                    fullscreen = 1
                    pass

            if event.key == pygame.K_ESCAPE:
                sys.exit()

            if event.key == pygame.K_UP:
                move_up()

            if event.key == pygame.K_DOWN:
                move_down()

            if event.key == pygame.K_LEFT:
                move_left()
            if event.key == pygame.K_RIGHT:
                move_right()
            if event.key == pygame.K_RETURN and not pygame.key.get_mods() & pygame.KMOD_ALT:
                run_app()

            if event.key == pygame.K_TAB:
                if not (pygame.key.get_mods() & pygame.KMOD_SHIFT):
                    next_category()
                else:
                    previous_category()


        


        if event.type == pygame.QUIT:
            pygame.quit()

            sys.exit()