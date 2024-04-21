from .LZ77.LZ77 import compress_lz77, decompress_lz77

import subprocess
import json
import os

def zip(read_from, write_to):
    with open(read_from, 'r') as file:
        data = file.read()
    
    ### LZ77
    # print("Compressing with lz77...")
    # data = compress_lz77(data)
    # data = json.dumps(data) # converting array to string
    # print("Finished.")
    ###
    
    with open('tmp.txt', 'w') as file:
        file.write(data)

    java_class_path = 'HuffmanEncode'
    classpath = './utils/Huffman'
    arg1 = 'tmp.txt'
    arg2 = write_to
    process = subprocess.run(['java', '-cp', classpath, java_class_path, arg1, arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        print("Error:", process.stderr)
        raise Exception("Java subprocess failed with return code {}".format(process.returncode))
    
    os.remove(arg1)
    
    return write_to
    
def unzip(read_from, write_to):
    java_class_path = 'HuffmanDecode'
    classpath = './utils/Huffman'
    arg1 = read_from
    arg2 = 'tmp.txt'
    process = subprocess.run(['java', '-cp', classpath, java_class_path, arg1, arg2], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if process.returncode != 0:
        print("Error:", process.stderr)
        raise Exception("Java subprocess failed with return code {}".format(process.returncode))
    
    with open(arg2, 'r') as file:
        recovered_data = file.read()
    
    ### LZ77
    # recovered_data = json.loads(recovered_data)
    # recovered_data = decompress_lz77(recovered_data)
    ###
    
    with open(write_to, 'w') as file:
        file.write(recovered_data)
        
    os.remove(arg2)
        
    return write_to
