from RsaPssSignature import RsaPssSignature
import os

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

def Menu(method):
  os.system("cls")
  print("(1) Automatically generate the signing and verifying process. ")
  print("(9) Exit from the system")

  print("Please select from one of the options above: ", end = "")
  choice = int(input())
  os.system("cls")

  if choice == 1:
    AutoGenerate(method)
  elif choice == 9:
    os.system("exit")
  else:
    Menu(method)

def AutoGenerate(method):
  print("Generating the Public and Private Key...")
  method.GenerateKeys()
  print(method.GetPublicKey())
  print()
  print(method.GetPrivateKey())
  print()

  # Get user input for the message to sign
  InputMessage(method)
  print()

  print("Generating the SHA256 Hash for the Message...")
  method.HashMessage()
  print("Hash: " + method.GetHashedMessage())
  print()

  print("Signing the message...")
  method.SignSignature()
  print("Digital Signature: " + method.GetSignature())
  print()

  print("--------------------------------------------------")
  print()

  print("Sending the message to receiver...")
  print("Message Receive: " + method.GetMessage())
  print("Digital Signature Receive: " + method.GetSignature())
  print()
  
  print("Verifying the message against the signature signed...")
  if(method.VerifySignature()):
    print("The signature is authentic.")
  else:
    print("The signature is not authentic.")
  print()

  os.system("pause")
  os.system("cls")
  Menu(method)

def main():
  method = RsaPssSignature()

  # Shows the Main Menu
  Menu(method)

main()