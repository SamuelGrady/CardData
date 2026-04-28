import itertools
from math import factorial, floor, log2
import bin_tools
from PIL import Image
import numpy as np
import math

def combination_to_number(combination):
    numbers = list(range(size))
    index = 0
    for i in range(size):
        base = factorial(size-1-i)
        index += numbers.index(combination[i])*base
        numbers.remove(combination[i])
    return index

def number_to_combination(index):
    numbers = list(range(size))
    combination = []
    for i in range(size):
        base = factorial(size-1-i)
        digit = floor(index/base)
#        print(index, numbers, combination, i, base, digit)
        combination.append(numbers[digit])
        numbers.pop(digit)
        index -= digit*base
    return combination

def numbers_to_cards(number_list):
    cards = []
    for suit in "sdch":
        for value in ["A"] + list(range(2,11)) + ["J", "Q", "K"]:
            cards.append(f"{value}{suit}")

    return [cards[i - 1] for i in number_list]

def cards_to_numbers(card_list):
    cards = []
    for suit in "sdch":
        for value in ["A"] + list(range(2,11)) + ["J", "Q", "K"]:
            cards.append(f"{value}{suit}")
    
    return [cards.index(card) + 1 for card in card_list]

imagebits = ""

try:
    image = Image.open('input.bmp').convert('L')
    image_array = np.array(image)

    for row in image_array:
        for pixel in row:
            imagebits += str(int(bool(pixel)))
except:
    pass

size = int(input('Size #>'))
print('\033[2J\033[H', end='') # clear the screen
# size = 52
try:
    while True:
        mode = input('(E)ncode or (D)ecode ?>').lower()
        if mode == 'e':
            max_bits = floor(log2(factorial(size)))-1
            textinput = input(f'Enter binary (<={max_bits} bits),\nor text (<={floor(max_bits/8)} characters)\n>')
            if imagebits and textinput == "image":
                bininput = imagebits
            elif bin_tools.is_binary(textinput):
                bininput = textinput
            else:
                bininput = bin_tools.text_to_binary(textinput)
            # index = int('1'+bininput,2)
            index = int(bininput,2)
            # print(f'Text input: {textinput}, Binary input: {bininput}, Base-10: {index}')
            combination = [i + 1 for i in number_to_combination(index)]
            # print(f'Final output: {combination}')

            print()
            print(f"Text: {textinput}")
            print(f"Binary: {bininput}")
            print(f"Base-10: {index}")
            print(f"Cards: {','.join(numbers_to_cards(combination))}")
        elif mode == 'd':
            listinput = input('Enter combination (seperated by comma)\n>')
            if any(not item.isdigit() for item in listinput.split(',')):
                combination = cards_to_numbers([item.strip() for item in listinput.split(',')])
            else:
                combination = [int(number) for number in listinput.split(',')]
            # print(f'\nInput: {combination}')
            index = combination_to_number([i - 1 for i in combination])
            binindex = bin(index)[2:]
            # print(bin(index))
            try:
                textoutput = bin_tools.binary_to_text(binindex)
            except:
                textoutput = "none"
            # print(f'Base-10: {index}\nBinary output: {binindex}\nText output: {textoutput}\n')
            
            print()
            print(f"Cards: {','.join(numbers_to_cards(combination))}")
            print(f"Base-10: {index}")
            print(f"Binary: {binindex}")
            print(f"Text: {textoutput}")

            imgbin = binindex.zfill(15*15) if len(binindex) < 15*15 else binindex[-(15*15):]
            # print(imgbin)
            # print('Image saved to output.bmp')
            image_size = int(math.sqrt(len(imgbin)))
            image_array = np.zeros((image_size, image_size), dtype=np.uint8)
            for i in range(image_size):
                for j in range(image_size):
                    bit_index = i*image_size + j
                    if bit_index < len(imgbin):
                        image_array[i][j] = 255 if imgbin[bit_index] == '1' else 0
            image = Image.fromarray(image_array)
            image.save('output.bmp')
        
        input()
        print("="*40)
        print()
except KeyboardInterrupt:
    print("\nExitting...")