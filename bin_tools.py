import binascii

def text_to_binary_file(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    binary_text = ''.join(format(ord(char), '08b') for char in text)

    with open(output_file, 'w') as file:
        file.write(binary_text)

def binary_to_text_file(input_file, output_file):
    with open(input_file, 'r') as file:
        binary_string = file.read().strip()

    # Split binary string into 8-bit segments (bytes)
    bytes_list = [binary_string[i:i+8] for i in range(0, len(binary_string), 8)]

    # Convert each byte to its ASCII character representation
    text = ''.join(chr(int(byte, 2)) for byte in bytes_list)

    with open(output_file, 'w') as file:
        file.write(text)

def text_to_binary(input_text):
    # binary_text = ''.join(format(ord(char), '08b') for char in input_text)
    h = binascii.hexlify(input_text.encode())
    binary_text = bin(int(h, 16))[2:].zfill(8 * len(input_text))
    return binary_text

def binary_to_text(input_binary):
    # bytes_list = [input_binary[i:i+8] for i in range(0, len(input_binary), 8)]
    # text = ''.join(chr(int(byte, 2)) for byte in bytes_list)
    if len(input_binary) % 8 != 0:
        input_binary = input_binary.zfill(len(input_binary) + (8 - len(input_binary) % 8)).strip()
    # print('|'+input_binary+'|')
    text = binascii.unhexlify('%x' % (int(input_binary, 2))).decode()
    return text

def is_binary(input_string):
    for char in input_string:
        if char not in {'0', '1'}:
            return False
    return True

if __name__ == "__main__":
    input_file = "input.txt"
    output_file = "output.txt"
    binary_to_text(input_file, output_file)
