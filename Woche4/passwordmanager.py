from cryptography.fernet import Fernet
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
  # Check if folder exists and if not, create one
  def __createFolder(self)-> None:
    if os.path.isdir(self.__folderpath):
      return
    else: 
      # Creates folder with NAME and KEYS folder inside it
      os.makedirs(self.__folderpath + 'Keys')

  # Get a list of all the files inside the folder
  def __getFolderContentList(self)-> list:
    dir_content = os.listdir(self.__folderpath)

    # remove Keys folder
    dir_content.remove('Keys')

    return dir_content

  # Print pretty menubar, optional text usually is the selected database
  def __printHeader(self, additionalText:str = '')-> None:
    print('=' * 40)
    print('{:^40s}'.format(self.name + ' ' + additionalText))
    print('=' * 40)

  # get the password list
  def __getPasswordList(self, file)-> list:
    password_list = list()

    file = open(file.name, 'r')
    file_content = file.read()

    # new entries are determined by linebreaks, create a list which each line
    content = file_content.split('\n')

    # iterate through each line
    for element in content:
      splitlist = element.split(':')

      # when the length is only 1, it means its an empty line, skip over that
      if len(splitlist) != 1:
        # would be better to use .find('https') but works so whatever
        if (splitlist[2] == 'https'):
          splitlist[2] = splitlist[2] + ':' + splitlist[3]
          splitlist.remove(splitlist[3])

        password_list.append([str(content.index(element)), splitlist[0], splitlist[1], splitlist[2], splitlist[3]])

    return password_list

  # create a pretty console output that looks like a table
  def __printPasswords(self, list: list)-> None:
    print('-'*100)
    print('{:20s}'.format('Index'), end='')
    print('{:20s}'.format('Name'), end='')
    print('{:20s}'.format('Passwort'), end='')
    print('{:20s}'.format('URL'), end='')
    print('{:20s}'.format('Notiz'))
    print('-'*100)

    for element in list:
      for x in element:
        print('{:20s}'.format(x), end='')
      print('')
    print('')

  # rewrite the whole database with the updated and new list entries
  def __updateDatabase(self, file, new_password_list: list)-> None:
    file.write('')
    file = open(file.name, 'a')
    for entry in new_password_list:
      file.write(entry[1] + ':' + entry[2] + ':' + entry[3] + ':' + entry[4] + '\n')
    
    # reset permission
    file = open(file.name, 'r')

# +------------------------------------------------------------------+
# |                           Encryption                             |
# +------------------------------------------------------------------+
  def __generateKey(self, name:str)-> None:
    key = Fernet.generate_key()
    with open(self.__folderpath + '/Keys/' + name + '.txt', 'wb') as filekey:
      filekey.write(key)

  def __loadKey(self, name):
    with open(self.__folderpath + '/Keys/' + name + '.txt', 'rb') as filekey:
      key = filekey.read()
    return key

  def __encryptFile(self, name)-> None:
    fernet = Fernet(self.__loadKey(name))
    with open(self.__folderpath + name + '.txt', 'rb') as file:
      original = file.read()

    encrypted = fernet.encrypt(original)
    with open(self.__folderpath + name + '.txt', 'wb') as encrypted_file:
      encrypted_file.write(encrypted)

  def __decryptFile(self, name)-> None:
    fernet = Fernet(self.__loadKey(name))
    with open(self.__folderpath + name + '.txt', 'rb') as enc_file:
      encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    with open(self.__folderpath + name + '.txt', 'wb') as dec_file:
      dec_file.write(decrypted)
# +------------------------------------------------------------------+
# |                Show initial menu with 3 options                  |
# +------------------------------------------------------------------+
  def run(self)-> None:
    self.__printHeader()
    print(' 1.) Eine neue Datenbank erstellen')
    print(' 2.) Eine bereits existierende Datenbank auswählen')
    print(' 3.) Beenden')

    print('Was möchten Sie tun? ', end = '')
    option = int(input())
    print('')

    # create DB
    if (option == 1):
      print('Bitte geben sie der neuen Datenbank einen geeigneten Namen: ', end = '')
      name = str(input())
      file = open(self.__folderpath + name + '.txt', 'w')

      # Generate Encryption Key with same filename
      self.__generateKey(name)

      # Encrypt the file immediatly
      self.__encryptFile(name)
      
      # show menu for edit/delete/add password
      self.__showDatabaseMenu(file)

    # SHOW LIST OF DATABASES
    if (option == 2):
      folder_list = self.__getFolderContentList()

      for idx, x in enumerate(folder_list):
        print('{0}.) {1}'.format(idx,x))

      print('Bitte geben Sie die Nummer der auszuwählenden Datenbank ein: ', end = '')
      option = int(input())

      databank = self.__folderpath + folder_list[option]

      file = open(databank, 'r')
        
      self.__showDatabaseMenu(file)

      # exit
      if (option == 3):
        return


# +------------------------------------------------------------------+
# |                Show detailed database menu options               |
# +------------------------------------------------------------------+
  def __showDatabaseMenu(self, file)-> None:
    file_name = os.path.basename(file.name)
    file_name = file_name.split('.')[0]

    isRunning = True
    while isRunning:
      self.__printHeader('(' + file_name + '.txt)')
      print(' 1.) Existierende Passwörter anzeigen')
      print(' 2.) Neues Passwort hinzufügen')
      print(' 3.) Löschen eines Passworts')
      print(' 4.) Aktualisieren eines Passworts')
      print(' 5.) Beenden')  
      print('Was möchten Sie tun? ', end = '')
      option = int(input())
  
      if (option == 1):
        self.__decryptFile(file_name)
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)
      elif (option == 2):
        self.__decryptFile(file_name)
        print('Geben Sie einen Usernamen ein: ')
        username = str(input())
        print('Geben Sie ein Passwort ein: ')
        password = str(input())
        print('Geben Sie eine URL ein: ')
        url = str(input())
        print('Geben Sie dem Eintrag eine Notiz: ')
        notiz = str(input())

        file = open(file.name, 'a')
        file.write(username + ':' + password + ':' + url + ':' + notiz + '\n')

        file = open(file.name, 'r')
        print('')
      elif (option == 3):
        self.__decryptFile(file_name)
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)
        
        print('Welches Passwort soll gelöscht werden? ', end = '')
        option = int(input())
        password_list.remove(password_list[option])
  
        file = open(file.name, 'w')
        self.__updateDatabase(file, password_list)
      elif (option == 4):
        self.__decryptFile(file_name)
        password_list = self.__getPasswordList(file)
        self.__printPasswords(password_list)
  
        print('Welches Passwort soll geändert werden? ', end = '')
        option = int(input())
  
        print('Bitte geben sie ein neues Passwort ein:  ')
        password_list[option][2] = str(input())
  
        file = open(file.name, 'w')
        self.__updateDatabase(file, password_list)
      elif (option == 5):
        # Stop the while loop
        self.__decryptFile(file_name)
        isRunning = False
      
      self.__encryptFile(file_name)


# +------------------------------------------------------------------+
# |                Execute code for testing purposes                 |
# +------------------------------------------------------------------+
if __name__ == '__main__':
  # Create an instance of PW Manager
  pwManager = PasswordManager('Passwortmanager')
  pwManager.run()
