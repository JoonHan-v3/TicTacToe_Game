import PySimpleGUI as sg 
import GameController as gc

FILE_PATH="PlayerHistory.txt"
playMode=0 # This variable identifies the play mode such as one player, two palyer.
           # 1: one player mode
           # 2: two players mode

# Create the buttons for game board.
button1=sg.Button('', size=(16,8), pad=(0,0))
button2=sg.Button('', size=(16,8), pad=(0,0))
button3=sg.Button('', size=(16,8), pad=(0,0))
button4=sg.Button('', size=(16,8), pad=(0,0))
button5=sg.Button('', size=(16,8), pad=(0,0))
button6=sg.Button('', size=(16,8), pad=(0,0))
button7=sg.Button('', size=(16,8), pad=(0,0))
button8=sg.Button('', size=(16,8), pad=(0,0))
button9=sg.Button('', size=(16,8), pad=(0,0))

# This tuple is used to identify the location of each button.
gameBoard=(
  [button1, button2, button3],
  [button4, button5, button6],
  [button7, button8, button9]
)

# This list contains only the buttons which are not checked. 
# At the moment the button clicked, the button is removed from the list.
buttonList=[
  button1, button2, button3,
  button4, button5, button6,
  button7, button8, button9
  ]

menuItem=[
  ["&Game", ["&Two Players", "&One Player",["&Go first", "&Go second"], "Player History", "&Exit"]],
]
menu=sg.Menu(menuItem, tearoff=False, pad=(200,1))

statusBar=sg.StatusBar(text='| Ln{1},Col{1}', text_color='black', background_color='white', justification='left', visible=True, key='status_bar')

layout = [
  [menu],
  [button1, button2, button3],
  [button4, button5, button6],
  [button7, button8, button9],
  [statusBar]
]

window = sg.Window('Tic-Tac-Toe Gamge',  layout)
controller=gc.Controller(buttonList)

#***************** Methods ******************

# This function formats the game board and variables
# when new game begins.
def formatInterface():
  global buttonList, playMode, controller

  for row in range(3): # Formats all the buttons
    for col in range (3):
      button=gameBoard[row][col]
      button.Update('', button_color='grey16', disabled=False)

  buttonList=[    # Fills all buttons in the list.
  button1, button2, button3,
  button4, button5, button6,
  button7, button8, button9
  ]

  controller=gc.Controller(buttonList) # Creates new Controller instance.
  statusBar.Update("")
  playMode=0 

def selectMarker():
  marker=sg.popup_get_text("Input your marker. It should be 'x' or 'o'.\n If you want to keep you marker, leave it blanked.")
  if marker==None:
    return
  if marker.lower().strip()=='o':
    gc.Controller.markers=['O', 'X']
    return
  elif marker.lower().strip() in('x', None, ''):
    gc.Controller.markers=['X', 'O']
    return
  else:
    sg.popup("You can input only 'x' or 'o'.")

    

def play(window, event, gameBoard, playMode):
  if playMode ==1: # Runs one player mode.
    controller.onePlayer(window, event, gameBoard)
  elif playMode==2: # Runs two players mode.
    controller.twoPlayer(window, event, gameBoard)


# This loop handles the events
while True:  
  event, value = window.read() # Reads events from window
  # When exit button is clicked, close the game.
  if event =="Exit" or event==sg.WIN_CLOSED:
    break

  # Player goes first in one player mode when 'Go first' menu option is clicked.
  elif event=="Go first":
    formatInterface() 
    playMode=1
    statusBar.Update("One play mode...")

    playerName = sg.popup_get_text('Player Name','Input Player Name..')
    selectMarker()
    controller.WriteHistory(playerName, FILE_PATH)
  # Player goes second in one player mode when 'Go second' menu option is selected
  elif event=="Go second":
    formatInterface()
    playMode=1
    statusBar.Update("One play mode...")

    playerName = sg.popup_get_text('Player Name','Input Player Name..')
    selectMarker()
    controller.WriteHistory(playerName, FILE_PATH)
    controller.ComputerOperation(gameBoard)
    
  # Runs two players mode.
  elif event=="Two Players":
    # Gets the player names from the input box.
    firstPlayerName = sg.popup_get_text('First Player','Input Player Name..')
    selectMarker()
    secondPlayerName = sg.popup_get_text('Second Player','Input Player Name..')
    #Formats the gamge interface and variables.
    formatInterface()
    statusBar.Update("Two play mode...")
    #Sets the players' name.
    controller.setNames(firstPlayerName, secondPlayerName)  
    playMode=2
    #Writes player names to the file.
    controller.WriteHistory(firstPlayerName, FILE_PATH)
    controller.WriteHistory(secondPlayerName, FILE_PATH)

  #Shows the player name history
  elif event=="Player History":
    statusBar.Update("Player names...")
    nameSet=controller.GetNameSet(FILE_PATH)
    stringHistory=controller.GetHistroyString(nameSet)
    sg.popup_scrolled(stringHistory, title="Player History", background_color='grey', text_color='yellow', size=(60,20), keep_on_top=True, modal=True)

  # After selects game mode, runs the game.
  else:
    play(window, event, gameBoard, playMode)  
window.close()


