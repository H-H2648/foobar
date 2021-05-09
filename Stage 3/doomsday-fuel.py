def solution(m):
    def checkZero(row):
        for ii in row:
            if ii != 0:
                return False
        return True

    def gcd(num1, num2):
        if num1 == 0 and num2 == 0:
            return 1
        if num1 == 0:
            return num2
        if num2 == 0:
            return num1
        if num1 > num2:
            num1, num2 = num2, num1
        while num2 % num1 != 0:
            num1, num2 = num2 % num1, num1
        return num1

    def lcm(num1, num2):
        return int(num1*num2/gcd(num1, num2))

    def fractionize(num, den):
        if num == 0:
            return (0, 1)
        else:
            div = gcd(num, den)
            return (int(num/div), int(den/div))


    def fractionAdd(fraction1, fraction2):
        num1, den1 = fraction1
        num2, den2 = fraction2
        if num1 == 0:
            return (num2, den2)
        elif num2 == 0:
            return (num1, den1)
        den = lcm(den1, den2)
        num = num1*den/den1 + num2*den/den2
        return fractionize(num, den)

    def fractionMult(fraction1, fraction2):
        num1, den1 = fraction1
        num2, den2 = fraction2
        den = den1*den2
        num = num1*num2
        return fractionize(num, den)

    def fractionRec(fraction):
        num, den = fraction
        return(den, num)

    def clean(matrix):
        nonZeroIndices= []
        zeroIndices = []
        newMatrix = []
        for ii in range(len(matrix)):
            if checkZero(matrix[ii]):
                newRow = [0]*len(matrix)
                newRow[ii] = 1
                newMatrix.append(newRow)
                zeroIndices.append(ii)
            else:
                nonZeroIndices.append(ii)
                newMatrix.append(matrix[ii])
        matrix = newMatrix
        for ii in range(len(matrix)):
            sum = 0
            for jj in range(len(matrix[ii])):
                sum += matrix[ii][jj]
            for jj in range(len(matrix[ii])):
                matrix[ii][jj] = fractionize(matrix[ii][jj], sum)
        return matrix, zeroIndices, nonZeroIndices

    def convert(fractions):
        if len(fractions) == 1:
            return ([fractions[0][0], fractions[0][1]])
        sol = []
        TRUE_LCM = 1
        for frac in fractions:
            den = frac[1]
            TRUE_LCM = lcm(den, TRUE_LCM)
        for frac in fractions:
            sol.append(frac[0]*int(TRUE_LCM/frac[1]))
        TRUE_GCD = gcd(sol[0], sol[1])
        for elem in sol[2:]:
            TRUE_GCD = gcd(TRUE_GCD, elem)
        for ii in range(len(sol)):
            sol[ii] = int(sol[ii]/TRUE_GCD)
        sol.append(TRUE_LCM * TRUE_GCD)
        return sol

    def upperTriangulize(coefficients, answer):
        index = len(answer) - 1
        while index > 0:
            for ii in range(index):
                #no need to worry about coefficients[index][index] = 0 since by the nature of the problem it will always
                #be nonzero
                answer[ii] = fractionAdd(answer[ii],
                                         fractionMult((-1, 1), fractionMult(answer[index], fractionMult(
                                             coefficients[ii][index],
                                             fractionRec(coefficients[index][index])
                                         ))
                                                      ))
                for jj in range(len(coefficients[ii])-1):
                    coefficients[ii][jj] = fractionAdd(coefficients[ii][jj],
                                                      fractionMult((-1, 1),  fractionMult(
                                                          coefficients[index][jj], fractionMult(coefficients[ii][index],
                                                                                fractionRec(coefficients[index][index])))))
            index -=1
            coefficients = coefficients[:-1]
            for ii in range(len(coefficients)):
                coefficients[ii] = coefficients[ii][:-1]
            answer = answer[:-1]
        finalCoefficient = coefficients[0][0]
        return fractionMult(answer[0], fractionRec(finalCoefficient))

    if m == [[0]]:
        return [1, 1]
    if len(m[0]) > 1 and checkZero(m[0][1:]):
        m, zeroIndices, nonZeroIndices = clean(m)
        print(zeroIndices)
        answer = [0]*len(zeroIndices)
        answer.append(1)
        return answer
    m, zeroIndices, nonZeroIndices = clean(m)
    #note this is not solved for nonZeroIndices
    general_matrix = []
    for ii in range(len(nonZeroIndices)):
        general_matrix.append([])
        for jj in range(len(nonZeroIndices)):
            if jj == ii:
                general_matrix[ii].append(fractionAdd(fractionize(1, 1),  fractionMult(fractionize(-1, 1), m[nonZeroIndices[ii]][nonZeroIndices[jj]])))
            else:
                general_matrix[ii].append(fractionMult(fractionize(-1, 1), m[nonZeroIndices[ii]][nonZeroIndices[jj]]))
    FINAL_ANSWER = []
    for jj in zeroIndices:
        answer = []
        for ii in range(len(nonZeroIndices)):
            value = (0, 0)
            value = fractionAdd(value, m[nonZeroIndices[ii]][jj])
            answer.append(value)
        coefficientsCopy = []
        for ii in range(len(general_matrix)):
            coefficientsCopy.append([])
            for kk in range(len(general_matrix[0])):
                coefficientsCopy[ii].append(general_matrix[ii][kk])
        answerCopy = []
        for ii in range(len(answer)):
            answerCopy.append(answer[ii])
        FINAL_ANSWER.append(upperTriangulize(coefficientsCopy, answerCopy))
    return convert(FINAL_ANSWER)






'''
trial=[
  [1,1,1,3,4,1,1,2],
  [4,1,3,3,2,3,0,4],
  [0,0,0,1,0,0,8,9],
  [0,0,3,0,0,0,0,0],
  [0,0,0,0,0,0,0,0], #terminal
  [0,0,0,0,0,0,0,0],  # terminal
  [0,0,0,0,0,0,0,0],  # terminal
  [0,0,0,0,0,0,0,0],  # terminal
]
'''


#print(trial)
#print(solution(trial))
#print(solution([[0, 2, 1, 0, 0], [0, 0, 0, 3, 4], [0, 0, 0, 0, 0], [0, 0, 0, 0,0], [0, 0, 0, 0, 0]]))
#print(solution([[0, 1, 0, 0, 0, 1], [4, 0, 0, 3, 2, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))



















