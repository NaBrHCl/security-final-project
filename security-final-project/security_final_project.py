import argparse
import os.path
from typing import TextIO


class Mode:
    ENCRYPT = 'encrypt'
    DECRYPT = 'decrypt'
    GENERATE_KEY = 'generate-key'


def main():
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

    match args.mode:
        case Mode.ENCRYPT:
            input_file = validate_file(parser, args, 'input')
            key_file = validate_file(parser, args, 'key')
            encrypt(input_file, key_file)
        case Mode.DECRYPT:
            input_file = validate_file(parser, args, 'input')
            key_file = validate_file(parser, args, 'key')
            decrypt(input_file, key_file)
        case Mode.GENERATE_KEY:
            output_file = validate_file(parser, args, 'output')
            generate_key(output_file)


def validate_file(parser: argparse.ArgumentParser, args: argparse.Namespace, file_argument_name: str) -> str:
    if getattr(args, file_argument_name) is None:
        parser.error(f'{file_argument_name} file not provided')

    if not os.path.isfile(getattr(args, file_argument_name)):
        parser.error(f'{file_argument_name} file not found')

    return getattr(args, file_argument_name)


def encrypt(input_file: str, key: str):
    print('encrypt endpoint')


def decrypt(input_file: str, key: str):
    print('decrypt endpoint')


def generate_key(output_file: str):
    print('generate-key endpoint')


if __name__ == '__main__':
    main()
