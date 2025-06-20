import heapq
from collections import defaultdict

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    freq = defaultdict(int)
    for byte in data:
        freq[byte] += 1
    return freq

def build_huffman_tree(freq_table):
    heap = [Node(byte, freq) for byte, freq in freq_table.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}

    if node is None:
        return

    if node.char is not None:
        code_map[node.char] = prefix

    build_codes(node.left, prefix + "0", code_map)
    build_codes(node.right, prefix + "1", code_map)

    return code_map

def compress(data):
    freq_table = build_frequency_table(data)
    root = build_huffman_tree(freq_table)
    codes = build_codes(root)

    encoded = ''.join(codes[byte] for byte in data)
    padding = 8 - len(encoded) % 8
    encoded = f"{padding:08b}" + encoded + '0' * padding

    b = bytearray()
    for i in range(0, len(encoded), 8):
        b.append(int(encoded[i:i+8], 2))

    return bytes(b), codes

def decompress(data, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    bit_string = ''.join(f"{byte:08b}" for byte in data)

    padding = int(bit_string[:8], 2)
    bit_string = bit_string[8:-padding] if padding > 0 else bit_string[8:]

    current_code = ""
    output = bytearray()

    for bit in bit_string:
        current_code += bit
        if current_code in reverse_codes:
            output.append(reverse_codes[current_code])
            current_code = ""

    return bytes(output)
