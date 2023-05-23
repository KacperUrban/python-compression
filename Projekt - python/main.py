from math import gcd
import collections
import pandas as pd
import matplotlib.pyplot as plt
import time


class RSA:
    def __init__(self, p, q, message):
        self.p = p
        self.q = q
        self.message = message
        self.n = 0
        self.e = 0
        self.d = 0
        self.ct = []
        self.mes = []

    def __str__(self):
        return f"Klucz publiczny = {self.e, self.n}, klucz prywatny = {self.d, self.n}, orygninalna wiadomosc = " \
               f"{self.message}"

    def generate_keys(self):
        # obliczamy n
        self.n = self.p * self.q

        # obliczamy funkcje Eulera
        t = (self.p - 1) * (self.q - 1)

        # wybieramy klucz publiczny, e
        for i in range(2, t):
            if gcd(i, t) == 1:
                self.e = i
                break

        # wybieramy klucz prywatny, d
        j = 0
        while True:
            if (j * self.e) % t == 1:
                self.d = j
                break
            j += 1

    def encryption(self):
        for i in range(0, len(self.message)):
            self.ct.append(ord(self.message[i]) ** self.e % self.n)
        print(f"Zaszyfrowana wiadomosc: {self.ct}")
        return self.ct

    def decryption(self):
        for i in range(0, len(self.message)):
            self.mes.append(chr((self.ct[i] ** self.d) % self.n))
        print(f"Odszyfrowana wiadomosc: {''.join(self.mes)}")


class Shannon:
    def __init__(self, message):
        self.message = str(message)
        self.c = {}
        self.encrypted_message = []
        self.letter_binary = []

    def generate_code(self):

        def create_list():
            list = dict(collections.Counter(self.message))
            list_sorted = sorted(iter(list.items()), key=lambda k_v: (k_v[1], k_v[0]), reverse=True)
            final_list = []
            for key, value in list_sorted:
                final_list.append([key, value, ''])
            return final_list

        def divide_list(list):
            if len(list) == 2:
                return [list[0]], [list[1]]
            else:
                n = 0
                for i in list:
                    n += i[1]
                x = 0
                distance = abs(2 * x - n)
                j = 0
                for i in range(len(list)):
                    x += list[i][1]
                    if distance < abs(2 * x - n):
                        j = i
            return list[0:j + 1], list[j + 1:]

        def label_list(list):
            # przypisywanie wartosi do lisci
            list1, list2 = divide_list(list)
            for i in list1:
                i[2] += '0'
                self.c[str(i[0])] = i[2]
            for i in list2:
                i[2] += '1'
                self.c[str(i[0])] = i[2]
            if len(list1) == 1 and len(list2) == 1:
                return
            label_list(list2)
            return self.c

        label_list(create_list())

    def compression(self):
        print("Zakodowane znaki:")
        for key, value in self.c.items():
            print(key, ' : ', value)
            self.letter_binary.append([key, value])
        for a in self.message:
            for key, value in self.c.items():
                if key in a:
                    self.encrypted_message.append(value)
        print(''.join(self.encrypted_message))

    def decompression(self):
        bitstring = ""
        for digit in self.encrypted_message:
            bitstring = bitstring + digit
        uncompressed_string = ""
        code = ""
        for digit in bitstring:
            code = code + digit
            pos = 0
            for letter in self.letter_binary:
                if code == letter[1]:
                    uncompressed_string = uncompressed_string + self.letter_binary[pos][0]
                    code = ""
                pos += 1

        print("Twoje rozpakowane dane:")
        print(uncompressed_string)


def divide_into_letters(words):
    letters = []
    for word in words:
        letters.extend(list(word))
        letters.extend(" ")
    return letters


if __name__ == '__main__':

    message = ""
    print("Wybierz tryb: ")
    choice = int(input("1. Wpisanie wiadomosci z terminala \n"
                       "2. Wpisanie wiadomosci z pliku\n"
                       "Wybor: "))

    if choice == 1:
        message = input("Wpisz wiadomosc do szyfrowania:")
    elif choice == 2:
        filename = input("Wpisz nazwe pliku do wczytania:")
        with open(filename, 'r') as f:
            x = f.read()
            message = divide_into_letters(x.split())
    else:
        filenames = ["1kb.txt", "5kb.txt", "10kb.txt", "50kb.txt", "100kb.txt", "280kb.txt", "1.1Mb.txt"]
        time_of_compression = []
        time_of_compression_and_decompression = []
        for filename in filenames:
            with open("data/" + filename, 'r') as f:
                x = f.read()
                message = divide_into_letters(x.split())
            start = time.time()
            start1 = time.time()
            shannon = Shannon(message)
            shannon.generate_code()
            shannon.compression()
            end = time.time()
            time_of_compression.append(end - start)
            shannon.decompression()
            end1 = time.time()
            time_of_compression_and_decompression.append(end1 - start1)
            with open("only_compressed/" + filename + "-compressed", 'w') as f:
                f.write(''.join(shannon.encrypted_message))
        print(time_of_compression)
