import os
from getpass import getpass
from FDH_Library.FHD_Properties import Properties
from FDH_Library.FHD_Lib import unhide_file
import tkinter as tk
from tkinter import filedialog as fd

secrets_path = 'secrets.cdf5'

OPTIONS = ['Clear Screen', 'Show Logs', 'Encrypt And Hide Folder',
           'Show And Decrypt Hidden Folder(s)', 'Delete Superuser Credentials', 'Exit']


def visuals(d_type=None):
    os.system('cls')
    pic_art_a = """
                                ███████╗██████╗       ██╗  ██╗██╗██████╗ ███████╗██████╗
                                ██╔════╝██╔══██╗      ██║  ██║██║██╔══██╗██╔════╝██╔══██╗
                                █████╗  ██║  ██║█████╗███████║██║██║  ██║█████╗  ██████╔╝
                                ██╔══╝  ██║  ██║╚════╝██╔══██║██║██║  ██║██╔══╝  ██╔══██╗
                                ██║     ██████╔╝      ██║  ██║██║██████╔╝███████╗██║  ██║
                                ╚═╝     ╚═════╝       ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
                                                             """

    pic_art_b = """
                                                                                                                            
                                                                                                            
                                  ░░                            ░░                                  ░░░░░░  
                                                              ██████            ░░                          
                                                            ██▓▓▒▒▒▒██                                      
                                                        ████████████▒▒██                                    
                                                    ████░░░░░░░░░░░░████  ████                              
                                                  ██░░░░░░░░░░░░░░░░░░░░██▓▓▓▓██                            
                                                ██░░░░░░░░░░░░░░░░░░░░░░░░██▒▒██                            
                                                ██░░░░░░░░░░░░░░░░░░░░░░░░░░██                              
                                              ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██  ██                          
                                              ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓██                        
                                              ██░░████░░░░░░░░░░░░████░░░░░░░░██▓▓██                        
                                              ██▒▒████░░░░░░░░░░░░████▒▒░░░░░░████                          
                                              ██▒▒▒▒░░░░██░░░░██░░░░▒▒▒▒░░░░░░██                            
                                              ██░░░░░░░░░░████░░░░░░░░░░░░░░██▒▒██                          
                                              ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░██▓▓██                          
                                                ██░░░░░░░░░░░░░░░░░░░░░░░░██▓▓▓▓██                          
                                  ░░              ████░░░░░░░░░░░░░░░░████  ████                            
                                                      ████████████████                                      
                                                      ██░░░░░░░░░░░░████                                    
                                                      ██░░░░░░░░░░░░██░░██                                  
                            ░░                      ██░░██░░░░░░░░██░░██░░██                                
                                                    ██░░░░██░░░░██░░░░██░░░░██                              
                                                    ██░░▓▓██░░░░██▓▓░░██████                                
                                                      ████  ████  ████                                      
                                                                                                            
                                                                                                            
                                                                        ░░                                  

    """

    if d_type is None:
        print(pic_art_a)
    else:
        print(pic_art_b)
    return


def is_secrets_present() -> bool:
    return True if os.path.exists(secrets_path) else False


def main():

    root = tk.Tk()
    root.withdraw()

    t_art = '::> '
    user_name, user_password, user, msg = None, None, None, ''


    while 1:
        if user == '6':
            visuals(d_type='b')
            print(' Have A Nice Day! :-)')
            os.system('pause')
            break

        visuals()
        print(msg)

        if not is_secrets_present():
            print('Set Up Administrative Login Credentials...')
            user_name = input(f"Enter User Name (Case Sensitive):\n{t_art}")
            user_password = input(f"Enter Password (Case Sensitive):\n{t_art}")

            msg_ = (f"\n******** Your Login Credentials ********\nUser_name: {user_name}\nPassword: {user_password}\n\n"
                    f"***Warning: This will be the only time you'll be able to see your password,\n"
                    f"and will not be able to see or change in future.***\n")
            print(msg_)
            print('If you wish to change something type "N"')
            print('If you wish to go forward type "Y"')
            print('If you wish to Quit type "Q"')
            user = input('Confirmed?(y/n/q)')

            if user == 'q':
                break

            if user != 'y':
                continue

        else:
            user_name = input(f"Enter User Name (Case Sensitive):\n{t_art}")
            user_password = getpass(f"Enter Password (Case Sensitive):\n{t_art}")

        properties = Properties(user_name=user_name, password_1=user_password)
        secret_data = properties.get_secrets()

        if secret_data is None or user_name != secret_data['un']:
            msg = 'Incorrect Username or Password'
            continue
        visuals()
        print(" Administrative Login Successful...\n")
        user_name = secret_data['un']
        print(f"\t\t\t\tWelcome {user_name}\n")

        t_art = t_art.replace('::', f'::({user_name})')
        while 1:

            if user == '-1':
                os.system('cls')
                visuals()

            for idx, option in enumerate(OPTIONS):
                print(f' <{idx + 1}> {option}')
            print()

            user = input(t_art)

            if user == '1':
                os.system('cls')
                visuals()

            elif user == '2':
                os.system('notepad Error Logs.log')

            elif user == '3':
                directory = fd.askdirectory(parent=root,
                                            initialdir="/",
                                            title="Select Folder To Be Encrypted",
                                            mustexist=True).replace('/', '\\\\')
                if directory == '':
                    continue
                dir_pwd = input("Enter Directory Password (Case Sensitive)\n::> ")
                properties.file_encryption(password=dir_pwd, path=directory)
                print(f"\nDirectory: {directory} Has Been Encrypted and Hidden.")
                print(f"You Can Decrypt And Un-Hide Your Folder Through Option (4)\n")
                secret_data = properties.get_secrets()

            elif user == '4':
                if len(secret_data['fl']) == 0:
                    print('Could Not Find Any Records To Show.\n')
                else:
                    hidden_folder_list = [tuple(_) for _ in secret_data['fl']]

                    print(f"\n|Total Records Found: {len(hidden_folder_list)}|\n")
                    for idx, vals in enumerate(hidden_folder_list):
                        folder_drive, folder_name, folder_id, folder_path = vals
                        print(f'<{idx}>\n'
                              f'\t-> Drive: {folder_drive}:/\n'
                              f'\t-> Folder Name: {folder_name}\n'
                              f'\t-> Folder Path: {folder_path}\n'
                              f'\t-> Folder Hash: {folder_id}\n')

                    try:
                        sub_user = int(input(f'Choose Folder To Decrypt Or Type "-1" To Cancel.\n{t_art}'))
                        if sub_user == -1:
                            continue
                        folder_drive, folder_name, folder_id, folder_path = hidden_folder_list[sub_user]
                        dir_pwd = getpass("Enter Directory Password (Case Sensitive)\n::> ")
                        properties.file_decryption(password=dir_pwd, path=folder_path)
                        secret_data = properties.get_secrets()
                        print(f"\n<{folder_path}>Has Been Decrypted and Un-Hidden.\n"
                              f"If You Can Not See Your Directory Or Can Not Access Your Files,\n"
                              f"Please Go To Main Menu And View Your Logs For More Info.\n")
                        del folder_drive, folder_name, folder_id
                    except Exception as e:
                        print(e)
                        print('Not A Valid Input. Choose From The Options.\n')

            elif user == '5':
                msg_ = (" You are about to delete your Super User Credentials. This will remove all the\n"
                        " login credentials and necessary data, and you might lose all your files and folders\n"
                        " which are protected, and won't be able to recover them.\n"
                        "**** MAKE SURE YOU DO NOT HAVE ANYTHING PROTECTED. IF SO PLEASE UNLOCK YOUR FOLDER BEFORE PROCEEDING.****\n")
                print(msg_)
                con_one = input('ARE YOU SURE?(Y/N)').lower()
                if con_one == 'y':
                    con_two = input('THIS IS YOUR LAST Warning. ARE YOU SURE?(Y/N)')
                    if con_one == con_two and con_two == 'y':
                        user = '6'
                        unhide_file(secrets_path)
                        os.remove(secrets_path)
                        os.remove('Error Logs.log')
                        break
                    else:
                        user = '-1'
                        continue
                else:
                    user = '-1'
                    continue

            elif user == '6':
                break


if __name__ == "__main__":
    main()
    pass
