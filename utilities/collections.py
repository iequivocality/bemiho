def split_list(_list, list_size):
    separate_list = []
    length = len(_list)
    for index_start in range(0, length, list_size):
        index_end = index_start + list_size
        if index_start + list_size >= length:
            separate_list.append(_list[index_start:length])
        else:
            separate_list.append(_list[index_start:index_end])
    return separate_list

def split_list_for_column_output(_list, col_num):
    length = len(_list)
    split_array = []
    max_count = length // col_num if length % col_num == 0 else ( length // col_num ) + 1
    for value in enumerate(_list):
        if value[0] <= max_count:
            row = []
            rowIndex = value[0]
            while(rowIndex < length):
                row.append(_list[rowIndex])
                rowIndex = rowIndex + max_count
            split_array.append(row)
        else:
            break
    return split_array

def print_matrix(matrix, string_value = lambda val : val):
    col_width = max(len(string_value(word)) for row in matrix for word in row) + 8  # padding
    for row in matrix:
        # for word in row:
        #     justified = string_value(word).ljust(col_width,'_')
        #     print(justified, col_width, len(string_value(word)))

        print(f'    {"".join(string_value(word).ljust(col_width) for word in row)}')