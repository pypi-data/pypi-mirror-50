"""
Maomao
"""

import sys

mao_table = [
        ( 'ao', ' '),
        ( 'aO', 'a'),
        ( 'Ao', 'e'),
        ( 'AO', 'i'),
        ( 'aoo', 'o'),
        ( 'aoO', 'u'),
        ( 'aOo', 't'),
        ( 'aOO', 'n'),
        ( 'Aoo', 's'),
        ( 'AoO', 'r'),
        ( 'AOo', 'h'),
        ( 'AOO', 'd'),
        ( 'aao', 'l'),
        ( 'aaO', 'c'),
        ( 'aAo', 'm'),
        ( 'aAO', 'f'),
        ( 'Aao', 'y'),
        ( 'AaO', 'w'),
        ( 'AAo', 'g'),
        ( 'AAO', 'p'),
        ( 'aaao', 'b'),
        ( 'aaaO', 'v'),
        ( 'AAAo', 'k'),
        ( 'Aaao', 'x'),
        ( 'AaaO', 'q'),
        ( 'AAAO', 'j'),
        ( 'aAAo', 'z'),
]

def is_mao(text):
    for letter in text:
        if letter.lower() in 'bcdefghijklnpqrstuvwxyz':
            return False
    return True

def eng_to_mao(text):
    translation = list(text)
    for i, letter in enumerate(translation):
        for mao, eng in mao_table:
            if letter.lower() == eng:
                if letter.istitle():
                    translation[i] = 'M'+mao+' '
                else:
                    translation[i] = 'm'+mao+' '
    return ''.join(translation)

def mao_to_eng(text):
    translation = text.split(' ')
    for i, word in enumerate(translation):
        for mao, eng in mao_table:
            head = ""
            mao_word = ""
            tail = ""
            list_word = list(word)
            while len(list_word):
                letter = list_word.pop(0)
                if letter not in "mM":
                    head += letter
                else:
                    mao_word += letter
                    break
            while len(list_word):
                letter = list_word.pop(0)
                if letter in 'aAoO':
                    mao_word += letter
                else:
                    tail += letter
                    break
            tail += ''.join(list_word)

            if mao_word[0:1].lower() == 'm' and mao_word[1:] == mao:
                if mao_word[0:1].istitle():
                    translation[i] = head+eng.upper()+tail
                else:
                    translation[i] = head+eng+tail
    return ''.join(translation)

def main():
    text = ' '.join(sys.argv[1:])
    if is_mao(text):
        print(mao_to_eng(text))
    else:
        print(eng_to_mao(text))

if __name__ == '__main__':
    main()


