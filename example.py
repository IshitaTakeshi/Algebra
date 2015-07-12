import galois

galois.set_modulus(3, [1, 0, 1])

primitive_polynomials = galois.find_primitive_polynomials(2)

#print(galois.find_minimal_polynomial(galois.PolynomialOnRing([1, 0])))
