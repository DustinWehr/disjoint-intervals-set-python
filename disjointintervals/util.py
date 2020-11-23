from functools import update_wrapper


def showcalls(method):
    def f(*args):
        print(f"\n{method.__name__}({','.join((str(arg) for arg in args))})")
        return method(*args)
    update_wrapper(f, method)
    return f


def showcalls_ret(method):
    def f(*args):
        rv = method(*args)
        print(
            f"\n{method.__name__}({','.join((str(arg) for arg in args))}) = {str(rv)}")
        return rv
    update_wrapper(f, method)
    return f


def showcalls_noself(method):
    def f(*args):
        print(
            f"\n{method.__name__}({','.join((str(arg) for arg in args[1:]))})")
        return method(*args)
    update_wrapper(f, method)
    return f


# from functools import update_wrapper
# def validintervals(method):
#     def with_valid_intervals_check(*args: Tuple[int,int]):
#         for arg in args:
#             assert arg[0] <= arg[1]
#         return method(*args)

#     update_wrapper(with_valid_intervals_check, method)
#     return with_valid_intervals_check
