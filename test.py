import unittest

import polynomial_galois
from polynomial_galois import Element, Polynomial, PolynomialOnRing

polynomial_galois.order = 3
polynomial_galois.order_polynomial = Polynomial('102')


class TestElement(unittest.TestCase):
    def test_init(self):
        a = Element(-1)
        self.assertEqual(a.element, 2)

        a = Element(4)
        self.assertEqual(a.element, 1)

    def test_complement(self):
        a = Element(1)
        c = a.complement()
        self.assertEqual(c.element, 2)

    def test_add(self):
        a = Element(1)
        b = Element(1)
        c = a+b
        self.assertEqual(c.element, 2)

        a = Element(2)
        b = Element(2)
        c = a+b
        self.assertEqual(c.element, 1)

    def test_mul(self):
        a = Element(1)
        b = Element(2)
        c = a*b
        self.assertEqual(c.element, 2)

        a = Element(3)
        b = Element(2)
        c = a*b
        self.assertEqual(c.element, 0)

    def test_sub(self):
        a = Element(1)
        b = Element(2)
        c = a-b
        self.assertEqual(c.element, 2)

        a = Element(0)
        b = Element(1)
        c = a-b
        self.assertEqual(c.element, 2)

    def test_div(self):
        a = Element(1)
        b = Element(2)
        c = a / b
        self.assertEqual(c.element, 2)

        a = Element(0)
        b = Element(2)
        c = a / b
        self.assertEqual(c.element, 0)


class TestPolynomial(unittest.TestCase):
    def test_str(self):
        a = Polynomial('11201')

    def test_remove_trailing_zeros(self):
        #a = Polynomial('0021')
        #self.assertEqual(str(a), '21')
        a = Polynomial('0000')
        #self.assertEqual(str(a), '0')

    def test_add_elementwise(self):
        c = Polynomial('0')

        a = [Element(0), Element(2), Element(1)]
        b = [Element(1), Element(2), Element(2)]
        elements = c._add_elementwise(a, b)
        self.assertEqual([1, 1, 0], [e.element for e in elements])

    def test_add(self):
        a = Polynomial('11201')
        b = Polynomial('12')
        c = a+b
        self.assertEqual(str(c), '11210')

        a = Polynomial('12')
        b = Polynomial('11201')
        c = a+b
        self.assertEqual(str(c), '11210')

        a = Polynomial('201')
        b = Polynomial('102')
        c = a+b
        self.assertEqual(str(c), '0')

    def test_complement(self):
        a = Polynomial('120')
        c = a.complement()
        self.assertEqual(str(c), '210')

    def test_sub(self):
        a = Polynomial('20101')
        b = Polynomial('10220')
        c = a-b
        self.assertEqual(str(c), '10211')

    def test_multiply_element_to_polynomial(self):
        a = Polynomial('0')

        e = a._multiply_element_to_polynomial(Polynomial('102'), Element(2))
        self.assertEqual(str(a._elements_to_polynomial(e)), '201')

        e = a._multiply_element_to_polynomial(Polynomial('2221'), Element(2))
        self.assertEqual(str(a._elements_to_polynomial(e)), '1112')

    def test_mul(self):
        a = Polynomial('11')
        b = Polynomial('12')
        c = a * b
        self.assertEqual(str(c), '102')

        a = Polynomial('221')
        b = Polynomial('120')
        c = a * b
        self.assertEqual(str(c), '20220')

        a = Polynomial('210')
        b = Polynomial('111')
        c = a * b
        self.assertEqual(str(c), '20010')

    def test_div(self):
        a = Polynomial('11')
        b = Polynomial('22')
        c = a / b
        self.assertEqual(str(c), '2')

        a = Polynomial('11201')
        b = Polynomial('102')
        c = a / b
        self.assertEqual(str(c), '110')

        a = Polynomial('21')
        b = Polynomial('11021')
        c = a / b
        self.assertEqual(str(c), '0')

    def test_mod(self):
        a = Polynomial('11201')
        b = Polynomial('102')
        c = a % b
        self.assertEqual(str(c), '11')

        a = Polynomial('102')
        b = Polynomial('11201')
        c = a % b
        self.assertEqual(str(c), '102')

        a = Polynomial('101')
        b = Polynomial('102')
        c = a % b
        self.assertEqual(str(c), '2')

    def test_tomonic(self):
        a = Polynomial('2021')
        self.assertEqual(str(a.tomonic()), '1012')

        a = Polynomial('1021')
        self.assertEqual(str(a.tomonic()), '1021')


class TestPolynomialOnRing(unittest.TestCase):
    def test_init(self):
        #TODO consider the behavior at initialization
        #a = PolynomialOnRing('11201')
        #self.assertEqual(str(a), '11')
        pass

    def test_add(self):
        a = PolynomialOnRing('112')
        b = PolynomialOnRing('120')
        c = a+b
        self.assertEqual(str(c), '1')

        a = PolynomialOnRing('12100')
        b = PolynomialOnRing('11211')
        c = a+b
        self.assertEqual(str(c), '10')

        a = PolynomialOnRing('201')
        b = PolynomialOnRing('102')
        c = a+b
        self.assertEqual(str(c), '0')

    def test_sub(self):
        a = PolynomialOnRing('20101')
        b = PolynomialOnRing('10220')
        c = a-b
        self.assertEqual(str(c), '11')

    def test_mul(self):
        a = PolynomialOnRing('11')
        b = PolynomialOnRing('12')
        c = a * b
        self.assertEqual(str(c), '0')

        a = PolynomialOnRing('221')
        b = PolynomialOnRing('120')
        c = a * b
        self.assertEqual(str(c), '21')

        a = PolynomialOnRing('210')
        b = PolynomialOnRing('111')
        c = a * b
        self.assertEqual(str(c), '12')

    def test_div(self):
        a = PolynomialOnRing('11')
        b = PolynomialOnRing('22')
        c = a / b
        self.assertEqual(str(c), '2')

        a = PolynomialOnRing('11021')
        b = PolynomialOnRing('21')
        c = a / b
        self.assertEqual(str(c), '0')

        a = PolynomialOnRing('21')
        b = PolynomialOnRing('11021')
        c = a / b
        self.assertEqual(str(c), '0')

    def test_mod(self):
        a = PolynomialOnRing('11201')
        b = PolynomialOnRing('101')
        c = a % b
        self.assertEqual(str(c), '20')


unittest.main()
