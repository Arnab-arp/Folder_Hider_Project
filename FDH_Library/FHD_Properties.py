# mod_path = [
# "E:\\PythonProjects\\FileHider\\FDH_Library\\FHD_AES.py",
# "E:\\PythonProjects\\FileHider\\FDH_Library\\FHD_Properties.py",
# "E:\\PythonProjects\\FileHider\\FDH_Library\\FHD_Secrets.py"
# ]
# import sys
#
# for paths in mod_path:
#     if paths not in sys.path:
#         sys.path.append(paths)
from FDH_Library import FHD_Secrets, FHD_Lib
from FDH_Library.FHD_AES import AESEncryption
from tqdm import tqdm
from gc import collect
import json
import os



V_BASE_PATH = 'secrets.cdf5'


class Properties:
    def __init__(self, password_1: str, user_name: str):
        self.__password_1 = password_1
        if not os.path.exists(V_BASE_PATH):
            FHD_Lib.create_jdata(password_1, user_name=user_name)

    def get_secrets(self) -> dict | None:

        """
        :return None | Dict:
        Function Description:
            Function returns a dictionary, if the first password is Correct
            else, Return s none with error log update.

        """
        mode = 'XB29'
        cls = AESEncryption(self.__password_1, file_location=V_BASE_PATH)
        sec_data_state = cls.PerformTask(encryption=False, dump_data=False)
        if isinstance(sec_data_state, bytes) or sec_data_state != 0:
            try:
                secret_json = json.loads(sec_data_state.decode())
                FHD_Lib.e_update(error_message=None, while_in_mode=mode)
                return secret_json
            except json.decoder.JSONDecodeError as e:
                msg = str(e) + '. Password Incorrect. Access denied.'
                FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
                del msg
                return None
        else:
            msg = 'Password Incorrect. Access denied.'
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return None


    def file_encryption(self, password: str, path, secrets: dict | None = None):
        """
        :return None:
        Function Description:
            Function encrypts a file given a password and file path
        """
        mode = '00C5'

        if not os.path.isdir(path):
            msg = 'Path provided is not of a Directory (Folder). Aborting...'
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        if secrets is None:
            secrets = self.get_secrets()
            if secrets is None:
                FHD_Lib.e_update(error_message='Encryption failed. Can not unpack necessary data.', while_in_mode=mode)
                return

        unq_id_hash = FHD_Lib.get_hash(path)
        if unq_id_hash in secrets.keys():
            msg = 'Previous records found. The contents of this folder may already be encrypted. Aborting.'
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        salt, hashed_info = FHD_Secrets.storable_hash_info(password)
        salt = FHD_Lib.reversible_byte_to_str_converter(data=salt, switch=True)  # Byte to String
        secrets[unq_id_hash] = {0: (salt, hashed_info)}

        folder_name = FHD_Lib.split_path_to_file(path)
        drive_name = list(path)[0]

        secrets['fl'].append([drive_name, folder_name, unq_id_hash, path])

        file_list = FHD_Lib.bloom_path(path)
        new_file_list = FHD_Lib.assign_ids(file_list)
        secrets[unq_id_hash][1] = new_file_list

        try:
            new_file_list = FHD_Lib.format_file_names(new_file_list)
        except Exception as e:
            msg = 'Exception occurred while renaming File. ' + str(e)
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        folder_name = FHD_Lib.split_path_to_file(path)
        ae_cls = ''
        for file_path in tqdm(new_file_list, desc=f'Encrypting {folder_name}'):
            ae_cls = AESEncryption(password=password, file_location=file_path)
            state = ae_cls.PerformTask(encryption=True, dump_data=True)
            if state != 200:
                msg = f'Exception occurred while Encrypting File {file_path}. Exited With State {state}'
                FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
                del msg
                return

        try:
            FHD_Lib.unhide_file(V_BASE_PATH)
            with open(V_BASE_PATH, 'w') as j_file:
                json.dump(secrets, j_file)
            AESEncryption(self.__password_1, file_location=V_BASE_PATH).PerformTask(encryption=True)
            FHD_Lib.hide_file(V_BASE_PATH)

            FHD_Lib.e_update(error_message=None, while_in_mode=mode)
        except Exception as e:
            FHD_Lib.e_update(error_message=e, while_in_mode=mode)

        FHD_Lib.hide_file(path)

        FHD_Lib.e_update(error_message=None, while_in_mode='9LP7')

        del salt, hashed_info, unq_id_hash, file_list, new_file_list, ae_cls, secrets
        collect()
        return


    def file_decryption(self, password: str, path, secrets: dict | None = None):
        """
        :return None:
        Function Description:
            Function decrypts a file given a password and file path
        """
        mode = 'EZQ1'
        if secrets is None:
            secrets = self.get_secrets()
            if secrets is None:
                FHD_Lib.e_update(error_message='Decryption failed. Can not unpack necessary data.', while_in_mode=mode)
                return

        unq_id_hash = FHD_Lib.get_hash(path)
        if unq_id_hash not in secrets.keys():
            msg = 'Decryption failed. Can not find the folder.'
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        salt, hashed_info = tuple(secrets[unq_id_hash]['0'])
        salt = FHD_Lib.reversible_byte_to_str_converter(salt, switch=False)

        if not FHD_Secrets.verify_user(user_input=password, stored_salt=salt, stored_hash=hashed_info):
            msg = 'Password to this folder is incorrect. Access is denied.'
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        name_list = [tuple(items) for items in secrets[unq_id_hash]['1']]

        try:
            name_list = FHD_Lib.format_file_names(name_list, reverse=True)
        except Exception as e:
            msg = 'Exception occurred while renaming File. ' + str(e)
            FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
            del msg
            return

        try:
            FHD_Lib.unhide_file(path)
            FHD_Lib.e_update(error_message=None, while_in_mode='HJH4')
        except Exception as e:
            msg = str(e) + 'Un-hiding folder failed.'
            FHD_Lib.e_update(error_message=msg, while_in_mode='HJH4')
            del msg
            return

        folder_name = FHD_Lib.split_path_to_file(path)

        for file_path in tqdm(name_list, desc=f'Decrypting {folder_name}'):
            ae_cls = AESEncryption(password=password, file_location=file_path)
            state = ae_cls.PerformTask(encryption=False, dump_data=True)
            if state != 200:
                msg = f'Exception occurred while Decrypting File {file_path}. Exited With State {state}'
                FHD_Lib.e_update(error_message=msg, while_in_mode=mode)
                del msg
                FHD_Lib.hide_file(path)
                return

        del secrets[unq_id_hash]

        drive_name = list(path)[0]

        for ind, vals in enumerate(secrets['fl']):
            if unq_id_hash in vals and drive_name in vals and path in vals:
                secrets['fl'].pop(ind)

        try:
            FHD_Lib.unhide_file(V_BASE_PATH)
            with open(V_BASE_PATH, 'w') as j_file:
                json.dump(secrets, j_file)
            AESEncryption(self.__password_1, file_location=V_BASE_PATH).PerformTask(encryption=True)
            FHD_Lib.hide_file(V_BASE_PATH)
            FHD_Lib.e_update(error_message=None, while_in_mode=mode)
        except Exception as e:
            FHD_Lib.e_update(error_message=e, while_in_mode=mode)

        try:
            del salt, hashed_info, unq_id_hash, name_list, ae_cls, secrets
            collect()
        except Exception as e:
            FHD_Lib.e_update(error_message=e, while_in_mode=mode)
            return


if __name__ == '__main__':
    FHD_Lib.unhide_file('E:\\PythonProjects\\Decoy')