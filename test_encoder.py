from CRC import CRCencoder, Polynomial
import pytest

@pytest.fixture
def CRC():
    return CRCencoder()

def test_setMessage(CRC):
    msg ='10111010'
    CRC.setMessage(msg)
    assert CRC.msg == Polynomial(msg)

def test_createDividentPoly(CRC):
    divident =CRC.createDivident(4)
    assert divident == Polynomial('10001')

def test_findGeneratingPolys_7_4(CRC):
    CRC.findGeneratingPolys(7,4)    
    assert CRC.gPolys[0]==Polynomial('1011')
    assert CRC.gPolys[1]==Polynomial('1101')

def test_findGeneratingPolys_15_11(CRC):
    CRC.findGeneratingPolys(15,11)    
    assert CRC.gPolys[0]==Polynomial('10011')
    assert CRC.gPolys[1]==Polynomial('11001')
    assert CRC.gPolys[2]==Polynomial('11111')

def test_findGeneratingPolys_31_26(CRC):
    CRC.findGeneratingPolys(31,26)    
    assert CRC.gPolys[0]==Polynomial('100101')
    assert CRC.gPolys[1]==Polynomial('101001')
    assert CRC.gPolys[2]==Polynomial('101111')
    assert CRC.gPolys[3]==Polynomial('110111')
    assert CRC.gPolys[4]==Polynomial('111011')
    assert CRC.gPolys[5]==Polynomial('111101')

def test_findGeneratingPolys_9_9(CRC):
    CRC.findGeneratingPolys(9,9)    
    assert CRC.gPolys[0]==Polynomial('1')
    
def test_encode(CRC):
    msg ='101101'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011') 
    encodedMsg=CRC.encode()
    assert encodedMsg == Polynomial('101101011')

def test_checkForError_correct(CRC):
    msg = '101101011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011') 
    assert Polynomial('0') == CRC.checkForError()

def test_checkForError_incorrect(CRC):
    msg = '101111011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011') 
    assert Polynomial('110') == CRC.checkForError()

def test_decode_correct(CRC):
    msg = '101101011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011')
    decodedMsg = CRC.decode()
    assert decodedMsg == Polynomial('101101')

def test_findError(CRC):
    msg = '101111011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011')
    reminder = CRC.checkForError()
    assert 4 == CRC.findError(reminder)

def test_findError2(CRC):
    msg = '101100011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011')
    reminder = CRC.checkForError()
    assert 3 == CRC.findError(reminder)

def test_decode_incorrect(CRC):
    msg = '101111011'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011')
    decodedMsg = CRC.decode()
    assert decodedMsg == Polynomial('101101')

def test_decode_incorrectFindIndexOfError(CRC):
    msg = '101101001'
    CRC.setMessage(msg)
    CRC.gPoly = Polynomial('1011')
    decodedMsg = CRC.decode()
    assert 1 == CRC.errorOn

def test_generateHammingCode(CRC):
    assert CRC.hammingCodes[7]==(15,11)

def test_generateGeneratingPolyForClosesHammingCode(CRC):
    CRC.setMessage('100001')
    codeType=CRC.findCodeType()
    assert codeType == (15,11)

