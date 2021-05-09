#IMPLEMENTATION OF BLOSSOM ALGORITHM
def solution(banana_list):
    #note to self might not need banana_dict
    def smallest_odd_divisor(total):
        while total % 2 == 0:
            total /= 2
        return int(total)

    def will_loop(num1, num2):
        total = num1 + num2
        div = smallest_odd_divisor(total)
        if num1 % div == 0:
            return False
        else:
            return True


    def indexify(banana_list):
        banana_dict = {}
        for ii in range(len(banana_list)):
            banana_dict[ii] = banana_list[ii]
        return banana_dict

    #if there is a cycle, then it returns True, cycle
    #if there is no cycle, it returns False, augmenting_path
    def is_cycle(path1, path2, end):
        path_set = set(path2)
        #if there is an intersect then we know that
        for node in path1:
            if node in path_set:
                path1.append(end)
                index_1 = path1.index(node)
                path2.reverse()
                index_2 = path2.index(node)
                #the cycle doesn't contain the final node (the starting node twice)
                cycle = path1[index_1:] + path2[:index_2]
                return True, cycle
        path1.append(end)
        path2.reverse()
        return False, path1 + path2

# matching consists of {node1: node2, node2:node1} where the key-value pair is determined by the matching
    def find_aug_or_blossoms(banana_dict, matching, open_vertices):
        layers = dict()
        #paths_before is the total path before reaching that vertex in the layer analysis
        paths_before = {}
        available_vertices = set()
        for banana in banana_dict:
            available_vertices.add(banana)
        #tells the vertices in each layer
        layers_dict = dict()
        layers_dict[0] = []
        for elem in open_vertices:
            path = []
            layers[elem] = 0
            paths_before[elem] = path
            layers_dict[0] = layers_dict[0] + [elem]
        ii = 0
        continue_loop = True
        #at ii we make layer ii+1
        while continue_loop:
            continue_loop = False
            layers_dict[ii+1] = []
            if ii % 2 == 0:
                for elem in layers_dict[ii]:
                    for banana in banana_dict:
                        if (elem != banana) and (not(elem in matching) or banana != matching[elem]) and will_loop(banana_dict[banana], banana_dict[elem]):
                            #if we add a new layer, continue_loop automatically becomes True
                            if (not (banana in layers)):
                                layers[banana] = ii+1
                                path = paths_before[elem] + [elem]
                                paths_before[banana] = path
                                layers_dict[ii+1] = layers_dict[ii+1] + [banana]
                                continue_loop = True
                            if (banana in layers) and (layers[banana] == ii):
                                cycle, path = is_cycle(paths_before[banana], paths_before[elem] + [elem], banana)
                                if cycle:
                                    for jj in range(0, len(path)-1, 2):
                                        matching[path[jj+1]] = path[jj+2]
                                        matching[path[jj+2]] = path[jj+1]
                                        banana_dict.pop(path[jj+1], None)
                                        banana_dict.pop(path[jj+2], None)
                                        if path[jj + 1] in open_vertices:
                                            open_vertices.remove(path[jj + 1])
                                        if path[jj + 2] in open_vertices:
                                            open_vertices.remove(path[jj + 2])
                                    return True
                                else:
                                    for jj in range(0, len(path), 2):
                                        matching[path[jj]] = path[jj+1]
                                        matching[path[jj+1]] = path[jj]
                                        if path[jj] in open_vertices:
                                            open_vertices.remove(path[jj])
                                        if path[jj + 1] in open_vertices:
                                            open_vertices.remove(path[jj + 1])
                                    return True
            if ii % 2 == 1:
                for elem in layers_dict[ii]:
                    if elem in matching:
                        banana = matching[elem]
                        if not(banana in layers):
                            layers[banana] = ii+1
                            path = paths_before[elem] + [elem]
                            paths_before[banana] = path
                            layers_dict[ii+1] = layers_dict[ii+1] + [banana]
                            available_vertices.remove(banana)
                            continue_loop = True
                        if (banana in layers) and (layers[banana] == ii):
                            cycle, path = is_cycle(paths_before[banana], paths_before[elem] + [elem], banana)
                            if cycle:
                                for jj in range(0, len(path) - 1, 2):
                                    matching[path[jj + 1]] = path[jj + 2]
                                    matching[path[jj + 2]] = path[jj + 1]
                                    banana_dict.pop(path[jj + 1], None)
                                    banana_dict.pop(path[jj + 2], None)
                                    if path[jj+1] in open_vertices:
                                        open_vertices.remove(path[jj + 1])
                                    if path[jj+2] in open_vertices:
                                        open_vertices.remove(path[jj + 2])
                                return True
                            else:
                                for jj in range(0, len(path), 2):
                                    matching[path[jj]] = path[jj + 1]
                                    matching[path[jj + 1]] = path[jj]
                                    if path[jj] in open_vertices:
                                        open_vertices.remove(path[jj])
                                    if path[jj+1] in open_vertices:
                                        open_vertices.remove(path[jj + 1])
                                return True
            ii += 1
        return False


    def match(banana_list):
        banana_dict = indexify(banana_list)
        matching = {}
        open_vertices = set()
        for banana in banana_dict:
            open_vertices.add(banana)
        while find_aug_or_blossoms(banana_dict, matching, open_vertices):
            pass
        return len(banana_list) - len(matching)

    return match(banana_list)


print(solution([1, 7, 3, 21, 13, 19]))


