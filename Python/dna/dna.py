import csv
import sys


def main():

    #   Checks that user has entered 2 cmd line arguments
    if len(sys.argv) != 3:
        print("Error: Please enter 2 command line arguments")
        sys.exit()

    #   Reads database file into a list of dictionaries and reads the str sequences into separate list
    people = []
    with open(sys.argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            people.append(row)
    strnames = reader.fieldnames[1:]

    #   Reads DNA sequence file into a string
    with open(sys.argv[2]) as file:
        sequence = file.read()

    #   Find longest match of each STR in DNA sequence, outputs a dictionary STR with str: freq
    str_freq = {}
    for subsequence in strnames:
        #   max num of times strname appears in given sequence
        str_freq[subsequence] = str(longest_match(sequence, subsequence))

    #   Check database for matching profiles
    for person in people:
        #   Checks if all the items in the subset are present in the superset
        if all(item in person.items() for item in str_freq.items()):
            print(person["name"])
            break
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
