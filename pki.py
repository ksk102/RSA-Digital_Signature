from RsaPssSignature import RsaPssSignature

class Pki:
  def __init__(self):
    self.publicKeyPair = {}
    self.privateKeyPair = {}

    self.rsa = RsaPssSignature()


  def CheckPair(self, email):
    # if email exists return the public key, else generate public and private keys
    if self.CheckEntryExists(email):
      return self.publicKeyPair[email], self.privateKeyPair[email]
    else:
      publicKey, privateKey = self.rsa.GenerateKeys() # generate public and private keys

      # add the public and private key into dictionary
      self.AddPair(email, publicKey, privateKey)

      return publicKey, privateKey


  def AddPair(self, email, publicKey, privateKey):
    self.publicKeyPair[email] = publicKey
    self.privateKeyPair[email] = privateKey


  def CheckEntryExists(self, email):
    if email in self.publicKeyPair:
      return True
    else:
      return False