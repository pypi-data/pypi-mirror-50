from type_registry import register

__all__ = []

@register('azure-reader', loc='us')
class AzureReader:
    def __init__(self, loc):
        self.loc = loc

    def __repr__(self):
        return f'AzureReader(loc="{self.loc}")'
