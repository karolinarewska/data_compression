import json
import time

################################################################################
# Huffman tree creation
################################################################################
def create_huffman_codes(huffman_tree):
    return {str(char): code for char, code in huffman_tree}


################################################################################
# Encoding
################################################################################
def huffman_encode(Input_data, codes):
    # Create new table for Input data - as a difference between [x] and [x+1] element
    diff_data = []
    abs_data = []
    for x in range(len(Input_data) - 1):
        if Input_data[x] - Input_data[x + 1] >= 0:
            abs_data.append(0)
        else:
            abs_data.append(1)

        diff_data.append(abs(Input_data[x] - Input_data[x + 1]))

    # Removing first value from Input and assign it as first_element
    first_element = Input_data[0]

    # Adding first_element to stream_array
    stream_array = []
    first_element_bin = bin(first_element)[2:]
    while len(first_element_bin) < size_of_first_element:
        first_element_bin = '0' + first_element_bin

    for e in first_element_bin:
        stream_array.append(int(e))

    # Encoding process for diff_data
    for i in range(len(diff_data)):
        stream_array.append(abs_data[i])
        data = codes[str(diff_data[i])]
        for e in data:
            stream_array.append(int(e))

    return stream_array


################################################################################
# Decoding
################################################################################
def huffman_decode(stream_array, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    final_array = []
    current_code = ''
    diff_data = []
    abs_data = []

    # Extract the first element from the stream
    first_value = stream_array[:size_of_first_element]
    del stream_array[:size_of_first_element]
    first_value_num = int("".join(map(str, first_value)), 2)
    final_array.append(first_value_num)

    #Extract the first abs from the stream
    first_abs = stream_array.pop(0)
    abs_data.append(first_abs)

    # Decode the differences and signs
    while stream_array:
        bit = str(stream_array.pop(0))
        current_code += bit

        if current_code in reverse_codes:
            symbol = reverse_codes[current_code]
            diff_data.append(int(symbol))
            current_code = ''
            if stream_array:
                abs_bit = stream_array.pop(0)
                abs_data.append(abs_bit)

    # Reconstruct the original data
    for i in range(len(diff_data)):
        if abs_data[i] == 1:
            next_value = final_array[-1] + diff_data[i]
        else:
            next_value = final_array[-1] - diff_data[i]
        final_array.append(next_value)

    return final_array


################################################################################
# TEST BENCH
################################################################################
time_start = time.ticks_cpu()
data_to_encode = []
size_of_first_element = 12

# Read Huffman tree
with open('huffman_tree_spring.json', 'r') as infile:
    huffman_tree = json.load(infile)


# Read data for coding/decoding
with open("2023_04_09-03.txt", 'r') as file:
    for line in file:
        data_to_encode.append(int(line))

data_to_encode = [x for x in data_to_encode if x != '-']

huffman_codes = create_huffman_codes(huffman_tree)
print("Huffman tree:", huffman_tree)
print("Huffman codes:", huffman_codes)

encoded_data = huffman_encode(data_to_encode, huffman_codes)
if encoded_data is not None:

    print("Original data:", data_to_encode)
    print("Encoded data:", encoded_data)
    print("Len of encoded data: ", len(encoded_data))
    decoded_data = huffman_decode(encoded_data, huffman_codes)
    print("Decoded data:", decoded_data)

    if decoded_data == data_to_encode:
        print("##### RESULT #####")
        print("Decode PASSED")
    else:
        print("##### RESULT #####")
        print("Decode FAILED")
else:
    print("Encoding failed due to missing Huffman code for a character.")

time_stop = time.ticks_cpu()
time = time_stop - time_start
print("Time of running program:", time)