from type_registry import register

__all__ = []


@register('aws-reader', key='test-key')
class AWSReader:
    def __init__(self, id, key):
        self.id = id
        self.key = key
