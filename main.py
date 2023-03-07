import os
import json
import shutil
import hashlib

class Blockchain:

    def __init__(self) -> None:
        count = os.listdir(r'c:\blockchain\Blockchain')
        if len(count) == 0:
            genHash = self.hashGenerator("genesis data")
            genesis = self.createBlock("genesis data", genHash, 0, id=0, price=100)
            json.dump(genesis, open(r'c:\blockchain\Blockchain\{}.txt'.format(
                genesis['hash']), 'w'))

    def options(self):
        print("1. Add Block\n 2. View Chain\n 3. Exit\n")

    def viewBlockChain(self):
        allBlocks = os.listdir(r'c:\blockchain\Blockchain')
        for fileName in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(fileName)))
            print(block)

    def myNft(self, id):
        allBlocks = os.listdir(r"c:\blockchain\Blockchain")
        myAsset = []
        for fileName in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(fileName)))
            if block['public_id'] == id:
                myAsset.append(block)
        print(myAsset)

    def addBlock(self, id):
        data = input(str("Enter your shayari...\n"))
        price = input(str("Enter price for your shayari...\n"))
        allBlocks = os.listdir(r'c:\blockchain\Blockchain')
        lastBlock = []
        for i in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(i)))
            if block['index'] == len(allBlocks) - 1:
                lastBlock.append(block)
        newBlock = self.createBlock(
            data, self.hashGenerator(data+str(len(allBlocks))), lastBlock[0]['hash'], id, price)
        json.dump(newBlock, open(r'c:\blockchain\Blockchain\{}.txt'.format(
            newBlock['hash']), 'w'))
        print("Block added successfully at address {}".format(
            newBlock['hash']))

    def addValidatedBlock (self, obj):
        allBlocks = os.listdir(r'c:\blockchain\Blockchain')
        lastBlock = []
        for i in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(i)))
            if block['index'] == len(allBlocks) - 1:
                lastBlock.append(block)
        newBlock = self.createBlock(
            obj['data'], self.hashGenerator(obj['data']+str(len(allBlocks))), lastBlock[0]['hash'], obj['public_id'], obj['price'])
        newBlock['isValidate'] = True
        json.dump(newBlock, open(r'c:\blockchain\Blockchain\{}.txt'.format(
            newBlock['hash']), 'w'))
        print("Block added successfully at address {}".format(
            newBlock['hash']))
        src = r'c:\blockchain\Blockchain'
        files = os.listdir(src)
        dst = r"c:\blockchain\Users\{}\ledger".format(obj['public_id'])
        for file_name in files:
            shutil.copy(src+"\\"+file_name, dst+"\\"+file_name)
        print("Copied successfully")

    def hashGenerator(self, data):
        result = hashlib.sha256(data.encode())
        return result.hexdigest()

    def createBlock(self, data, hash, prev_hash, id, price):
        singleBlock = {}
        count = os.listdir(r'c:\blockchain\Blockchain')
        singleBlock['index'] = len(count)
        singleBlock['data'] = data
        singleBlock['hash'] = hash
        singleBlock['prev_hash'] = prev_hash
        singleBlock['public_id'] = id
        singleBlock['price'] = price
        singleBlock['isValidate'] = False
        return singleBlock
    
    def viewNft(self):
        allBlocks = os.listdir(r'c:\blockchain\Blockchain')
        for fileAdd in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(fileAdd), "r"))
            if block['isValidate'] == True:
                print(block)

    def validate(self, index):
        print(index)
        allBlocks = os.listdir(r'c:\blockchain\Blockchain')
        file = {}
        for fileAdd in allBlocks:
            block = json.load(open(r'c:\blockchain\Blockchain\{}'.format(fileAdd), "r"))
            if block['index'] == index:
                file = block
        file['isValidate'] = True
        self.addValidatedBlock(file)

    def adminOptions(self):
        print("Validate NFT\n")
        bol = True
        def option():
            print("1. View All NFt\n2. Validate NFt\n3. Exit\n")
        while bol == True:
            inp = input(str("\nAdmin: Choose your option (0 to view options)\n"))
            if inp=="0":
                option()
            elif inp=="1":
                self.viewBlockChain()
            elif inp=="2":
                ch = int(input("\nEnter index value of NFT to be validated:\n"))
                self.validate(ch)
            elif inp=="3":
                bol = False
            else:
                print("Invalid Input\n")

class User:
    def __init__(self) -> None:
        print("Welcome to the NFT marketplace")

    def options(self):
        print("1. Signup\n2. Login\n3. View All Transactions\n4. View My NFT\n5. Add Block\n6. Validate NFT\n7. View All NFT\n8. Exit\n")

    def createUser(self):
        name = input(str("Enter your name:\n"))
        noOfUsers = os.listdir(r'c:\blockchain\Users')
        publicId = len(noOfUsers)
        password = input("Enter your password\n")
        newUser = {'name': name, 'Public Id': publicId, 'password': password}
        os.mkdir(r'c:\blockchain\Users\{}'.format(publicId))
        print("Your credentials\n")
        print(newUser)
        path = r'c:\blockchain\Users\{}\credentials.txt'.format(publicId)
        ledgerPath = r'c:\blockchain\Users\{}\ledger'.format(publicId)
        os.mkdir(ledgerPath)
        src = r'c:\blockchain\Blockchain'
        files = os.listdir(src)
        dst = r"c:\blockchain\Users\{}\ledger".format(publicId)
        for file_name in files:
            shutil.copy(src+"\\"+file_name, dst+"\\"+file_name)
        print("Copied successfully")
        json.dump(newUser, open(path, 'w'))

    def validateUser(self):
        id = input("Enter your public ID\n")
        usersAddress = r"c:\blockchain\Users"
        allUsersId = os.listdir(usersAddress)
        if id in allUsersId:
            password = input(str("Enter your password\n"))
            credentials = json.load(open(r"c:\blockchain\Users\{}\credentials.txt".format(id)))
            if password == credentials['password']:
                print("Credentials matched")
                return [1, id]
            else:
                print("Login failed")
                return [0]
        else:
            print("This public ID does not exist")

a = True

user = User()
bc = Blockchain()
f = False
ad = False
while a == True:
    val = input("Enter your choice [ 0 for options ]")
    if val == '0':
        user.options()
    elif val == '1':
        user.createUser()
    elif val == '2':
        flag = user.validateUser()
        if flag[0] == 1:
            f = True
        else:
            f = False
    elif val == "3":
        bc.viewBlockChain()
    elif val =="4":
        flag = user.validateUser()
        if flag[0] == 0:
            f = False
        else:
            f = True
            bc.myNft(flag[1])
    elif val == "5":
        flag = user.validateUser()
        bc.addBlock(flag[1])
    elif val == '6':
        id = input(str("Enter your Public Id\n"))
        password = input(str("Enter your password\n"))
        if id == "0":
            if password != "raj":
                ad = False
                print("Incorrect Password\n")
            else:
                ad = True
                bc.adminOptions()
        else:
            ad = False
            print("Only Admin can validate the NFT\n")
    elif val == '7':
        bc.viewNft()
    else:
        a = False