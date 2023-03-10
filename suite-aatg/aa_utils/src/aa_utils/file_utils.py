import os
from typing import List


class Csv(object):
    def __init__(self, file, delimiter=','):
        self.__f = file
        self.__delimiter = delimiter

    def get_values(self, ignore_first_line=False):
        with open(self.__f, 'r') as f:
            if ignore_first_line:
                return [l.rstrip().split(self.__delimiter) for l in f.readlines()[1:]]
            return [l.rstrip().split(self.__delimiter) for l in f.readlines()]


def get_temp_dir():
    return os.environ['temp']


def try_rename_file(old_name, new_name):
    """
    Rename file.
    :param str old_name: full qualified file name (eg: C:/temp/old.txt)
    :param str new_name: new full qualified file name (eg: C:/temp/new.txt)
    :return: A bool which indicates if rename operation was successfully
    :rtype: bool
    """
    try:
        os.rename(old_name, new_name)
        print(f"Debug: renamed {old_name} to {new_name}")
        return True
    except Exception as e:
        print(f"Warn: could not rename {old_name}")
        print(e)
        return False


def rename_files(directory, replace_string=None, prefix=None, suffix=None):
    """
    Rename all files (without extension) in given directory using either replace_string, prefix or suffix.
    :param str directory: path where files should be renamed
    :param str replace_string: replaces the entire file name
    :param str prefix: append prefix (with underscore) to existing file name
    :param str suffix: append suffix (with underscore) to existing file name
    """
    success = 0
    todo = len([f for f in os.listdir(directory)])

    for f in os.listdir(directory):
        old = os.path.join(directory, f)
        new = None

        old_name = f.split('.')[0]  # remove extension(s)
        if replace_string:
            new = os.path.join(directory, f.replace(old_name, replace_string))
        if prefix:
            new = os.path.join(directory, f.replace(old_name, '{}_{}'.format(prefix, old_name)))
        if suffix:
            new = os.path.join(directory, f.replace(old_name, '{}_{}'.format(old_name, suffix)))

        if try_rename_file(old, new):
            success += 1

    print(f"Info: renamed {success}/{todo} files in {directory}")


def find_files_by_extension(path, extension):
    """
    Find files with given extensions in given path. All subdirectories are included.
    :param str path: Root path
    :param str extension: The extension of the files e.g. ".txt"
    :rtype: List[str]
    :return: A list of all objects found
    """

    result = []
    total = 0
    for root, dirs, files in os.walk(path):
        files_by_ext = [f for f in files if f.endswith(extension)]
        if any(files_by_ext):
            total += len(files_by_ext)
            print(f'{root}: {len(files_by_ext)} ({files_by_ext})')

            for file in files_by_ext:
                result.append(os.path.join(root, file))

    print(f"Found {total} files with extension {extension}")
    return result
