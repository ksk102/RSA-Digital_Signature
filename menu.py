from RsaPssSignature import RsaPssSignature
import os

def Menu():
  os.system("cls")

  method = RsaPssSignature()

  # Menu for user to choose
  print("(1) Automatically generate the signing and verifying process.")
  print("(2) Manually handle the signing and verifying process.")
  print("(9) Exit from the system")

  print("Please select from one of the options above: ", end = "")
  try:
    choice = int(input())
  except(ValueError):
    choice = 9
  os.system("cls")

  if choice == 1:
    AutoGenerate(method)
  elif choice == 2:
    ManualMenu()
  elif choice == 9:
    exit()
  else:
    Menu(method)

def ManualMenu(method = None):
  os.system("cls")

  if not method:
    method = RsaPssSignature()

  print("(1) Generate the Public and Private Key.")
  print("(2) Insert the message to send.")
  print("(3) Sign the message.")
  print("(4) Send and verify the signature.")
  print("(5) Alter the message and verify.")
  print("(9) Go back to previous menu")

  print("Please select from one of the options above: ", end = "")
  try:
    choice = int(input())
  except(ValueError):
    choice = 9
  os.system("cls")

  if choice == 1:
    GenerateKeys(method)
  elif choice == 2:
    InputMessage(method)
    GenerateHash(method)
  elif choice == 3:
    try:
      SignMessage(method)
    except(AttributeError):
      print("Error! Hashed message, public and private keys are needed to sign the message")
  elif choice == 4:
    try:
      SendAndVerifySignature(method)
    except(AttributeError):
      print("Error! Please sign the message first, before sending it")
  elif choice == 5:
    try:
      InputMessage(method)
      GenerateHash(method)

      os.system("pause")

      SendAndVerifySignature(method)
    except(AttributeError):
      print("Error! Authentic message is not sign yet, please sign the message first before try to tamper it")
  elif choice == 9:
    Menu()
  else:
    ManualMenu(method)

  os.system("pause")
  os.system("cls")
  ManualMenu(method)

def AutoGenerate(method):
  GenerateKeys(method)
  InputMessage(method)
  GenerateHash(method)
  SignMessage(method)

  print("--------------------------------------------------")
  print()

  SendAndVerifySignature(method)

  os.system("pause")
  os.system("cls")
  Menu()

def GenerateKeys(method):
  print("Generating the Public and Private Key...")
  method.GenerateKeys()
  print(method.GetPublicKey())
  print()
  print(method.GetPrivateKey())
  print()

# Get the message for signing
def InputMessage(method):
  error = ""
  while True:
    print(error + "Insert the message that you wish to send: ", end = "")
    message = input()

    if method.SetMessage(message):
      break
    else:
      error = "Message must not be empty! "

  print()

def GenerateHash(method):
  print("Generating the SHA256 Hash for the Message...")
  method.HashMessage()
  print("Hash: " + method.GetHashedMessage())
  print()

def SignMessage(method):
  print("Signing the message...")
  method.SignSignature()
  print("Digital Signature: " + method.GetSignature())
  print()

def SendAndVerifySignature(method):
  print("Sending the message to receiver...")
  print("Message Signed: " + method.GetSignedMessage())
  print("Message Receive: " + method.GetMessage())
  print("Digital Signature: " + method.GetSignature())
  print()
  
  print("Verifying the message against the signature signed...")
  if(method.VerifySignature()):
    print("The signature is authentic.")
  else:
    print("The signature is not authentic.")
  print()

def main():
  # Shows the Main Menu
  Menu()

if __name__ == '__main__':
  main()