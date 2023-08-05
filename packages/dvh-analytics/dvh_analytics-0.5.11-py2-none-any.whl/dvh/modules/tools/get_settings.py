from os.path import isfile
from .io.preferences.options import load_options


SETTINGS_PATHS = load_options(return_attr='SETTINGS_PATHS')


def get_settings(settings_type):
    """
    :param settings_type: either 'sql' or 'import'
    :return:
    """
    if isfile('/this_is_running_in_docker'):
        return SETTINGS_PATHS['docker'][settings_type]
    else:
        return SETTINGS_PATHS['default'][settings_type]


def parse_settings_file(abs_file_path):
    with open(abs_file_path, 'r') as document:
        settings = {}
        for line in document:
            line = line.split()
            if not line:
                continue
            if len(line) > 1:
                settings[line[0]] = line[1:][0]
                # Convert strings to boolean
                if line[1:][0].lower() == 'true':
                    settings[line[0]] = True
                elif line[1:][0].lower() == 'false':
                    settings[line[0]] = False
            else:
                settings[line[0]] = ''
    return settings
