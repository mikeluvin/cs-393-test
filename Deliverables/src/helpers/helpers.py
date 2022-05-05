def check_nat(num: int):
    '''
    Returns True if the input is a natural number.
    '''
    return type(num) == int and num >= 0


def check_valid_lst(lst: list, length: int, valid_func):
    '''
    Returns True if all elements in the list satisfy the constraints in 
    valid_func and the list is the desired length.
    '''
    if type(lst) != list or (length is not None and len(lst) != length):
        return False

    return all(valid_func(x) for x in lst)


def check_type_and_membership(var, typ, set_):
    '''
    Returns True if var is of type typ and is in set_.
    '''
    return type(var) == typ and var in set_


def check_increasing(lst: list):
    for i in range(1, len(lst)):
        if lst[i] < lst[i - 1]:
            return False

    return True


def is_eq_or_mono_incr(f1: int, f2: int):
    '''
    Returns a boolean indicating if f1 = f2 or f1 + 1 = f2.
    '''
    return f1 == f2 or f1 + 1 == f2