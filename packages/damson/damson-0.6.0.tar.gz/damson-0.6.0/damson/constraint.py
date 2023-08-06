from .exception import (NotPassRequireException, NotPassDataTypeException, NotPassBetweenException,
                        WrongIntervalException)


class DamsonConstraint(object):
    """
    This class is the base constraint and all damson's constraint extends to it.
    """

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class Required(DamsonConstraint):
    """
    Make a promise that the field must to be exist
    """

    def __call__(self, obj, name):
        flag = True if not name or (obj and name in obj) else False
        if not flag:
            raise NotPassRequireException(field=name, constraint='the field is required')
        return flag


class DataType(DamsonConstraint):
    """
    Make a promise about the field's type in python.
    args: python's build-in types,likes: int/str/list and etc.
    """

    def __init__(self, *args):
        self.types = args

    def __call__(self, obj, name):
        if len(self.types) <= 0 or not name:
            return True
        if obj and name in obj:
            flag = isinstance(obj[name], self.types)
            if not flag:
                types_str = '(' + (','.join([x.__name__ for x in self.types if x])) + ')'
                raise NotPassDataTypeException(field=name, constraint='the type must be one of %s' % types_str)
            return flag
        else:
            return True


class Between(DamsonConstraint):
    """
    Make a promise that the field's value is between the interval
    """

    def __init__(self, start=None, end=None, sopen=False, eopen=True):
        self.start = start
        self.end = end
        self.sopen = sopen
        self.eopen = eopen

    def __interval_str(self):
        """
        Format interval
        :return: a formatted interval string
        """
        return '{left}{start},{end}{right}'.format(
            left='(' if self.sopen else '[',
            start=self.start if self.start else 'N',
            end=self.end if self.end else 'N',
            right=')' if self.eopen else ']'
        )

    def __call__(self, obj, name):
        if not obj or not name or not (name in obj):
            return True
        if self.start and self.end and self.start > self.end:
            raise WrongIntervalException('the start is more than the end', start=self.start, end=self.end)
        v = obj[name]
        left_flag = True
        right_flag = True
        if self.start:
            left_flag = v > self.start if self.sopen else v >= self.start
        if self.end:
            right_flag = v < self.end if self.eopen else v <= self.end

        if not left_flag or not right_flag:
            raise NotPassBetweenException(field=name, constraint=self.__interval_str())
        else:
            return True
