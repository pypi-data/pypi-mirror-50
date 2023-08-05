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
