from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256, SHA384, SHA512, SHA1, MD5
from Crypto import Random
from base64 import b64encode, b64decode
import re

class RsaPssSignature:
  # Set the hashing algorithm
  hashAlgo = SHA256

  # Method to set the hashing algorith
  def SetHashAlgo(self, hashMethod):
    if hashMethod == "SHA256":
      self.hashAlgo = SHA256    
    elif hashMethod == "SHA384":
      self.hashAlgo = SHA384
    elif hashMethod == "SHA512":
      self.hashAlgo = SHA512
    elif hashMethod == "SHA1":
      self.hashAlgo = SHA1
    elif hashMethod == "MD5":
      self.hashAlgo = MD5
    else:
      return False

    return True

  # Set the message for signing
  def SetMessage(self, message):
    # message cannot be empty
    if message == "" or not message:
      return False
    else:
      self.message = message.strip()
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
    return self.GetKeyInPEM(self.private) 
  
  # Get the public key
  def GetPublicKey(self):
    return self.GetKeyInPEM(self.public)

  def GetKeyInPEM(self, key):
    return key.exportKey("PEM").decode('utf-8')

  # Get the hashed message
  def GetHashedMessage(self):
    return self.hashedMessage.hexdigest()

  # Get the signature of the message
  def GetSignature(self):
    return b64encode(self.signature).decode()

  def GetSignatureFromString(self, signature):
    return b64decode(signature.encode('utf-8'))

  def GetHashAlgo(self, HashType = None):
    if HashType is None:
      HashType = self.hashAlgo

    if HashType == SHA256:
      return "SHA256"
    elif HashType == SHA384:
      return "SHA384"
    elif HashType == SHA512:
      return "SHA512"
    elif HashType == SHA1:
      return "SHA1"
    elif HashType == MD5:
      return "MD5"

  def GetSignedDocument(self):
    signedDocument = ""
    signedDocument += "-----BEGIN RSA PSS MESSAGE-----\n"
    signedDocument += "Hash: " + str(self.GetHashAlgo()) + "\n\n"
    signedDocument += self.GetMessage() + "\n"
    
    signedDocument += "-----BEGIN RSA PSS SIGNATURE-----\n"
    signedDocument += self.GetSignature() + "\n"
    signedDocument += "-----END RSA PSS SIGNATURE-----"

    return signedDocument

  def GetMessageFromSignedDoc(self, signedDoc):
    regexStart = '^(-----BEGIN RSA PSS MESSAGE-----)(\s)(Hash: )(\w+)(\s\s)'
    # regexStart = '^(-----BEGIN RSA PSS MESSAGE-----)(\s)(Hash: )(' + self.GetHashAlgo() + ')(\s\s)'
    regexEnd = '(-----BEGIN RSA PSS SIGNATURE-----)(\s)(.*)(\s)(-----END RSA PSS SIGNATURE-----)$'

    return self.GetValueFromSignedDoc(signedDoc, regexStart, regexEnd)


  def GetHashAlgoFromSignedDoc(self, signedDoc):
    regexStart = '^(-----BEGIN RSA PSS MESSAGE-----)(\s)(Hash: )'
    regexEnd = '(\s){2}(.|\s)*(\s)(-----BEGIN RSA PSS SIGNATURE-----)(\s)(.*)(\s)(-----END RSA PSS SIGNATURE-----)$'
    
    return self.GetValueFromSignedDoc(signedDoc, regexStart, regexEnd)

  
  def GetSignatureFromSignedDoc(self, signedDoc):
    regexStart = '^(-----BEGIN RSA PSS MESSAGE-----)(\s)(Hash: )(\w+)(\s){2}(.|\s)*(\s)(-----BEGIN RSA PSS SIGNATURE-----)(\s)'
    regexEnd = '(\s)(-----END RSA PSS SIGNATURE-----)$'

    return self.GetValueFromSignedDoc(signedDoc, regexStart, regexEnd)


  def GetValueFromSignedDoc(self, signedDoc, regexStart, regexEnd):
    message = signedDoc

    if re.search(regexStart, message) and re.search(regexEnd, message):
      message = re.sub(regexStart, "", message)
      message = re.sub(regexEnd, "", message)
      message = message.strip()

      return message
    else:
      return False