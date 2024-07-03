import csv
import json

################################################################################
# tANS decode table creation
################################################################################
def create_tANS_table():
    symbol_data = []
    for i in range(len(alphabet)):
        symbol_data.extend([alphabet[i]] * Ocr[i])

    # Spread table, spread = 3
    spread_data = [None] * len(symbol_data)

    for i, symbol in enumerate(symbol_data):
        spread_data[(spread * i) % len(symbol_data)] = symbol

    # Enumerate Appearances, build decoding table
    values = list(range(L, 2*L))

    x_tmp = [0] * len(spread_data)
    i = 0
    for a in alphabet:
        x = Ocr[i]
        for j in range(len(spread_data)):
            if spread_data[j] == a:
                x_tmp[j] = x
                x = x + 1
        i = i + 1

    nbBits = [0] * len(spread_data)
    newX = [0] * len(spread_data)

    for i in range(L):
        shift = 0
        while newX[i] < L:
            newX[i] = x_tmp[i] << shift
            nbBits[i] = shift
            shift = shift + 1

    # Check if newX are within the range [L, 2*L - 1]
    try:
        for val in newX:
            if val < L or val > 2*L-1 :
                raise ValueError(f'ERROR Value of newX {val} is out of range')
    except ValueError as error:
        print(error)
        exit(1)

    # Create final tANS decode table
    result_with_values = list(zip(values, spread_data, x_tmp, nbBits, newX))

    print("tANS decode table:")
    for i in range(len(result_with_values[0])):
        for pair in result_with_values:
            print(f'{pair[i]:<2}', end='  ')
        print()
    print("-"*100)

    return values, spread_data, x_tmp, nbBits, newX

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

def count_total_values(counts):
    return sum(counts)


def calculate_approximate_counts(counts, L, total_count):
    approximate_counts = []
    adjusted_counts = []

    # Step 1: Calculate the initial approximate counts as floats
    initial_counts = [(count * L) / total_count for count in counts]

    # Step 2: Round and ensure count of 1 remains 1
    for count, initial_count in zip(counts, initial_counts):
        if count == 1:
            adjusted_counts.append(1)
        else:
            adjusted_counts.append(int(round(initial_count)))

    # Step 3: Adjust the sum of approximate counts to be exactly L
    current_sum = sum(adjusted_counts)
    difference = L - current_sum

    print("#####", adjusted_counts)
    # Adjust counts to ensure the sum is exactly L
    for i in range(abs(difference)):
        if difference > 0:
            # Increment first value that is not already 1
            for j in range(len(adjusted_counts)):
                if adjusted_counts[j] != 1:
                    adjusted_counts[j] += 1
                    break
        elif difference < 0:
            # Decrement first value greater than 1
            for j in range(len(adjusted_counts)):
                if adjusted_counts[j] > 1:
                    adjusted_counts[j] -= 1
                    break

    return adjusted_counts


#################################################################
spread = 3
L = 8192

file_path = "C:/Users/kiraw/Documents/MGR/Dane/PM10/wiosna_2017-2021_hist.csv"
alphabet, counts = read_csv_and_create_arrays(file_path)

total_count = count_total_values(counts)
Ocr = calculate_approximate_counts(counts, L, total_count)

values, spread_data, x_tmp, nbBits, newX = create_tANS_table()

# Write tANS table to the separate files:
with open('tANS_values_spring.json', 'w') as file:
    json.dump(values, file)
with open('tANS_spread_data_spring.json', 'w') as file:
    json.dump(spread_data, file)
with open('tANS_x_tmp_spring.json', 'w') as file:
    json.dump(x_tmp, file)
with open('tANS_nbBits_spring.json', 'w') as file:
    json.dump(nbBits, file)
with open('tANS_newX_spring.json', 'w') as file:
    json.dump(newX, file)

# Write alphabet table to the file:
with open('alphabet_spring.json', 'w') as file:
    json.dump(alphabet, file)

total_count = count_total_values(Ocr)
print("Total count:", total_count)
