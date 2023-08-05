┏━━━━┓┏━━━┓┏━┓    ┏┓┏━━━┓┏┓           ┏┓       ┏┓
┃┏┓┏┓┃┃┏━┓┃┃    ┗┓┃┃┃┏━┓┃┃┃           ┃┗┓┏┛┃
┗┛┃┃┗┛┃┃    ┃┃┃┏┓┗┛┃┃┃    ┗┛┃┃           ┗┓┗┛┏┛
       ┃┃       ┃┗━┛┃ ┃┃┗┓    ┃┃┃┏━┓┃┃    ┏┓   ┗┓┏┛
       ┃┃       ┃┏━┓┃ ┃┃    ┃    ┃┃┗┻━┃┃┗━┛┃       ┃┃
       ┗┛       ┗┛    ┗┛ ┗┛    ┗━┛┗━━━┛┗━━━┛       ┗┛

Tangly is a very simple package  that lets you display lists in form of tables, it is written bt Rafael Rayes. You are free to use it as you wish. 

To install it simply use 
```
pip install tangly
```
Then to import it we use:
```
import tangly
```



See what we can do to display a table with students and scores:

```
my_list = [["Johny", "57"],
				["Nath", "89"],
				["Alex", "78"],]
```
Here we defined our list of students and their respective scores.
To display this as a table we use the 'table()' command:
```
table(my_list)
```
This will be the output:
```
| first  | second  |
----------------------
| Johny  | 57      |
| Nath    | 89      |
| Alex     | 78      |
```
Notice that the columns names are 'first' and 'second'. To change this we use some additional parameters:

```
table(my_list, 'Student' , 'Score' )

```

This will be the output:

```
| Student  | Score  |
-------------------------
| Johny     | 57       |
| Nath       | 89       |
| Alex        | 78       |
```
Much Better.





