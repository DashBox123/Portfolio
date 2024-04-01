#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
// we don't need a second array of alphabets. in ASCII A starts at 65, which means we can subtract 65 from each character that the
// player enters and the resulting number will be the index of the points array

int compute_score(string word);
void print_result(int score1, int score2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    print_result(score1, score2);
}

/* FUNCTION DEFINITION
1. calculates length of string entered
2. initialises score = 0
3. loops over every character in the string
4. capitalises each character
5. subtracts 65 from it (because 65 is the ASCII for a capital A) - this returns the index of the character's score
in the scores array
6. uses this index to extract score from the scores array and adds to an int score
*/
int compute_score(string word)
{
    int word_length = strlen(word);
    int score = 0;
    for (int i = 0; i < word_length; i++)
    { // if statement assigns score 0 for non alphabetical characters
        char upper_char = toupper(word[i]);
        if (!isalpha(upper_char))
        {
            score += 0;
            break;
        }
        int index_score = upper_char - 65;
        score += POINTS[index_score];
    }
    return score;
}

void print_result(int score1, int score2)
{
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score1 < score2)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}
