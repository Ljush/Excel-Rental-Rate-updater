from .alphanum_cypher import cyphers
def col_list_updater(col_list, col_multiplier):
    letter_first, num_first = cyphers()
    col_list_final = []
    for i in col_list:
        # convert cell string into list
        temp = list(i)
        # take the second letter from the column catagory e.g: A(E), B(X), etc.
        letter = temp[1]
        # convert the letter into a number from letter_first,
        # add the multiple of 5 from col_change_multiplier, update the new column letter accordingly
        number_from_cypher = letter_first[letter]
        find_col = (number_from_cypher + col_multiplier)
        # If column is past A(Z) <- Z being the last column for the A category
        # subtract 26 to get a remainder while moving the first letter up one (B to C, etc)
        if find_col > 26:
            while find_col > 26:
                first_letter = temp[0]
                another_cypher_number = letter_first[first_letter]
                another_cypher_number += 1
                temp[0] = num_first[another_cypher_number]
                find_col -= 26
        temp[1] = num_first[find_col]
        # change list back into string element, add it to the final version of the column list
        i = ''.join(temp)
        col_list_final.append(i)
    return col_list_final