def solution(h, q):
    def power_2(num):
        if num == 0:
            return False
        else:
            power = 1
            while power < num:
                power *= 2
            if power == num:
                return True
            else:
                return False
    sol = []
    for elem in q:
        if elem >= 2**h - 1:
            sol.append(-1)
            continue
        else:
            addition = 0
            index = h - 1
            while not(power_2(elem + 1)) and not(power_2(elem + 2)):
                moving = 2**index - 1
                if elem > moving:
                    elem -= moving
                    addition += moving
                index -=1
            if power_2(elem + 1):
                sol.append(addition + 2*elem + 1)
            if power_2(elem + 2):
                sol.append(addition + elem + 1)
    return sol


