import unittest

import galois
from galois import Element, Polynomial, PolynomialOnRing

galois.set_modulus(3, [1, 0, 2])


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
    def test_init(self):
        a = Polynomial([1, 1, 2, 0, 1])
        self.assertEqual(a.tolist(), [1, 1, 2, 0, 1])

    def test_str(self):
        galois.set_modulus(25, [1, 0, 2])

        a = Polynomial([1, 0, 23, 00, 12])
        self.assertEqual(str(a), '1 0 23 0 12')

        galois.set_modulus(3, [1, 0, 2])

    def test_remove_trailing_zeros(self):
        a = Polynomial([0, 0, 2, 1])
        self.assertEqual(a.tolist(), [2, 1])
        a = Polynomial([0, 0, 0, 0])
        self.assertEqual(a.tolist(), [0])

    def test_add_elementwise(self):
        c = Polynomial([0])

        a = [Element(0), Element(2), Element(1)]
        b = [Element(1), Element(2), Element(2)]
        elements = c._add_elementwise(a, b)
        self.assertEqual([1, 1, 0], [e.element for e in elements])

    def test_add(self):
        a = Polynomial([1, 1, 2, 0, 1])
        b = Polynomial([1, 2])
        c = a+b
        self.assertEqual(c.tolist(), [1, 1, 2, 1, 0])

        a = Polynomial([1, 2])
        b = Polynomial([1, 1, 2, 0, 1])
        c = a+b
        self.assertEqual(c.tolist(), [1, 1, 2, 1, 0])

        a = Polynomial([2, 0, 1])
        b = Polynomial([1, 0, 2])
        c = a+b
        self.assertEqual(c.tolist(), [0])

    def test_complement(self):
        a = Polynomial([1, 2, 0])
        c = a.complement()
        self.assertEqual(c.tolist(), [2, 1, 0])

    def test_sub(self):
        a = Polynomial([2, 0, 1, 0, 1])
        b = Polynomial([1, 0, 2, 2, 0])
        c = a-b
        self.assertEqual(c.tolist(), [1, 0, 2, 1, 1])

    def test_multiply_element_to_polynomial(self):
        a = Polynomial([0])

        e = a._multiply_element_to_polynomial(Polynomial([1, 0, 2]),
                                              Element(2))
        p = a._elements_to_polynomial(e)
        self.assertEqual(p.tolist(), [2, 0, 1])

        e = a._multiply_element_to_polynomial(Polynomial([2, 2, 2, 1]),
                                              Element(2))
        p = a._elements_to_polynomial(e)
        self.assertEqual(p.tolist(), [1, 1, 1, 2])

    def test_mul(self):
        a = Polynomial([1, 1])
        b = Polynomial([1, 2])
        c = a * b
        self.assertEqual(c.tolist(), [1, 0, 2])

        a = Polynomial([2, 2, 1])
        b = Polynomial([1, 2, 0])
        c = a * b
        self.assertEqual(c.tolist(), [2, 0, 2, 2, 0])

        a = Polynomial([2, 1, 0])
        b = Polynomial([1, 1, 1])
        c = a * b
        self.assertEqual(c.tolist(), [2, 0, 0, 1, 0])

    def test_div(self):
        a = Polynomial([1, 1])
        b = Polynomial([2, 2])
        c = a / b
        self.assertEqual(c.tolist(), [2])

        a = Polynomial([1, 1, 2, 0, 1])
        b = Polynomial([1, 0, 2])
        c = a / b
        self.assertEqual(c.tolist(), [1, 1, 0])

        a = Polynomial([2, 1])
        b = Polynomial([1, 1, 0, 2, 1])
        c = a / b
        self.assertEqual(c.tolist(), [0])

    def test_mod(self):
        a = Polynomial([1, 1, 2, 0, 1])
        b = Polynomial([1, 0, 2])
        c = a % b
        self.assertEqual(c.tolist(), [1, 1])

        a = Polynomial([1, 0, 2])
        b = Polynomial([1, 1, 2, 0, 1])
        c = a % b
        self.assertEqual(c.tolist(), [1, 0, 2])

        a = Polynomial([1, 0, 1])
        b = Polynomial([1, 0, 2])
        c = a % b
        self.assertEqual(c.tolist(), [2])

    def test_tomonic(self):
        a = Polynomial([2, 0, 2, 1])
        a = a.tomonic()
        self.assertEqual(a.tolist(), [1, 0, 1, 2])

        a = Polynomial([1, 0, 2, 1])
        a.tomonic()
        self.assertEqual(a.tolist(), [1, 0, 2, 1])


class TestPolynomialOnRing(unittest.TestCase):
    def test_init(self):
        #TODO consider the behavior at initialization
        #a = PolynomialOnRing('11201')
        #self.assertEqual(str(a), '11')
        pass

    def test_add(self):
        a = PolynomialOnRing([1, 1, 2])
        b = PolynomialOnRing([1, 2, 0])
        c = a+b
        self.assertEqual(c.tolist(), [1])

        a = PolynomialOnRing([1, 2, 1, 0, 0])
        b = PolynomialOnRing([1, 1, 2, 1, 1])
        c = a+b
        self.assertEqual(c.tolist(), [1, 0])

        a = PolynomialOnRing([2, 0, 1])
        b = PolynomialOnRing([1, 0, 2])
        c = a+b
        self.assertEqual(c.tolist(), [0])

    def test_sub(self):
        a = PolynomialOnRing([2, 0, 1, 0, 1])
        b = PolynomialOnRing([1, 0, 2, 2, 0])
        c = a-b
        self.assertEqual(c.tolist(), [1, 1])

    def test_mul(self):
        a = PolynomialOnRing([1, 1])
        b = PolynomialOnRing([1, 2])
        c = a * b
        self.assertEqual(c.tolist(), [0])

        a = PolynomialOnRing([2, 2, 1])
        b = PolynomialOnRing([1, 2, 0])
        c = a * b
        self.assertEqual(c.tolist(), [2, 1])

        a = PolynomialOnRing([2, 1, 0])
        b = PolynomialOnRing([1, 1, 1])
        c = a * b
        self.assertEqual(c.tolist(), [1, 2])

    def test_div(self):
        a = PolynomialOnRing([1, 1])
        b = PolynomialOnRing([2, 2])
        c = a / b
        self.assertEqual(c.tolist(), [2])

        a = PolynomialOnRing([1, 1, 0, 2, 1])
        b = PolynomialOnRing([2, 1])
        c = a / b
        self.assertEqual(c.tolist(), [0])

        a = PolynomialOnRing([2, 1])
        b = PolynomialOnRing([1, 1, 0, 2, 1])
        c = a / b
        self.assertEqual(c.tolist(), [0])

    def test_mod(self):
        a = PolynomialOnRing([1, 1, 2, 0, 1])
        b = PolynomialOnRing([1, 0, 1])
        c = a % b
        self.assertEqual(c.tolist(), [2, 0])


unittest.main()
