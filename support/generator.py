import os
import random
import string

AUTOTEST = "AUTOTEST"


def generate_random_string(length=8):
    return ''.join(random.sample(string.ascii_lowercase, length))


def generate_random_password(length=10):
    return generate_random_string(length) + "1Q_"


def generate_random_email(length=10):
    random_string = generate_random_string(length)
    return f"{AUTOTEST}{random_string}@example.com"


def generate_random_phone_number():
    code = "613"
    random_int = str(random.randint(7000000, 7999999))
    return "".join([code, random_int])


def generate_random_file_name(length=8):
    return generate_random_string(length=length) + ".txt"

def create_temp_files(configs, num_files=1):
    parent_folder = configs.scan_folder
    os.makedirs(parent_folder, exist_ok=True)

    files_paths = []
    for _ in range(num_files):
        unique_id = generate_random_string()
        folder_name = f'folder_{unique_id}'
        file_name = f'{unique_id}.txt'

        folder_path = os.path.join(parent_folder, folder_name)
        file_path = os.path.join(folder_path, file_name)

        os.makedirs(folder_path, exist_ok=True)

        with open(file_path, 'w') as file:
            file.write(str(unique_id))

        files_paths.append(file_path)

    return files_paths