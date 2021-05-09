import math
#apparently reflections are commutative perpendicularly
def solution(dimensions, your_position, trainer_position, distance):

    def distance_squared(your_position, trainer_position):
        return (trainer_position[1] - your_position[1])**2 + (trainer_position[0]- your_position[0])**2

    def direction(your_position, trainer_position):
        x = trainer_position[0] - your_position[0]
        y = trainer_position[1] - your_position[1]
        norm = math.sqrt(x*x + y*y)
        return (round(x/norm, 8), round(y/norm, 8))



    def reflect(axis, bound, dimension, your_position, trainer_position):
        new_trainer_position = [None, None]
        new_your_position = [None, None]
        if axis == "Left":
            new_trainer_position[0] = bound - (trainer_position[0] - bound)
            new_trainer_position[1] = trainer_position[1]
            new_your_position[0] = bound- (your_position[0] - bound)
            new_your_position[1] = your_position[1]
            return (bound - dimension[0], new_your_position, new_trainer_position)
        if axis == "Down":
            new_trainer_position[0] = trainer_position[0]
            new_trainer_position[1] = bound - (trainer_position[1] - bound)
            new_your_position[0] = your_position[0]
            new_your_position[1] = bound - (your_position[1] - bound)
            return (bound - dimension[1], new_your_position, new_trainer_position)
        if axis == "Right":
            new_trainer_position[0] = bound + (bound - trainer_position[0])
            new_trainer_position[1] = trainer_position[1]
            new_your_position[0] = bound + (bound - your_position[0])
            new_your_position[1] = your_position[1]
            return (bound + dimension[0], new_your_position, new_trainer_position)
        if axis == "Up":
            new_trainer_position[0] = trainer_position[0]
            new_trainer_position[1] = bound + (bound - trainer_position[1])
            new_your_position[0] = your_position[0]
            new_your_position[1] = bound + (bound - your_position[1])
            return (bound + dimension[1], new_your_position, new_trainer_position)



    def destination(dimensions, trainer_position, your_position, reflections):
        trainer_position_copy = []
        your_position_copy = []
        for pos in trainer_position:
            trainer_position_copy.append(pos)
        for pos in your_position:
            your_position_copy.append(pos)
        if 'Left' in reflections:
            side_bound = 0
        elif "Right" in reflections:
            side_bound = dimensions[0]
        if 'Up' in reflections:
            height_bound = dimensions[1]
        elif "Down" in reflections:
            height_bound = 0
        for axis in reflections:
            if axis in ['Left', 'Right']:
                side_bound, your_position_copy, trainer_position_copy = reflect(axis, side_bound, dimensions, your_position_copy, trainer_position_copy)
            if axis in ['Up', 'Down']:
                height_bound, your_position_copy, trainer_position_copy = reflect(axis, height_bound, dimensions, your_position_copy, trainer_position_copy)
        return trainer_position_copy, your_position_copy

    def update(hit_lst, dimensions, trainer_position, your_position, reflections):
        trainer_hit, you_hit = destination(dimensions, trainer_position, your_position, reflections)
        slope_trainer, slope_you, trainer_norm2, you_norm2 = direction(your_position, trainer_hit), direction(your_position, you_hit), distance_squared(your_position, trainer_hit), distance_squared(your_position, you_hit)
        hit_lst.append((slope_trainer[0], slope_trainer[1], 0, trainer_norm2))
        hit_lst.append((slope_you[0], slope_you[1], 1, you_norm2))


    def solution_helper(hit_lst,  dimensions, your_position, trainer_position, reflection_type, max_length_x, max_length_y):
        if len(reflection_type) == 1:
            reflections = []
            if reflection_type[0] in ["Left", "Right"]:
               for ii in range(1, max_length_x):
                    reflections.append(reflection_type[0])
                    update(hit_lst, dimensions, trainer_position, your_position, reflections)
            else:
                for ii in range(1, max_length_y):
                    reflections.append(reflection_type[0])
                    update(hit_lst, dimensions, trainer_position, your_position, reflections)
        else:
            for ii in range(1, max_length_x):
                for jj in range(1, max_length_y):
                    reflections = []
                    for _ in range(ii):
                        reflections.append(reflection_type[0])
                    for _ in range(jj):
                        reflections.append(reflection_type[1])
                    update(hit_lst, dimensions, trainer_position, your_position, reflections)

    hit_lst = []
    max_distance2 = distance**2


    types = [['Left'], ['Right'], ['Up'], ['Down'], ['Left', 'Up'], ['Left', 'Down'], ['Right', 'Down'], ['Right', 'Up']]

    max_length_x = int(math.ceil((float(your_position[0] + distance))/float(dimensions[0]))) + 1
    max_length_y = int(math.ceil((float(your_position[1] + distance))/float(dimensions[1]))) + 1
    if distance_squared(your_position, trainer_position) > max_distance2:
        return 0
    else:
        direct = direction(your_position, trainer_position)
        hit_lst.append((direct[0], direct[1], 0, distance_squared(your_position, trainer_position)))
    for reflect_type in types:
        solution_helper(hit_lst, dimensions, your_position, trainer_position, reflect_type, max_length_x, max_length_y)
    true_hit = {}
    for history in hit_lst:
        if (history[0], history[1]) in true_hit:
            if true_hit[(history[0], history[1])][1] > history[3]:
                true_hit[(history[0], history[1])] = (history[2], history[3])
        else:
            if history[3] > max_distance2:
                continue
            else:
                true_hit[(history[0], history[1])] = (history[2], history[3])
    count = 0
    for history in true_hit:
        if true_hit[history][0] == 0:
            count +=1
    return count

