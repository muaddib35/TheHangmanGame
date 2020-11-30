import os
import time
import random



# ********** Global Variables ****************
FILENAME = "words.txt" # dictionary file name
DICTIONARY = []
PICKEDWORDS = []
SELECTEDWORD = ""
FOUNDCHARS = []
PLAYERCHARS = []
PLAYERTURN = 0
GAMEMESSAGE = "You are waiting in a cold cell ..."

LOSTMESSAGES = ["And the bells begins to chime", "You doesn't too much time", "Sands of time for you are running low", "They take you to the Gallows Pole", "To the Gallows Pole ...", "Hallowed be thy name"]
FOUNDMESSAGE = ["You were lucky !", "Hmmmm.... You found it !", "Bravo !", "Good choice !"]


"""
ASCII Hangmans drawn by Chris Horton (https://gist.github.com/chrishorton)
"""

HANGMANS = ['''
  +---+
  |   |
      |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
      |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
  |   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========''', '''
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========''']



def formatSelectedWord():
    """
        formats words like _ A _ D _
    """
    global SELECTEDWORD
    global FOUNDCHARS
    jokerChar = "_"
    seperator = " "

    result = ""
    for i in range(0, len(SELECTEDWORD)-1):
        if SELECTEDWORD[i] in FOUNDCHARS:
            result += SELECTEDWORD[i]
        else:
            result += jokerChar
        if i != len(SELECTEDWORD):    
            result += seperator
    
    return result


def checkWord():
    global SELECTEDWORD
    global FOUNDCHARS
    created = ""
    for i in range(0, len(SELECTEDWORD)-1):
        
        if SELECTEDWORD[i] in FOUNDCHARS:
            created += SELECTEDWORD[i]
    if created.strip() == SELECTEDWORD.strip():
        return True
    else:
        return False



def pickaWord():
    """
        randomly selects a word from dictionary array
    """
    global DICTIONARY
    global SELECTEDWORD
    theWord = random.sample(DICTIONARY,1)
    if theWord[0] in SELECTEDWORD:
        pickaWord()
    else:
        SELECTEDWORD = theWord[0]

def inputCharacter():
    """
        Oyuncu sadece karakter girebilmeli onu kontrol edip kullanıyoruz ...
    """
    CHARACTERS = ['A','B','C','D','E','F','G','H',
    'I','J','K','L','M', 'N', 'O', 'P','R','S','T','U','W','X','V','Y','Z']
    result = ""
    while result not in CHARACTERS:
        result = input("Please enter a character (type qq to exit game) : ")
        if result == "qq" or result == "QQ":
            exit()
            

        if result.upper() in CHARACTERS:
            return result.upper()
   


def loadDictionary():
    """
        Loads dictionary from text file to FILENAME
    """
    global FILENAME
    global DICTIONARY

    if os.path.exists(FILENAME):
        myFile = open(FILENAME, "r")
        row = ""
        for row in myFile:
            DICTIONARY.append(row.upper())
    else:
        print("Error could not load dictionary file: {:s}".format(FILENAME))
        exit()

def clearScreen():
    """ 
    Clears console for drawing
    """

    # nt for windows posix for linux and macosx
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def wellcomeScreen():
    """
       Create Wellcome Screen for Game
    """
    clearScreen()
    print('''
  +---+
  |   |
  O   |
 /|\  | HANGMAN GAME
 / \  |
      |
=========''')

def drawHangMan():
    global HANGMANS
    global PLAYERTURN
    global GAMEMESSAGE
    
    figure = []
    figure = HANGMANS[PLAYERTURN].split("\n")
    clearScreen()

    print(GAMEMESSAGE)

    time.sleep(0.3)
    i =0 
    for i in range(0, len(figure)):
        print(figure[i])
        time.sleep(0.3)

    a = formatSelectedWord()
    print(a)    

def checkResponse(q: str):
    """
    check response yes, no, y, n
    """
    validAnswers = {"Yes": True, "Y": True, "y": True, "No": False, "N": False, "n": False}
    response = ""
    while response not in validAnswers:
        response = input(q+ " (Type Yes, Y, y, No, N, N or type exit) : ")
        
        if response.strip().lower() == "exit":
            exit()
        if response in validAnswers:
            return validAnswers[response]

def newGame():
    global PLAYERCHARS
    global FOUNDCHARS
    global PLAYERTURN
    global GAMEMESSAGE
    clearScreen()
    pickaWord()
    PLAYERCHARS = []
    FOUNDCHARS = []
    PLAYERTURN = 0
    GAMEMESSAGE = "You are waiting in a cold cell ..."

def main():

    global SELECTEDWORD
    global FOUNDCHARS
    global PLAYERTURN
    global PLAYERCHARS
    global GAMEMESSAGE
    global FOUNDMESSAGE
    global LOSTMESSAGES
    wellcomeScreen()
    
    playerResponse = checkResponse("Would you like to play?")

    while playerResponse:
        newGame()
        print("new game started")
        gameResult = 0 # 0 contiune game, 1 player won, 2 player lost
        t = ""
        while gameResult == 0:
            drawHangMan()
            
            
            t = inputCharacter()
            if (t in PLAYERCHARS) or (t in FOUNDCHARS):
                GAMEMESSAGE = "LOL ! You typed {:s} again! You are funny !".format(t)
                PLAYERTURN +=1
            else:
                if t in SELECTEDWORD:
                    FOUNDCHARS.append(t)
                    GAMEMESSAGE = random.sample(FOUNDMESSAGE,1)[0]
                else:
                    PLAYERCHARS.append(t)
                    GAMEMESSAGE = LOSTMESSAGES[PLAYERTURN]
                    PLAYERTURN += 1
            print(GAMEMESSAGE)
            turnResult = checkWord()
            if turnResult:
                gameResult = 1
            if PLAYERTURN >= 6:
                gameResult = 2
        
        if gameResult == 1:
            drawHangMan()
            print("You won the game !!!!")
        elif gameResult == 2:
            drawHangMan()
            print("You lost !")
            print("The WORD was {:s} ".format(SELECTEDWORD))

        playerResponse = checkResponse("Would you like to play again?")

loadDictionary()
main()
