def pow_func(base, exponent):
    """Calculate the power of a number."""
    return base ** exponent


def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b