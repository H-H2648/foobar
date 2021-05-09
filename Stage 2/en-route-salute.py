def solution(s):
    #peopleDict will be a dictionary recording the number of people walking towards them behind and in front
    #key is the index
    #the value is (behind, front) pair (counts the number of ">" behind and number of "<" in front)
    peopleDict = {}
    #behind is by default 0 as we index at 0 (no one is behind us)
    behind = 0
    front = 0
    for ii in range(1, len(s)):
        if s[ii] == '<':
            front +=1
    peopleDict[0] = (behind, front)
    for ii in range(1, len(s)):
        if s[ii - 1] == ">":
            behind +=1
        if s[ii] == "<":
            front -=1
        peopleDict[ii] = (behind, front)
    saluteCount = 0
    for ii in range(len(s)):
        if s[ii] == ">":
            saluteCount += peopleDict[ii][1]
        if s[ii] == "<":
            saluteCount += peopleDict[ii][0]
    return saluteCount

