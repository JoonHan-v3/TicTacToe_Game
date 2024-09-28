"""
    This class contains the methods to control the game.

    Name: <Joon Han>
    Date: <4/8/21>
    Notes: <Tic-Toc-Toe game>
"""

import random
import PySimpleGUI as sg

class Controller:
    #Variables
    _clickCounter=0  #Counts the number button clicked.
    _buttonList=[]   #Contains the buttons. When the instance is created, it is initialized.
    _playerNames={"first":"X", "second":"O"} #Contains the default players' names.
    _ifWon=False #Identifies if the player wins.
    markers=['X','O']
    #playerScore={} # Stores the player history


    #When the instance is created, defines buttonList.
    def __init__(self, buttons):
        global buttonList
        buttonList=buttons

    # Sets the players' naeme. 
    # When no name is input, uses default names
    def setNames(self, firstName, secondName):
        global markers
        if not firstName in (None, ''): 
            self._playerNames["first"]=firstName
        else:
            self._playerNames["first"]=markers[0]
        if not secondName in (None, ''):
            self._playerNames["second"]=secondName
        else:
            self._playerNames["second"]=markers[1]

    # Two player mode
    def twoPlayer(self, window,event, gameBoard):
        if self._clickCounter%2==0: # When the clickCounter is even, first player goes.
            self.HumanOperation_twoPlayer(window,event, gameBoard, self._playerNames["first"], Controller.markers[0])

        elif self._clickCounter%2==1: # When the clickCounter is odd, second player goes.
            self.HumanOperation_twoPlayer(window,event, gameBoard, self._playerNames["second"], Controller.markers[1])

    # One player mode
    def onePlayer(self, window, event, gameBoard):
        self.HumanOperation_onePlayer(window,event, gameBoard)
        if self._ifWon:
                return
        self.ComputerOperation(gameBoard)
            
    # This method contains the playing action in two players mode.   
    def HumanOperation_twoPlayer(self, window,event, gameBoard, playerName, marker):
        button=window[event]    # Gets the clicked button.
        button.update(marker, button_color=('white','black'), disabled=True)  # Marks and changes button color.
        self._clickCounter+=1  # clickedCounter increased by one.
        # When the player wins, shows the message.
        if self._isWon(gameBoard, marker):
            sg.popup('Game over! {0} won the game.'.format(playerName))
            self._DisableGameBoard(gameBoard)
        # When the game is drawn, shows the message.
        elif self._isDrawn(gameBoard):
            sg.popup('Game over! The game drawn.')  
            self._DisableGameBoard(gameBoard)

    # This method contains the playing action in one players mode.
    def HumanOperation_onePlayer(self, window,event, gameBoard):
        global buttonList
        # When all the buttons in the buttonList are removed, shows message.
        if len(buttonList)==0:
            sg.popup('Game over! The game drawn.') 
            self._DisableGameBoard(gameBoard) 
            return
        button=window[event] # Gets the clicked button.
        button.update(Controller.markers[0], button_color=('white','black'), disabled=True) # Marks and changes button color.
        # Checks if the player wins.
        if self._isWon(gameBoard, Controller.markers[0]):
            sg.popup('Game over! You won the game.')
            self._DisableGameBoard(gameBoard)
            self._ifWon=True
            return
        # Removed the clicked button from the buttonList.
        else:
            buttonList.remove(button)

    # This method contains the computer's action in one player mode.   
    def ComputerOperation(self, gameBoard):
        global buttonList
        # Checks if the buttonList is empted.
        # If so, shows message.
        if len(buttonList)==0:
            sg.popup('Game over! The game drawn.')
            self._DisableGameBoard(gameBoard)  
            return
        index=random.randint(0, len(buttonList)-1) # Gets the random number between 0 and the length of list.
        button=buttonList[index] # Gets the button with the random index.
        button.update(Controller.markers[1], button_color=('white','black'), disabled=True) # Marks and changes button color.
        # Checks if the computer wins the game.
        if self._isWon(gameBoard,Controller.markers[1]):
            sg.popup('Game over! Computer won the game.')
            self._DisableGameBoard(gameBoard)
            return
        # Removes the clicked button from buttonList.
        else:
            buttonList.remove(button)

    # When the game is over, disables all the buttons.  
    def _DisableGameBoard(self, gameBoard):
        for row in range(3):
            for col in range(3):
                button=gameBoard[row][col]
                button.update(disabled=True)

    # Checks if the game is drawn.
    def _isDrawn(self, gameBoard):
        isDrawn=True
        for row in range(3):
            for col in range(3):
                if gameBoard[row][col].GetText()=='':
                    isDrawn=False
                    return
        return isDrawn

    # Checks if the player wins the game.     
    def _isWon(self, gameBoard,mark):
        isWon=False
        #Checks in diagonal.
        if gameBoard[0][0].GetText()==mark and gameBoard[1][1].GetText()==mark and gameBoard[2][2].GetText()==mark:
            # If the player wins the game, identifies the buttons.
            gameBoard[0][0].Update(button_color=('white','blue'))
            gameBoard[1][1].Update(button_color=('white','blue'))
            gameBoard[2][2].Update(button_color=('white','blue'))
            isWon=True
            return isWon
        #Checks in diagonal.
        if gameBoard[0][2].GetText()==mark and gameBoard[1][1].GetText()==mark and gameBoard[2][0].GetText()==mark:
            # If the player wins the game, identifies the buttons.
            gameBoard[0][2].Update(button_color=('white','blue'))
            gameBoard[1][1].Update(button_color=('white','blue'))
            gameBoard[2][0].Update(button_color=('white','blue'))
            isWon=True 
            return isWon

        else:
            for index in range(3):
                #Checks in row.
                if gameBoard[index][0].GetText()==mark and gameBoard[index][1].GetText()==mark and gameBoard[index][2].GetText()==mark:
                    # If the player wins the game, identifies the buttons.
                    gameBoard[index][0].Update(button_color=('white','blue'))
                    gameBoard[index][1].Update(button_color=('white','blue'))
                    gameBoard[index][2].Update(button_color=('white','blue'))
                    isWon=True
                    return isWon
                #Checks in column.
                if gameBoard[0][index].GetText()==mark and gameBoard[1][index].GetText()==mark and gameBoard[2][index].GetText()==mark:
                    # If the player wins the game, identifies the buttons.
                    gameBoard[0][index].Update(button_color=('white','blue'))
                    gameBoard[1][index].Update(button_color=('white','blue'))
                    gameBoard[2][index].Update(button_color=('white','blue'))
                    isWon=True
                    return isWon
            return isWon

    # Gets the history set from file.
    def GetNameSet (self, file):
        nameSet=set({}) # Stores the player history

        try:
            with open(file) as historyFile:
                fileContent=historyFile.read()
                if fileContent!=None:
                    names=fileContent.splitlines()
                    for name in names:
                        nameSet.add(name)
        except Exception as e:
            print(str(e))
        return nameSet
        
    # Turns the set into string
    def GetHistroyString(self, nameSet):
        historyString=''
        nameList=list(nameSet)
        for index in range(len(nameList)):
            name=nameList[index]
            if historyString=='':
                historyString=name
            else:
                historyString +='\n'+name

        return historyString

    def WriteHistory(self, name, file):
        nameSet=self.GetNameSet(file)
        nameSet.add(name)
        historyString=self.GetHistroyString(nameSet)

        try:
            with open(file,'w') as historyFile:
                historyFile.write(historyString)
        except Exception as e:
            print(str(e))
