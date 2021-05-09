import copy

def solution(g):

    #the last columns
    initial_True = [
        [[True, False], [False, False]],
        [[False, True], [False, False]],
        [[False, False], [True, False]],
        [[False, False], [False, True]]
    ]

    initial_False = [
        [[False, False], [False, False]],
        [[True, True], [False, False]],
        [[True, False], [True, False]],
        [[True, False], [False, True]],
        [[False, True], [True, False]],
        [[False, True], [False, True]],
        [[False, False], [True, True]],
        [[False, True], [True, True]],
        [[True, True], [True, False]],
        [[True, True], [False, True]],
        [[True, False], [True, True]],
        [[True, True], [True, True]]
    ]

    double_dict_True = {
        (True, True): [],
        (True, False): [(False, False)],
        (False, True): [(False, False)],
        (False, False): [(True, False), (False, True)]
    }

    double_dict_False = {
        (True, True): [(True, True), (True, False), (False, True), (False, False)],
        (True, False): [(True, True), (True, False), (False, True)],
        (False, True): [(True, True), (True, False), (False, True)],
        (False, False): [(True, True), (False, False)]
    }

    #based on key (bottom_left, top_left, top_right)

    triple_dict_True = {
        (True, True, True): [],
        (True, True, False): [],
        (True, False, True): [],
        (True, False, False): [False],
        (False, True, True): [],
        (False, True, False): [False],
        (False, False, True): [False],
        (False, False, False): [True]
    }

    triple_dict_False = {
        (True, True, True): [True, False],
        (True, True, False): [True, False],
        (True, False, True): [True, False],
        (True, False, False): [True],
        (False, True, True): [True, False],
        (False, True, False): [True],
        (False, False, True): [True],
        (False, False, False): [False]
    }

    def take_from(value, possible_columns):
        total_columns = []
        for columns in possible_columns:
            key = (columns[-1][0], columns[-1][1])
            if value:
                super_dict = double_dict_True
            else:
                super_dict = double_dict_False
            values = super_dict[key]
            length = len(values)
            for jj in range(length):
                elem0, elem1 = values[jj]
                if jj < length - 1:
                    columns_copy = copy.deepcopy(columns)
                    columns_copy.append([elem0, elem1])
                    total_columns.append(columns_copy)
                else:
                    columns.append([elem0, elem1])
                    total_columns.append(columns)
        return total_columns




    def first_update_with_column(value, column, count):
        new_columns_dict = {}
        key = (column[0], column[1])
        if value:
            super_dict = double_dict_True
        else:
            super_dict = double_dict_False
        values = super_dict[key]
        for elem0, elem1 in values:
            if (elem0, elem1) in new_columns_dict:
                new_columns_dict[(elem0, elem1)] = new_columns_dict[(elem0, elem1)] + count
            else:
                new_columns_dict[(elem0, elem1)] = count
        return new_columns_dict

    def take_from_with_columns(value, column, temp_new_dict, ii):
        new_dict = {}
        for possible_col in temp_new_dict:
            key = (column[ii+1], column[ii], possible_col[ii])
            if value:
                super_dict = triple_dict_True
            else:
                super_dict = triple_dict_False
            values = super_dict[key]
            count = temp_new_dict[possible_col]
            for val in values:
                possible_col_copy = copy.deepcopy(possible_col)
                possible_col_copy = list(possible_col_copy)
                possible_col_copy.append(val)
                possible_col_copy = tuple(possible_col_copy)
                if possible_col_copy in new_dict:
                    new_dict[possible_col_copy] = new_dict[possible_col_copy] + count
                else:
                    new_dict[possible_col_copy] = count
        return new_dict


    def update(columns, index, nebula):
        for ii in range(1, len(nebula)):
            columns = take_from(nebula[ii][index], columns)
        return columns

    def update_with_column(column, temp_new_dict, index, nebula):
        for ii in range(1, len(nebula)):
            temp_new_dict = take_from_with_columns(nebula[ii][index], column, temp_new_dict, ii)
        return temp_new_dict


    def add_column(columns_dict, nebula, index):
        #so we start with the 0 column for index = 0
        if index == 0:
            if nebula[0][0]:
                possible_columns = initial_True
            else:
                possible_columns = initial_False
            possible_columns = update(possible_columns, index, nebula)
            for columns in possible_columns:
                final_column = []
                for row in columns:
                    final_column.append(row[-1])
                final_column_key = tuple(final_column)
                if final_column_key in columns_dict:
                    columns_dict[final_column_key] = columns_dict[final_column_key] + 1
                else:
                    columns_dict[final_column_key] = 1
            return columns_dict
        else:
            new_columns_dict = {}
            for column in columns_dict:
                count = columns_dict[column]
                temp_new_dict = first_update_with_column(nebula[0][index], column, count)
                temp_new_dict = update_with_column(column, temp_new_dict, index, nebula)
                for key in temp_new_dict:
                    if key in new_columns_dict:
                        new_columns_dict[key] = new_columns_dict[key] + temp_new_dict[key]
                    else:
                        new_columns_dict[key] = temp_new_dict[key]
        return new_columns_dict



    columns_dict = {}
    for index in range(len(g[0])):
        columns_dict = add_column(columns_dict, g, index)
    total = 0
    for key in columns_dict:
        total += columns_dict[key]
    return total

#print(solution([[True, True], [True, True]]))
#print(solution([[True, False, True], [False, True, False], [True, False, True]]))
#print(solution([[True, False, True, False, False, True, True, True], [True, False, True, False, False, False, True, False], [True, True, True, False, False, False, True, False], [True, False, True, False, False, False, True, False], [True, False, True, False, False, True, True, True]]))
#print(solution([[True, True, False, True, False, True, False, True, True, False], [True, True, False, False, False, False, True, True, True, False], [True, True, False, False, False, False, False, False, False, True], [False, True, False, False, False, False, True, True, False, False]]))

