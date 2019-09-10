#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>

// **prototype function**//
int shift(char c);
int main(int argc, string argv[])
{
    // **Check 2 arguments**//
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }
    // **check if there is no digit in argument** //
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]))
        {
            printf("Usage: ./vigenere keyword\n");
            return 1;
        }
    }
    // **Prompt user for plain-text** //
    string plaintext = get_string("plaintext: ");
    int j = 0;
    // **Vigenere cipher** //
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        // **As in caesar cipher, there we are adding our shift value** //
        if (isupper(plaintext[i]))
        {
            printf("%c", (plaintext[i]  + shift(argv[1][j]) - 65) % 26 + 65);
            j++;
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (plaintext[i]  + shift(argv[1][j]) - 97) % 26 + 97);
            j++;
        }
        else
        {
        // **If a char is not a letter, do not add key from the argument** //
            printf("%c", plaintext[i]);
        }
        // **If all characters from argument is used,**//
        // it will get back to the start to re-use again **//
        if (j > (strlen(argv[1]) - 1))
        {
            j = 0;
        }
    }
    printf("\n");
}
// **this Convert characters into numbers** //
int shift(char c)
{
    if (isupper(c))
    {
        c -= 65;
    }
    else if (islower(c))
    {
        c -= 97;
    }
    return c;
}
