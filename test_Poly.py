from CRC import Polynomial
import pytest

def test_PolyCreate():    
    poly = Polynomial('010101')
    assert isinstance(poly,Polynomial)

def test_PolyCreateWithZero():
    poly = Polynomial('0')
    assert poly.bin == 0

def test_binaryRepresentationFromString():
    binRepres = '0101011011'
    poly = Polynomial(binRepres)
    assert poly.bin == int(binRepres,2)

def test_binaryRepresentationFromInt():
    x=8
    poly = Polynomial(x)
    assert poly.bin == x

def test_raiseExceptionWhenInvalidInput():    
    with pytest.raises(Exception) as e_info:
        Polynomial(5.8)

def test_lenOfpoly():
    poly = Polynomial('1111110101')
    assert len(poly) == 10

def test_polynomialEquiality():
    poly1 = Polynomial('10101')
    poly2 = Polynomial('10101')
    assert poly1 == poly2

def test_polynomialEquialityWithNone():
    poly = Polynomial('10101')
    res = (poly == None)
    assert res == False

def test_getBinRepresentation():
    binary = '1001'
    poly= Polynomial(binary)
    assert poly.getBinary()==binary

def test_getPolynomialRepresentation():
    poly = Polynomial('100101101')
    assert 'x^8 + x^5 + x^3 + x^2 + x^0' == poly.getPolynomialRepresentation()

def test_modifyPolynomial():
    poly= Polynomial('1010001')
    poly.change(0,0)
    poly.change(2,1)    
    assert poly == Polynomial('1010100')

def test_modifyPolinomialOutOfIndex():
    poly= Polynomial('1')
    poly.change(1,1)
    poly.change(3,1)  
    poly.change(5,0)  
    assert poly == Polynomial('1011')

def test_modifyPolinomialWithOtherPolinomial():
    polyToBeChanged= Polynomial('1010001')
    changeBy=Polynomial('111')
    changedPoly =polyToBeChanged.changeByPoly(changeBy)
    assert changedPoly == Polynomial('1010111')

def test_flipBit():
    poly = Polynomial('100101011')
    poly.flipBit(5)
    assert poly == Polynomial('100001011')

def test_flipBitOutOfIndex():
    poly = Polynomial('1')
    with pytest.raises(Exception) as e_info:
        poly.flipBit(3)
    

def test_xOr():
    poly1 = Polynomial('10101')
    poly2 = Polynomial('00100')
    assert poly1.xOr(poly2)==17

def test_shiftBinaryLeft():
    poly1 = Polynomial('10101')
    poly1.shiftBinary(4)
    assert poly1 == Polynomial('101010000')

def test_shiftBinaryRight():
    poly1 = Polynomial('10101')
    poly1.shiftBinary(-4)
    assert poly1 == Polynomial('1')

def test_div():
    poly1 = Polynomial('11110101011101010')
    poly2 = Polynomial('10110')
    division = poly1/poly2
    print(division[0],division[1])    
    assert division == [Polynomial('1101100001100'),Polynomial('10')]

def test_div2():
    poly1 = Polynomial('1110')
    poly2 = Polynomial('1001')
    division = poly1/poly2   
    print(division[0],division[1])    
    assert division == [Polynomial('1'),Polynomial('111')]