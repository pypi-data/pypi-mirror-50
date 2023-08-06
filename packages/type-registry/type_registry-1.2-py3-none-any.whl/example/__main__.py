import os

from type_registry import print_registry, load_yaml_str

here = os.path.join(os.path.abspath(os.path.dirname(__file__)), '..')

sample = '''
data:
  __factory__: azure-reader
model:
  __factory__: simple
  layers: 2
  hidden_size: 128
  env: $ENV_VALUE
  passed: $PASSED_VALUE
'''


if __name__ == '__main__':
    os.environ['ENV_VALUE'] = '10'

    print_registry(colored=True)

    print('\nWriting the registry to file')
    with open(os.path.join(here, 'sample-registry.txt'), 'w') as f:
        print_registry(file=f)

    print('\nConstructing from yaml config')
    details = load_yaml_str(sample, {'PASSED_VALUE': 20})
    for k, v in details.items():
        print(' ' * 2, k, '=', v)
