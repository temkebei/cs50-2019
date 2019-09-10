import cs50
import os.path
import sys


def main():
    # ensures correct command line input
    if len(sys.argv) != 2 or len(str(sys.argv[1])) < 5 or str(sys.argv[1][len(str(sys.argv[1])) - 4: len(str(sys.argv[1]))]) != ".txt":
        print("Usage: python bleep.py dictionary")
        # error handling
        sys.exit(1)

    # checks that the dictionary file exists, opens file if so, exits with error code if not
    if os.path.isfile(sys.argv[1]) != True:
        print("File does not exist")
        sys.exit(1)
    else:
        dictionary = open(sys.argv[1], "r")

    # creates an empty set to store dictionary words, iterates through each line of dictionary adding words to set
    words = set()
    for line in dictionary:
        words.add(line.rstrip("\n"))
    dictionary.close()

    # splits p into list of individual words and iterates through them
    p = cs50.get_string("What message would you like to censor?\n")
    for word in p.split():
        if str.lower(word) in words:
            print("*" * len(word), end=" ")
        else:
            print(word, end=" ")
    print()
    sys.exit(0)


if __name__ == "__main__":
    main()