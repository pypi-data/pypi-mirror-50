""" Writen by Rafael Rayes, Tangly will help you transforming
a list into a table.
USAGE:


import tangly

my_list = [['this', 'that'],
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
version = '2.0.0'
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
def printar3(your_list, first_column, second_column, third_column):
    pa = []
    pa.append('┌')
    pa.append('─'*(len(first_column)+3))
    pa.append('┬')
    pa.append('─'*(len(second_column)+3))
    pa.append('┬')
    pa.append('─'*(len(third_column)+3))
    pa.append('┐')
    print(''.join(pa))
    print("│",first_column," │", second_column, " │", third_column, " │")
    pa[0] = '├'
    pa.reverse()
    pa[0] = '┤'
    pa.reverse()
    pa[2] = '┼'
    pa[4] = '┼'
    print(''.join(pa))
    
    for i in your_list:
        print("│",i[0], " "*(len(first_column)-len(i[0])), "│",
            i[1], " "*(len(second_column)-len(i[1])), "│",
            i[2], " "*(len(third_column)-len(i[2])), "│",)
    pa[0] = '└'
    pa[2] = '┴'
    pa[4] = '┴'
    pa.reverse()
    pa[0] = '┘'
    pa.reverse()
    print(''.join(pa))
def aumentar3(your_list, first_column, second_column, third_column):
    for item in your_list:
        while len(item[0]) > len(first_column):
            first_column = first_column + ' '
        while len(item[1]) > len(second_column):
            second_column = second_column + ' '
        while len(item[2]) > len(third_column):
            third_column = third_column + ' '
    printar3(your_list, first_column, second_column, third_column)
def printar(your_list, first_column, second_column):
    ap = []
    ap.append("┌")
    ap.append("─"*(len(first_column)+3))
    ap.append('┬')
    ap.append("─"*(len(second_column)+3))
    ap.append("┐")
    print(*ap, sep= '')
    print("│",first_column," │", second_column, " │")
    ap[0] = '┤'
    ap[2] = '┼'
    e = ap[3]
    ap[3] = ap[1]
    ap[1] = e
    ap.reverse()
    ap[0] = '├'
    print(*ap, sep= '')
    for i in your_list:
        print("│",i[0], " "*(len(first_column)-len(i[0])), "│",
            i[1], " "*(len(second_column)-len(i[1])), "│",)
    ap[0] = '┘'
    ap.reverse()
    ap[0] = '└'
    ap[2] = '┴'
    e = ap[3]
    ap[3] = ap[1]
    ap[1] = e
    print(*ap, sep= '')
def aumentar(your_list, first_column, second_column):
    for item in your_list:
        while len(item[0]) > len(first_column):
            first_column = first_column + ' '
        while len(item[1]) > len(second_column):
            second_column = second_column + ' '
    printar(your_list, first_column, second_column)
def checar(your_list, first_column, second_column, third_column):
    for i in your_list:
        if len(i) > 2:
            aumentar3(your_list, first_column, second_column, third_column)
            break
        elif len(i) == 1:
            print("your list must have at least 2 columns")
            break
        else:
            aumentar(your_list, first_column, second_column)
            break
def table(your_list, first_column = 'first', second_column='second', third_column = 'third'):
    checar(your_list, first_column, second_column, third_column)
