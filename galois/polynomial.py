from util import decimal_to_base_n


modulus = 0
modulu_polynomial = None


def set_modulus(modulus_, polynomial):
    """
    modulus_ : int
    polynomial : list
    """
    global modulus, modulus_polynomial
    modulus = modulus_
    modulus_polynomial = Polynomial(polynomial)


class Element(object):
    def __init__(self, element):
        """
        Parameters
        element: The actual value of an element of a polynomial, given in int.
        """

        assert(isinstance(element, int))
        assert(modulus != 0)
        self.element = element % modulus

    def __eq__(self, other):
        return self.element == other.element

    def __str__(self):
        return str(self.element)

    def __add__(self, other):
        e = (self.element + other.element) % modulus
        return Element(e)

    def __mul__(self, other):
        e = (self.element * other.element) % modulus
        return Element(e)

    def __pow__(self, n):
        assert(n >= 0)
        if(n == 0):
            return Element(1)

        e = Element(1)
        for i in range(n):
            e *= self
        return e

    def __sub__(self, other):
        c = other.complement()
        e = (self.element + c.element) % modulus
        return Element(e)

    def __truediv__(self, other):
        for e in range(modulus):
            if((e * other.element) % modulus == self.element):
                return Element(e)
        return None

    def complement(self):
        return Element(modulus-self.element)


class Polynomial(object):
    def __init__(self, elements):
        """
        Parameters
        elements: Elements of a polynomial which given in string.
                  e.g "201" means 2*x^2+1
        """

        if not(isinstance(elements, list)):
            raise TypeError("Elements must be given as list")

        assert(modulus != 0)
        self.elements = [Element(e) for e in elements]
        self.elements = self._remove_trailing_zeros(self.elements)

    def _remove_trailing_zeros(self, elements):
        """
        Parameters:
        polynomial: list
        """
        """Remove trailing zeros. e.g., '000212' to '212'"""

        zero = Element(0)
        n = 0
        for i, e in enumerate(elements):
            if(i == len(elements)-1):
                return [elements[-1]]
            if(e != zero):
                n = i
                break
        return elements[n:]

    def __str__(self):
        return ' '.join(map(str, self.elements))

    def __setitem__(self, key, item):
        self.elements[key] = item

    def _add_elementwise(self, polynomial1, polynomial2):
        assert(len(polynomial1) == len(polynomial2))
        return [e1+e2 for e1, e2 in zip(polynomial1, polynomial2)]

    def __pow__(self, n):
        """
        pow(Polynomial([0]), 0) is defined as Polynomial([0])
        """

        assert(n >= 0)

        if(n == 0):
            return Polynomial([1])

        p = Polynomial([1])
        for i in range(n):
            p *= self
        return p

    def __len__(self):
        """Returns the degree of polynomial"""
        return len(self.elements)

    def __iter__(self):
        return iter(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def tolist(self):
        elements = map(str, self.elements)
        elements = list(map(int, elements))
        return elements

    def _elements_to_polynomial(self, elements):
        elements = map(str, elements)
        elements = list(map(int, elements))
        return Polynomial(elements)

    def __add__(self, polynomial):
        if(len(self) < len(polynomial)):
            e = self._add_elementwise(self, polynomial[-len(self):])
            elements = polynomial[:-len(self)] + e
        else:
            e = self._add_elementwise(self[-len(polynomial):], polynomial)
            elements = self[:-len(polynomial)] + e
        elements = self._remove_trailing_zeros(elements)
        p = self._elements_to_polynomial(elements)
        return p

    def complement(self):
        elements = [e.complement() for e in self]
        return self._elements_to_polynomial(elements)

    def __sub__(self, polynomial):
        return self+polynomial.complement()

    def _subtract_elementwise(self, polynomial1, polynomial2):
        """Compute polynomial1-polynomial2 element-wise"""
        assert(len(polynomial1) == len(polynomial2))
        return [e1-e2 for e1, e2 in zip(polynomial1, polynomial2)]

    def _multiply_element_to_polynomial(self, polynomial, element):
        """multiply a scalar to a polynomial"""
        return [element * e for e in polynomial]

    def __mul__(self, polynomial):
        """Multiple self to polynomial"""
        #the degree of the product
        degree = len(polynomial) + len(self) - 1
        product = [Element(0) for i in range(degree)]

        #compute polynomial * self
        s = len(polynomial)
        for i, e in enumerate(reversed(self)):
            p = self._multiply_element_to_polynomial(polynomial, e)
            t = self._add_elementwise(product[degree-s-i:degree-i], p)
            product[degree-s-i:degree-i] = t

        product = self._remove_trailing_zeros(product)
        return self._elements_to_polynomial(product)

    def _divide_with_remainder(self, polynomial1, polynomial2):
        """Compute polynomial1 / polynomial2"""
        """Returns: quotient and remainder"""

        if(len(polynomial2) > len(polynomial1)):
            return Polynomial([0]), self

        s = len(polynomial2)

        subtracted = polynomial1[:s]
        quotient = []
        for i in range(len(polynomial1)-s+1):
            element = subtracted[0]
            q = element / polynomial2[0]
            quotient.append(q)

            a = self._multiply_element_to_polynomial(polynomial2, q)
            subtracted = self._subtract_elementwise(subtracted, a)
            subtracted = subtracted[-s+1:]

            #FIXME comparison at each iteration
            if(s+i == len(polynomial1)):
                return quotient, subtracted

            subtracted.append(polynomial1[s+i])

    def __truediv__(self, polynomial):
        quotient, remainder = self._divide_with_remainder(self, polynomial)
        quotient = self._elements_to_polynomial(quotient)
        return quotient

    def __eq__(self, polynomial):
        a = isinstance(self, Polynomial) and isinstance(polynomial, Polynomial)
        b = self.tolist() == polynomial.tolist()
        return a and b

    def __mod__(self, polynomial):
        if(polynomial == Polynomial([0])):
            raise ZeroDivisionError

        quotient, remainder = self._divide_with_remainder(self, polynomial)
        remainder = self._elements_to_polynomial(remainder)
        return remainder

    def tomonic(self):
        e = Element(1) / self.elements[0]
        elements = self._multiply_element_to_polynomial(self.elements, e)
        return self._elements_to_polynomial(elements)


class PolynomialOnRing(Polynomial):
    def __init__(self, elements):
        super(PolynomialOnRing, self).__init__(elements)

    def __add__(self, polynomial):
        p = super(PolynomialOnRing, self).__add__(polynomial)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())

    def __sub__(self, polynomial):
        p = super(PolynomialOnRing, self).__sub__(polynomial)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())

    def __mul__(self, polynomial):
        p = super(PolynomialOnRing, self).__mul__(polynomial)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())

    def __pow__(self, n):
        p = super(PolynomialOnRing, self).__pow__(n)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())

    def __truediv__(self, polynomial):
        p = super(PolynomialOnRing, self).__truediv__(polynomial)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())

    def __mod__(self, polynomial):
        p = super(PolynomialOnRing, self).__mod__(polynomial)
        p = p % modulus_polynomial
        return PolynomialOnRing(p.tolist())


def is_primitive_root(polynomial):
    one = PolynomialOnRing([1])
    k = pow(modulus, len(polynomial)) - 1
    p = pow(polynomial, k)
    return p == one


def find_primitive_roots(degree):
    roots = []
    n = pow(modulus, degree)
    for i in range(2, n):
        e = decimal_to_base_n(i, modulus)
        p = PolynomialOnRing(e)
        if(is_primitive_root(p)):
            roots.append(p)
    return roots


def find_minimal_polynomial(polynomial):
    zero = PolynomialOnRing([0])
    i = 1

    while True:
        minimal_polynomial = decimal_to_base_n(i, modulus)

        p = PolynomialOnRing([0])
        for degree, coefficient in enumerate(reversed(minimal_polynomial)):
            c = PolynomialOnRing([coefficient])
            p += c * pow(polynomial, degree)

        if(p == zero):
            return PolynomialOnRing(minimal_polynomial)

        i += 1


def find_primitive_polynomials(degree):
    roots = find_primitive_roots(degree)
    primitive_polynomials = []
    for root in roots:
        p = find_minimal_polynomial(root)
        primitive_polynomials.append(p)
        print("root: {!s:>5}  p: {!s:>5}".format(root, p))
    return primitive_polynomials
