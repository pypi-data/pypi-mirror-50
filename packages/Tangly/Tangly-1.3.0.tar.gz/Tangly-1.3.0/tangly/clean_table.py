"""All creddits for this function goes to @salt on discord.
I didn't write any of this code"""

def clean_table(my_lists=[['John Smith', '356 Grove Rd', '123-4567'],\
                          ['Mary Sue', '311 Penny Lane', '555-2451'],\
                          ['A Rolling Stone', 'N/A', 'N/A']],\
                headers=['Name', 'Address', 'Phone Number']):
    number_of_columns = len(headers)

    #Check that sizes match up
    for my_list in my_lists:
        if len(my_list) != number_of_columns:
            print("Number of items in rows don't match number of headers.")
            return

    my_lists.insert(0, headers) #Combine headers and my_lists
    table = zip(*my_lists) #Transpose my_lists to iterate over columns
    for i, column in enumerate(table):
        max_length = max([len(item) for item in column])
        #Pad the length of items in each column
        for j, item in enumerate(column):
            my_lists[j][i] += " " * (max_length - len(item))

    #Construct table
    table = ["│ " + " │ ".join(row) + " │" for row in my_lists]

    box_drawing = [left +\
                   mid.join("─" * (len(item) + 2) for item in my_lists[0]) + \
                   right
                   for left, mid, right in [("┌", "┬", "┐"),\
                                            ("├", "┼", "┤"),\
                                            ("└", "┴", "┘")]]

    table.insert(0, box_drawing[0]) #Top of box
    table.insert(2, box_drawing[1]) #Horizontal Line after Headers
    table.append(box_drawing[2])    #Bottom of box
    table = "\n".join(table)

    print(table)
    #return table #Alternatively use this line to save the table as a string
