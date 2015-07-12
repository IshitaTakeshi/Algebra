def decimal_to_base_n(x, n):
    assert(x >= 0)

    if x == 0:
        return [0]

    base_n = []
    while x > 0:
        base_n.append(x % n)
        x = x // n
    base_n.reverse()
    return base_n
