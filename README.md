# jewelry
Python decorators for data science.

## ArgChecker
`ArgChecker` is a class with a main method, `enforce_type_hints`, that serves as a decorator to ensure data types passed into a function match the type hints for that function.

```python
from typing import Union
from decorators import ArgChecker
ac = ArgChecker()

def multiply_unsafe(a, b):
    return a * b

@ac.enforce_type_hints
def multiply_safe(a: Union[int, float],
                  b: Union[int, float]):
    return a * b

multiply_unsafe([1], 2)  
# [1, 1]

multiply_safe([1], 2)  
# AssertionError: arg a is type <class 'list'>; doesn't match (int, float)
```
