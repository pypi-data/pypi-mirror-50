# A small module for getting diagonals in a 2D Array

```python
import diagonal
arr = [] #your array
```

### Definition

#### get(arr, start = "0", direction = "up", type="all")

**start** (single character)

0 - start from the first row

m - start from m'th row

**direction** (string)

up - uses upward direction for traversal

down - downward direction for traversal

**type **(string)

all - default value which indicates that all diagonals are considered

main - gives the main diagonal of square matrix

anti - gives anti diagonal of square matrix

zigzag - gives zigzag traversal of the matrix



---



### Usages

1. Square matrix

   * Main diagonal  `diagonal.get(arr, type = "main")`

   * Anti diagonal `diagonal.get(arr, type = "anti")`

   * Also zigzags upwards and downwards

     ` diagonal.get(arr, type = "zigzag" ,direction ="up")`

2. Other matrices

   All traversals except main and anti diagonals

   Ex: `diagonal.get(arr, start = "0", direction = "up")` gives all diagonals starting from the first elements traversed in upward direction.

### Return values

* Any errors return a string

* Main and Anti diagonal traversals returns a list

* ZigZag traversals return a list

* Others return a list of list having individual diagonals

  