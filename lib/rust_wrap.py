import subprocess as sp
import os

NAUTILUS_HOME = os.environ.get('NAUTILUS_HOME', '~')

def encode(input_name, output_name, key_name):
    return sp.run([f'{NAUTILUS_HOME}/flash-otp/target/release/flash-otp', 'encode', input_name, output_name, key_name], capture_output=True)

def decode(input_name, output_name, key_name):
    return sp.run([f'{NAUTILUS_HOME}/flash-otp/target/release/flash-otp', 'decode', input_name, output_name, key_name], capture_output=True)

