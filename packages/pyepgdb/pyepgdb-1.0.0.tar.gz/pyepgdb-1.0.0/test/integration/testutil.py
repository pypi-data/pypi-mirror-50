import os


def get_resource_path (filename):
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),
                        'resources', filename)
