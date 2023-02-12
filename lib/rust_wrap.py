import subprocess as sp


def encode(input_name, output_name, key_name):
    return sp.run(['../flash-otp/target/release/flash-otp', 'encode', input_name, output_name, key_name], capture_output=True)

def decode(input_name, output_name, key_name):
    return sp.run(['../flash-otp/target/release/flash-otp', 'decode', input_name, output_name, key_name], capture_output=True)

