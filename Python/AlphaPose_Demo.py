import os
from time import sleep as s

PATH = "/Users/jrowe/onedrive/documents/github/balancebot" #os.getcwd()

print(os.getcwd())
os.chdir("/Users/jrowe/alphapose")
print("Alphapose Directory Enabled:", os.getcwd()[-9:]=='alphapose')
print(os.listdir())

#Bring Python Directory Back To PATH
os.chdir(PATH)