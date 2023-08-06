import sys

_registered_types = {}

def register_type(name, **kwargs):
    """
    A decorator that can be used on classes or factory methods
    to easily add them as an instantiable type with a simple name

    Example:
        @register('my_class')
        class MyClass:
            ...

        @register_type('simple', name='other')
        def factory_method(name):
            ...
    """
    def decorator_wrapper(k):
        global _registered_types
        check_name = name.lower()
        if check_name in _registered_types:
            raise ValueError(f'Cannot re-register {name} as it has already been registered')

        _registered_types[check_name] = {'factory_method': k, 'default_values': kwargs}
        return k

    return decorator_wrapper

# This is basically just an alias
register = register_type


def register_library(name, factory_method, **kwargs):
    """
    This function allows you to register 3rd party libraries into the type system. For example
    to add the RandomForestClassifier from sklearn you would add the following.

    Example:
        register_library('random-forest', sklearn.ensemble.RandomForestClassifier, max_depth=10, n_estimators=100)

    """
    check_name = name.lower()
    if check_name in _registered_types:
        raise ValueError(f'Cannot re-register {name} as it has already been registered')

    _registered_types[check_name] = {'factory_method': factory_method, 'default_values': kwargs}


def find_type(name):
    """
    This function will return the details for a registered type, using the
    name it was registered with to find the entry

    Examples:
        func_details = find_type('my-class')
        func_details['factory_method'](...)

    :param name: (string) the name of the registered factory method
    :returns: (dict) details around the registered type, including default params
    """
    name = name.lower()
    if name not in _registered_types:
        raise ValueError(f'Cannot find {name} as it has not be registered')

    return _registered_types[name]


def print_registry(indent=2, out_fp=sys.stdout):
    """
    This is a helper method that can be used to print out everything that has
    been registered with the system.  It attempts to provide a hierarchical
    view of the types
    """
    print(' ' * indent, 'registry', file=out_fp)
