# This serves as a simple reference to RSA functions that I have created that may or may not be used

import random


def convert_binary_string(n):
    if n == 0:  # Conditional checks if decimal expression is zero and will simply return 0 for binary
        return "0"
    binary = ""
    while n > 0:  # While loop converts decimal integer to binary by looping through each digit by index, taking modulo 2 and replacing it with remainder; either 1 or 0
        binary = str(n % 2) + binary
        n = n // 2

    return binary


def fme(b, n, m):  # function takes number b with large exponent value n, and finds the mod m quickly
    result = 1
    square = b  # simply assigning b which is our main integer to variable 'square'
    while n > 0:  # this while loop will convert each digit of exponent n to binary
        k = n % 2  # finds modulo of n, will either be 1 or 0 (binary)
        if k == 1:
            result = (result * square) % m  # multiplies result by square, then finds mod m and sets the new value to variable result
        square = (square * square) % m  # multiplies square by itself, then finds mod m and sets the new value to variable square
        n = n // 2  # divides exponent n by 2 and sets the floor value to n. This prevents an infinite loop
    return result


def Euclidean_Alg(a, b):
    # Loop works its way down a and b's factors to find the greatest common divisor
    while b > 0:
        modulo = a % b
        a = b
        b = modulo
        x = a
    return x


def EEA(a, b):
    # represent our initial values of s1, t1, s2 and t2 to find our coefficients
    (s1, t1) = (1, 0)
    (s2, t2) = (0, 1)

    # Loop works its way down a and b's factors to find Bezout's co-efficients (s, t) where (a*s + b*t = 1)
    while b > 0:
        modulo = a % b
        q = a // b
        a = b
        b = modulo

        # updating values of s1_hat, s2_hat, t1_hat, t2_hat, s1, s2, t1 and t2
        (s1_hat, t1_hat) = (s2, t2)
        (s2_hat, t2_hat) = (s1 - q * s2, t1 - q * t2)
        (s1, t1) = (s1_hat, t1_hat)
        (s2, t2) = (s2_hat, t2_hat)

        x = a
    return x, (s1, t1)


def Find_Public_Key_e(p, q):
    n = p * q
    phi_n = (p - 1) * (q - 1)  # value will equal a relatively prime integer
    e = random.randint(2, phi_n - 1)

    while Euclidean_Alg(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)  # e can be any random integer between 2 (lowest prime) and phi_n - 1

    return n, e


def Find_Private_Key_d(e, p, q):
    phi_n = (p - 1) * (q - 1)  # value will equal a relatively prime integer

    eea_result = EEA(e, phi_n)  # returns gcd as well as Bezout's co-efficient's
    gcd = eea_result[0]
    s = eea_result[1][0]

    if gcd != 1:
        print("Error: e and phi_n are not relatively prime!")

    d = s % phi_n  # modular inverse of e

    return d


def Convert_Text(_string):
    integer_list = []
    for char in _string:
        integer_list.append(ord(char))  # ord() return unicode character

    return integer_list


def Convert_Num(_list):
    _string = ''
    for i in _list:
        _string += chr(i)  # chr() converts from unicode to ascii text
    return _string


def Encode(n, e, message):
    cipher_text = []
    message_list = Convert_Text(message)
    for i in message_list:
        cipher_text.append(fme(i, e, n))  # need fme() otherwise running function is slow
    return cipher_text


def Decode(n, d, cipher_text):
    decode_list = []
    for i in cipher_text:
        decode_list.append(fme(i, d, n))  # need fme() otherwise running function is slow
    message = Convert_Num(decode_list)
    return message

def factorize(n):
    # brute force finds q in n
    for i in range(2, n):
        if n % i == 0:
            return i
    return False