import base64
def encode_base64(file):
    with open(file, 'rb') as binary_file:
        base64EncodedFile = base64.b64encode(binary_file.read()).decode('ascii')
    return base64EncodedFile