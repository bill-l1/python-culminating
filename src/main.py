

#   Python Culminating Task for ICS2O
#   Create a Video Game using Pygame
#               Bill Li

import pygame
import sys
import time
import random
import math

#define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (211, 211, 211)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

#initiate pygame
pygame.init()


#create variables
stageWidth = 1360
stageHeight = 700
size = (stageWidth, stageHeight)
screen = pygame.display.set_mode(size)
logo = pygame.image.load("recipeskull.png")
pygame.display.set_icon(logo)
pygame.display.set_caption("The Bone Zone")

#game loop controllers
mainMenu = False
done = False
gameOver = False
 
clock = pygame.time.Clock()

topBar = pygame.image.load("topbar.png")
botBar = pygame.image.load("botbar.png")

currentRoom = 0
roomMoulding = pygame.image.load("mouldingroom.png")
roomAnimatron = pygame.image.load("animatronroom.png")
roomCheckout = pygame.image.load("checkoutroom.png")
roomSnail = pygame.image.load("recipesnail.png")
roomBee = pygame.image.load("recipebee.png")
roomSnake = pygame.image.load("recipesnake.png")
roomFish = pygame.image.load("recipefish.png")
roomCow = pygame.image.load("recipecow.png")
roomDragon = pygame.image.load("recipedragon.png")

topBarGroup = pygame.sprite.LayeredUpdates()
roomGroup = pygame.sprite.LayeredUpdates()
botBarGroup = pygame.sprite.LayeredUpdates()
slotGroup = pygame.sprite.LayeredUpdates()

inventoryText = pygame.font.SysFont('trebuchetms', 18)
mouldText = pygame.font.SysFont('trebuchetms', 24)
moneyText = pygame.font.SysFont('trebuchetms', 30)


holding = False

#inventory/item values

skulls = 0 #1
shortbones = 0 #2,3
longbones = 0 #4,5
curvedbones = 0 #6,7,8,9
dusts = 0 #5

#if there is extra dust inside the moulds, this will keep track of how many are stored in which mould
moulds = [0, 0, 0, 0]

#when objects are placed in the animatron, recipeSquares is updated
recipeSquares = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]

#recipes to check with recipeSquares
recipeEmpty = [[0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0]]

recipeSnail = [[0, 0, 0, 0, 0],
               [0, 0, 1, 0, 0],
               [0, 0, 0, 0, 0]]

recipeBee = [[0, 0, 0, 0, 0],
               [0, 3, 1, 0, 0],
               [0, 0, 0, 0, 0]]

recipeSnake = [[0, 0, 0, 0, 0],
               [0, 3, 5, 1, 0],
               [0, 0, 0, 0, 0]]

recipeFish = [[0, 0, 2, 0, 0],
               [0, 0, 5, 1, 0],
               [0, 0, 2, 0, 0]]

recipeCow = [[0, 0, 0, 0, 0],
               [0, 7, 5, 3, 1],
               [0, 2, 0, 2, 0]]

recipeDragon = [[8, 5, 5, 9, 0],
               [7, 5, 5, 3, 1],
               [0, 2, 0, 2, 0]]

#preloading surfaces to place in an array
objectSkull = pygame.image.load("objectskull.png")
objectShortbone = pygame.image.load("objectshortbone.png")
objectLongbone = pygame.image.load("objectlongbone.png")
objectCurvedbone = pygame.image.load("objectcurvedbone.png")
objectDust = pygame.image.load("objectdust.png")
objectSnail = pygame.image.load("objectsnail.png")
objectBee = pygame.image.load("objectbee.png")
objectSnake = pygame.image.load("objectsnake.png")
objectFish = pygame.image.load("objectfish.png")
objectCow = pygame.image.load("objectcow.png")
objectDragon = pygame.image.load("objectdragon.png")

holdObjects = [0, objectSkull, objectShortbone, objectLongbone, objectCurvedbone, objectDust, objectSnail, objectBee, objectSnake, objectFish, objectCow, objectDragon]

#used for the animatron, that shows if your creation failed or not
noticeText = "-"

#-1 patience means that there is no customer, above 0 means that there is one
patience = -1
#[0,0,0] means there is no customer, array shows what objects need to be placed to complete an order
order = [0,0,0]
#reward for the current customer's order
reward = 0

#current money
money = 20

#after a customer's order is complete, the timer starts
customerTimer = 0
rentTimer = 0

#how long it takes depends on this variable
customerTimerMax = 300
rentTimerMax = 1260

#level that determines how much rent needs to be paid
rentLevel = 0

moneyUpdate = 0
moneyUpdateTimer = 0
moneyUpdateTimerMax = 30

difficultyLevel = 0

#rating is 0 here, but it is set to 1 when the game is initialized
rating = 0.00

#flavor text that gives a reason why you lost in the game over screen
loseText = ""

# I create class files to interact with mouse click because it allows me to organize which functions I need called for each condition.
# All the class files are labelled button, because that's what they are essentially.
# The functions inside the class are the same for every sprite:
# __init__, essential
# onClick, called from checkClick function, which is when the MOUSEBUTTONDOWN event is triggered.
# onRelease, same thing but with MOUSEBUTTONUP
# changeImage, only on some if I need to update what the sprite looks like

#for inventory buttons that appear in the top bar
#holding down on them will drag out an object to hold
class InventoryButton(pygame.sprite.Sprite):
    def __init__(self, Type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("inventory"+Type+".png")
        self.type = Type
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        global holding
        global skulls
        global shortbones
        global longbones
        global curvedbones
        global dusts
        
        if(self.type == "skull" and skulls > 0):
             holding = 1
             skulls -= 1
        if(self.type == "shortbone" and shortbones > 0):
             holding = 2
             shortbones -= 1
        if(self.type == "longbone" and longbones > 0):
             holding = 3
             longbones -= 1
        if(self.type == "curvedbone" and curvedbones > 0):
             holding = 4
             curvedbones -= 1
        if(self.type == "dust" and dusts > 0):
             holding = 5
             dusts -= 1
        if(self.type == "snail"):
            holding = 6
            self.type = empty

        self.image = pygame.image.load("inventory"+self.type+".png")
       

    def onRelease(self):
        print "e"

#for the slot that holds the skeleton, basically does the same thing as InventoryButton but it's more specific
class SkeletonSlot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("inventoryempty.png")
        self.type = "empty"
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        global holding
        if(self.type == "snail"):
            self.type = "empty"
            holding = 6
        elif(self.type == "bee"):
            self.type = "empty"
            holding = 7
        elif(self.type == "snake"):
            self.type = "empty"
            holding = 8
        elif(self.type == "fish"):
            self.type = "empty"
            holding = 9
        elif(self.type == "cow"):
            self.type = "empty"
            holding = 10
        elif(self.type == "dragon"):
            self.type = "empty"
            holding = 11
            
        self.changeImage()

    def onRelease(self):
        print "e"

        

    def changeImage(self):
        self.image = pygame.image.load("inventory"+self.type+".png")



#sprite for the moulds, checks if there's sufficient dust inside to produce bones
class MouldButton(pygame.sprite.Sprite):
    def __init__(self, Type, Dusts, Limit, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("mould"+Type+".png")
        self.type = Type
        self.dusts = Dusts
        self.limit = Limit
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y
        print self.limit

    def onClick(self):
        global shortbones
        global longbones
        global curvedbones
        global skulls
        global moulds

        if(self.type == "skull" and self.dusts >= self.limit):
            self.dusts -= self.limit
            moulds[0] = self.dusts
            skulls += 1
        if(self.type == "shortbone" and self.dusts >= self.limit):
            self.dusts -= self.limit
            moulds[1] = self.dusts
            shortbones += 1
        if(self.type == "longbone" and self.dusts >= self.limit):
            self.dusts -= self.limit
            moulds[2] = self.dusts
            longbones += 1
        if(self.type == "curvedbone" and self.dusts >= self.limit):
            self.dusts -= self.limit
            moulds[3] = self.dusts
            curvedbones += 1
        
            
    def onRelease(self):
        global holding
        global dusts
        global moulds
        if(holding == 5):
            dusts -= 1
            self.dusts += 1
            if(self.type == "skull"):
                moulds[0] = self.dusts
            if(self.type == "shortbone"):
                moulds[1] = self.dusts
            if(self.type == "longbone"):
                moulds[2] = self.dusts
            if(self.type == "curvedbone"):
                moulds[3] = self.dusts
        


#for any other sprites that I need that I feel don't require their own sprite type
class MiscButton(pygame.sprite.Sprite):
    def __init__(self, Type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(Type+".png")
        self.type = Type
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        if(self.type == "recipebutton"):
            global currentRoom
            if(currentRoom > 2):
                initRoom(1)
            else:
                initRoom(3)
        elif(self.type == "arrowleft"):
            global currentRoom
            initRoom(currentRoom-1)
        elif(self.type == "arrowright"):
            global currentRoom
            initRoom(currentRoom+1)
        elif(self.type == "animatronbutton"):
            global noticeText
            for target in slotGroup:
                slot = target

            if(recipeSquares == recipeSnail):
                slot.type = "snail"
                noticeText = "SUCCESSFUL"
            elif(recipeSquares == recipeBee):
                slot.type = "bee"
                noticeText = "SUCCESSFUL"
            elif(recipeSquares == recipeSnake):
                slot.type = "snake"
                noticeText = "SUCCESSFUL"
            elif(recipeSquares == recipeFish):
                slot.type = "fish"
                noticeText = "SUCCESSFUL"
            elif(recipeSquares == recipeCow):
                slot.type = "cow"
                noticeText = "SUCCESSFUL"
            elif(recipeSquares == recipeDragon):
                slot.type = "dragon"
                noticeText = "SUCCESSFUL"
            else:
                noticeText = "FAILED"
            slot.changeImage()
            
            for target in roomGroup:
                target.value = 0
                target.changeImage()
            
        elif(self.type == "buydust"):
            global dusts
            global money
            if(money-5 >= 0):
                dusts += 1
                addMoney(-1)

        elif(self.type == "switchmoulding"):
            initRoom(0)
        elif(self.type == "switchanimatron"):
            initRoom(1)
        elif(self.type == "switchcheckout"):
            initRoom(2)
        

    def onRelease(self):
        print "e"

    def changeImage(self):
        print "e"


# This feature ended up being unused, it slowed down gameplay from having to click another time for no reason
class AnimatronSlot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("animatronempty.png")
        self.type = "empty"
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        global slotGroup
        if(self.type == "snail"):
            self.type = "empty"
            for slot in slotGroup:
                slot.value = "snail"
                slot.changeImage()
                
            
        self.changeImage()

    def onRelease(self):
        print "e"

        

    def changeImage(self):
        self.image = pygame.image.load("animatron"+self.type+".png")




# This is the square sprite in the Animatron:
# onClick rotates the object that is currently inside it.
# onRelease checks if player is holding an object then changes its image to match the object that was placed inside
class RecipeSquare(pygame.sprite.Sprite):
    def __init__(self, ArrayPos, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.arrayPos = ArrayPos
        global recipeSquares
        self.value = recipeSquares[ArrayPos[0]][ArrayPos[1]]
        self.changeImage()
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        global skulls
        global shortbones
        global longbones
        global curvedbones
        if(self.value == 1):
            self.value = 0
            skulls += 1
        elif(self.value == 3):
            self.value = 0
            shortbones += 1
        elif(self.value == 5):
            self.value = 0
            longbones += 1
        elif(self.value == 9):
            self.value = 0
            curvedbones += 1
        elif(self.value == 2 or self.value == 4 or self.value == 6 or self.value == 7 or self.value == 8):
            self.value += 1
        
        self.changeImage()

    def onRelease(self):
        global holding
        global recipeSquares
        if(holding > 0 and holding != 5):
            if(holding == 1):
                global skulls
                self.value = 1
                skulls -= 1

            elif(holding == 2):
                global shortbones
                self.value = 2
                shortbones -= 1
                
            elif(holding == 3):
                global longbones
                self.value = 4
                longbones -= 1

            elif(holding == 4):
                global curvedbones
                self.value = 6
                curvedbones -= 1
                
            self.changeImage()
        
    def changeImage(self):
        recipeSquares[self.arrayPos[0]][self.arrayPos[1]] = self.value 
        if(self.value == 0):
            self.image = pygame.image.load("recipeempty.png")
        elif(self.value == 1):
            self.image = pygame.image.load("recipeskull.png")
        elif(self.value == 2):
            self.image = pygame.image.load("recipeshortbone0.png")
        elif(self.value == 3):
            self.image = pygame.image.load("recipeshortbone1.png")
        elif(self.value == 4):
            self.image = pygame.image.load("recipelongbone0.png")
        elif(self.value == 5):
            self.image = pygame.image.load("recipelongbone1.png")
        elif(self.value == 6):
            self.image = pygame.image.load("recipecurvedbone0.png")
        elif(self.value == 7):
            self.image = pygame.image.load("recipecurvedbone1.png")
        elif(self.value == 8):
            self.image = pygame.image.load("recipecurvedbone2.png")
        elif(self.value == 9):
            self.image = pygame.image.load("recipecurvedbone3.png")



# Customer sprite, self explanatory
# onRelease checks if the object in order array matches what object the player is holding
class Customer(pygame.sprite.Sprite):
    def __init__(self, Image, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(Image+".png")
        self.rect = pygame.Rect((0, 0), self.image.get_size())
        self.rect.x = x
        self.rect.y = y

    def onClick(self):
        print "e"
        
    def onRelease(self):
        global holding
        global order
        global slotGroup
        if(order[0] == holding):
            order[0] = 0
            holding = 0
        elif(order[1] == holding):
            order[1] = 0
            holding = 0
        elif(order[2] == holding):
            order[2] = 0
            holding = 0



        
# initiating function for the game: adds all the necessary sprites(buttons) to the top and bottom bars,
# placing them in the topBarGroup and botBarGroup sprite groups           
def initGame():
    global customerTimer
    global customerTimerMax
    global rentTimer
    global rentTimerMax
    global rating
    global rentLevel

    inventorySkull = InventoryButton("skull", 20, 20)
    topBarGroup.add(inventorySkull)

    inventoryShortBone = InventoryButton("shortbone", 140, 20)
    topBarGroup.add(inventoryShortBone)

    inventoryLongBone = InventoryButton("longbone", 260, 20)
    topBarGroup.add(inventoryLongBone)

    inventoryCurvedBone = InventoryButton("curvedbone", 380, 20)
    topBarGroup.add(inventoryCurvedBone)

    inventoryDust = InventoryButton("dust", 500, 20)
    topBarGroup.add(inventoryDust)

    recipeButton = MiscButton("recipebutton", 1200, 20)
    topBarGroup.add(recipeButton)
    
    skeletonSlot = SkeletonSlot(850, 20)
    slotGroup.add(skeletonSlot)

    switchMoulding = MiscButton("switchmoulding", 20, 620)
    botBarGroup.add(switchMoulding)

    switchAnimatron = MiscButton("switchanimatron", 280, 620)
    botBarGroup.add(switchAnimatron)

    switchCheckout = MiscButton("switchcheckout", 540, 620)
    botBarGroup.add(switchCheckout)

    rentLevel = 5
    
    customerTimer = customerTimerMax
    rentTimer = rentTimerMax

    rating = 1.00


#initializes room-specific sprites, placing them in the roomGroup sprite group
def initRoomObjects(Room):
    global roomGroup
    global moulds
    roomGroup = pygame.sprite.LayeredUpdates()
    if(Room == 0):
        # Moulding
        global moulds
        
        mouldSkull = MouldButton("skull", moulds[0], 3, 500, 170)
        roomGroup.add(mouldSkull)

        mouldShortBone = MouldButton("shortbone", moulds[1], 1, 700, 170)
        roomGroup.add(mouldShortBone)

        mouldLongBone = MouldButton("longbone", moulds[2], 2, 900, 170)
        roomGroup.add(mouldLongBone)

        mouldCurvedBone = MouldButton("curvedbone", moulds[3], 3, 1100, 170)
        roomGroup.add(mouldCurvedBone)

        buyDust = MiscButton("buydust", 90, 485)
        roomGroup.add(buyDust)
        

    elif(Room == 1):
        # Animatron
        global recipeSquares
        room = pygame.image.load("animatronroom.png")

        #double for loop that uses the recipeSquares array to know how many square sprites to initialize
        for row in range(len(recipeSquares)):
            for column in  range(len(recipeSquares[row])):
                newsquare = RecipeSquare([row, column], 120+column*135, 240+row*110)
                roomGroup.add(newsquare)

        animatronButton = MiscButton("animatronbutton", 900, 400)
        roomGroup.add(animatronButton)

        animatronSlot = AnimatronSlot(1050, 400)
        roomGroup.add(animatronSlot)
    elif(Room == 2):
        #checkout
        global patience
        global noticeText
        customerSprite = Customer("customergrey", 400, 360)
        roomGroup.add(customerSprite)
        orderSprite = Customer("orderbox", 530, 180)
        roomGroup.add(orderSprite)
        noticeText = "-"

    #recipe book is counted as seperate rooms, these initialize the arrows
    elif(Room == 3):
        rightArrow = MiscButton("arrowright", 1200, 500)
        roomGroup.add(rightArrow)

    elif(Room == 4 or Room == 5 or Room == 6 or Room == 7):
        leftArrow = MiscButton("arrowleft", 50, 500)
        roomGroup.add(leftArrow)
        
        rightArrow = MiscButton("arrowright", 1200, 500)
        roomGroup.add(rightArrow)
        
    elif(Room == 8):
        leftArrow = MiscButton("arrowleft", 50, 500)
        roomGroup.add(leftArrow)

# draws the sprites in the topBarGroup sprite group and text
def drawTopBar():
    screen.blit(topBar, (0, 0))
    topBarGroup.draw(screen)
    slotGroup.draw(screen)
    
    global skulls
    global shortbones
    global longbones
    global curvedbones
    global dusts
    global money
    global moneyUpdate
    global moneyUpdateTimer
    
    skullText = inventoryText.render(str(skulls), False, WHITE)
    screen.blit(skullText, (100, 100))
    
    shortBoneText = inventoryText.render(str(shortbones), False, WHITE)
    screen.blit(shortBoneText, (220, 100))

    longBoneText = inventoryText.render(str(longbones), False, WHITE)
    screen.blit(longBoneText, (340, 100))

    curvedBoneText = inventoryText.render(str(curvedbones), False, WHITE)
    screen.blit(curvedBoneText, (460, 100))

    dustText = inventoryText.render(str(dusts), False, WHITE)
    screen.blit(dustText, (580, 100))

    moneySprite = pygame.image.load("money.png")
    screen.blit(moneySprite, (650, 45))
    
    Money = moneyText.render(str(money), False, WHITE)
    screen.blit(Money, (720, 50))

    if(moneyUpdateTimer > 0):
        if(moneyUpdate < 0):
            moneyUpdateText = str(moneyUpdate)
        else:
            moneyUpdateText = "+"+str(moneyUpdate)
        MoneyUpdate = moneyText.render(moneyUpdateText, False, WHITE)
        screen.blit(MoneyUpdate, (760, 50))

    if(currentRoom >= 3):
        recipeExit = pygame.image.load("recipeexit.png")
        screen.blit(recipeExit, (1200, 20))

# draws the sprites in the roomGroup sprite group and text
def drawRoom(Room):
    if(Room == 0):
        global moulds
        screen.blit(roomMoulding, (0, 140))
        
        skullMouldText = mouldText.render(str(moulds[0])+"/3", False, RED)
        screen.blit(skullMouldText, (545, 400))
        
        shortBoneMouldText = mouldText.render(str(moulds[1])+"/1", False, RED)
        screen.blit(shortBoneMouldText, (745, 400))

        longBoneMouldText = mouldText.render(str(moulds[2])+"/2", False, RED)
        screen.blit(longBoneMouldText, (945, 400))

        curvedBoneMouldText = mouldText.render(str(moulds[3])+"/3", False, RED)
        screen.blit(curvedBoneMouldText, (1145, 400))
    elif(Room == 1):
        global noticeText
        screen.blit(roomAnimatron, (0, 140))
        
        animatronText = mouldText.render(noticeText, False, RED)
        screen.blit(animatronText, (1000, 550))
    elif(Room == 2):
        global patience
        global customerTimer
        screen.blit(roomCheckout, (0, 140))

        if(patience != -1):        
            patienceText = mouldText.render("Patience", False, BLACK)
            screen.blit(patienceText, (800, 260))

            patienceBackRect = pygame.Rect(800, 300, 400, 30)
            pygame.draw.rect(screen, RED, patienceBackRect)
            
            patienceFrontRect = pygame.Rect(800, 300, 400*float(patience/100), 30)
            pygame.draw.rect(screen, GREEN, patienceFrontRect)
        else:
            patienceText = moneyText.render("Next customer in: "+str(int(math.ceil(customerTimer/60))), False, BLACK)
            screen.blit(patienceText, (500, 300))
        
    elif(Room == 3):
        screen.blit(roomSnail, (0, 140))
    elif(Room == 4):
        screen.blit(roomBee, (0, 140))
    elif(Room == 5):
        screen.blit(roomSnake, (0, 140))
    elif(Room == 6):
        screen.blit(roomFish, (0, 140))
    elif(Room == 7):
        screen.blit(roomCow, (0, 140))
    elif(Room == 8):
        screen.blit(roomDragon, (0, 140))
    if(Room != 2 or patience > 0):
        roomGroup.draw(screen)
    
    if(Room == 2):
        global patience
        global roomGroup
        if(patience > 0):
            global order
            
            texts = ["23123", "123123", "123213"]
            
            for i in range(len(order)):
                if(order[i] == 0):
                    texts[i] = "-"
                elif(order[i] == 6):
                    texts[i] = "snail"
                elif(order[i] == 7):
                    texts[i] = "bee"
                elif(order[i] == 8):
                    texts[i] = "snake"
                elif(order[i] == 9):
                    texts[i] = "fish"
                elif(order[i] == 10):
                    texts[i] = "cow"
                elif(order[i] == 11):
                    texts[i] = "dragon"
            
            
            
            order0 = inventoryText.render(texts[0], False, BLACK)
            screen.blit(order0, (545, 200))

            order1 = inventoryText.render(texts[1], False, BLACK)
            screen.blit(order1, (545, 230))

            order2 = inventoryText.render(texts[2], False, BLACK)
            screen.blit(order2, (545, 260))

# draws the sprites in the botBarGroup sprite group and text            
def drawBotBar():
    global rating
    global rentTimer
    global rentLevel
    screen.blit(botBar, (0, 610))
    botBarGroup.draw(screen)
    
    ratingText = moneyText.render("Rating: "+str(rating), False, YELLOW)
    screen.blit(ratingText, (830, 635))

    rentText = moneyText.render("Next lease ("+str(rentLevel)+") in: "+str(int(math.ceil(rentTimer/60))), False, WHITE)
    screen.blit(rentText, (1030, 635))


#function that is called whenever MOUSEBUTTONDOWN event is triggered
#checks every sprite in each sprite group to see if the mouse was over it when the mouse was clicked
def checkClick():
    for target in topBarGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onClick()

    for target in roomGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onClick()
    
    for target in botBarGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onClick()

    for target in slotGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onClick()

#function that is called whenever MOUSEBUTTONUP event is triggered
#checks every sprite in each sprite group to see if the mouse was over it when the mouse was released
def checkRelease():
    for target in topBarGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onRelease()

    for target in roomGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onRelease()
    
    for target in botBarGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onRelease()

    for target in slotGroup:
        if(target.rect.collidepoint(pygame.mouse.get_pos())):
           target.onRelease()


    #if the player was holding an object, releasing it in midair will place it back to where it came from   
    global holding
    if(holding == 1):
        global skulls
        skulls += 1
    elif(holding == 2):
        global shortbones
        shortbones += 1
    elif(holding == 3):
        global longbones
        longbones += 1
    elif(holding == 4):
        global curvedbones
        curvedbones += 1
    elif(holding == 5):
        global dusts
        dusts += 1
    elif(holding == 6):
        for slot in slotGroup:
            slot.type = "snail"
            slot.changeImage()
    elif(holding == 7):
        for slot in slotGroup:
            slot.type = "bee"
            slot.changeImage()
    elif(holding == 8):
        for slot in slotGroup:
            slot.type = "snake"
            slot.changeImage()
    elif(holding == 9):
        for slot in slotGroup:
            slot.type = "fish"
            slot.changeImage()
    elif(holding == 10):
        for slot in slotGroup:
            slot.type = "cow"
            slot.changeImage()
    elif(holding == 11):
        for slot in slotGroup:
            slot.type = "dragon"
            slot.changeImage()
            
    holding = 0

# unneccessary function (could just move currentRoom = Room into initRoomObjects,
# too much of a pain to remove though
def initRoom(Room):
    global currentRoom
    currentRoom = Room
    initRoomObjects(currentRoom)

#if the player is holding something, this draws correct object and places it so it's centered
def drawHoldObject():
    global holdObjects
    global holding
    if(holding > 0):
        drawObject = holdObjects[holding]
        mousePos = pygame.mouse.get_pos()
        screen.blit(drawObject, (mousePos[0]-drawObject.get_width()/2, mousePos[1]-drawObject.get_height()/2))
    

#spawns a new customer
def customerCreate():
    global patience
    global order
    global reward
    global difficultyLevel
    
    order0 = 0
    order1 = 0
    order2 = 0
    
    #creates a new randomly generated order depending on the current difficulty level
    #order value corresponds with the holding value of the skeleton
    if(difficultyLevel == 0):
        rng = random.randint(0, 1)
        if(rng == 0):
            order0 = 6
        elif(rng == 1):
            order0 = 7
    if(difficultyLevel == 1):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 6
            order1 = 6
        elif(rng == 1):
            order0 = 7
        elif(rng == 2):
            order0 = 7
            order1 = 6
    if(difficultyLevel == 2):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 7
            order1 = 6
        elif(rng == 1):
            order0 = 7
            order1 = 7
        elif(rng == 2):
            order0 = 6
            order1 = 6
            order2 = 6
    if(difficultyLevel == 3):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 8
        elif(rng == 1):
            order0 = 8
            order1 = 6
        elif(rng == 2):
            order0 = 7
            order1 = 7
            order2 = 6
    if(difficultyLevel == 4):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 8
            order1 = 7
        elif(rng == 1):
            order0 = 8
            order1 = 6
        elif(rng == 2):
            order0 = 9
    if(difficultyLevel == 5):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 8
            order1 = 8
        elif(rng == 1):
            order0 = 9
            order1 = 6
        elif(rng == 2):
            order0 = 8
            order1 = 7
    if(difficultyLevel == 6):
        rng = random.randint(0, 2)
        if(rng == 0):
            order0 = 8
            order1 = 9
            order2 = 6
        elif(rng == 1):
            order0 = 9
            order1 = 7
        elif(rng == 2):
            order0 = 8
            order1 = 8
    if(difficultyLevel == 7):
        rng = random.randint(0, 3)
        if(rng == 0):
            order0 = 9
            order1 = 9
        elif(rng == 1):
            order0 = 9
            order1 = 8
        elif(rng == 2):
            order0 = 10
        elif(rng == 3):
            order0 = 8
            order1 = 8
            order2 = 7
    if(difficultyLevel == 8):
        rng = random.randint(0, 3)
        if(rng == 0):
            order0 = 10
            order1 = 6
        elif(rng == 1):
            order0 = 9
            order1 = 9
            order2 = 6
        elif(rng == 2):
            order0 = 10
        elif(rng == 3):
            order0 = 9
            order1 = 8
            order2 = 7
    if(difficultyLevel == 9):
        rng = random.randint(0, 4)
        if(rng == 0):
            order0 = 10
            order1 = 9
        elif(rng == 1):
            order0 = 9
            order1 = 9
            order2 = 9
        elif(rng == 2):
            order0 = 10
            order1 = 10
        elif(rng == 3):
            order0 = 11
        elif(rng == 4):
            order0 = 10
            order1 = 8
            order2 = 7
    if(difficultyLevel == 10):
        rng = random.randint(0, 4)
        if(rng == 0):
            order0 = 11
            order1 = 10
        elif(rng == 1):
            order0 = 11
            order1 = 6
            order2 = 9
        elif(rng == 2):
            order0 = 10
            order1 = 10
            order2 = 8
        elif(rng == 3):
            order0 = 11
            order1 = 9
        elif(rng == 4):
            order0 = 10
            order1 = 10
            order2 = 10
    #places it into the order array
    order = [order0, order1, order2]
    
    #calculates the money earned for the player when the order is completed
    for i in order:
        if(i == 6):
            reward += 5
        elif(i == 7):
            reward += 7
        elif(i == 8):
            reward += 12
        elif(i == 9):
            reward += 17
        elif(i == 10):
            reward += 21
        elif(i == 11):
            reward += 32
    #resets patience meter
    patience = 100.00

#when customer's order is complete, calculates rating and adds to reward and resets everything
def customerFinish():
    global patience
    global money
    global reward

    bonus = 0
    if(patience > 65):
        addRating(1.5)
        bonus = reward*0.2
    elif(patience <= 65 and patience > 10):
        addRating(round(patience/65, 2))
    elif(patience <= 10):
        addRating(-round((1-patience/10)/2, 2))
    patience = -1
    addMoney(int(math.ceil(reward+bonus)))
    reward = 0
    
#when patience gets below 0, reduce rating and resets everything
def customerTimeOut():
    global patience
    global order
    global reward
    patience = -1
    addRating(-1)
    order = [0, 0, 0]
    reward = 0

#reduces money every so often
#rent needs to be paid more as time goes on
def payRent():
    global money
    global rentLevel
    addMoney(-rentLevel)
    rentLevel += 1


#function for adding or subtracting money,
#updates the text near it to show how much it changed by
def addMoney(Money):
    global money
    global moneyUpdate
    global moneyUpdateTimer
    global moneyUpdateTimerMax
    
    money += Money
    moneyUpdate = Money
    moneyUpdateTimer = moneyUpdateTimerMax

#function for adding or subtracting rating
def addRating(Rating):
    global rating
    rating += Rating

#main menu loop before game starts
while not mainMenu:

    screen.fill(WHITE)

    mainmenutext2 = inventoryText.render("Press space to play", False, BLACK)
    screen.blit(mainmenutext2, (600, 400))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainMenu = True
            done = True
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                mainMenu = True

    pygame.display.flip()
    clock.tick(60)

#starts the game
initGame()
initRoom(0)

#main game loop
while not done:

    #events
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                initRoom(0)
            if event.key == pygame.K_s:
                initRoom(1)
            if event.key == pygame.K_d:
                initRoom(2)
        if event.type == pygame.MOUSEBUTTONUP:
            checkRelease()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            checkClick()

    #a bunch of if statements to check for different things
    if(patience > 0):
        patience -= 0.05

    if(order[0] == 0 and order[1] == 0 and order[2] == 0 and patience > 0):
        customerFinish()

        
    if(patience <= 0 and order[0] != 0 and order[1] != 0 and order[2] != 0):
        customerTimeOut()
    

    if(rentTimer <= 0):
        payRent()
        rentTimer = rentTimerMax
    if(customerTimer <= 0):
        customerCreate()
        customerTimer = customerTimerMax

    if(moneyUpdateTimer > 0):
        moneyUpdateTimer -= 1
    
    rentTimer -= 1
    if(patience == -1):
        customerTimer -= 1

    #determines difficulty level based on rating
    difficultyLevel = int(math.floor(rating-1)/3)
    print difficultyLevel

    #checks if rating or money goes below 0 to end the game
    if(rating < 0):
        loseText = "Your store's service was horrible!"
        done = True

    if(money < 0):
        loseText = "You went bankrupt!"
        done = True


    screen.fill(WHITE)


    drawTopBar()
    drawRoom(currentRoom)
    drawBotBar()
    drawHoldObject()
    

    pygame.display.flip()
 

    clock.tick(60)

#main game loop finishes when the player loses, goes to this loop instead
#shows the game over screen
while not gameOver:

    screen.fill(WHITE)

    mainmenutext = inventoryText.render("Game Over!", False, BLACK)
    mainmenutext2 = inventoryText.render(loseText, False, BLACK)
    screen.blit(mainmenutext, (650, 300))
    screen.blit(mainmenutext2, (600, 400))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainMenu = True
            done = True
            gameOver = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gameOver = True

    pygame.display.flip()
    clock.tick(60)



pygame.quit()
