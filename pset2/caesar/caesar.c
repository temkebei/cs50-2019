#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // **Check for 2 arguments** //
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
    // **Check if argument is a digit** //
    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (!isdigit(argv[1][i]))
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    // **Convert string argument into int** //
    int argument = atoi(argv[1]);
    // **Prompt user for plaintext** //
    string plaintext = get_string("plaintext: ");
    // **Caesar cipher algorithm** //
    printf("ciphertext: ");
    for (int i = 0; i < strlen(plaintext); i++)
    {
        if (isupper(plaintext[i]))
        {
            printf("%c", (plaintext[i]  + argument - 65) % 26 + 65);
        }
        else if (islower(plaintext[i]))
        {
            printf("%c", (plaintext[i]  + argument - 97) % 26 + 97);
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
}

