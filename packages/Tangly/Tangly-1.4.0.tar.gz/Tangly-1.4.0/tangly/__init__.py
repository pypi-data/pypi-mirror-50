""" Writen by Rafael Rayes, Tangly will help you transforming
a list into a table.
USAGE:


import tangly

my_list = [['this', 'that'],
           ['these', 'those'],]

tangly.table(my_list)


"""

name = 'Tangly'
version = '1.4'
def clean_table(my_lists=[['John Smith', '356 Grove Rd', '123-4567'],\
                          ['Mary Sue', '311 Penny Lane', '555-2451'],\
                          ['A Rolling Stone', 'N/A', 'N/A']],\
                headers=['Name', 'Address', 'Phone Number']):
    from tangly import clean_table
    clean_table.clean_table(my_lists, headers)
def help():
    from tangly import tangly_help
    tangly_help.help()
def table(your_list, first_column='first', second_column= 'second'):
    from tangly import table
    table.checar(your_list, first_column, second_column)
