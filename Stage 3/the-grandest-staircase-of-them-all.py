def solution(n):
    solution_array = []
    for ii in range(n):
        row = []
        for jj in range(n):
            row.append(0)
        solution_array.append(row)
    #solution_array[ii][jj] = numbers way to write ii + 1 as sum of distinct numbers greater than or equal to jj + 1 (jj + 1 because index at 0)
    for ii in range(n):
        for jj in range(n-1, -1, -1):
            if jj == ii:
                solution_array[ii][jj] = 1
            if jj < ii:
                solution_array[ii][jj] = solution_array[ii][jj+1] + solution_array[ii - jj - 1][jj+1]
    return solution_array[n-1][0] - 1





