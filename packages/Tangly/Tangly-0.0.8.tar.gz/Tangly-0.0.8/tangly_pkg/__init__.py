""" Writen by Rafael Rayes, 28 July, Taby will help you transforming
a list into a table.
USAGE:


import Tangly

my_list = [['this', 'that']",
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
def table(your_list, first_colum='first', second_colum='second', ps_colum_name_have_to_be_bigger_then_items=True, error_message=False):
        print("|",first_colum," |", second_colum, " |")
        print("-"*(len(first_colum)+len(second_colum)+9))
        for i in your_list:
            print("|",i[0], " "*(len(first_colum)-len(i[0])), "|",
                  i[1], " "*(len(second_colum)-len(i[1])), "|",)
        if error_message==True:
            print("The colum name must be bigger then all items in it")
            print("Type the additional argument: error_message=False , to disable this message")
