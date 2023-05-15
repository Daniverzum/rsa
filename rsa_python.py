import math, random


def generate_key(p: int, q: int) -> tuple[tuple[int, int], tuple[int, int]]:
    p, q = int(p), int(q)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        e = random.randrange(2, phi)
        lnkt = math.gcd(e, phi)
        if lnkt == 1:
            d = _get_d(e, phi)
            if e != d and d != -1:
                break

    return ((d, n), (e, n))


def _get_d(e: int, m: int) -> int:
    for x in range(1, m):
        if (e * x) % m == 1:
            return x
    return -1


def encrypt(public_key: tuple[int, int], plain: int) -> int:
    e, n = public_key
    plain = int(plain)

    encrypted = (plain**e) % n

    return encrypted


def decrypt(private_key: tuple[int, int], cipher: int) -> int:
    d, n = private_key
    cipher = int(cipher)

    decrypted = (cipher**d) % n

    return decrypted


def sign(private_key: tuple[int, int], message: int) -> tuple[int, int]:
    d, n = private_key
    message = int(message)

    signature = (message ** d) % n

    return (message, signature)


def verify(public_key: tuple[int, int], signed_message: tuple[int, int]) -> bool:
    e, n = public_key
    message, signature = int(signed_message[0]), int(signed_message[1])

    verified = (signature**e) % n == message

    return verified


def encrypt_text(public_key: tuple[int, int], plain_msg: str) -> str:
    encrypted = ""
    for letter in plain_msg:
        encrypted += chr(encrypt(public_key, ord(letter)))

    return encrypted


def decrypt_text(private_key: tuple[int, int], cipher_msg: str) -> str:
    decrypted = ""
    for letter in cipher_msg:
        decrypted += chr(decrypt(private_key, ord(letter)))

    return decrypted


def sign_text(private_key: tuple[int, int], plain_message: str) -> list[tuple[int, int]]:
    signed_message = []
    for letter in plain_message:
        signed_message.append(sign(private_key, ord(letter)))

    return signed_message


def verify_text(private_key: tuple[int, int], signed_message: list[tuple[int, int]]) -> bool:
    verified = True
    for msg_letter, signed_letter in signed_message:
        if not verify(private_key, (msg_letter, signed_letter)):
            verified = False

    return verified


def main():
    print("notes: > the larger the key, the larger message it can cipher")
    print("       > too big q and p could make the program really slow")
    print("       > p and q must be prime")
    print("       > p != q")
    print("")
    print("(1) - Number encryption")
    print("(2) - Text encryption")
    p = 13
    q = 17
    selected = int(input("Select: "))
    if selected == 1:
        p = input("p: ")
        q = input("q: ")
        public, private = generate_key(p, q)
        print("Public Key: ", public)
        print("Private Key: ", private)
        msg = input("Write msg: ")
        encrypted_msg = encrypt(public, msg)
        print("Encrypted msg:", encrypted_msg)
        decrypted_msg = decrypt(private, encrypted_msg)
        print("Decrypted msg:", decrypted_msg)
        print()
        signed_message = sign(private, msg)
        print("signed_message:", signed_message)
        print("signature_verified:", verify(public, signed_message))

    if selected == 2:
        p = input("p: ")
        q = input("q: ")
        public, private = generate_key(p, q)
        print("Public Key: ", public)
        print("Private Key: ", private)
        msg = input("Write msg: ")
        encrypted_msg = encrypt_text(public, msg)
        print("Encrypted msg:", encrypted_msg)
        decrypted_msg = decrypt_text(private, encrypted_msg)
        print("Decrypted msg:", decrypted_msg)
        print()
        signed_message = sign_text(private, msg)
        print("signed_message:", signed_message)
        print("signature_verified:", verify_text(public, signed_message))


#===========================================================
if __name__ == "__main__":
    main()