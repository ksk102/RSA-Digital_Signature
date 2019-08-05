from RsaPssSignature import RsaPssSignature

class Pki:
  def __init__(self):
    self.publicKeyPair = {}
    self.privateKeyPair = {}

    self.rsa = RsaPssSignature()


  def checkPair(self, email):
    # if email exists return the public key, else generate public and private keys
    if email in self.publicKeyPair:
      return self.publicKeyPair[email], self.privateKeyPair[email]
    else:
      publicKey, privateKey = self.rsa.GenerateKeys() # generate public and private keys

      # add the public and private key into dictionary
      self.addPair(email, publicKey, privateKey)

      return publicKey, privateKey


  def addPair(self, email, publicKey, privateKey):
    self.publicKeyPair[email] = publicKey
    self.privateKeyPair[email] = privateKey