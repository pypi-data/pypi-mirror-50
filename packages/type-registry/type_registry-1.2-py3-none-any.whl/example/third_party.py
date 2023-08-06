import itertools

from type_registry import register, register_library


register_library('iter', itertools.chain)


@register('factory')
def sample_factory_method(**kwargs):
    print(kwargs)
    return []
