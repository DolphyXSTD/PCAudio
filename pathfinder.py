from pkg_resources import resource_filename

def find_path(file_name):
    file_path = resource_filename(__name__, file_name)
    return file_path
