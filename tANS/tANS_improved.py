import json
import time


################################################################################
# Encoding
################################################################################
def tANS_encode(values, spread_data, x_tmp, L, Input_data, size_of_first_element):
    def last_xtmp(symbol):
        for j in range(L - 1, -1, -1):
            if spread_data[j] == symbol:
                return x_tmp[j]
        return 0

    diff_data = [abs(Input_data[i] - Input_data[i + 1]) for i in range(len(Input_data) - 1)]
    abs_data = [0 if Input_data[i] >= Input_data[i + 1] else 1 for i in range(len(Input_data) - 1)]
    first_element = Input_data[0]

    stream_array = []
    first_element_bin = bin(first_element)[2:]
    num_leading_zeros = size_of_first_element - len(first_element_bin)
    stream_array.extend([0] * num_leading_zeros + [int(e) for e in first_element_bin])

    for x in range(L):
        if diff_data[0] == spread_data[x]:
            first_appearance = values[x]
            break
    tmp = first_appearance

    for i in range(len(diff_data) - 1):
        last_x = last_xtmp(diff_data[i + 1])
        next_symbol = diff_data[i + 1]
        stream_tmp = tmp
        stream_bit_array = []
        stream_array.append(abs_data[i])
        while stream_tmp > last_x:
            stream_bit = stream_tmp & 1
            stream_tmp >>= 1
            stream_bit_array.append(stream_bit)
        stream_array.extend(reversed(stream_bit_array))
        for x in range(L):
            if stream_tmp == x_tmp[x] and next_symbol == spread_data[x]:
                tmp = values[x]

    stream_array.append(abs_data[-1])
    last_element = bin(tmp)[3:]
    stream_array.extend([int(e) for e in last_element])

    return stream_array


################################################################################
# Decoding
################################################################################
def tANS_decode(spread_data, nbBits, newX, L, stream_array, size_of_first_element):
    final_array = []
    first_value = stream_array[:size_of_first_element]
    stream_array = stream_array[size_of_first_element:]
    first_value_num = int("".join(map(str, first_value)), 2)
    final_array.append(first_value_num)

    i = len(bin(2 * L - 1)) - 3
    last_bits = stream_array[-i:]
    stream_array = stream_array[:-i]
    last_bits.insert(0, 1)
    next_num = int("".join(map(str, last_bits)), 2)

    diff_array = [stream_array.pop()]

    decoded_table = []
    while stream_array:
        bit_num = nbBits[next_num - L]
        next_num_from_table = newX[next_num - L]
        shift_array = stream_array[-bit_num:]
        shift_num = int("".join(map(str, shift_array)), 2)
        stream_array = stream_array[:-bit_num]

        sign_value = stream_array.pop()
        diff_array.append(sign_value)

        found_symbol = spread_data[next_num - L]
        decoded_table.append(found_symbol)
        next_num = next_num_from_table + shift_num

    found_symbol = spread_data[next_num - L]
    decoded_table.append(found_symbol)
    final_decode = decoded_table[::-1]
    final_diff = diff_array[::-1]

    for x in range(len(final_diff)):
        if final_diff[x] == 1:
            value = final_array[x] + final_decode[x]
        else:
            value = final_array[x] - final_decode[x]

        final_array.append(value)

    return final_array


################################################################################
# TEST BENCH
################################################################################
#time_start = time.ticks_cpu()
L = 8192
size_of_first_element = 12
Input_data = []

with open('tANS_values_spring.json', 'r') as file:
    values = json.load(file)
with open('tANS_spread_data_spring.json', 'r') as file:
    spread_data = json.load(file)
with open('tANS_x_tmp_spring.json', 'r') as file:
    x_tmp = json.load(file)
with open('tANS_nbBits_spring.json', 'r') as file:
    nbBits = json.load(file)
with open('tANS_newX_spring.json', 'r') as file:
    newX = json.load(file)
with open('alphabet_spring.json', 'r') as file:
    alphabet = json.load(file)
with open("2023_04_09-03.txt", 'r') as file:
    for line in file:
        Input_data.append(int(line.strip()))

Input_data = [x for x in Input_data if x != '-']

encoded_values = tANS_encode(values, spread_data, x_tmp, L, Input_data, size_of_first_element)
print("Encoded value: ", encoded_values)
print("Len of encoded value: ", len(encoded_values))

decoded_values = tANS_decode(spread_data, nbBits, newX, L, encoded_values, size_of_first_element)

print("##### TEST BENCH #####")
print("Input data:")
print(Input_data)
print("Decoded data:")
print(decoded_values)

if decoded_values == Input_data:
    print("##### RESULT #####")
    print("Decode PASSED")
else:
    print("##### RESULT #####")
    print("Decode FAILED")

#time_stop = time.ticks_cpu()
#time = time_stop - time_start
#print("Time of running program:", time)

