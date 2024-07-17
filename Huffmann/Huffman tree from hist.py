import heapq
import json
import csv


################################################################################
# Huffman tree creation
################################################################################
def create_huffman_tree(freq_dict):
    heap = [[freq, [char, '']] for char, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


################################################################################
# Merge alfabet and counts into one dictionary
################################################################################
def merge_arrays_to_dict(keys, values):
    # Check if both lists have the same length
    if len(keys) != len(values):
        raise ValueError("Both tables have to have the same length.")

    # Merge lists into one dictionary
    merged_dict = {keys[i]: values[i] for i in range(len(keys))}

    return merged_dict


################################################################################
# Histogram data update
################################################################################
def read_csv_and_create_arrays(file_path):
    lower_ranges = []
    counts = []

    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            lower_range = int(row['Dolny zakres'])
            count = int(row['Liczebność'])

            if count != 0:
                lower_ranges.append(lower_range)
                counts.append(count)

    return lower_ranges, counts

################################################################################
# Main operations
################################################################################

file_path = "C:/Users/kiraw/Documents/MGR/Dane/PM10/zima_2017-2021_hist.csv"
alphabet, counts = read_csv_and_create_arrays(file_path)
print(alphabet)
print(counts)

freq_dict = merge_arrays_to_dict(alphabet, counts)
print(freq_dict)
huffman_tree = create_huffman_tree(freq_dict)
print(huffman_tree)

with open('huffman_tree_winter.json', 'w') as outfile:
    json.dump(huffman_tree, outfile)
    print("PASSED")




