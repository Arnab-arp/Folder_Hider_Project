import hashlib
import os


def storable_hash_info(verification_info: str, salt=None) -> tuple[bytes, str]:
    """
    :param verification_info: String
    :param salt:
    :return tuple[bytes, str]:
    """
    if salt is None:
        salt = os.urandom(16)
    salted_info = salt + verification_info.encode()
    hash_obj = hashlib.sha256(salted_info)
    hashed_info = hash_obj.hexdigest()
    return salt, hashed_info


def verify_user(user_input, stored_salt, stored_hash) -> bool:
    """
    :param user_input:
    :param stored_salt:
    :param stored_hash:
    :return bool:
    """
    _, hashed_input = storable_hash_info(user_input, stored_salt)
    return hashed_input == stored_hash


if __name__ == '__main__':
    pass
    # # Example usage:
    # user_input = input("Enter verification info: ")
    #
    # if verify_user_input(user_input, stored_salt, stored_hash):
    #     print("User verified successfully!")
    # else:
    #     print("Verification failed.")


