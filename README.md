# jewelry

## Overview
`ArgChecker` is a class with a main method, `enforce_type_hints`, that serves as a decorator to ensure data types passed into a function match the type hints for that function.

```python
from typing import Union
from jewelry import ArgChecker
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

## Installation
To use the code in this, open a Terminal and type the following:

```bash
git clone https://github.com/mgsosna/jewelry.git
```

Then, navigate to the `jewelry` directory and install the Python wheel. You can do this with the following command:

```bash
pip install dist/jewelry-0.1.0-py3-none-any.whl
```

Once you have `jewelry` installed in your Python environment, you can import `ArgChecker` with `from jewelry import ArgChecker`. Finally, make sure your Python environment contains the modules in `requirements.txt`.
