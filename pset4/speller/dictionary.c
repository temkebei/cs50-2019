// Implements a dictionary's functionality

#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char *word; //[LENGTH + 1];// removed
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// the sum of word in dictionary//***** added
int total = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO // *****
       node *node = malloc(sizeof(node));
        if (node == NULL)
        {
            unload();
            return 1;
        }
        node->word = malloc(sizeof(char) * (LENGTH + 1));
        strcpy(node->word, word);
        if (hashtable[hash(node->word)] != NULL)
        {
            node->next = hashtable[hash(node->word)];
            hashtable[hash(node->word)] = node;
        }
        else
        {

            hashtable[hash(node->word)] = node;
            node->next = NULL;
        }
        total++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO // *****
    return total;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO // *****
    node *head = hashtable[hash(word)];
    node *cursor = head;
    while (cursor != NULL)
    {
        // if words are same then return true and break out of loop
        if (!strcasecmp(cursor->word, word))
        {
            return true;
            break;
        }
        // if the words are different then move to the next node in linked list
        else
        {
            cursor = cursor->next;
        }
    }
    return false;

}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO // *****
   for (int i = 0; i < N; i++)
    {
        node *head = hashtable[i];
        while (head != NULL)
        {
            node *temp = head;
            head = head->next;
            free(temp);
        }
    }
    return true;
}
