""" Writen by Rafael Rayes and @salt, Tangly will help you transforming
a list into a table.
USAGE:


import tangly

my_list = [['this', 'that'],
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
version = '1.4.2'
#This function was completely coded by @salt, thanks mate :)
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
def help():
    print("hello, you are using tangly, a simple tool to display lists as tables")
    print("Here is what you need to do to use it:\n\n")
    print("1- Create a list like so:\n")
    print(">>> my_list = [['he', 'she'],")
    print("              ['his', 'hers'],]")
    print("\n\nNow just use the command table() to tranform it:\n")
    print(">>> table(my_list)")
    print("\nThis will be the output:\n")
    print("""| first  | second |
-------------------
| he     | she    |
| his    | hers   |""")
    print("""\n\nYou can also use some aditional parameters to change the columns
names:\n\n""")
    print(">>> table(my_list, 'male', 'female')\n")
    print("This will be the output:\n\n")
    print("""| male  | female  |
-------------------
| he    | she     |
| his   | hers    |\n\n""")
    print("Simple as that.\n")
    insta = input("would you like to see instalation help too?(y/n)")
    if insta == 'y':
        print("\n\n\n")
        print("--"*40)
        print("""\n\n\nTo install Tangly, you must have pip installed,
then, on the terminal,  type:\n
pip install tangly\n
although it is not nescessary you might also need to try:\n
pip3 install tangly , this will give you the version for python 3.x\n\n
Now to import it just type:\n
>>>import tangly
\nall done""")
    else:
        pass
def printar(your_list, first_column, second_column):
    print("|",first_column," |", second_column, " |")
    print("-"*(len(first_column)+len(second_column)+9))
    for i in your_list:
        print("|",i[0], " "*(len(first_column)-len(i[0])), "|",
            i[1], " "*(len(second_column)-len(i[1])), "|",)
def aumentar(your_list, first_column, second_column):
    for item in your_list:
        while len(item[0]) > len(first_column):
            first_column = first_column + ' '
        while len(item[1]) > len(second_column):
            second_column = second_column + ' '
    printar(your_list, first_column, second_column)
def checar(your_list, first_column, second_column):
    a = len(your_list)*2
    x = 0
    for sublist in your_list:
        for i in sublist:
            x +=1
            if len(i) < len(first_column) and len(i) < len(second_column) and x == a:
                print("oi")
                printar(your_list, first_column, second_column)
                break
        
            else:
                aumentar(your_list, first_column, second_column)
                break
        break

def table(your_list, first_column='first', second_column= 'second'):
    checar(your_list, first_column, second_column)
