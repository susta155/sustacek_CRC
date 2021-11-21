
class Polynomial:
    def __init__(self,binRepresentation):
        if isinstance(binRepresentation,str):
            self.bin = int(binRepresentation,2)
        elif isinstance(binRepresentation,int):
            self.bin = binRepresentation
        else:
            raise ValueError(f'Polynomial got input {type(binRepresentation)} expected str or int')

    # lenght of polynomial(number of inexis) so its not n but n+1
    def __len__(self):        
        return len(bin(self.bin))-2

    #polynomials are equal when theit\r binary representation is the same
    def __eq__(self,other):
        if other is None:
            return False
        return self.bin ==other.bin
   
    def getBinary(self):
        return bin(self.bin)[2:] 

    def __str__(self):
        return self.getBinary()   

    def getPolynomialRepresentation(self):
        reprentation = ""
        #convert binary to list and reverse string in order to index correctly
        binRepesentation = list(self.getBinary()[::-1])

        index = 0
        for num in binRepesentation:            
            if num == '1':
                reprentation = f" + x^{index}" + reprentation
            index +=1
        return reprentation[3:]
    
    def change(self,pos,changeTo):
        if pos <0 or not isinstance(pos,int):
            raise ValueError(f"Position needs to be positive number type integer")

        if isinstance(changeTo,str):
            changeTo = int(changeTo)

        if changeTo != 1 and changeTo !=0:        
            raise ValueError(f"Cannot set index of polynomial to {changeTo}")

        #convert binary to list and reverse string in order to index correctly
        binRepesentation = list(self.getBinary()[::-1])

        #change on given position
        while pos > len(binRepesentation)-1:
            #pad by zeroeas until changed position is in list
            binRepesentation.append(0)

        binRepesentation[pos] = changeTo
        #convert back to binary
        binRepesentation=binRepesentation[::-1] #reverse back
        string = ''
        for x in binRepesentation:
            string += str(x)        
        self.bin = int(string,2)

    def flipBit(self,pos):
        if pos > len(self)-1:
            raise ValueError('Position to flip is out of range')
        #convert binary to list and reverse string in order to index correctly
        binRepesentation = list(self.getBinary()[::-1])
        changeTo = int(not int(binRepesentation[pos]))
        self.change(pos,changeTo)
    
    def changeByPoly(self,other):
        #convert binary to list and reverse string in order to index correctly
        binRepesentation = list(other.getBinary()[::-1])
        newPoly = Polynomial(self.bin)
        for x in range(len(binRepesentation)):
            newPoly.change(x,binRepesentation[x])
        return newPoly
    
    def xOr(self,other):
        b1 = self.bin
        b2= other.bin
        return b1 ^ b2
    
    #shifts bin representation by n positive num to left negative to right
    def shiftBinary(self,n):
        self.bin = int(self.bin*(2**n))    

    def __truediv__(self,other):
        current = Polynomial(self.bin)        
        divider = Polynomial(other.bin)

        #initial lenght of divider Polynomial
        startLen = len(divider)        
        div = Polynomial('0')

        posToChange=0
        while startLen <= len(current):
            if current == Polynomial('0'):
                break

            shiftBy = len(current) - len(divider)
            posToChange +=shiftBy
            div.change(posToChange,1)
            divider.shiftBinary(shiftBy)

            reminder = current.xOr(divider)            
            current = Polynomial(int(reminder))
           

        return [div,current]
            
class CRCencoder:
    def __init__(self):
        self.gPolys = []
        self.gPoly = None
        self.msg = None
        self.errorOn = None
        self.hammingCodes = self.generateHammingCodes(10)[::-1]

    def setMessage(self,msg):
        self.msg = Polynomial(msg)
    
    #find generating polynomials with size of (n,k) and saves them into 'self.gPolys' 'self.msg' must be set before
    def findGeneratingPolys(self,n,k):    
        self.gPolys.clear()              
        dividentPoly = self.createDivident(n)        
        endRange = 2**(n-k+1)
        startRange = 2**(n-k)        
        for x in range(startRange,endRange):
            
            if x ==0:
                continue

            poly=Polynomial(x)
            [q, r] = dividentPoly/poly                       
            if r == Polynomial('0'):                                                
                self.gPolys.append(poly)      
   
   #returns Polynomial in type x^n + 1 used for finding the generating polynomials
    def createDivident(self,n):
        divident = Polynomial(2**n) 
        divident.change(0,1)        
        return divident

    #returns encoded msg, 'self.msg' and 'self.gPoly' must by set before
    def encode(self):
        if self.gPoly==None:
            raise RuntimeError('Before encoding generating Polynomial must be set')
        
        if self.msg==None:
            raise RuntimeError('Before encoding Message must be set')

        shiftBy = len(self.gPoly)-1
        encodedMsg = Polynomial(self.msg.bin)
        encodedMsg.shiftBinary(shiftBy)

        [q,r] = encodedMsg/self.gPoly        
        encodedMsg = encodedMsg.changeByPoly(r)               
        return encodedMsg

    #returs reminder after polynomial division
    def checkForError(self):
        if self.gPoly==None:
            raise RuntimeError('Before checking message generating Polynomial must be set')

        [q,r] = self.msg/self.gPoly
        return r

    def decode(self):
        self.errorOn = None
        reminder = self.checkForError()
        shiftBy = -(len(self.gPoly) - 1)
        decodedMsg = Polynomial(self.msg.bin)
        if reminder != Polynomial('0'):        
            index = self.findError(reminder)
            print(f"Error found on bit {index}")
            self.errorOn = index
            decodedMsg.flipBit(index)
            
        decodedMsg.shiftBinary(shiftBy)
        return decodedMsg

    #returns index of found error in 'self.msg'
    def findError(self,reminder):
        msgLen =len(self.msg)
        for x in range(msgLen):
            divident=Polynomial(2**x)
            [q,r] = divident/self.gPoly
            if r == reminder:
                return x
        raise Exception('Error not found, probably because of multiple errors ocurencies, that are not implemented :(')

    #generate Hamming codes types, returns listo of (n,k)
    def generateHammingCodes(self,number):
        codes = []
        for r in range(2,number+2):
            n=2**r-1
            k=n-r
            codes.append((n,k))
        return codes

    #finds mest Hamming code to use   
    def findCodeType(self):
        if self.msg==None:
            raise RuntimeError('Before encoding Message must be set')
        
        msgLen = len(self.msg)        
        codeType = None
        for type in self.hammingCodes:
            if type[1]>=msgLen:
                codeType = type
        return codeType

    #find generating polynomial for closest hamming code 'self.msg' must be set before
    def findgGeneratingPolyAutomatic(self):
        if self.msg==None:
            raise RuntimeError('Before finding of generating poly Message must be set')
        codeType = self.findCodeType()
        self.findGeneratingPolys(codeType[0],codeType[1])
        return codeType
        
         


        

        