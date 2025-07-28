from app.cache import get_cache, set_cache


def pow_func(base, exponent):
    """Calculate the power of a number."""
    cache_key = f"power:{base}:{exponent}"
    cached = get_cache(cache_key)
    if cached is not None:
        return cached

    result = base ** exponent
    set_cache(cache_key, result)

    return result


def fibonacci(n):
    """Calculate the nth Fibonacci number."""
    cache_key = f"fibonacci_{n}"
    cached = get_cache(cache_key)
    if cached is not None:
        return cached

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b

    set_cache(cache_key, a)

    return a


def factorial(n):
    """Calculate the factorial of a number."""
    cache_key = f"factorial_{n}"
    cached = get_cache(cache_key)
    if cached is not None:
        return cached

    result = 1
    for i in range(2, n + 1):
        result *= i

    set_cache(cache_key, result)

    return result
