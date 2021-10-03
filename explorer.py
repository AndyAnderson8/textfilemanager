import os
import time
from pathlib import Path

copiedFileDir = None
copiedFileAction = None

def generateDashLine(string, character):
  dashLine = ""
  for i in range(len(string)):
    dashLine = dashLine + character
  return dashLine

def getParentDirectory(directory):
  try:
    parentDir = str(Path(directory).parents[0])
    return parentDir
  except IndexError:
    navigateFiles(input("\nEnter drive path: ")) #This can be changed if neccesary, see below
    #print("\nInvalid selection")
    #return directory

def standardizeSize(size): #converts byte size to appropriate unit
  sizeUnitsAbbr = ["B", "KB", "MB", "GB", "TB", "PB", "EB"]
  i = 0
  while size >= 1024:
    size /= 1024
    i += 1
  unit = sizeUnitsAbbr[i]
  return int(size), unit #int for rounding down

def printFiles(directory):
  dirFiles = os.listdir(directory)
  i = 1
  print("[" + str(i) +"] ...") #back in directory
  for file in dirFiles:
    i += 1
    fileDir = str(directory) + "\\" + str(file) #full dir; adds only one backslash
    fileSize = standardizeSize(os.path.getsize(fileDir)) #gets size in bytes, calls to standardize
    print("[" + str(i) + "] " + file + " - " + str(fileSize[0]) + " " + fileSize[1])
  return dirFiles

def navigateFiles(startingDirectory):
  print("\n" + generateDashLine(startingDirectory, "-") + "\n" + startingDirectory + "\n" + generateDashLine(startingDirectory, "-"))
  dirFiles = printFiles(startingDirectory) #calls function and stores files in directory
  try:
    selection = int(input("\nEnter selection number: "))-2 #did -2 cause indexing starts at 0, first actual file choice is 2
    if selection == -1:
      cwd = getParentDirectory(startingDirectory)
      navigateFiles(cwd) #goes up a directory
    elif selection <= (len(dirFiles)-1): #subtracting 1 cause selection should be additionally accounting for the back
      cwd = startingDirectory + "\\" + dirFiles[selection]
      try: #its a folder
        navigateFiles(cwd)
      except NotADirectoryError: #its a file
        action = int(input("[1] ...\n[2] Open\n[3] Copy\n[4] Cut\n[5] Paste\n[6] Delete\n[7] Rename\n\nEnter selection number: "))-2 #used -2 because indexing etc, also 1 is back
        if selection != -1:
          manageFile(cwd, action)
      except PermissionError:
        print("\nInsufficient access privileges.")
      navigateFiles(startingDirectory)
    else:
      print("\nInvalid selection")
      navigateFiles(startingDirectory)
  except ValueError:
      print("\nInvalid selection")
      navigateFiles(startingDirectory)

def manageFile(fileDir, action):
  global copiedFileDir, copiedFileAction
  if action == 0: #open
    os.startfile(fileDir)
    print("\nFile opening successful")
  elif action == 1: #copy
    copiedFileDir = fileDir
    copiedFileAction = 0 #setting to copy mode
    print("\nFile successfully copied")
  elif action == 2: #cut TODO READ BELOW TODO on wait time. Cut is totally broken
    copiedFileDir = fileDir
    copiedFileAction = 1 #setting to cut mode
    print("\nFile succesfully cut")
  elif action == 3: #paste - FIX THIS CAUSE YOU GOTTA SELECT A RANDOM FILE FIRST
    if copiedFileDir == None:
      print("\nNothing to paste")
    else:
      file = os.path.basename(copiedFileDir)
      fileName = os.path.splitext(file)[0]
      fileExtention = os.path.splitext(file)[1]
      if copiedFileAction == 0: #copy mode
        os.popen("copy " + copiedFileDir + " " + getParentDirectory(fileDir) + "\\" + fileName + "-Copy" + fileExtention)#distinguishes instead of overriding
      elif copiedFileAction == 1: #cut mode
        os.popen("copy " + copiedFileDir + " " + getParentDirectory(fileDir) + "\\" + fileName + fileExtention)
        time.sleep(10) # TODO I think this is required because it doesnt copy fast enough, fix this
        os.remove(copiedFileDir)
      copiedFileDir = None
      copiedFileAction = None
      time.sleep(1) #TODO doesn't show up new file right away so add checker
      print("\nFile paste succesful")
  elif action == 4: #delete
    confirm = input("Are you sure you want to delete this file? (type 'yes' to confirm): ")
    if confirm == "yes":
      os.remove(fileDir)
      print("\nFile deletion successful")
    else: 
      print("\nOperation canceled")
  elif action == 5: #rename
    fileExtention = os.path.splitext(fileDir)[1]
    newName = input("Enter new name: ")
    os.rename(fileDir, getParentDirectory(fileDir) + "\\" + newName + fileExtention)
    print("\nFile rename successful - " + getParentDirectory(fileDir) + "\\" + newName + fileExtention)
  else:
    print("\nInvalid selection") 
  navigateFiles(getParentDirectory(fileDir))

launchMsg = "Andy's File Explorer v1"
print("\n" + generateDashLine(launchMsg, "-") + "\n" + launchMsg + "\n" + generateDashLine(launchMsg, "-"))
getParentDirectory("C:\\") #bad code here. Intentionally errors