import os


def get_filename_last_update(file_name):
    return '?u=' + str(os.path.getmtime(file_name))
