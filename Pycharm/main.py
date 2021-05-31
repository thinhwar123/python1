import random
from base64 import b64encode

import Crypto.Random
import hashlib
import numpy as np
import sys
from Crypto.Cipher import ChaCha20
from PIL import Image

def PRNG0(seed, total_pixels):
    # phương pháp cơ bản
    # Phương pháp nửa bình phương (Middle-square method)
    # return int(str(int(seed) ** 2).zfill(8)[2:6]) % total_pixels

    # phương pháp đồng dư bậc 2 với n = 10
    # return int(int(seed) * (int(seed) + 1) % 2**10) % total_pixels

    # phương pháp đồng dư tuyến tính (Linear congruence algorithm) với c = 13, a = 17 và m = 10091
    # return int(17 * int(seed) + 13) % 10091 % total_pixels

    # phương pháp dựa trên lý thuyết số học
    # Blum Blum Shub algorithm với p = 21169 và q = 22189
    # return int(int(seed) ** 2 % (21169 * 22189)) % total_pixels

    # Blum–Micali algorithm với g = 173 và p = 20173
    # return int(173 ** int(seed) % 20173) % total_pixels

    # phương pháp dựa trên mật mã học nguyên thuỷ
    # phương pháp sử dụng hàm băm SHA-256
    # return int.from_bytes(hashlib.sha256(str(seed).encode()).digest(), "little") % total_pixels

    # phương pháp đặc biệt
    # ChaCha20 algorithm
    key = 55528940176513310056720497386431866891917161321970637298210495689590489365111
    cipher = ChaCha20.new(key=key.to_bytes(32, "little"), nonce=int(seed).to_bytes(8, "little"))
    ciphertext = cipher.encrypt(int(123).to_bytes(32,"little"))
    return int.from_bytes(ciphertext, "little") % total_pixels

    return 1

def EncodeBasic(src, message, dest , seed):

    message += "$end"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    print("Thông điệp được mã hoá thành dạng nhị phân:")
    print(b_message)

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))


    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n
    # np.set_printoptions(threshold=sys.maxsize)
    print("Ma trận điểm ảnh bao gồm " + str(array.size//n) +" điểm ảnh")



    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")
    else:
        index=0
        already_seen = list()
        while index < req_pixels:
            seed = PRNG0(seed, total_pixels)
            if seed not in already_seen:
                already_seen.append(seed)
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
        print("Bộ số giả ngẫu nhiên:")
        print(already_seen)
        print("Image Encoded Successfully")


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
