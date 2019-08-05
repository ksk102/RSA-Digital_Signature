from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
from Crypto import Random
from base64 import b64encode, b64decode

class RsaPssSignature:
  # Set the hashing algorithm
  hashAlgo = SHA256

  # Set the message for signing
  def SetMessage(self, message):
    # message cannot be empty
    if message == "" or not message:
      return False
    else:
      self.message = message
      return True

  # Generate public and private key
  def GenerateKeys(self, keysize = 1024):
    randomGenerator = Random.new().read
    key = RSA.generate(keysize, randomGenerator)

    self.private = key
    self.public = key.publickey()

    return self.public, self.private

  # Hash the message
  def HashMessage(self, message = None):
    if not message:
      message = self.message

    self.hashedMessage = self.hashAlgo.new(message.encode())

  # Sign for the hashed message
  def SignSignature(self, key = None, hashedMessage = None):
    if not key:
      key = self.private

    if not hashedMessage:
      hashedMessage = self.hashedMessage

    # to remember the signed message
    self.signedMessage = self.GetMessage()

    signer = pss.new(key)
    self.signature = signer.sign(hashedMessage)

  # Verify the signature against the message (hashed)
  def VerifySignature(self, hashedMessage = None, signature = None, key = None):
    if not hashedMessage:
      hashedMessage = self.hashedMessage

    if not signature:
      signature = self.signature

    if not key:
      key = self.public

    verifier = pss.new(key)
    try:
      verifier.verify(hashedMessage, signature)
      return True
    except(ValueError, TypeError):
      return False

  # Get the plaintext message
  def GetMessage(self):
    return self.message
  
  # Get the message that get signed
  def GetSignedMessage(self):
    return self.signedMessage

  # Get the private key
  def GetPrivateKey(self):
    return GetKeyInPEM(self.private) 
  
  # Get the public key
  def GetPublicKey(self):
    return GetKeyInPEM(self.public)

  def GetKeyInPEM(self, key):
    return str(key.exportKey("PEM"))

  # Get the hashed message
  def GetHashedMessage(self):
    return self.hashedMessage.hexdigest()

  # Get the signature of the message
  def GetSignature(self):
    return str(b64encode(self.signature))