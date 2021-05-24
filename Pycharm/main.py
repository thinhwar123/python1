import random

import Crypto.Random
import hashlib
import numpy as np
from Crypto.Cipher import AES
from PIL import Image


def PRNG0(seed, total_pixels):
    # phương pháp cơ bản
    # Phương pháp nửa bình phương (Middle-square method)
    # return int(str(int(seed) ** 2).zfill(8)[2:6]) % total_pixels

    # phương pháp bình phương bậc 2 với n = 10
    # return int(int(seed) * (int(seed) + 1) % 2**10) % total_pixels

    # phương pháp đồng dư tuyến tính (Linear congruence algorithm) với c = 13, a = 17 vaf m = 10091
    # return int(17 * int(seed) + 13) % 10091 % total_pixels

    # phương pháp dựa trên lý thuyết số học
    # Blum Blum Shub algorithm với p = 21169 và q = 22189
    # return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels

    # Blum–Micali algorithm với g = 173 và p = 20173
    return int(173 ** int(seed) % 20173) % total_pixels

    return 1

def EncodeBasic(src, message, dest , seed):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "$end"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        already_seen = set()
        while index < req_pixels:
            seed = PRNG0(seed, total_pixels)
            if seed not in already_seen:
                already_seen.add(seed)
                for i in range(0, 3):
                    if index < req_pixels:
                        array[seed][i] = int(bin(array[seed][i])[2:9] + b_message[index], 2)
                        index += 1
            else:
                print("ERROR: Need another key")
                break

        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        enc_img.save(dest)
        print("Image Encoded Successfully")
        print(already_seen)

def DecodeBasic(src, seed):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n
    start = 64
    while 1:
        hidden_bits = ""
        temp_seed = seed
        for p in range(start):
            temp_seed = PRNG0(temp_seed, total_pixels)
            for q in range(0, 3):
                hidden_bits += (bin(array[temp_seed][q])[2:][-1])

        hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            if message[-4:] == "$end":
                break
            else:
                message += chr(int(hidden_bits[i], 2))
        if "$end" in message:
            print("Hidden Message:", message[:-4])
            break
        else:
            start += 64



def run(seed):
    print("1: Encode Basic")
    print("2: Decode Basic")
    func = input()

    if func == '1':
        print("Enter Source Image Path")
        src = input()
        print("Enter Message to Hide")
        message = input()
        print("Enter Destination Image Path")
        dest = input()
        print("Encoding...")
        EncodeBasic(src, message, dest, seed)

    elif func == '2':
        print("Enter Source Image Path")
        src = input()
        print("Decoding...")
        DecodeBasic(src, seed)

    else:
        print("ERROR: Invalid option chosen")


if __name__ == '__main__':
    seed = "1234"
    run(seed)
