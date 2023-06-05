from Crypto.Util.number import getPrime


class RSA:
    def __init__(self, key_size):
        self.key_size = key_size
        self.n = 0
        self.e = 0
        self.d = 0

    def __str__(self):
        return f"Klucz publiczny = {self.e, self.n}, klucz prywatny = {self.d, self.n}"

    def generate_keys(self):
        # Generowanie liczb pierwszych p i q
        p = getPrime(self.key_size // 2)
        q = getPrime(self.key_size // 2)

        # Obliczanie n
        self.n = p * q

        # Obliczanie funkcji Eulera
        t = (p - 1) * (q - 1)

        # Wybieranie klucza publicznego e
        self.e = 65537  # Wartość zalecana dla e

        # Obliczanie klucza prywatnego d
        self.d = pow(self.e, -1, t)

    def encryption(self, message):
        encrypted_message = []
        for char in message:
            m = ord(char)
            c = pow(m, self.e, self.n)
            encrypted_message.append(c)
        return encrypted_message

    def decryption(self, encrypted_message):
        decrypted_message = ""
        for c in encrypted_message:
            m = pow(c, self.d, self.n)
            char = chr(m)
            decrypted_message += char
        return decrypted_message


if __name__ == '__main__':

    while (True):
        try:
            file_path = input("Podaj ścieżkę do pliku: ")

            # Wczytanie zawartości pliku
            with open(file_path, 'r') as file:
                message = file.read()

            rsa = RSA(2048)  # Rozmiar klucza 2048 bitów
            rsa.generate_keys()
            encrypted = rsa.encryption(message)
            print(f"Zaszyfrowana wiadomość: {encrypted}")

            # Zapisanie zaszyfrowanej wiadomości do pliku
            encrypted_file_path = input("Podaj ścieżkę do pliku, w którym chcesz zapisać zaszyfrowaną wiadomość: ")
            with open(encrypted_file_path, 'w') as encrypted_file:
                encrypted_file.write(str(encrypted))

            decrypted = rsa.decryption(encrypted)
            print(f"Odszyfrowana wiadomość: {decrypted}")
        except:
            print("Program zakonczony!")
