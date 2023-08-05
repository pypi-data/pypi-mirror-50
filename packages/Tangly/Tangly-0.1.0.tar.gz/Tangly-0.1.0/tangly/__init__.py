""" Writen by Rafael Rayes, 28 July, Taby will help you transforming
a list into a table.
USAGE:


import tangly

my_list = [['this', 'that']",
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
def table(your_list, first_column='first', second_column='second'):
    for sublist in your_list:
        for item in sublist:
            if len(item) < len(first_column) and len(item) < len(second_column) :
                print("|",first_column," |", second_column, " |")
                print("-"*(len(first_column)+len(second_column)+9))
                for i in your_list:
                    print("|",i[0], " "*(len(first_column)-len(i[0])), "|",
                            i[1], " "*(len(second_column)-len(i[1])), "|",)
                break
                break
            else:
                print("Error: The name of the coulmns need to be bigger the all items in your lis.")
                break
        break
