#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int *compute_properties(string text);
int cl_score(int arr[]);

int main(void)
{
    // keeps asking user for text until they actually enter something. They cannot pass it empty
    string text;
    do
    {
        text = get_string("Text: ");
    }
    while (strlen(text) < 1);

    // calls our compute function which returns an array containing lettercount = [0] wordcount [1] sentencecount[2]
    int *properties = compute_properties(text);
    // calls the cl calculation function that uses the number of letters, words, sentences, to calculate single int score
    int cl_index = cl_score(properties);

    // if return pre-defined values for score > 15 or < 1
    if (cl_index > 15)
    {
        printf("Grade 16+\n");
    }
    else if (cl_index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", cl_index);
    }
}

// function calculates number of letters, words, and sentences in text and returns as an array of 3 integers
int *compute_properties(string text)
{
    // number of characters in text
    int text_length = strlen(text);
    int words = 1; // words is initialised as 1 as user has to enter at least a single character
    int sentences = 0;
    int letters = 0;
    static int properties[3]; // array declaration that holds 3 ints //idk what the static thing does for now
    // loop over each char in the text
    for (int i = 0; i < text_length; i++)
    {
        // if char is alphabetical add 1 to letter count
        if (isalpha(text[i]))
        {
            letters += 1;
        }
        // if char is period, exclamation, or question mark, add 1 to sentence count
        else if (text[i] == 46 || text[i] == 33 || text[i] == 63)
        {
            sentences += 1;
        }
        // if char is a space, add 1 to word count
        else if (text[i] == 32)
        {
            words += 1;
        }
    }
    properties[0] = letters;
    properties[1] = words;
    properties[2] = sentences;
    return properties;
}
// function takes input of int array, and extracts the number of letters, words, sentences to use in cl calculation score. returns
// single integer as score
int cl_score(int arr[])
{
    // calculates L and S by first type casting arr[i] into floats, then rounding using round() then typecasting to int
    float L = ((float) arr[0] / (float) arr[1]) * 100;
    float S = ((float) arr[2] / (float) arr[1]) * 100;
    // actual calculation of cl index, rounded to nearest int
    int cl_index = round((0.0588 * L) - (0.296 * S) - 15.8);
    return cl_index;
}
