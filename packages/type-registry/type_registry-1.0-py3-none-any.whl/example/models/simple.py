from type_registry import register

__all__ = []

@register('simple')
class SimpleModel:
    def __init__(self, *kwargs):
        self._args = kwargs
