# Example Package
Tangly is a very simple package  that lets you display lists in form of tables, it is written bt Rafael Rayes. You are free to use it as you wish. 




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
Unfortunately, to display the data better, it is advisable that the columns names are bigger then all items in their respective sublist. Notice how 'Student' has more characters then "jhony" , "Nath", and "Alex" the same for score, 57, 89, 78



