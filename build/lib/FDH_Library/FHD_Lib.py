from collections.abc import Iterable
from FDH_Library.FHD_AES import AESEncryption
from datetime import datetime
import hashlib
import base64
import uuid
import json
import os


E_BASE_PATH = 'Error Logs.log'
V_BASE_PATH = 'secrets.cdf5'


modes = {
    'XB29': 'VERIFICATION',
    '00C5': 'FILE ENCRYPTION',
    '9LP7': 'FOLDER HIDING',
    'EZQ1': 'FILE DECRYPTION',
    'HJH4': 'FOLDER UN-HIDING',
    '90B3': 'PATH EXISTS',
}


def is_iterable(variable: any) -> bool:
    """
    :param variable: any
    :return bool:

    Function Description:
        Returns; True if an object is of type list or tuple,
                 False if any other data type.
    """
    return isinstance(variable, Iterable) and not isinstance(variable, (str, bytes))


def reversible_byte_to_str_converter(data: bytes | str, switch: bool) -> bytes | str:
    """
    :param data: Bytes or String
    :param switch: Bool
    :return bytes | str:

    Function Description:
        Converts byte type object to string, and string type object to bytes.
        If Switch is True, converts bytes to string;
        else if switch is false converts string to bytes;
    """
    if switch:
        return base64.b64encode(data).decode('utf-8')
    return base64.b64decode(data)



def get_hash(path: str) -> str:

    """
    :param path:
    :return str:

    Function Description:
        Functions return the hash value for the unique id of the file or the folder.
    """

    unique_id = str(os.stat(path).st_ino)
    hash_object = hashlib.sha256()
    hash_object.update(unique_id.encode('utf-8'))
    hash_hex = hash_object.hexdigest()
    return hash_hex


def e_update(error_message, while_in_mode) -> None:
    """
    :param error_message:
    :param while_in_mode:
    :return None:

    Function description:
        Executing this function will create a (.log) file containing error messages (if not exists, else update file.).
            error_message: Argument takes string type or None type object. IF, error_message is None,
                           the log file is updated with 'Event ID - 1000' meaning process executed successfully.
                           ELSE, a unique event ID is generated and the log file is updated with the error message.
            while_in_mode: Argument takes int type object only. Primarily used to determine at what stage, the error
                           has been encountered. (Predefined in the 'modes' dictionary)
    """

    current_datetime = datetime.now()
    with open(E_BASE_PATH, 'a') as file:
        if error_message is None:
            msg = (f'Event ID - {while_in_mode} \n'
                   f'   > timestamp - {current_datetime}\n'
                   f'   > mode - {modes[while_in_mode]} PASSED\n'
                   f'   > No Exception Caught\n'
                   f'   > Process finished.\n\n')
            file.write(msg)
        else:
            msg = (f'Event ID - {while_in_mode} \n'
                   f'   > timestamp - {current_datetime}\n'
                   f'   > mode - {modes[while_in_mode]} FAILED\n'
                   f'   > Exception Caught: {error_message}\n\n'
                   )
            file.write(msg)

        return


def extract_file_path(dir_list: list) -> list:

    """
    :param dir_list:
    :return list:

    Function Description:
        This function takes in a 'List of directory paths (with escape character)' and returns
        the 'List of all available file paths'.

    Example Usage:
        Input:
            directories = ["D:\\\\SteamLibrary", "D:\\\\Driver64\\\\Windows\\\\ASUS\\\\Config"]
            temp = Features.extract_file_path(dir_list=directories)
            print(temp)
        Output:
            [
            'D:\\\\SteamLibrary\\\\libraryfolder.vdf', 'D:\\\\SteamLibrary\\\\steam.dll',
            'D:\\\\SteamLibrary\\\\steamapps\\\\appmanifest_460930.acf.404734390.tmp',
            'D:\\\\SteamLibrary\\\\steamapps\\\\common\\\\Wildlands\\\\dxdiag.txt',
            'D:\\\\SteamLibrary\\\\steamapps\\\\common\\\\Wildlands\\\\graphicstatedump.txt',
            'D:\\\\SteamLibrary\\\\steamapps\\\\common\\\\Wildlands\\\\logs\\\\uplay_crash_reporter.txt',
            'D:\\\\Driver64\\\\Windows\\\\ASUS\\\\Config\\\\McAfee.ini',
            'D:\\\\Driver64\\\\Windows\\\\ASUS\\\\Config\\\\ProductLine.ini'
            ]
    """
    mode = '90B3'
    all_file_list = []
    try:
        for directory in dir_list:
            for dirpath, dirnames, filenames in os.walk(directory):
                for filename in filenames:
                    full_path = os.path.join(dirpath, filename)
                    all_file_list.append(full_path)
        return all_file_list
    except Exception as e:
        e_update(e, while_in_mode=mode)
        raise Exception(e)


def bloom_path(path: str) -> None | list:

    """
    :param path: Path to folder or file
    :return None | list:

    Function Description:
        This function will return a list of files, in the specified path.
            if the path is of a 'single' file; return list containing file path.
            else if path is of a folder; return list containing file paths in that folder and its sub-folder.
            else if the path is not valid; return None, with an error message updated in the Error Logs.log file.

    Exxample Usage:
        path = "D:\\New Folder"
        file_list = bloom_path(path=path)
        Output:
        >> ['D:\\New folder\\Scripts\\python.exe', 'D:\\New folder\\pythonw.exe', ...]
    """
    mode = '90B3'
    if not os.path.exists(path):
        e_update(error_message='False Path. Path Do Not Exists', while_in_mode=mode)
        return None
    file_list = []
    dir_list = []

    if os.path.isfile(path):
        file_list.append(path)
    else:
        dir_list.append(path)
    file_list += extract_file_path(dir_list)

    return file_list


def create_jdata(password_1: str, user_name: str) -> None:
    """
    :return None:
    Function Description:
        Calling this function will generate (.JSON) files, which keeps all the important data of the file paths,
        previous names, changed names, etc.
    """

    v_data = {
            'un': user_name,
            'fl': []

              }

    with open(V_BASE_PATH, 'w') as j_file:
        json.dump(v_data, j_file)

    AESEncryption(password=password_1, file_location=V_BASE_PATH).PerformTask(encryption=True)
    hide_file(V_BASE_PATH)
    return


def split_path_to_file(file_path: str) -> str:

    """
    :param file_path:
    :return str:
    Function Description:
        Extracts the name of a file from its file path.
    Example usage:
        temp = split_path_to_file(file_path='D:\\New Folder\\secret.mp3')
        Output:
        >> 'secret.mp3'
    """

    return file_path.split('\\')[-1]


def assign_ids(file_list: list[str]) -> list[tuple[str, str]]:
    """
    :param file_list:
    :return list[tuple[str, str]]:

    Function Description:
        This functions takes in a list of file path, assigns them with a unique id, to mask the original file name
        and file type (.cdf5). Returns a list of tuples containing the previous file name and the new given file name.

    Example Usage:
        file_list = ['D:\\New folder\\Scripts\\python.exe', 'D:\\New folder\\Scripts\\pythonw.exe', ...]
        new_list = assign_ids(file_list = file_list)

        Output:
        >> [('D:\\New folder\\Scripts\\python.exe',
        'D:\\New folder\\Scripts\\85e7688f-ee2e-4820-a3dc-e5f58c064463.cdf5'),
        ('D:\\New folder\\Scripts\\pythonw.exe',
        'D:\\New folder\\Scripts\\b03a6409-e53a-45b7-a62b-cfa834303f95.cdf5'), ...]
    """

    modified_list = []
    unique = []
    extension = '.cdf5'

    i = 0

    while len(modified_list) != len(file_list):
        assignable_id = str(uuid.uuid4())
        if assignable_id not in unique:
            unique.append(assignable_id)
            prev_file_name = split_path_to_file(file_list[i])
            new_file_path = file_list[i].replace(prev_file_name, assignable_id + extension)
            modified_list.append((file_list[i], new_file_path))
            i += 1

    del unique, extension
    return modified_list


def format_file_names(modified_list: list[tuple], reverse: bool = False) -> list[str]:

    """
    :param modified_list:
    :param reverse: bool
    :return list[str]:

    Function Description:
        This function takes a list of tuples containing the previous file name and new file name,
        renames the file, and returns a list, containing the new file name only.

        if reverse is False:
            Previous file name will be renamed to its new file name.
            New file name will be renamed to its previous file name.

    Example Usage:
        name_list = [('D:\\New folder\\Scripts\\python.exe',
                      'D:\\New folder\\Scripts\\85e7688f-ee2e-4820-a3dc-e5f58c064463.cdf5'),
                     ('D:\\New folder\\Scripts\\pythonw.exe',
                      'D:\\New folder\\Scripts\\b03a6409-e53a-45b7-a62b-cfa834303f95.cdf5'), ...]

        formatted_name = format_file_names(modified_list = name_list)
        Output:
        >> ['D:\\New folder\\Scripts\\85e7688f-ee2e-4820-a3dc-e5f58c064463.cdf5',
            'D:\\New folder\\Scripts\\b03a6409-e53a-45b7-a62b-cfa834303f95.cdf5', ...]

    """

    new_list = []
    if not reverse:
        for prev_path, new_path in modified_list:
            if os.path.exists(prev_path):
                os.rename(prev_path, new_path)
                new_list.append(new_path)
        return new_list

    for new_path, prev_path in modified_list:
        if os.path.exists(prev_path):
            os.rename(prev_path, new_path)
            new_list.append(new_path)
    return new_list



def hide_file(file_path: str) -> str | Exception:
    """
    :param file_path: Path of file or folder
    :return str | Exception:

    Function Description:
        Hides a file or folder using os.system(), and returns 'OK' if the function runs successfully
        else returns the exception.
    """

    command = f'attrib +h +s +r "{file_path}"'
    try:
        os.system(command)
        return 'OK'
    except Exception as e:
        return e


def unhide_file(file_path: str) -> str | Exception:
    """
        :param file_path: Path of file or folder
        :return str | Exception:

        Function Description:
            Un-hides a file or folder using os.system(), and returns 'OK' if the function runs successfully
            else returns the exception.

        """

    command = f'attrib -h -s -r "{file_path}"'
    try:
        os.system(command)
        return 'OK'
    except Exception as e:
        return e


if __name__ == "__main__":
    pass
    # print(get_hash("D:\\New folder\\pyvenv.cfg"))
    # help(is_iterable)


