from type_registry import register

__all__ = []

@register('azure-reader', loc='us')
class AzureReader:
    def __init__(self, loc):
        self.loc = loc
