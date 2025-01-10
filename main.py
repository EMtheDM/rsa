import random


# Checks if number is prime or not
def is_prime(m):
    if m <= 1:
        return False
    for i in range(2, int(m ** 0.5) + 1):
        if m % i == 0:
            return False
    return True


def fme(a, n, b):  # function takes number with high exponent value, and finds mod value quickly
    result = 1
    square = a
    while n > 0:  # this loop converts number n into binary index by index
        k = n % 2
        if k == 1:
            result = (result * square) % b  # multiplies result and square, then finds the mod of that value and b
        square = (square * square) % b  # multiplies square by itself, then finds the mod of that value and b
        n = n // 2  # changes the value of n by dividing by 2 and getting floor value so while loop isn't infinite
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


# main function provides organization and starting point for running python script
def main():
    # Ask user for a prime number
    while True:
        try:
            p = int(input("Please enter a prime number: "))
            if is_prime(p):
                break
            else:
                print(f"{p} is not a prime number. Try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")  # exception exists in case user doesn't enter an integer.

    # Ask user for a second prime number
    while True:
        try:
            q = int(input("Please enter a second prime number: "))
            if is_prime(q) and q != p:
                break
            elif q == p:
                print("The second number cannot be the same as the first number.")
            else:
                print(f"{q} is not a prime number. Try again.")
        except ValueError:
            print("Invalid input. Please enter an integer.")  # exception exists in case user doesn't enter an integer.

    public_key = Find_Public_Key_e(p, q)
    n = public_key[0]
    e = public_key[1]
    print(f"public key n: {n}")
    print(f"public key e: {e}")

    q = factorize(n)  # brute force method of finding value of q if only n is known.
    p = n // q
    print(f"factor of n, p: {p}")
    print(f"factor of n, q: {q}")

    d = Find_Private_Key_d(e, p, q)  # d is the modular inverse of our exponent e.
    print(f"private key d: {d}")

    original_message = input("Please type out your message: ")

    encrypted_message = Encode(n, e,
                               original_message)  # function converts string to ascii unicode, then encrypts using fme() function.
    print(f"Encoded Message: {encrypted_message}")

    decrypted_message = Decode(n, d,
                               encrypted_message)  # function uses fme() function to decrypt back to ascii unicode, then converts back into string.

    print(f"Decoded Message: {decrypted_message}")


if __name__ == "__main__":
    main()