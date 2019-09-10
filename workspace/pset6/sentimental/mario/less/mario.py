from cs50 import get_int

def main():
    while True:
        height = get_int("Height: ")
        width = height
        if height >= 1 and height <= 23:
            break

    for i in range(height):
        num_hashes = i + 1
        num_spaces = width - num_hashes

        print(" " * num_spaces, end="")
        print("#" * num_hashes)

if __name__ == "__main__":
    main()