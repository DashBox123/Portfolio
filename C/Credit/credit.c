#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
The following code will:
1. Ask user to enter a card number
2. Check it against luhn's algorithm
3. If luhn's algorithm fails, code prints "INVALID"
4. If luhn's algorithm succeeds, code determines whether the card number is visa, mastercard, amex, or none of them, and prints accordingly

Rules followed to determine card type:
1. Amex cards are 15 digits and start with 34 or 37
2. Mastercard cards are 16 digits and start with 51,52,53,54,55
3. Visa cards are 13 or 16 digits and start with 4
*/

/// Explicit Functions used
int get_longlength(long x); ///Gets the length of a long
int get_firstlong(long x);  ///Gets the first number of a long
int get_firsttwolong(long x); ///gets the first two numbers of a long
int alt_prod(long x); ///multiplies every other digit, starting at the second last, by 2 and sums them all up
int alt_sum(long x); ///sums up every other digit, starting at the last
bool valid_amex(long x); ///returns true if entered number matches amex format
bool valid_visa(long x); ///returns true if entered number matches visa format
bool valid_mastercard(long x); ///returns true if entered number matches mastercard format
bool luhns(long x); ///returns true if luhn's algorithm determine's card number is genuine

///Variables used
long number; ///Stores card number that user enters

int main(void)
{
    ///gets a card number from user
    number = get_long("Number: ");
    ///runs luhns algorithm
    if (luhns(number) == false)
    {
        printf("INVALID\n");
    }
    ///determines card type if luhn's algorithm is succesful
    else
    {
        if (valid_amex(number))
        {
        printf("AMEX\n");
        }
    else if (valid_visa(number))
        {
        printf("VISA\n");
        }
    else if (valid_mastercard(number))
        {
        printf("MASTERCARD\n");
        }
    else
    {
        printf("INVALID\n");
    }
    }
}

///Function Definitions
int get_longlength (long x)
{
    char str[256];
    sprintf(str, "%ld", x);
    int len = strlen(str);
    return len;
}

int get_firstlong (long x)
{
    while(x >= 10)
    {
        x = x / 10;
    }
    return (int) x;
}

int get_firsttwolong (long x)
{
    while(x >= 100){
        x = x / 10;
    }
    x =  x % 100;
    return (int) x;
}

bool valid_amex (long x)
{
    if (
        (get_firsttwolong(x) == 34 ||
        get_firsttwolong(x) == 37) &&
        (get_longlength(x) == 15)
    )
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool valid_mastercard (long x)
{
    if (
        (get_firsttwolong(x) == 51 ||
        get_firsttwolong(x) == 52 ||
        get_firsttwolong(x) == 53 ||
        get_firsttwolong(x) == 54 ||
        get_firsttwolong(x) == 55) &&
        (get_longlength(x) == 16)
    )
    {
        return true;
    }
    else
    {
        return false;
    }
}

bool valid_visa (long x)
{
    if (
        (get_firstlong(x) == 4) &&
        (get_longlength(x) == 16 ||
         get_longlength(x) == 13)
    )
    {
        return true;
    }
    else
    {
        return false;
    }
}

int alt_prod (long x)
{
    int alt_prod = 0;
    int rem;
    x = x / 10;
    while (x > 1)
    {
        rem = x % 10;
        rem = rem * 2;
        if (rem > 9)
        {
            alt_prod = alt_prod + (rem % 10) + (rem / 10);
        }
        else
        {
          alt_prod = alt_prod + rem;
        }
        x = x / 100;
    }
    return alt_prod;
}

int alt_sum (long x)
{
    int alt_sum = 0;
    int rem;
    while (x > 1)
    {
        rem = x % 10;
        alt_sum = alt_sum + rem;
        x = x / 100;
    }
    return alt_sum;
}

bool luhns (long x)
{
    int prod = alt_prod(x);
    int sum = alt_sum(x);
    int tot_sum = prod + sum;
    if (tot_sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }
}
