from __future__ import print_function
import inspect
from .exception import DamsonException
from .constraint import DamsonConstraint
from .support import func_args_to_dict


def validate(obj, **kwargs):
    """
    Apply the rules to validate the  dict, and it will return the result and errors.


    Examples:
    import damson
    from damson.exception import Require,Between

    data={'age':18}
    result,errors=damson.validate_raise(data,age=[Require(),Between(1,150)])

    if not result:
        print errors

    :param obj: A object extended to dict will be validated
    :param kwargs: The validation rules
    :return: (result:bool,errors:list)
    """
    if not isinstance(obj, dict):
        raise DamsonException('the argument of validate function must to be a dict.')
    errors = []
    if len(kwargs) <= 0:
        return True, errors
    for field in kwargs:
        rules = kwargs[field]
        if len(rules) <= 0:
            continue
        for rule in rules:
            try:
                if isinstance(rule, DamsonConstraint):
                    rule(obj, field)
            except Exception as e:
                errors.append(str(e))
    return len(errors) <= 0, errors


def validate_raise(obj, **kwargs):
    """
    Apply the rules to validate the  dict. if the field's value is not matched rule, it will throws exception.

    Examples:
    import damson
    from damson.exception import Require,Between

    data={'age':18}
    damson.validate_raise(data,age=[Require(),Between(1,150)])

    :param obj: A object extended to dict will be validated
    :param kwargs: The validation rules
    :return: result or exception
    """
    if not isinstance(obj, dict):
        raise DamsonException('the argument of validate function must to be a dict.')
    if len(kwargs) <= 0:
        return True
    for field in kwargs:
        rules = kwargs[field]
        if len(rules) <= 0:
            continue
        for rule in rules:
            if isinstance(rule, DamsonConstraint):
                rule(obj, field)
    return True


def verify(**rules):
    """
    This decoration wrapper is used to check the arguments of function. If the arguments does not match rules, it will
    throw exception. you can use it likes:

    import damson
    from damson.constraint import DataType

    @damson.verify(a=[DataType(int)],b=[DataType(int)])
    def add(a,b):
        return a+b

    add(2,3)   # 5
    add(2,3.0) # throws exception

    :param rules: declares the constraint
    :return: result
    """

    def func(fn):
        def wrapper(*args, **kwargs):
            if inspect.isfunction(fn):
                params = {}
                args_map = func_args_to_dict(fn, args)
                params.update(args_map)
                params.update(kwargs)
                validate_raise(params, **rules)
            else:
                print('Abort to execute validation, because that it just only apply on function')
            return fn(*args, **kwargs)

        return wrapper

    return func
