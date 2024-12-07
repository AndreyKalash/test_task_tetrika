def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        arg_names = func.__code__.co_varnames

        for i, arg in enumerate(args):
            param_name = arg_names[i]
            if param_name in annotations:
                param_type = annotations[param_name]
                if not isinstance(arg, param_type) or (
                    param_type is int and isinstance(arg, bool)
                ):
                    raise TypeError(
                        f"Аргумент '{param_name}' должен быть '{param_type.__name__}'"
                    )

        for param_name, arg in kwargs.items():
            if param_name in annotations:
                param_type = annotations[param_name]
                if not isinstance(arg, param_type) or (
                    param_type is int and isinstance(arg, bool)
                ):
                    raise TypeError(
                        f"Аргумент '{param_name}' должен быть '{param_type.__name__}'"
                    )

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
