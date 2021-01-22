import inspect
import numpy as np
import typing
from typing import Tuple, Any
from typing_inspect import get_origin


# noinspection PyUnresolvedReferences,PyTypeHints
class ArgChecker:
    """
    | Methods for checking whether arguments passed into a function are of the provided
    | types.
    """

    def enforce_type_hints(self, func):
        """
        | A decorator that ensures arguments passed into a function match the
        | datatypes provided in the type hints.
        |
        | If any dtype is possible for an argument, use typing.Any as the type hint
        |
        | Example
        | -------
        | def add(a: int, b: int):
        |   return a + b
        |
        | Without decorator: add('a', 'b') --> 'ab'  (func has unintended behavior)
        | With decorator:    add('a', 'b') --> AssertionError
        |
        | -------------------------------------------------------------------------
        | Parameters
        | ----------
        |  func
        |    The function being decorated
        |
        |
        | Returns
        | -------
        |  func_w_arg_dtypes_validated
        |    The same function, but throwing an error if inputted dtypes do not
        |    match type hints
        """
        # Get the meta-data from the function
        full_argspec = inspect.getfullargspec(func)

        arg_names = full_argspec.args

        type_hints = full_argspec.annotations
        type_hints = self._make_typings_comparable(type_hints)

        def func_w_arg_dtypes_validated(*args, **kwargs):

            self._check_positional_args(args, arg_names, type_hints)
            self._check_keyword_args(kwargs, type_hints)

            return func(*args, **kwargs)

        # Propagate the original function's name and docstring to decorated function
        func_w_arg_dtypes_validated.__name__ = func.__name__
        func_w_arg_dtypes_validated.__doc__ = func.__doc__
        return func_w_arg_dtypes_validated

    def _make_typings_comparable(self,
                                 types_dict: dict) -> dict:
        """
        | Function argument types cannot be directly compared to objects in Python's
        | built-in typing module because typing objects are special Python classes.
        |
        | For example, type(List[int]) is typing._GenericAlias, but so is:
        |   * type(Dict[str, int])
        |   * type(Union[int, str])
        |   * type(Optional[int])
        |
        | Another problem is that to compare whether a datatype is within the accepted
        | Tuple[*dtypes], Union[*dtypes], or Optional, we must access the dtypes within
        | these objects, as opposed to checking if there is a match with the object
        | itself. (If the type hint is just int, on the other hand, we can compare directly
        | with isinstance(type(arg), int).)
        |
        | This function:
        |    1) Converts typing special classes List, Dict, and Tuple to their generic Python
        |       equivalents
        |    2) Overwrites Union and Optional with the tuples within them
        |    3) Adds np.int64 as a valid dtype if the accepted type is int
        |
        | -----------------------------------------------------------------------------------
        | Parameters
        | ----------
        |  types_dict : dict
        |    Dict of type hints
        |    e.g. {'a': Union[int, str], 'b': Optional[str], 'c': pd.DataFrame}
        |
        |
        | Returns
        | -------
        |  dict
        |    Dict in format for direct comparison
        |    e.g. {'a': (int, np.int64, str), 'b': (str, NoneType), 'c': pd.DataFrame}
        """
        new_dict = types_dict.copy()

        for arg_name in new_dict:

            arg_type = new_dict[arg_name]

            # Convert List -> list, Dict -> dict, Tuple -> tuple
            orig_type = get_origin(arg_type)

            if orig_type in [list, dict, tuple]:
                new_dict[arg_name] = orig_type
                continue

            # Extract info from typing.
            # Union[int, str] -> (int, str), Optional[int] -> (int, NoneType)
            if type(arg_type) == typing._GenericAlias:
                new_dict[arg_name] = arg_type.__args__

                if int in new_dict[arg_name]:
                    new_dict[arg_name] += (np.int64,)

            # Add np.int64 if type is int. int -> (int, np.int64), (int, str) -> (int, np.int64, str)
            if arg_type == int:
                new_dict[arg_name] = (arg_type, np.int64)
            elif isinstance(arg_type, tuple) and int in arg_type:
                new_dict[arg_name] += (np.int64,)

        return new_dict

    def _check_positional_args(self,
                               args: Tuple[Any],
                               arg_names: list,
                               type_hints: dict) -> None:
        """
        | Check whether all argument types in args tuple match argument types in
        | type_hints dict. If type_hints dict has typing.Any, that argument check
        | is skipped. Raises AssertionError if arg dtype and corresponding dtypes
        | in type_hints don't match.
        |
        | -----------------------------------------------------------------------
        | Parameters
        | ----------
        |  args : tuple
        |    Tuple of positional arguments, e.g. (1, 'abc')
        |
        |  arg_names : list
        |    List of argument names, necessary because args is only arg values
        |
        | type_hints : dict
        |    Dict of type hints, e.g. {'a': (int, float), 'b': str}
        |
        |
        | Returns
        | -------
        |  None
        """
        for i, arg in enumerate(args):

            arg_name = arg_names[i]
            if arg_name == 'self':
                continue

            accepted_types = type_hints[arg_name]
            if accepted_types == typing.Any:
                continue

            assert isinstance(arg, accepted_types), \
                f"arg {arg_name} is type {type(arg)}; doesn't match {accepted_types}"

    def _check_keyword_args(self,
                            kwargs: dict,
                            type_hints: dict) -> None:
        """
        | Check whether all argument types in kwargs dict match argument types in
        | type_hints dict. If type_hints dict has typing.Any, that argument check
        | is skipped. Raises AssertionError if arg dtype and corresponding dtypes
        | in type_hints don't match.
        |
        | -----------------------------------------------------------------------
        | Parameters
        | ----------
        |  kwargs : dict
        |    Dict of keyword arguments, e.g. {'a': 1, 'b': 'abc'}
        |
        | type_hints : dict
        |    Dict of type hints, e.g. {'a': (int, float), 'b': str}
        |
        |
        | Returns
        | -------
        |  None
        """
        # Check keyword args
        for arg_name in kwargs.keys():

            accepted_types = type_hints[arg_name]

            if type_hints[arg_name] == typing.Any:
                continue

            assert isinstance(kwargs[arg_name], accepted_types), \
                f"arg {arg_name} is type {type(kwargs[arg_name])}; doesn't match {accepted_types}"
