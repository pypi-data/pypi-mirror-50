import sys

from termcolor import cprint

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


def print_registry(indent=2, out_fp=sys.stdout, colored=False):
    """
    This is a helper method that can be used to print out everything that has
    been registered with the system.  It attempts to provide a hierarchical
    view of the types that have been registered with the system.

    :param indent: (int) the indentation to use per level
    :param out_fp: (fp_like) the output file (defaults to sys.stdout)
    :param colored: (bool) whether to include ASCII terminal coloring (defaults to False)
    """
    def color_print(msg, color=None, **kwargs):
        if not colored or not color:
            print(msg, **kwargs)
        else:
            cprint(msg, color, **kwargs)

    # 1. Get the list of all the types and modules
    registered = [(v['factory_method'], k) for k, v in _registered_types.items()]

    # 2. Split each type into all the packages
    no_module = [r[0] for r in registered if not hasattr(r[0], '__module__')]
    registered = [(r[0].__module__.split('.'),  (r[1], r[0].__name__)) for r in registered if hasattr(r[0], '__module__')]

    # 3. Combine into a tree
    def build_tree(keys, leaf, tree):
        # NOTE: This should not ever happen
        if len(keys) <= 0:
            return {}

        if len(keys) == 1:
            # We are at the end, so lets assign the leaf value
            tree[keys[0]] = leaf
        else:
            # Otherwise lets keep building the tree
            next_key = keys[0]
            next_tree = tree.get(next_key, {})
            tree[next_key] = next_tree

            build_tree(keys[1:], leaf, next_tree)

    tree = {}
    for r in registered:
        build_tree(r[0], r[1], tree)

    # 4. Print tree
    def print_tree(ind, tree):
        for k, v in tree.items():
            color_print((' ' * (ind-1)) + ' - ' + k, color='green', file=out_fp)
            if type(v) == tuple:
                color_print((' ' * (ind + indent + 2)) + v[0] + ':', color='blue', file=out_fp, end=' ')
                color_print(v[1], color='green', file=out_fp)
            else:
                print_tree(ind + indent, v)

    color_print('registry:', color='red', file=out_fp)
    print_tree(0, tree)
