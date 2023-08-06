from argparse import RawTextHelpFormatter
from datetime import datetime
import configparser
import zipfile
import hashlib
import argparse
import os.path
import glob
import re

def get_file_name(dir_path):

    """Getting the file name from path
    
    Arguments:
        dir_path -- Contains the path of the file
    
    Returns:
        File name from the path
        
    """

    # split_path = os.path.split(os.path.realpath(dir_path))
    # print(split_path)
    split_path = dir_path.split("\\")
    return '"' + split_path[len(split_path) - 1] + '"'

def get_dir_path(dir_path):

    """From glob's path, it replaces all double back slash to one forward slash
    
    Arguments:
        dir_path -- Contains the path of the file
    
    Returns:
        Returns the whole path of the file with double quote marks
    """

    return f'"{os.path.dirname(os.path.abspath(dir_path))}"'

def get_file_size(dir_path):

    """A function to get the file size
    
    Arguments:
        dir_path -- Contains the path of the file

    Returns
        Returns the file size of the file using the getsize method from os.path

    """

    file_realpath = os.path.realpath(dir_path)
    return os.path.getsize(file_realpath)

def get_file_hasher(dir_path):
    
    """Gets the hash value of a file in both MD5 and SHA1
    
    Arguments:
        dir_path -- Contains the path of the file
    
    Returns:
        Returns a list that contains the md5 and sha1 value of a file
    """
    
    file_realpath = os.path.realpath(dir_path)
    hasher_md5 = hashlib.md5()
    hasher_sha1 = hashlib.sha1()
    try:
        with open(file_realpath, 'rb') as afile:
            buf = afile.read()
            hasher_md5.update(buf)
            hasher_sha1.update(buf)
    except Exception as e:
        print(e)
    return [hasher_md5.hexdigest(), hasher_sha1.hexdigest()]

def export_csv(dir_path, csv_name, include_date, include_time):

    """Generates a file containing path, name and size of files within the directory
    
    Arguments:
        dir_path -- Contains the path of the directory or folder
        csv_name -- Contains the name the user want for his or her CSV file
        include_date -- a boolean type variable, if set as true, the date is concatenated in the file name
        include_time -- a boolean type variable, if set as true, the time is concatenated in the file name

    Returns:
        Returns e to print an exception, and if it executes successfully, returns True as default value for the function

    """

    timestamp = datetime.now()
    timestamp_date = timestamp.strftime("%Y-%m-%d")
    timestamp_time = timestamp.strftime("%H-%M-%S")

    if include_date and include_time:
        csv_name += f" {timestamp_date}_{timestamp_time}"
    elif include_date:
        csv_name += f" {timestamp_date}"
    elif include_time:
        csv_name += f" {timestamp_time}"

    files = []
    if dir_path[len(dir_path) - 1] != '/':
        dir_path += '/'
    for root, directories, file_names in os.walk(os.path.realpath(dir_path)):
        files.extend(glob.iglob(root + "/*.*", recursive=True))
    
    try:
        with open(csv_name, "w") as new_file:
            file_list = []
            file_list.append(f'File Directory,File Name,File Size,MD5,SHA1')
            for file_info in files:
                if os.path.isfile(file_info):
                    file_list.append(f"{get_dir_path(file_info)},{get_file_name(file_info)},{get_file_size(file_info)},{get_file_hasher(file_info)[0]},{get_file_hasher(file_info)[1]}")
            new_file.write("\n".join(file_list))
        
        with zipfile.ZipFile(csv_name + '.zip', 'w') as zip_file:
            zip_file.write(csv_name)
            print("Success!")

    except Exception as e:
        return e
    return True

def check_valid_path(path):

    """Checks the path if it is a valid directory
    
    Arguments:
        path -- Contains the path of the directory or folder
    
    Returns:
        Returns as True if the path is a directory or the path exist else if the path is the path directs to a file, it returns false
    """

    real_path = os.path.realpath(path)
    if os.path.isfile(real_path):
        return False
    return True if os.path.isdir(real_path) or os.path.exists(real_path) else False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Exports all file information into a file, it includes all files in a directory/folder.\n"
                                                            "Remove any succeeding back slash '\\' if it prints out any errors")
    parser.add_argument("directory", help="Full path of a folder", default='', nargs="?")
    parser.add_argument("file_name", help="File name for the output", default='', nargs="?")
    parser.add_argument("-d", "--date", action="store_true", help="Include date in the file name", default='')
    parser.add_argument("-t", "--time", action="store_true", help="Include time in the file name", default='')
    user_inp = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('config.ini')

    include_date = False
    include_time = False

    if user_inp.date:
        include_date = True
    
    if user_inp.time:
        include_time = True

    if not os.path.isdir(user_inp.directory):
        if "/" in user_inp.directory or "\\" in user_inp.directory:
            print(f"Invalid path or file name")
        else:
            if user_inp.directory == '':
                file_name = config['default']['output_name']
            else:
                file_name = user_inp.directory
            config_dir = os.path.realpath(config['default']['directory'])
            export_csv(config_dir, file_name, include_date, include_time)
    elif user_inp.file_name == '':
        export_csv(user_inp.directory, os.path.realpath(config['default']['output_name']), include_date, include_time)
    else:
        export_csv(user_inp.directory, user_inp.file_name, include_date, include_time)