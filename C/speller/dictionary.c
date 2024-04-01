// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include "dictionary.h"
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Buckets of size BASE^4 (28^4) in hash table
const unsigned int N = BASE * BASE * BASE * BASE;

// Hash table initialised to NULL
node *table[N] = {NULL};

//  global variable storing the number of words that have been counted;
int words;


// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // hashes the word
    unsigned int hashcode = hash(word);

    if (table[hashcode] == NULL)
    {
        //  word not in dicionary
        return false;
    }
    //  else
    for (node *ptr = table[hashcode]; ptr != NULL; ptr = ptr -> next)
    {
        if (strcasecmp(word, ptr -> word) == 0)
        {
            //  if word found
            return true;
        }
    }
    return false;
}

// Hashes word to a number
// Looks at the first 4 characters in a word (including apostrophes and newlines)
// We need an array of size 28^4 to deal with the hashcodes this function generates
unsigned int hash(const char *word)
{
    int hash_array[4] = {0, 0, 0, 0};  //  empty int array to store the 4 'base-28' values | 0 = no character, 28 = ', 1-27 = A - Z
    unsigned int hash_code = 0;
    int wordlen = strlen(word); //  length of the word
    int loop_limit; //  loop limiter to ensure words with < 4 characters are handled properly without overflow

    if (wordlen < 4)
    {
        loop_limit = wordlen;
    }
    else
    {
        loop_limit = 4;
    }

    for (int i = 0; i < loop_limit; i++)
    {
        if (word[i] == '\'')
        {
            //  if apostrophe
            hash_array[i] = 27;
        }
        else if (word[i] == '\n')
        {
            //  if newline character
            hash_array[i] = 0;
        }
        else
        {
            hash_array[i] = toupper(word[i]) - 64;  //  this gives A = 1, B = 2 etc.
        }

        //  calculating final hash code using base-28
        hash_code += hash_array[i] * (int) pow((double) BASE, (double) i);
    }
    return hash_code;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open file
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    char *rword = malloc(LENGTH * sizeof(char)); //  temporary memory for word, used during reading loop
    unsigned int hashcode;

    while(fscanf(input, "%s", rword) != EOF)
    {
        node *n = malloc(sizeof(node)); //  creates memory for new node
        strcpy(n -> word, rword);   //  copies word from dictionary to new node
        words++;    //  increments words variable as the function adds more words
        hashcode = hash(rword); //  runs word through hash function to obtain hashcode

        //  checking if array already contains a list at the specified hash code
        if (table[hashcode] != NULL)
        {
            // if array already has a pointer to a linked list
            n -> next = table[hashcode];
            table[hashcode] = n;
        }
        else
        {
            n -> next = NULL;
            table[hashcode] = n;
        }
        free(n);
    }
    fclose(input);  //  closing dictionary file
    free(rword); //  free memory for temporary word

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return words;
}



//  frees linked list
void free_list(node *n)
{
    //  Handle base case
    if (n->next == NULL)
    {
        free(n);
        return;
    }

    // Free next recursively
    free_list(n -> next);

    // TODO: Free word
    free(n);
}


// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // iterate over hashmap array and free list
    for (int i = 0; i < N; i++)
    {
        free_list(table[i]);
    }
    return false;
}


