from sys import argv
from random import shuffle

def main(text):
    text = text.strip()

    split_text = text.split(" ")

    shuffled_letters = text.replace(" ", "")
    shuffled_letters = list(shuffled_letters)
    shuffle(shuffled_letters)

    words_lenths = []
    for word in split_text:
        words_lenths.append(len(word))

    shuffled_text = []
    for length in words_lenths:
        word = ""
        for _ in range(length):
            word += shuffled_letters.pop()
        shuffled_text.append(word)
    print(" ".join(shuffled_text))


if __name__ == "__main__":
    main(argv[1])
