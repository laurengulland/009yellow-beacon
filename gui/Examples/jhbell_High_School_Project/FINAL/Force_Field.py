import pygame
import os.path
import math
import re
import inspect

def isValidFloatString(s):
    regex = ["^[+\-]?[0-9]+\.?[0-9]*[eE][+\-]?[0-9]+$", "^[+/-]?[0-9]+\.?[0-9]*$", "^[+/-]?[0-9]*\.?[0-9]+$", "^[+\-]?[0-9]*\.?[0-9]+[eE][+\-]?[0-9]+$"]
    for k in regex:
        seeker = re.compile(k)
        if bool(seeker.search(s)):
            return bool(seeker.search(s))
    return False

def gencollisiontest(l):
    for n in range(len(l)):
        for r in range(len(l)):
            if l[n][0] and l[r][0] and r != n and ((l[n][1] - l[r][1])**2 + (l[n][2] - l[r][2])**2) <= (l[n][5] + l[r][5])**2:
                return True
    return False

def speccollisiontest(l, index, testx, testy, testradius):
    for n in range(len(l)):
        if l[n][0] and n != index and ((l[n][1] - testx)**2 + (l[n][2] - testy)**2) <= (l[n][5] + testradius)**2:
            return True
    return False
    
def scaleexp(sc):
    if sc >= 1 and sc < 10:
        return 0
    if sc < 1:
        return scaleexp(sc*10)-1
    if sc >= 10:
        return scaleexp(sc/10)+1

def scalebar(sc):
    if sc >= 1 and sc < 10:
        return 1/sc
    if sc < 1:
        return scalebar(sc*10)
    if sc >= 10:
        return scalebar(sc/10)

# Define colors
black    = (   0,   0,   0)
white    = ( 255, 255, 255)
green    = (   0, 255,   0)
red      = ( 255,   0,   0)
brown    = ( 150,  75,   0)
blue     = (   0,   0, 255)
yellow   = ( 255, 255,   0)
backcolor = (0x9F, 0xAF, 0xF8)
spaceblue = (0x1B, 0x1B, 0x9E)
editblue = (   0, 110, 173)
 
pygame.init()

pat = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Define images
addbodyon = pygame.image.load(os.path.join(pat+'\\addbodyon.png'))
addbodyoff = pygame.image.load(os.path.join(pat+'\\addbodyoff.png'))
gravityoff = pygame.image.load(os.path.join(pat+'\\gravityoff.png'))
gravityon = pygame.image.load(os.path.join(pat+'\\gravityon.png'))
electricityoff = pygame.image.load(os.path.join(pat+'\\electricityoff.png'))
electricityon = pygame.image.load(os.path.join(pat+'\\electricityon.png'))
magnetismoff = pygame.image.load(os.path.join(pat+'\\magnetismoff.png'))
magnetismon = pygame.image.load(os.path.join(pat+'\\magnetismon.png'))
deletebody = pygame.image.load(os.path.join(pat+'\\deletebody.png'))
movebodyon = pygame.image.load(os.path.join(pat+'\\movebodyon.png'))
movebodyoff = pygame.image.load(os.path.join(pat+'\\movebodyoff.png'))
bodyvelocityoff = pygame.image.load(os.path.join(pat+'\\bodyvelocityoff.png'))
bodyvelocityon = pygame.image.load(os.path.join(pat+'\\bodyvelocityon.png'))
bodymassoff = pygame.image.load(os.path.join(pat+'\\bodymassoff.png'))
bodymasson = pygame.image.load(os.path.join(pat+'\\bodymasson.png'))
bodychargeoff = pygame.image.load(os.path.join(pat+'\\bodychargeoff.png'))
bodychargeon = pygame.image.load(os.path.join(pat+'\\bodychargeon.png'))
bodyradiusoff = pygame.image.load(os.path.join(pat+'\\bodyradiusoff.png'))
bodyradiuson = pygame.image.load(os.path.join(pat+'\\bodyradiuson.png'))
playbig = pygame.image.load(os.path.join(pat+'\\playbig.png'))
playsmall = pygame.image.load(os.path.join(pat+'\\playsmall.png'))
pause = pygame.image.load(os.path.join(pat+'\\pause.png'))
reset = pygame.image.load(os.path.join(pat+'\\reset.png'))

#Define bodies ex. body# = [exist?, x-pos, y-pos, x-momentum, y-momentum, radius, mass, charge, xp-sto, yp-sto, xm-sto, ym-sto]
morgue = []
  
# Set the width and height of the screen [width,height]
size = [1100,880]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Force Field")
 
#Loop until the user clicks the close button.
done = False

#Sets the current mode to edit mode; False is run mode.
currentmode = True
creation = True

#Sets that all forces are active.
gravity = True
electricity = True
magnetism = True

morebody = True

choose = 0

clickon = True
keyon = True

editspace = False
editenter = False
scale = 1
scalesto = 1
message = ""
drag = False
grasp = True

movebody = False
bodyvelocity = False
bodymass = False
bodycharge = False
bodyradius = False

textxpos = False
textypos = False
textxvel = False
textyvel = False
textmass = False
textcharge = False
textradius = False

textscale = False
texttime = False
texttimescale = False

textcursorpos = 0
text = ["", "", "", "", "", "", "", "", "", "", ""]
shift = True

bounceint = 0
bouncebool = True

bigg = 6.67384e-11
bigk = 8.98755e9
mu4pi = 1e-7

t = 0
dt = 0.025
timescale = 1
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# -------- Main Program Loop -----------
while not done:
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    if editspace and movebody and drag:
        x,y=pygame.mouse.get_pos()
        if grasp:
            grasp = False
            grx = (x-410)*scale-morgue[choose][1]
            gry = (410-y)*scale-morgue[choose][2]
        if not speccollisiontest(morgue, choose, (x-410)*scale-grx, (410-y)*scale-gry, morgue[choose][5]):
            morgue[choose][1] = (x-410)*scale-grx
            morgue[choose][2] = (410-y)*scale-gry
        text[1] = "{:+.2e}".format(morgue[choose][1])
        text[2] = "{:+.2e}".format(morgue[choose][2])
    if not textscale:
        text[8] = "{:+.2e}".format(scale)
    if not texttime:
        text[9] = "{:+.2e}".format(dt)
    if not texttimescale:
        text[10] = "{:+.2e}".format(timescale)
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        if currentmode:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if clickon:
                    message = ""
                x,y=pygame.mouse.get_pos()
                if x >= 830 and x <= 1080 and y >= 735 and y <= 810 and clickon and creation:
                    currentmode = False
                    creation = False
                    clickon = False
                if x >= 830 and x <= 945 and y >= 735 and y <= 810 and clickon and not creation:
                    currentmode = False
                    clickon = False
                if x >= 965 and x <= 1080 and y >= 735 and y <= 810 and clickon and not creation:
                    for n in range(len(morgue)):
                        for k in range(1,8):
                            morgue[n][k] = morgue[n][k+7]
                        morgue[n][0] = morgue[n][15]
                    scale = scalesto
                    creation = True
                    clickon = False
                if x >= 820 and x <= 920 and y >= 695 and y <= 725 and clickon:
                    textscale = True
                elif textscale:
                    textscale = False
                    if isValidFloatString(text[8]):
                        if abs(float(text[8])) > 0:
                            scale = abs(float(text[8]))
                        text[7] = "{:+.2e}".format(scale)
                if x >= 960 and x <= 1060 and y >= 695 and y <= 725 and clickon:
                    texttime = True
                elif texttime:
                    texttime = False
                    if isValidFloatString(text[9]):
                        if abs(float(text[9])) > 0:
                            dt = abs(float(text[9]))
                        text[9] = "{:+.2e}".format(dt)
                if x >= 960 and x <= 1060 and y >= 845 and y <= 875 and clickon:
                    texttimescale = True
                elif texttimescale:
                    texttimescale = False
                    if isValidFloatString(text[10]):
                        if abs(float(text[10])) > 0:
                            timescale = abs(float(text[10]))
                        text[10] = "{:+.2e}".format(timescale)
                if x >= 820 and x <= 870 and y >= 100 and y <= 150 and clickon:
                    morebody = not(morebody)
                    if morebody:
                        editspace = False
                    clickon = False
                if x >= 890 and x <= 940 and y >= 100 and y <= 150 and clickon:
                    gravity = not(gravity)
                    clickon = False
                if x >= 960 and x <= 1010 and y >= 100 and y <= 150 and clickon:
                    electricity = not(electricity)
                    clickon = False
                if x >= 1030 and x <= 1080 and y >= 100 and y <= 150 and clickon:
                    magnetism = not(magnetism)
                    clickon = False
                if morebody and not drag:
                    if x > 45 and x < 775 and y > 45 and y < 775 and clickon:
                        clickon = False
                        collide = 0
                        mout = 0
                        for k in morgue:
                            if k[0] and ((k[1] - scale*(x-410))**2 + (k[2] - scale*(410-y))**2) < (k[5] + scale*40)**2:
                                collide = 1
                                break
                        if collide == 0:
                            morgue.append([True, (x-410)*scale, (410-y)*scale, 0, 0, 30*scale, 8e8, 0, (x-410)*scale, (410-y)*scale, 0, 0, 30*scale, 8e8, 0, True])
                            choose = len(morgue) - 1
                            editspace = True
                            editenter = True
                        if collide != 0:
                            for n in range(len(morgue)):
                                if morgue[n][0] and (morgue[n][1] - scale*(x-410))**2 + (morgue[n][2] - scale*(410-y))**2 < (morgue[n][5])**2:
                                    if not editspace or (choose != n and editspace):
                                        editenter = True
                                    if editspace and movebody and choose == n:
                                        drag = True
                                    choose = n
                                    editspace = True
                                    morebody = False
                                    mout = 1
                                    break
                            if mout == 0:
                                message = "Cannot add bodies too close!"
                if not morebody and not drag:
                    if x > 10 and x < 810 and y > 10 and y < 810 and clickon:
                        clickon = False
                        collide = 0
                        for n in range(len(morgue)):
                            if morgue[n][0] and (morgue[n][1] - scale*(x-410))**2 + (morgue[n][2] - scale*(410-y))**2 < (morgue[n][5])**2:
                                collide = 1
                                if not editspace or (choose != n and editspace):
                                    editenter = True
                                if editspace and movebody and choose == n:
                                    drag = True
                                choose = n
                                editspace = True
                                break
                        if collide == 0:
                            editspace == False
            if editenter:
                editenter = False
                for n in range(1,8):
                    text[n] = "{:+.2e}".format(morgue[choose][n])
            if editspace:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y=pygame.mouse.get_pos()
                    if x >= 850 and x <= 900 and y >= 250 and y <= 300 and clickon:
                        morgue[choose][0] = False
                        for r in range(1,len(morgue[choose])):
                            morgue[choose][r] = 0
                        editspace = False
                        clickon = False
                    if x >= 850 and x <= 900 and y >= 320 and y <= 370 and clickon:
                        movebody = not(movebody)
                        if movebody:
                            bodyvelocity = False
                            bodymass = False
                            bodycharge = False
                            bodyradius = False
                        clickon = False
                    if x >= 850 and x <= 900 and y >= 390 and y <= 440 and clickon:
                        bodyvelocity = not(bodyvelocity)
                        if bodyvelocity:
                            movebody = False
                            bodymass = False
                            bodycharge = False
                            bodyradius = False
                        clickon = False
                    if x >= 850 and x <= 900 and y >= 460 and y <= 510 and clickon:
                        bodymass = not(bodymass)
                        if bodymass:
                            bodyvelocity = False
                            movebody = False
                            bodycharge = False
                            bodyradius = False
                        clickon = False
                    if x >= 850 and x <= 900 and y >= 530 and y <= 580 and clickon:
                        bodycharge = not(bodycharge)
                        if bodycharge:
                            bodyvelocity = False
                            bodymass = False
                            movebody = False
                            bodyradius = False
                        clickon = False
                    if x >= 850 and x <= 900 and y >= 600 and y <= 650 and clickon:
                        bodyradius = not(bodyradius)
                        if bodyradius:
                            bodyvelocity = False
                            bodymass = False
                            bodycharge = False
                            movebody = False
                        clickon = False
                    if movebody and x >= 920 and x <= 1045 and y >= 325 and y <= 355 and clickon:
                        textxpos = True
                    elif textxpos:
                        textxpos = False
                        if isValidFloatString(text[1]):
                            if not speccollisiontest(morgue, choose, float(text[1]), morgue[choose][2], morgue[choose][5]):
                                morgue[choose][1] = float(text[1])
                        text[1] = "{:+.2e}".format(morgue[choose][1])
                    if movebody and x >= 920 and x <= 1045 and y >= 425 and y <= 455 and clickon:
                        textypos = True
                    elif textypos:
                        textypos = False
                        if isValidFloatString(text[2]):
                            if not speccollisiontest(morgue, choose, morgue[choose][1], float(text[2]), morgue[choose][5]):
                                morgue[choose][2] = float(text[2])
                        text[2] = "{:+.2e}".format(morgue[choose][2])
                    if bodyvelocity and x >= 920 and x <= 1045 and y >= 325 and y <= 355 and clickon:
                        textxvel = True
                    elif textxvel:
                        textxvel = False
                        if isValidFloatString(text[3]):
                            morgue[choose][3] = float(text[3])
                        text[3] = "{:+.2e}".format(morgue[choose][3])
                    if bodyvelocity and x >= 920 and x <= 1045 and y >= 425 and y <= 455 and clickon:
                        textyvel = True
                    elif textyvel:
                        textyvel = False
                        if isValidFloatString(text[4]):
                            morgue[choose][4] = float(text[4])
                        text[4] = "{:+.2e}".format(morgue[choose][4])
                    if bodymass and x >= 920 and x <= 1045 and y >= 325 and y <= 355 and clickon:
                        textmass = True
                    elif textmass:
                        textmass = False
                        if isValidFloatString(text[6]):
                            morgue[choose][6] = float(text[6])
                        text[6] = "{:+.2e}".format(morgue[choose][6])
                    if bodycharge and x >= 920 and x <= 1045 and y >= 325 and y <= 355 and clickon:
                        textcharge = True
                    elif textcharge:
                        textcharge = False
                        if isValidFloatString(text[7]):
                            morgue[choose][7] = float(text[7])
                        text[7] = "{:+.2e}".format(morgue[choose][7])
                    if bodyradius and x >= 920 and x <= 1045 and y >= 325 and y <= 355 and clickon:
                        textradius = True
                    elif textradius:
                        textradius = False
                        if isValidFloatString(text[5]):
                            if abs(float(text[5])) > 5 and not speccollisiontest(morgue, choose, morgue[choose][1], morgue[choose][2], abs(float(text[5]))):
                                morgue[choose][5] = abs(float(text[5]))
                        text[5] = "{:+.2e}".format(morgue[choose][5])
            if event.type == pygame.KEYDOWN:
                key = event.key
                if keyon:
                    if key == 303 or key == 304:
                        shift = True
                    else:
                        keyon = False
                        if shift and key == 61:
                            key = 43
                        if shift and key == 101:
                            key = 69
                    for n in range(10):
                        if [textxpos, textypos, textxvel, textyvel, textradius, textmass, textcharge, textscale, texttime, texttimescale][n]:
                            if key == 8 or key == 127:
                                text[n+1] = text[n+1][0:-1]
                                break
                            elif key == 13 or key == 271:
                                for k in range(7):
                                    [textxpos, textypos, textxvel, textyvel, textradius, textmass, textcharge][k] = False
                                break
                            elif key in [45, 43, 46, 101, 69, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 269, 270]:
                                for char in [45, 43, 46, 101, 69, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]:
                                    if key == char:
                                        text[n+1] = text[n+1] + chr(key)
                                        break
                                for char in [256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 269, 270, 271]:
                                    if key == char and char == 269:
                                        text[n+1] = text[n+1] + "-"
                                        break
                                    elif key == char and char == 270:
                                        text[n+1] = text[n+1] + "+"
                                        break
                                    elif key == char and char == 266:
                                        text[n+1] = text[n+1] + "."
                                        break
                                    elif key == char:
                                        text[n+1] = text[n+1] + chr(key-208)
                                        break
                                break
                                    
            if event.type == pygame.KEYUP:
                keyon = True
                if event.key == 303 or event.key == 304:
                    shift = False
            if event.type == pygame.MOUSEBUTTONUP:
                clickon = True
                drag = False
                grasp = True
        else:
            editspace = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y=pygame.mouse.get_pos()
                if x >= 830 and x <= 945 and y >= 735 and y <= 810 and clickon:
                    currentmode = True
                    clickon = False
                if x >= 965 and x <= 1080 and y >= 735 and y <= 810 and clickon:
                    for n in range(len(morgue)):
                        for k in range(1,8):
                            morgue[n][k] = morgue[n][k+7]
                        morgue[n][0] = morgue[n][15]
                    scale = scalesto
                    currentmode = True
                    creation = True
                    clickon = False
            if event.type == pygame.MOUSEBUTTONUP:
                clickon = True
                drag = False
                grasp = True
    if currentmode and creation:
        for n in range(len(morgue)):
            for k in range(1,8):
                morgue[n][k+7] = morgue[n][k]
            morgue[n][15] = morgue[n][0]
        scalesto = scale
    if not editspace:
        movebody = False
        bodyvelocity = False
        bodymass = False
        bodycharge = False
        bodyradius = False
        textxpos = False
        textypos = False
        textxvel = False
        textyvel = False
        textmass = False
        textcharge = False
        textradius = False
    
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
  
  
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
    if not currentmode:
        for ty in range(int(0.025*timescale//dt)):
            f = []
            for n in range(len(morgue)):
                f.append([0, 0])
                if morgue[n][0]:
                    for k in range(len(morgue)):
                        if morgue[k][0] and n != k:
                            rkn = [morgue[k][1]-morgue[n][1], morgue[k][2]-morgue[n][2]]
                            rnk = [-morgue[k][1]+morgue[n][1], -morgue[k][2]+morgue[n][2]]
                            rmag = ((rkn[0])**2 + (rkn[1])**2)**0.5
                            dirkn = [rkn[0]/rmag, rkn[1]/rmag]
                            dirnk = [rnk[0]/rmag, rnk[1]/rmag]
                            if magnetism:
                                b = mu4pi*morgue[k][7]*(morgue[k][3]*rnk[1] - morgue[k][4]*rnk[0])
                                f[n][0] += morgue[n][4]*b
                                f[n][1] += -morgue[n][3]*b
                            if gravity:
                                f[n][0] += dirkn[0]*bigg*morgue[n][6]*morgue[k][6]/(rmag**2)
                                f[n][1] += dirkn[1]*bigg*morgue[n][6]*morgue[k][6]/(rmag**2)
                            if electricity:
                                f[n][0] += dirnk[0]*bigk*morgue[n][7]*morgue[k][7]/(rmag**2)
                                f[n][1] += dirnk[1]*bigk*morgue[n][7]*morgue[k][7]/(rmag**2)
            for n in range(len(morgue)):
                if morgue[n][0]:
                    morgue[n][1] += morgue[n][3]*dt + 0.5*f[n][0]*(dt**2)/morgue[n][6]
                    morgue[n][2] += morgue[n][4]*dt + 0.5*f[n][1]*(dt**2)/morgue[n][6]
                    morgue[n][3] += f[n][0]/morgue[n][6]
                    morgue[n][4] += f[n][1]/morgue[n][6]
            for n in range(len(morgue)):
                if morgue[n][0]:
                    for k in range(len(morgue)):
                        if morgue[k][0] and n != k and ((morgue[k][1] - morgue[n][1])**2 + (morgue[k][2] - morgue[n][2])**2) < (morgue[k][5] + morgue[n][5])**2:
                            morgue[n][5] = (morgue[n][5]**2 + morgue[k][5]**2)**0.5
                            morgue[n][1] = (morgue[n][1]*morgue[n][6] + morgue[k][1]*morgue[k][6])/(morgue[n][6]+morgue[k][6])
                            morgue[n][2] = (morgue[n][2]*morgue[n][6] + morgue[k][2]*morgue[k][6])/(morgue[n][6]+morgue[k][6])
                            morgue[n][3] = (morgue[n][3]*morgue[n][6] + morgue[k][3]*morgue[k][6])/(morgue[n][6]+morgue[k][6])
                            morgue[n][4] = (morgue[n][4]*morgue[n][6] + morgue[k][4]*morgue[k][6])/(morgue[n][6]+morgue[k][6])
                            morgue[n][6] = morgue[n][6] + morgue[k][6]
                            morgue[n][7] = morgue[n][7] + morgue[k][7]
                            morgue[k][0] = False
            pygame.time.delay(int(dt/timescale*1000))

    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
 
    for n in range(len(morgue)):
        if morgue[n][0] and abs(morgue[n][1]) + morgue[n][5] > 390*scale:
            scale = (abs(morgue[n][1]) + morgue[n][5])/390
        if morgue[n][0] and abs(morgue[n][2]) + morgue[n][5] > 390*scale:
            scale = (abs(morgue[n][2]) + morgue[n][5])/390
 
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
     
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(backcolor)
    pygame.draw.rect(screen, spaceblue, [10,10,800,800])
    screen.blit(((pygame.font.Font(None,60)).render("FORCE FIELD",True,black)), [820,10])
    screen.blit(((pygame.font.Font(None,30)).render("by John Bell, IV",True,black)), [880,62])
    screen.blit(((pygame.font.Font(None,30)).render("Scale",True,black)), [820,670])
    screen.blit(((pygame.font.Font(None,20)).render("m/px",True,black)), [922,702])
    pygame.draw.rect(screen, white, [820,695,100,30])
    if bouncebool and textscale:
        screen.blit(((pygame.font.Font(None,27)).render(text[8] + "|",True,black)), [825,697])
    else:
        screen.blit(((pygame.font.Font(None,27)).render(text[8],True,black)), [825,697])
    screen.blit(((pygame.font.Font(None,30)).render("Time Step",True,black)), [960,670])
    screen.blit(((pygame.font.Font(None,25)).render("s",True,black)), [1063,700])
    pygame.draw.rect(screen, white, [960,695,100,30])
    if bouncebool and texttime:
        screen.blit(((pygame.font.Font(None,27)).render(text[9] + "|",True,black)), [965,697])
    else:
        screen.blit(((pygame.font.Font(None,27)).render(text[9],True,black)), [965,697])
    screen.blit(((pygame.font.Font(None,30)).render("Time Scale",True,black)), [960,820])
    screen.blit(((pygame.font.Font(None,20)).render("s/s",True,black)), [1063,850])
    pygame.draw.rect(screen, white, [960,845,100,30])
    if bouncebool and texttimescale:
        screen.blit(((pygame.font.Font(None,27)).render(text[10] + "|",True,black)), [965,847])
    else:
        screen.blit(((pygame.font.Font(None,27)).render(text[10],True,black)), [965,847])
    if gravity:
        screen.blit(gravityon, [890,100])
    else:
        screen.blit(gravityoff, [890,100])
    if electricity:
        screen.blit(electricityon, [960,100])
    else:
        screen.blit(electricityoff, [960,100])
    if magnetism:
        screen.blit(magnetismon, [1030,100])
    else:
        screen.blit(magnetismoff, [1030,100])
    if currentmode:
        if morebody:
            screen.blit(addbodyon, [820,100])
        else:
            screen.blit(addbodyoff, [820,100])
        if creation:
            screen.blit(playbig, [830,735])
        else:
            screen.blit(playsmall, [830,735])
            screen.blit(reset, [965,735])
    else:
        screen.blit(pause, [830,735])
        screen.blit(reset, [955,735])
    pygame.draw.rect(screen, black, [25, 785, int((100*scalebar(scale))//1), 10])
    screen.blit(((pygame.font.Font(None,45)).render("10 m",True,black)), [int((100*scalebar(scale))//2),755])
    screen.blit(((pygame.font.Font(None,25)).render(str(int(scaleexp(scale))+2),True,black)), [int((100*scalebar(scale))//2)+32,748])
    for k in morgue:
        if k[0]:
            if k[7] > 0:
                col = red
            elif k[7] < 0:
                col = blue
            else:
                col = brown
            pygame.draw.circle(screen, col, (int((410+k[1]/scale)//1),int((410-k[2]/scale)//1)), int((k[5]/scale)//1))
    if editspace:
        if morgue[choose][0]:
            if morgue[choose][7] > 0:
                col = red
            elif morgue[choose][7] < 0:
                col = blue
            else:
                col = brown
            pygame.draw.circle(screen, yellow, (int((410+(morgue[choose][1])/scale)//1),int((410-(morgue[choose][2])/scale)//1)), int(((morgue[choose][5])/scale)//1))
            high = 1
            if morgue[choose][5]/scale > 5:
                pygame.draw.circle(screen, col, (int((410+(morgue[choose][1])/scale)//1),int((410-(morgue[choose][2])/scale)//1)), int(((morgue[choose][5])/scale-5)//1))
        pygame.draw.rect(screen, editblue, [830,190,250,470])
        namecount = 0
        for n in range(len(morgue)):
            if morgue[n][0]:
                namecount += 1
                if n == choose:
                    break
        screen.blit(((pygame.font.Font(None,45)).render("Body " + str(namecount),True,black)), [900,205])
        screen.blit(deletebody, [850,250])
        if movebody:
            screen.blit(movebodyon, [850,320])
            screen.blit(((pygame.font.Font(None,30)).render("X-Position",True,black)), [920,300])
            pygame.draw.rect(screen, white, [920,325,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("m",True,black)), [1048,330])
            if bouncebool and textxpos:
                screen.blit(((pygame.font.Font(None,27)).render(text[1] + "|",True,black)), [925,327])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[1],True,black)), [925,327])
            screen.blit(((pygame.font.Font(None,30)).render("Y-Position",True,black)), [920,400])
            pygame.draw.rect(screen, white, [920,425,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("m",True,black)), [1048,430])
            if bouncebool and textypos:
                screen.blit(((pygame.font.Font(None,27)).render(text[2] + "|",True,black)), [925,427])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[2],True,black)), [925,427])
        else:
            screen.blit(movebodyoff, [850,320])
        if bodyvelocity:
            screen.blit(bodyvelocityon, [850,390])
            screen.blit(((pygame.font.Font(None,30)).render("X-Velocity",True,black)), [920,300])
            pygame.draw.rect(screen, white, [920,325,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("m/s",True,black)), [1048,330])
            if bouncebool and textxvel:
                screen.blit(((pygame.font.Font(None,27)).render(text[3] + "|",True,black)), [925,327])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[3],True,black)), [925,327])
            screen.blit(((pygame.font.Font(None,30)).render("Y-Velocity",True,black)), [920,400])
            pygame.draw.rect(screen, white, [920,425,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("m/s",True,black)), [1048,430])
            if bouncebool and textyvel:
                screen.blit(((pygame.font.Font(None,27)).render(text[4] + "|",True,black)), [925,427])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[4],True,black)), [925,427])
        else:
            screen.blit(bodyvelocityoff, [850,390])
        if bodymass:
            screen.blit(bodymasson, [850,460])
            screen.blit(((pygame.font.Font(None,30)).render("Mass",True,black)), [920,300])
            pygame.draw.rect(screen, white, [920,325,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("kg",True,black)), [1048,330])
            if bouncebool and textmass:
                screen.blit(((pygame.font.Font(None,27)).render(text[6] + "|",True,black)), [925,327])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[6],True,black)), [925,327])
        else:
            screen.blit(bodymassoff, [850,460])
        if bodycharge:
            screen.blit(bodychargeon, [850,530])
            screen.blit(((pygame.font.Font(None,30)).render("Charge",True,black)), [920,300])
            pygame.draw.rect(screen, white, [920,325,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("C",True,black)), [1048,330])
            if bouncebool and textcharge:
                screen.blit(((pygame.font.Font(None,27)).render(text[7] + "|",True,black)), [925,327])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[7],True,black)), [925,327])
        else:
            screen.blit(bodychargeoff, [850,530])
        if bodyradius:
            screen.blit(bodyradiuson, [850,600])
            screen.blit(((pygame.font.Font(None,30)).render("Radius",True,black)), [920,300])
            pygame.draw.rect(screen, white, [920,325,125,30])
            screen.blit(((pygame.font.Font(None,25)).render("m",True,black)), [1048,330])
            if bouncebool and textradius:
                screen.blit(((pygame.font.Font(None,27)).render(text[5] + "|",True,black)), [925,327])
            else:
                screen.blit(((pygame.font.Font(None,27)).render(text[5],True,black)), [925,327])
        else:
            screen.blit(bodyradiusoff, [850,600])
        
    screen.blit(((pygame.font.Font(None,70)).render(message,True,red)), [60,350])
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
     
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
    
    if bounceint < 50:
        bounceint += 1
    else:
        bounceint = 0
    if bounceint//25 == 0:
        bouncebool = True
    else:
        bouncebool = False
    # Limit to 20 frames per second
    if currentmode:
        clock.tick(40)
     
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()