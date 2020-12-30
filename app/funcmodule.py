import yaml

def parser(data):
    """Parsing a configuration file using PyYAML.

    :param data: The opened configuration to parse.
    :type data: textIO
    :return: The parsed configuration file.
    :rtype: dict
    """


    parsed = yaml.safe_load(data)
    
    return parsed