import argparse
import json
import os.path
from typing import Optional, TextIO


class Mode:
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'
    GENERATE_KEY = 'generate-key'


class Transformation:
    def __init__(self, type: str, key: Optional[int | str]):
        self.type = type
        self.key = key


TRANSFORMATION_TYPES = ('caesar', 'reverse', 'vigenere')

parser = argparse.ArgumentParser(
    description='A simple CLI tool for encryption and decryption of files.',
    epilog="""Example Usage:
        python script.py encrypt -i file.txt -k key.txt
        python script.py decrypt -i file.txt -k key.txt
        python script.py generate-key -o key.txt
        """,
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument(
    'mode',
    choices=[Mode.ENCRYPT, Mode.DECRYPT, Mode.GENERATE_KEY],
    help='Mode of operation. Encryption or decryption of the file'
)
parser.add_argument(
    '-i', '--input',
    required=False,
    help='Path to the input file (to encrypt or decrypt)'
)
parser.add_argument(
    '-o', '--output',
    required=False,
    help='Path to the output file, optional (for encryption, decryption or generation of key file)'
)
parser.add_argument(
    '-k', '--key',
    required=False,
    help='Path to the key file (to encrypt or decrypt)'
)

args = parser.parse_args()


def main():
    match args.mode:
        case Mode.ENCRYPT:
            input_file: str = validate_file('input')
            key_file: str = validate_file('key')
            output_file: Optional[str] = validate_file('output', False)

            encrypt(input_file, key_file, output_file)

        case Mode.DECRYPT:
            input_file: str = validate_file('input')
            key_file: str = validate_file('key')
            output_file: Optional[str] = validate_file('output', False)

            decrypt(input_file, key_file, output_file)

        case Mode.GENERATE_KEY:
            if getattr(args, 'output') is None:
                parser.error('output file not provided')
            output_file: str = args.output

            generate_key(output_file)


def validate_file(file_argument_name: str, required: bool = True) -> str | None:
    if getattr(args, file_argument_name) is None:
        if not required:
            return None
        parser.error(f'{file_argument_name} file not provided')

    if not os.path.isfile(getattr(args, file_argument_name)):
        parser.error(f'{file_argument_name} file not found')

    return getattr(args, file_argument_name)


def encrypt(input_file: str, key: str, output_file: str):
    print('encrypt endpoint')


def decrypt(input_file: str, key: str, output_file: str):
    print('decrypt endpoint')


def generate_key(output_file: str):
    file: Optional[TextIO] = None

    try:
        file = open(output_file, 'w')
    except OSError:
        parser.error(f'cannot write to \'{output_file}\'')

    transformations: list[Transformation] = []

    while True:
        display_encryption_prompt()
        transformation_index: int = get_positive_int_input(
            min_input=1,
            max_input=len(TRANSFORMATION_TYPES),
            can_escape=True
        )

        # if the user decides to stop adding transformations
        if transformation_index == -1:
            break

        type: str = TRANSFORMATION_TYPES[transformation_index - 1]

        key: Optional[int | str] = None

        match type:
            case 'caesar':
                print('Enter the key (1-25): ', end='')
                key = get_positive_int_input(min_input=1, max_input=25)

            case 'reverse':
                pass

            case 'vigenere':
                print('Enter the key (a word): ', end='')
                key = get_non_empty_input()

        transformations.append(Transformation(type, key))
        print(f'added: type - {type}, key - {key}\n')

    if file is not None:
        json.dump([transformation.__dict__ for transformation in transformations], file)
        file.close()
        print(f'key stored at \'{output_file}\'')


def display_encryption_prompt():
    print(f'''Select an encryption method (e.g. enter \'1\' for {TRANSFORMATION_TYPES[0]})
    or Enter nothing to terminate
    ''')
    display_encryption_methods()
    print()


def display_encryption_methods():
    for i, type in enumerate(TRANSFORMATION_TYPES):
        print(f'{i + 1}. {type}')


def print_error(message: str):
    """
    Print an error message in red.
    :param message: The error message to display.
    """
    print(f'\033[91m{message}\033[00m')


def get_non_empty_input() -> str:
    while True:
        str_input = input()

        if len(str_input) == 0:
            print_error('Input cannot be empty')
            continue

        return str_input


def get_positive_int_input(min_input: int = 0, max_input: Optional[int] = None, can_escape=False) -> int:
    """
    Get a positive integer input from the user, optionally between min_input and max_input inclusively.
    If the user escapes, -1 is returned.

    :param min_input: The minimum accepted input.
    :param max_input: The maximum accepted input.
    :param can_escape: Whether the user can choose not to provide an input by submitting nothing.
    :return: The valid input from user.
    """

    while True:
        raw_input: str = input()

        if can_escape and raw_input == '':
            return -1

        if not raw_input.isdigit():
            print_error('Integer only')
            continue

        int_input: int = int(raw_input)

        if int_input < min_input:
            print_error(f'Input cannot be less than {min_input}')
            continue

        if int_input > max_input:
            print_error(f'Input cannot be more than {max_input}')
            continue

        return int_input


if __name__ == '__main__':
    main()
