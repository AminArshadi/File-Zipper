from collections import deque
    
def find_longest_match(search_buffer, look_ahead_buffer):
    current_len = len(look_ahead_buffer)
    while current_len != -1:
        match_sequence = look_ahead_buffer[:current_len]
        if match_sequence in search_buffer:
            distance = len(search_buffer) - search_buffer.rfind(match_sequence)
            length = current_len
            matched_chars = None
            if distance == 0 and length == 0:
                matched_chars = '' if current_len == len(look_ahead_buffer) else look_ahead_buffer[current_len]
                return (distance, length, matched_chars)
            else:
                return (distance, length, matched_chars)
        current_len -= 1
    return (0, 0, look_ahead_buffer[0] if look_ahead_buffer else '')

def compress_lz77(chars):
    search_buffer, look_ahead_buffer, result = deque(), deque(chars), []
    i = 1
    while i <= len(chars):
        longest_match = find_longest_match(''.join(search_buffer), ''.join(look_ahead_buffer))
        result.append(longest_match)
        length = 1 if longest_match[1] == 0 else longest_match[1]
        while length != 0:
            search_buffer.append(look_ahead_buffer.popleft())
            length -= 1
            i += 1
    return result

def decompress_lz77(compressed_data):
    decompressed = []
    for distance, length, next_char in compressed_data:
        if distance == 0 and length == 0:
            decompressed.append(next_char)
        else:
            start = len(decompressed) - distance
            decompressed.extend(decompressed[start:start + length])
            if next_char:
                decompressed.append(next_char)
    return ''.join(decompressed)
