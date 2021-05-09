def solution(x):
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    newSol = ""
    for letter in x:
        if letter in alphabets:
            newSol += alphabets[25 - alphabets.index(letter)]
        else:
            newSol += letter
    return newSol



