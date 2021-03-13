import json
import urllib.request

from tkinter import *
from tkinter import messagebox

'''
contents in order
def drawCard(deckId)
def getValue(card)
def game()
def refreshDealerCards()
def init()
def hasHit()
def hasStand()
graphics initialization

order code runs in
1. mainloop()
2. numPlayerInput() after number of players is inputted
3. game()
4. hasHit() if hit button pressed
5. hasStand() if stand button pressed
6. decision happens if special case in hasHit() or hasStand()
7. Moves on to next player
8. (hasnt been done yet) ask if another player wants to be played or not
'''


def drawCard(deckId):
    req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/' + deckId + '/draw/?count=1',
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    cardData = data['cards'][0]
    return cardData['code']

def getDrawData(deckId):
    req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/' + deckId + '/draw/?count=1',
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

    cardData = data['cards'][0]

    return cardData
    # cardData['code'] returns card code; cardData['image'] returns image of the card

def getValue(card):
    val = card[0:1]
    if(val.isnumeric()):
        if(val=='0'):
            return 10
        else:
            return int(val[0:1])
    elif(val=='A'):
        return 11
    else:
        return 10


def game():
    global labelPlayerTurn
    labelPlayerTurn = Label(root, text = "TURN OF PLAYER " + str(currPlayer), font = ("Verdana", 13))
    labelPlayerTurn.pack()
    labelPlayerTurn.place(x = 5, y = 5)
    req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1',
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    )

    #json file of the deck
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    global deckID, playerList, dealerCards, imageList
    deckID = data['deck_id']

    #filling player list
    #playerList[0] is cards of player 0, playerList[1] is cards of player 1 and so on
    playerList = {}
    imageList = {}
    for x in range(int(numPlayers)):
        playerList[x] = None
        imageList[x] = None
    #filling hands
    for x in range(len(playerList)):
        codeArr = []
        imgArr = []


        #draw once for player
        draw = getDrawData(deckID)
        codeArr.append(draw['code'])
        imgArr.append(draw['image'])

        #draw again
        draw = getDrawData(deckID)
        codeArr.append(draw['code'])
        imgArr.append(draw['image'])

        playerList[x] = codeArr
        imageList[x] = imgArr
    
    global dealerCards
    refreshDealerCards()
    
    
    displayCards()

root = Tk()
root.title("BLACKJACK")
myCanvas = Canvas(root, width = 750, height = 660, bg = "Lime")
myCanvas.pack()
labelPlayers = Label(root, text = "ENTER NUMBER OF PLAYERS:", font = ("Verdana", 13))
labelPlayers.pack()
labelPlayers.place(x = 180, y = 100)

global imageLabelList
imageLabelList = []

def newRound():
    global deckID
    print('OLD DECK: ' + deckID)
    req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1',
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
    )

    #json file of the deck
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    deckID = data['deck_id']
    print("NEW DEKK:" + deckID)
    for x in range(len(playerList)):
        codeArr = []
        imgArr = []


        #draw once for player
        draw = getDrawData(deckID)
        codeArr.append(draw['code'])
        imgArr.append(draw['image'])

        #draw again
        draw = getDrawData(deckID)
        codeArr.append(draw['code'])
        imgArr.append(draw['image'])

        playerList[x] = codeArr
        imageList[x] = imgArr

def refreshResultsText():
    resultsText = ""
    for x in range(int(numPlayers)):
        resultsText+="Player Number " + str(x) + " has " + str(playerWins[x]) + " wins, " + str(playerLosses[x]) + " losses, and " + str(playerTies[x]) + " pushes" + "\n"
    labelResults['text'] = resultsText

def refreshDealerCards():
    global dealerCards, deckID, dealerCardImages
    dealerCards = []
    dealerCardImages = []

    #draw once for dealer
    draw = getDrawData(deckID)
    dealerCards.append(draw['code'])
    dealerCardImages.append(draw['image'])

    #draw again
    draw = getDrawData(deckID)
    dealerCards.append(draw['code'])
    dealerCardImages.append(draw['image'])

    displayCards()

def nextPlayer():
    global currPlayer, nextMove
    nextPlayerButton['state'] = DISABLED
    drawButton['state'] = NORMAL
    hitButton['state'] = NORMAL
    dealerCardsLabel['text'] = "DEALERS REVEALED CARD:"
    if(nextMove=="END"):
        refreshResultsText()
        refreshDealerCards()
        displayCards()
        if(currPlayer<numPlayers-1):
            currPlayer+=1
            refreshDealerCards()
            displayCards()
        else:
            currPlayer=0
            newRound()
            displayCards()
            refreshDealerCards()
        labelPlayerTurn['text'] = "TURN OF PLAYER: " + str(currPlayer)

    elif(currPlayer<numPlayers-1):
        currPlayer+=1
        refreshDealerCards()
        displayCards()
    else:
        currPlayer=0
        newRound()
        displayCards()
        refreshDealerCards()
    labelPlayerTurn['text'] = "TURN OF PLAYER: " + str(currPlayer)
    
    #checking if next player has blackjack
    sum = 0
    for card in playerList[currPlayer]:
        sum+=getValue(card)
    if(sum==21):
        nextPlayerButton['state'] = NORMAL
        dealerSum1 = 0
        for card1 in dealerCards:
            dealerSum1+=getValue(card1)
        if(dealerSum1==21):
            messagebox.showinfo("RESULT", "DEALER AND PLAYER BOTH GOT BLACKJACK, PUSH!")
            playerTies[currPlayer]+=1
            drawButton['state'] = DISABLED
            hitButton['state'] = DISABLED
        else:
            messagebox.showinfo("RESULT", "PLAYER GOT A BLACKJACK AND WON, CONGRATS :D!")
            playerWins[currPlayer]+=1
            drawButton['state'] = DISABLED
            hitButton['state'] = DISABLED

def init(b):
    drawButton.pack()
    drawButton.place(x = 450, y = 550)
    hitButton.pack()
    hitButton.place(x = 650, y = 550)
    nextPlayerButton.pack()
    nextPlayerButton.place(x=650,y=100)
    nextPlayerButton['state']= DISABLED
    dealerCardsLabel.pack()
    dealerCardsLabel.place(x = 5, y = 50)
    playerCardsLabel.pack()
    playerCardsLabel.place(x = 5, y = 290)
    
    global numPlayers
    if(b==players1):
        numPlayers = 1
    if(b==players2):
        numPlayers = 2
    if(b==players3):
        numPlayers = 3
    if(b==players4):
        numPlayers = 4

    players1.destroy()
    players2.destroy()
    players3.destroy()
    players4.destroy()
    labelPlayers.destroy()

    global playerWins, playerTies, playerLosses
    playerWins = []
    playerTies = []
    playerLosses = []
    
    
    for x in range(int(numPlayers)):
        playerWins.append(0)
        playerTies.append(0)
        playerLosses.append(0)

    resultsText = ""
    for x in range(int(numPlayers)):
        resultsText+="Player Number " + str(x) + " has " + str(playerWins[x]) + " wins, " + str(playerLosses[x]) + " losses, and " + str(playerTies[x]) + " pushes" + "\n"
    global labelResults
    labelResults = Label(root, text = resultsText, font = ("Verdana", 11), bg="Red")
    labelResults.place(x = 353,y = 0)

    game()

def hasHit():
    nextMove = "CONTINUE"
    draw = getDrawData(deckID)
    cardToAppend = draw['code']
    playerList[currPlayer].append(cardToAppend)
    imageList[currPlayer].append(draw['image'])
    displayCards()

    sum = 0
    for card in playerList[currPlayer]:
        numAces = 0
        if(card[0:1]=='A' and numAces==0):
            sum+=11
        elif(card[0:1]=='A' and numAces>0):
            sum+=1
        else:
            sum+=getValue(card)
    
    #checking for blackjack or busts, if not then continue normally
    print("CARDS AFTER HITTING: " + str(playerList[currPlayer]) + " , SUM IS " + str(sum))
    print("TESTING- Dealer cards: " + str(dealerCards))
    if(sum>21):
        displayEntireDealer()
        messagebox.showinfo("RESULT","PLAYER " + str(currPlayer) + " BUSTED!")
        nextPlayerButton['state']= NORMAL
        drawButton['state'] = DISABLED
        hitButton['state'] = DISABLED
        playerLosses[currPlayer]+=1
        nextMove = 'END'
    elif(sum==21):
        drawButton['state'] = DISABLED
        hitButton['state'] = DISABLED
        displayEntireDealer()
        dealerSum = getValue(dealerCards[0]) + getValue(dealerCards[1])
        if(dealerSum==21):
            messagebox.showinfo('RESULT", '"DEALER AND PLAYER BOTH GOT A BLACKJACK, ITS A PUSH(TIE)!")
            playerTies[currPlayer]+=1
            nextPlayerButton['state']= NORMAL
        else:
            displayEntireDealer()
            messagebox.showinfo("RESULT","YOU GOT A BLACKJACK, CONGRATULATIONS!")
            playerWins[currPlayer]+=1
            nextPlayerButton['state']= NORMAL
        nextMove = "END"
    refreshResultsText()



def hasStand():
    nextPlayerButton['state']= NORMAL
    drawButton['state'] = DISABLED
    hitButton['state'] = DISABLED
    global currPlayer
    print("DEALERS SECOND CARD: " + str(dealerCards[1]))
    dealerSum = getValue(dealerCards[0]) + getValue(dealerCards[1])
    while(dealerSum<=17):#dealer draws cards til sum >=17
        draw = getDrawData(deckID)
        newCard = draw['code']
        dealerCards.append(newCard)
        dealerCardImages.append(draw['image'])
        displayCards()
        print("DEALER DREW A " + str(dealerCards[len(dealerCards)-1]))
        dealerSum+=(getValue(newCard))
    print("DEALERS CARDS: " + str(dealerCards))
    print("DEALERS SUM: " + str(dealerSum))

    sum = 0
    for card in playerList[currPlayer]:
        numAces = 0
        if(card[0:1]=='A' and numAces==0):
            sum+=11
        elif(card[0:1]=='A' and numAces>0):
            sum+=1
        else:
            sum+=getValue(card)

    
    displayEntireDealer()
    #final outcome
    if(dealerSum>21):
        messagebox.showinfo("RESULT","DEALER BUSTED, YOU WIN!")
        playerWins[currPlayer]+=1
    else:
        if(sum>dealerSum):
            messagebox.showinfo("RESULT",'YOU WIN!')
            playerWins[currPlayer]+=1
            
        elif(sum<dealerSum):
           messagebox.showinfo("RESULT",'YOU LOSE :(')
           playerLosses[currPlayer]+=1
        else:
            messagebox.showinfo("RESULT",'TIED, ITS A PUSH!')
            playerTies[currPlayer]+=1
    refreshResultsText()

def displayEntireDealer():
    dealerCardsLabel['text'] = "DEALERS ENTIRE HAND AFTER DRAWING:"
    count2 = 0
    for card in dealerCardImages:
        dealerCardUrl = card
        
        fileName = str(dealerCards[count2]) + ".jpg"
        

        
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')]
        urllib.request.install_opener(req) #adds the header

        urllib.request.urlretrieve(dealerCardUrl, fileName) #gets the image from url; fileName will be the image's file name
  
        pic = PhotoImage(file=fileName)
        resizedPic = pic.subsample(2, 2)
        
        dealercardImage = Label(root, image = resizedPic )
        dealercardImage.photo = resizedPic #ensures label doesn't stay blank
        dealercardImage.pack()
        dealercardImage.place(x = 5+(112*count2), y = 100)
        dealercardImage.config(width=105, height = 151)

        imageLabelList.append(dealercardImage)
        count2 = count2 + 1

def displayCards():
    
    for label in imageLabelList: #wipes all cards to be added again
        label.destroy()
    imageLabelList.clear()
    

    sum = 0
    for card in playerList[currPlayer]:
        numAces = 0
        if(card[0:1]=='A' and numAces==0):
            sum+=11
        elif(card[0:1]=='A' and numAces>0):
            sum+=1
        else:
            sum+=getValue(card)

    
   
    count = 0
    for card in imageList[currPlayer]:
        

        cardUrl = card
        fileName = str(playerList[currPlayer][count]) + ".jpg"
        

        
        req = urllib.request.build_opener()
        req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')]
        urllib.request.install_opener(req) #adds the header

        urllib.request.urlretrieve(cardUrl, fileName) #gets the image from url; fileName will be the image's file name
  
        pic = PhotoImage(file=fileName)
        resizedPic = pic.subsample(2, 2)
        
        cardImage = Label(root, image = resizedPic )
        cardImage.photo = resizedPic #ensures label doesn't stay blank
        cardImage.pack()
        cardImage.place(x = 5+(112*count), y = 325)
        cardImage.config(width=105, height = 151)

        imageLabelList.append(cardImage)
        count = count + 1
    
    
    dealerCardUrl = dealerCardImages[0]
    
    fileName = str(dealerCards[0]) + ".jpg"
    

    
    req = urllib.request.build_opener()
    req.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36')]
    urllib.request.install_opener(req) #adds the header

    urllib.request.urlretrieve(dealerCardUrl, fileName) #gets the image from url; fileName will be the image's file name

    pic = PhotoImage(file=fileName)
    resizedPic = pic.subsample(2, 2)
    
    dealercardImage = Label(root, image = resizedPic )
    dealercardImage.photo = resizedPic #ensures label doesn't stay blank
    dealercardImage.pack()
    dealercardImage.place(x = 5, y = 100)
    dealercardImage.config(width=105, height = 151)

    imageLabelList.append(dealercardImage)
    

       


players1 = Button(root, height = 5, width = 10, text = "1", command=lambda: init(players1))
players2 = Button(root, height = 5, width = 10, text = "2", command=lambda: init(players2))
players3 = Button(root, height = 5, width = 10, text = "3", command=lambda: init(players3))
players4 = Button(root, height = 5, width = 10, text = "4", command=lambda: init(players4))
players1.pack()
players2.pack()
players3.pack()
players4.pack()
players1.place(x = 180, y = 150)
players2.place(x = 280, y = 150)
players3.place(x = 380, y = 150)
players4.place(x = 480, y = 150)

global nextMove, currPlayer
currPlayer = 0
nextMove = "Continue"
global drawButton, hitButton, nextPlayerButton
global playerCardsLabel, dealerCardsLabel


dealerCardsLabel = Label(root, text = "DEALERS REVEALED CARD:", font = ("Verdana", 11))
playerCardsLabel = Label(root, text = "YOUR CARDS:", font = ("Verdana", 11))
drawButton = Button(root, height = 5, width = 10, text = "HIT", command = lambda: hasHit())
hitButton = Button(root, height = 5, width = 10, text = "STAND", command = lambda: hasStand())


nextPlayerButton = Button(root, height = 5, width = 10, text = "NEXT PLAYER", command = lambda: nextPlayer(), bg="Light blue")
root.mainloop()