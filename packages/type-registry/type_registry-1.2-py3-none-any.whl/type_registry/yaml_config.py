"""
This is a simple function to allow us to easily load yaml
and have it construct an object is specified
"""
import logging
import yaml
import os

from pprint import pprint
from string import Template

from .registrar import find_type



__all__ = ['load_yaml', 'load_yaml_str']


logger = logging.getLogger(__name__)


_yaml_initialized = False
def construct_yaml_stream(in_stream):
    """
    A function that can be used to construct yaml into python objects
      and utilizes the python constructor in doing so

    :param in_stream: (io.Stream) a stream to load the contents from
    :returns: (dict|obj) The constructed yaml results
    """

    global _yaml_initialized

    logger.info('Request to construct yaml')

    if not _yaml_initialized:
        def _object_creator(loader, node, deep=True):
            mapping = {}
            for key_node, value_node in node.value:
                key = loader.construct_object(key_node, deep=deep)
                value = loader.construct_object(value_node, deep=deep)
                mapping[key] = value

            if '__factory__' in mapping:
                print('I am here')
                try:
                    _cls = mapping['__factory__']
                    del mapping['__factory__']
                    logger.debug('__factory__ found in yaml, attempting to construct %s', _cls)

                    # This line is used for referencing modules by a registered alias
                    if type(_cls) == str:
                        registrar_values = find_type(_cls)
                        _cls = registrar_values['factory_method']
                        default_args = registrar_values['default_values']
                        mapping = {**default_args, **mapping}

                    return _cls(**mapping)
                except Exception as e:
                    logger.error('Failed to construct yaml object %s, %s', e, str(mapping))
                    raise e

            return loader.construct_mapping(node, deep)

        logger.info(f'Registering yaml constructor for python !obj types')
        yaml.add_constructor('!obj', _object_creator, yaml.Loader)

        _yaml_initialized = True

    return yaml.load(in_stream)


def construct_types_in_dict(config: dict) -> dict:
    """
    This function can take in a dictionary type object and using depth-first iteration it
    will dynamically construct types if they have a `__factory__` key.
    """
    generated_dict = {}

    # 1. First iterate through all children in the current object
    for key, value in config.items():
        if type(value) == dict:
            generated_dict[key] = construct_types_in_dict(value)
        else:
            generated_dict[key] = config[key]

    # 2. Second apply the construction method for the current type (if it has a __factory__ key)
    if '__factory__' in generated_dict.keys():
        factory_method = generated_dict['__factory__']
        del generated_dict['__factory__']

        if type(factory_method) == str:
            registered_type = find_type(factory_method)
            factory_method = registered_type['factory_method']
            default_args = registered_type['default_values']
            generated_dict = {**default_args, **generated_dict}

        return factory_method(**generated_dict)

    # This is the standard return if a __factory__ is not found
    return generated_dict


def load_yaml_str(yaml_str, template_params=None, return_config_str=False):
    """
    load_yaml_str will take in a string that has the correct yaml formatting
    and generate classes or types according to the configuration in the yaml.

    Example:
        with open(my_file, 'r') as f:
            yaml_str = f.read()

        params = {'SOURCE_PATH': '/tmp/source', 'AGE': 30}
        object = load_yaml_str(yaml_str, params)

    :param yaml_str: (string) yaml string to construct
    :param template_params: (optional: dict) key value pairs where the key
        represents a value in the config to update.
    :param return_config_str: (optional: bool) whether to return the entire config
        string with the constructed type
    :returns: The constructed type from the yaml config or tuple of type and config
        if boolean option is set the True
    """
    template_params = template_params or {}
    config_str = Template(yaml_str).substitute({**os.environ, **template_params})
    (config, config_str) = (construct_yaml_stream(config_str), config_str)

    constructed = construct_types_in_dict(config)
    if return_config_str:
        return (constructed, config_str)
    else:
        return constructed


def load_yaml(yaml_file, template_params=None, return_config_str=False):
    """
    load_yaml_str will take in a string that has the correct yaml formatting
    and generate classes or types according to the configuration in the yaml.

    Example:
        params = {'SOURCE_PATH': '/tmp/source', 'AGE': 30}
        object = load_yaml_str('my_file.yaml', params)

    :param yaml_file: (string) yaml filename to load
    :param template_params: (optional: dict) key value pairs where the key
        represents a value in the config to update.
    :returns: The constructed type from the yaml config
    """
    with open(yaml_file, 'r') as yaml_config:
        yaml_str = yaml_config.read()

    return load_yaml_str(yaml_str, template_params, return_config_str)
