import inspect


def func_args_to_dict(func, args):
    """
    Make the arguments of function to a named dict

    Examples:

    from damson.support import func_args_to_dict

    def wrapper(fn):
        def func(*args,**kwargs):
            named_args=func_args_to_dict(fn,args)
            print(named_args)

            return fn(*args,**kwargs)
        return func

    @wrapper
    def add(a,b):
       return a+b



    :param func: A instance of function
    :param args: the arguments
    :return: a named argument dict
    """
    if not inspect.isfunction(func) or not isinstance(args, (list, tuple)):
        raise ValueError()
    varnames = func.__code__.co_varnames
    if 'self' in varnames:
        args = args[1:]
        varnames = [x for x in varnames if x != 'self']

    kvmap = {}
    # Special function declare, likes: f(*args),f(*args,**kwargs)
    if 'key' in varnames and 'value' in varnames:
        for index, arg in enumerate(args):
            kvmap[str(index)] = arg
        return kvmap
    # Deal normal function declare, likes:f(a,b),f(a,b,*args),f(a,b,*args,**kwargs)
    for pos, varname in enumerate(varnames):
        if pos >= len(args):
            break
        if varname == 'args':
            for index, arg in enumerate(args[pos:]):
                kvmap[str(index)] = arg
            break
        else:
            kvmap[varname] = args[pos]
    return kvmap
