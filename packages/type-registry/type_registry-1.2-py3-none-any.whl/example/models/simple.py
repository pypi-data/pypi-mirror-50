from type_registry import register

__all__ = []

@register('simple')
class SimpleModel:
    def __init__(self, **kwargs):
        self._args = kwargs

    def __repr__(self):
        args = ','.join([f'{k}={v}' for k, v in self._args.items()])
        return f'SimpleModel({args})'


@register('other')
class OtherModel:
    pass
