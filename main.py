import os
import random
import zlib
import lzma
from marshal import dumps, loads
import time

# Constants
JUNK_DATA = "__skid__" * 15  # Placeholder string used for obfuscation
CHAR_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def apply_gradient(text):
    os.system("")  # Enable ANSI escape codes in Windows terminal
    faded_text = ""
    red_value = 40

    for line in text.splitlines():
        faded_text += f"\033[38;2;{red_value};0;220m{line}\033[0m\n"
        red_value = min(red_value + 15, 255)  # Increment red value and cap at 255

    return faded_text

def generate_random_var_name(length=10):
    return ''.join(random.choice(CHAR_SET) for _ in range(length))

def compress_text(text):

    compressed_data = zlib.compress(text.encode())
    return lzma.compress(compressed_data)

def encrypt_with_compression(text):

    compiled_code = compile(text, '<string>', 'exec')
    marshalled_code = dumps(compiled_code)
    
    obfuscated_script = f'{JUNK_DATA}="{JUNK_DATA}";exec(loads({marshalled_code}));{JUNK_DATA}="{JUNK_DATA}"'
    compressed_script = compress_text(obfuscated_script)
    
    return f"import zlib, lzma\nexec(zlib.decompress(lzma.decompress({compressed_script})))"

def simple_encryption(text):
    compiled_code = compile(text, '<string>', 'exec')
    marshalled_code = dumps(compiled_code)
    
    obfuscated_script = f'from marshal import loads\nexec(loads({marshalled_code}))'
    return f'{JUNK_DATA}="{JUNK_DATA}";{obfuscated_script};{JUNK_DATA}="{JUNK_DATA}"'

def encrypt_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError("File not found")
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # Apply two layers of encryption
    encrypted_code = encrypt_with_compression(code)
    encrypted_code = simple_encryption(encrypted_code)

    # Determine the output filename based on the input filename
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_filename = f'{file_name}-obf.py'

    # Write the encrypted code to a new file
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(encrypted_code)

    return output_filename

def main():
    # Clear the screen and print the title with gradient effect
    clear_screen()
    print(apply_gradient('''
     ██░ ██  ▄▄▄        ██████  ██░ ██ 
    ▓██░ ██▒▒████▄    ▒██    ▒ ▓██░ ██▒
    ▒██▀▀██░▒██  ▀█▄  ░ ▓██▄   ▒██▀▀██░
    ░▓█ ░██ ░██▄▄▄▄██   ▒   ██▒░▓█ ░██ 
    ░▓█▒░██▓ ▓█   ▓██▒▒██████▒▒░▓█▒░██▓
     ▒ ░░▒░▒ ▒▒   ▓▒█░▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒
     ▒ ░▒░ ░  ▒   ▒▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░
     ░  ░░ ░  ░   ▒   ░  ░  ░   ░  ░░ ░
     ░  ░  ░      ░  ░      ░   ░  ░  ░
    '''))

    try:
        # Prompt the user to enter the path of the file to be encrypted
        file_path = input('Drag and drop your file here: ').strip()

        # Encrypt the file
        print('\n[+] Encrypting...')
        encrypted_file = encrypt_file(file_path)
        print('[+] Done\n')

        # Clear the screen and confirm completion
        clear_screen()
        print(f'Done! Your file is encrypted and saved as {encrypted_file}\n')
        print('[+] Thanks for using this tool')

        time.sleep(5)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(5)

if __name__ == '__main__':
    main()
