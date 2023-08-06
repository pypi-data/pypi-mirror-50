class DamsonException(Exception):
    """
    This class is the base Exception and all damson's exception extends to it.
    """
    __kw_field = 'field'
    __kw_constraint = 'constraint'

    def __init__(self, *args, **kwargs):
        self.message = args[0] if len(args) > 0 else ''
        self.field = kwargs.get(self.__kw_field)
        self.constraint = kwargs.get(self.__kw_constraint)

    def __str__(self):
        field_line = '' if not self.field else '"%s" is invalid! ' % self.field
        constraint_line = '' if not self.constraint else '[constraint:%s] ' % self.constraint
        return '<damson> {clazz}:{field}{constraint}{message} extra={extra}'.format(
            clazz=self.__class__.__name__,
            field=field_line,
            constraint=constraint_line,
            message='' if len(self.message) <= 0 else self.message + '.',
            extra=self.args[1:]
        )


class WrongIntervalException(DamsonException):
    """
    WrongIntervalException
    """
    pass


class NotPassRequireException(DamsonException):
    """
    NotPassRequireException
    """
    pass


class NotPassDataTypeException(DamsonException):
    """
    NotPassDataTypeException
    """
    pass


class NotPassBetweenException(DamsonException):
    """
    NotPassDataTypeException
    """
    pass
