from LZ77.LZ77 import compress_lz77, decompress_lz77

import subprocess
import json
import os

def zip(read_from, write_to):
    with open(read_from, 'r') as file:
        data = file.read()
        
    compressed_data = compress_lz77(data)
    list_string = json.dumps(compressed_data)
    with open('tmp.txt', 'w') as file:
        file.write(list_string)

    java_class_path = 'HuffmanEncode'
    classpath = './Huffman'
    arg1 = 'tmp.txt'
    arg2 = write_to
    subprocess.run(['java', '-cp', classpath, java_class_path, arg1, arg2])
    
    os.remove('tmp.txt')
    
    return write_to
    
def unzip(read_from, write_to):
    java_class_path = 'HuffmanDecode'
    classpath = './Huffman'
    arg1 = read_from
    arg2 = 'tmp.txt'
    subprocess.run(['java', '-cp', classpath, java_class_path, arg1, arg2])
    
    with open(arg2, 'r') as file:
        list_string = file.read()
    
    recovered_list = json.loads(list_string)
    recovered_data = decompress_lz77(recovered_list)
    with open(write_to, 'w') as file:
        file.write(recovered_data)
        
    os.remove('tmp.txt')
        
    return write_to
        
tmp = zip('genes.txt', 'zipped_genes.txt')
unzip(tmp, 'recovered_genes.txt')
