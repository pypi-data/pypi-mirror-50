""" Writen by Rafael Rayes, Tangly will help you transforming
a list into a table.
USAGE:


import tangly

my_list = [['this', 'that'],
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
version = '1.1'
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
        print("""\n\n\nTo install Tangly, you must have pip installed,
then, on the terminal,  type:\n
pip install tangly\n
although it is not nescessary you might also need to try:\n
pip3 install tangly , this will give you the version for python 3.x\n\n
Now to import it just type:\n
>>>import tangly
\nall done""")
    else:
        pa
def printar(your_list, first_column, second_column):
    print("|",first_column," |", second_column, " |")
    print("-"*(len(first_column)+len(second_column)+9))
    for i in your_list:
        print("|",i[0], " "*(len(first_column)-len(i[0])), "|",
            i[1], " "*(len(second_column)-len(i[1])), "|",)
def aumentar(your_list, first_column, second_column):
    for item in your_list:
        for i in item:
            while len(i) > len(first_column):
                first_column = first_column + ' '
            while len(i) > len(second_column):
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
