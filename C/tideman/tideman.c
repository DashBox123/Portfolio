#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
} pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }
        record_preferences(ranks);
        printf("\n");
    }

    add_pairs();

    sort_pairs();

    lock_pairs();

    print_winner();

    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // loops over all of the candidate names held in candidates array
    for (int i = 0; i < candidate_count; i++)
    {
        // if candidate name is found, then inputs user candidate index into ranks array at index rank
        if (strcmp(candidates[i], name) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // TODO
    // loop over the ranks array
    for (int i = 0; i < candidate_count; i++)
    {
        // for each candidate in the ranks array, add 1 for every candidate that comes after it
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]] += 1;
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
            else if (preferences[i][j] < preferences[j][i])
            {
                pairs[pair_count].winner = j;
                pairs[pair_count].loser = i;
                pair_count++;
            }
        }
    }
    // TODO
    return;
}

// Sort pairs in decreasing order by strength of victory...uses bubble sort
void sort_pairs(void)
{
    pair temp[2];
    int swaps;
    do
    {
        swaps = 0;
        for (int i = 0; i < pair_count - 1; i++)
        {
            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[i + 1].winner][pairs[i + 1].loser])
            {
                temp[0] = pairs[i + 1];
                temp[1] = pairs[i];
                pairs[i] = temp[0];
                pairs[i + 1] = temp[1];
                swaps++;
            }
        }
    }
    while (swaps != 0);

    return;
}

bool loop(int k, int i)
{
    // int i is the loser
    // int k is the corresponding winner
    // 1. if the loser of the pair being added already exists as a winner in the array
    // 2. if yes > we need to check for a cycle
    if (k == i)
    {
        return true;
    }

    for (int j = 0; j < pair_count; j++)
    {
        // checks whether the loser in the pair being added already exists in the locked array as a winner
        if (locked[i][j])
        {
            if (loop(k, j))
            {
                return true;
            }
        }
    }

    // if the previous loop does not trigger then the loser in the pair being added does not exist or. there is no cycle, therefore
    // return false
    return false;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // TODO
    // the locked array by default has false in all values
    // this loop assigns all winning pairs to the locked array
    for (int i = 0; i < pair_count; i++)
    {
        if (!loop(pairs[i].winner, pairs[i].loser)) // if adding this pair does not cause a loop
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    int false_count;

    for (int l = 0; l < pair_count; l++)
    {
        false_count = 0;
        for (int w = 0; w < pair_count; w++)
        {
            if (!locked[w][l])
            {
                false_count++;
            }
            if (false_count == candidate_count)
            {
                printf("%s\n", candidates[l]);
                return;
            }
        }
    }
    return;
}
