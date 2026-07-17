#!/usr/bin/env python3
"""
next_prime.py

Termux-ready script to find the next prime after a (possibly 100+ digit) integer.

Usage:

    python next_prime.py
    # then paste or type your big number and press Enter

or:

    echo 1234567890123 | python next_prime.py
    python next_prime.py 1234567890123
"""

import sys
import random

# Optional: use sympy if installed for deterministic primality checking
try:
    from sympy import isprime as sympy_isprime
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False


def is_probable_prime(n: int, rounds: int = 32) -> bool:
    """
    Miller–Rabin probabilistic primality test.

    For large numbers (100+ digits), this is extremely reliable with ~32 rounds.
    Returns True if n is probably prime, False if definitely composite.
    """

    # Handle small cases fast
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as d * 2^s with d odd
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # Witness loop
    for _ in range(rounds):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            # Composite
            return False

    # Probably prime
    return True


def is_prime(n: int) -> bool:
    """
    Unified primality test.
    - Uses sympy.isprime() if available (deterministic).
    - Otherwise uses Miller–Rabin probabilistic test.
    """
    if HAS_SYMPY:
        return sympy_isprime(n)
    return is_probable_prime(n)


def next_prime(n: int) -> int:
    """
    Return the smallest prime strictly greater than n.
    Works for very large integers (hundreds of digits).
    """
    if n < 2:
        return 2

    # Start from the next integer
    candidate = n + 1

    # If even, step to odd
    if candidate % 2 == 0:
        candidate += 1

    # Increment by 2 (stay on odd numbers only)
    while not is_prime(candidate):
        candidate += 2

    return candidate


def read_input_int() -> int:
    """
    Read an integer from either:
    - command line argument, or
    - stdin / interactive input.
    """
    # 1) Command line argument
    if len(sys.argv) >= 2:
        user_input = sys.argv[1].strip()
    else:
        # 2) stdin or interactive prompt
        if sys.stdin.isatty():
            user_input = input("Enter an integer (can be 100+ digits): ").strip()
        else:
            user_input = sys.stdin.read().strip()

    if not user_input:
        print("No input provided.", file=sys.stderr)
        sys.exit(1)

    try:
        return int(user_input)
    except ValueError:
        print("Error: input is not a valid integer.", file=sys.stderr)
        sys.exit(1)


def main():
    n = read_input_int()
    p = next_prime(n)
    print(p)


if __name__ == "__main__":
    main()
