import os

class PasswordManager:
  def __init__(self, name: str):
    self.name = name
    self.__executionpath = os.getcwd()
    self.__folderpath = self.__executionpath + '/' + name + '/'
    self.__createFolder()

# +------------------------------------------------------------------+
# |                        Private functions                         |
# +------------------------------------------------------------------+
  def __createFolder(self):
    if os.path.isdir(self.__folderpath):
      return
    else:
      os.makedirs(self.__folderpath)
  
  def __getFolderContentList(self):
    dir_content = os.listdir(self.__folderpath)
    return dir_content
  
  def __printHeader(self, additionalText=""):
    print("="*40)
    print('{:^40s}'.format(self.name + " " + additionalText))
    print("="*40)

  def __getPasswordList(self, file):
    password_list = list()

    file_content = file.read()
    content = file_content.split('\n')

    for element in content:
      splitlist = element.split(':', 2)
      if (len(splitlist) != 1):
        password_list.append([str(content.index(element)), splitlist[0], splitlist[1], splitlist[2]])

    return password_list

  def __printPasswords(self, list: list):
    print("-"*100)
    print('{:20s}'.format('Index'), end="")
    print('{:20s}'.format('Name'), end="")
    print('{:20s}'.format('Passwort'), end="")
    print('{:20s}'.format('URL'), end="")
    print('{:20s}'.format('Notiz'))
    print("-"*100)

    for element in list:
      for x in element:
        print('{:20s}'.format(x), end="")
      print("")
    
    print("")
  
  def __updateDatabase(self, file, new_password_list):
    print(new_password_list)
    file.write("")
    file = open(file.name, 'a')
    for entry in new_password_list:
      file.write(entry[1] + ':' + entry[2] + ':' + entry[3] + '\n')
    
    file = open(file.name, 'r')

# +------------------------------------------------------------------+
# |                Show initial menu with 3 options                  |
# +------------------------------------------------------------------+
  def run(self):
    self.__printHeader()
    print(" 1.) Eine neue Datenbank erstellen")
    print(" 2.) Eine bereits existierende Datenbank auswählen")
    print(" 3.) Beenden")

    print("Was möchten Sie tun? ", end = "")
    option = int(input())
    print("")

    if (type(option) == int):
      # create DB
      if (option == 1):
        print("Bitte geben sie der neuen Datenbank einen geeigneten Namen: ", end = "")
        name = str(input())
        file = open(self.__folderpath + name + ".txt", "w")
        
        self.showDatabaseMenu(file)

      # SHOW LIST OF DATABASES
      if (option == 2):
        folderDictionary = self.__getFolderContentList()

        for idx, x in enumerate(folderDictionary):
          print("{0}.) {1}".format(idx,x))

        print("Bitte geben Sie die Nummer der auszuwählenden Datenbank ein: ", end = "")
        option = int(input())

        # Databank assigned
        databank = self.__folderpath + folderDictionary[option]

        file = open(databank, 'r')
        
        self.showDatabaseMenu(file)
      # exit
      if (option == 3):
        return
    else:
      print("Falscher Input, bitte nur Ganzzahlen benutzen!")

# +------------------------------------------------------------------+
# |                Show detailed database menu options               |
# +------------------------------------------------------------------+
  def showDatabaseMenu(self, file):
    self.__printHeader("(" + os.path.basename(file.name) + ")")
    print(" 1.) Existierende Passwörter anzeigen")
    print(" 2.) Neues Passwort hinzufügen")
    print(" 3.) Löschen eines Passworts")
    print(" 4.) Aktualisieren eines Passworts")
    print(" 5.) Beenden")

    print("Was möchten Sie tun? ", end = "")
    option = int(input())

    if (type(option) == int):
      if (option == 1):
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)

      if (option == 2):
        print("Geben sie einen Usernamen ein: ")
        username = str(input())
        print("Geben sie ein Passwort ein: ")
        password = str(input())
        print("Geben sie eine URL ein (optional): ")
        url = str(input())

        # append to file
        file = open(file.name, 'a')
        file.write(username + ':' + password + ':' + url + '\n')
        
        print("")
      
      if (option == 3):
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)
        # get input
        print("Welches Passwort soll gelöscht werden? ", end = "")
        option = int(input())
        password_list.remove(password_list[option])

        file = open(file.name, 'w')
        self.__updateDatabase(file, password_list)


      if (option == 4):
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)
        print(password_list)
        # get input

      if (option == 5):
        return
    else:
      print("Falscher Input, bitte nur Ganzzahlen benutzen!")

# +------------------------------------------------------------------+
# |                Execute code for testing purposes                 |
# +------------------------------------------------------------------+
if __name__ == "__main__":
  # Create an instance of PW Manager
  pwManager = PasswordManager('Passwortmanager')

  pwManager.run()
