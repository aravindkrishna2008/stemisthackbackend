import random

value = random.randint(1, 400)
arr_additions_losses = []

def get_stock_value(value, arr_additions_losses, r):
    if value <= 15:
        a = random.randint(0, 5+r)
    if len(arr_additions_losses) > random.randint(10, 20):
        arr_additions_losses = []
        value += random.randint(-15-r, 15+r)
    else:
        a = random.randint(-5-r, 5+r)
        value += a
        arr_additions_losses.append(a)

    return value, arr_additions_losses

total_values = [(0, value)]

def adjust_randomness(original_list, randomness_param):
    new_list = []
    for tpl in original_list:
        index, value = tpl
        deviation = randomness_param * 5  # Adjust the scale of randomness using a parameter
        new_value = int(round(random.gauss(value, deviation)))
        new_list.append((index, new_value))
    return new_list


def get_entire_stock_history(a, r):
    global value
    global arr_additions_losses
    for i in range(a):
        value, arr_additions_losses = get_stock_value(value, arr_additions_losses,r)
        total_values.append((i+1, value))

    k = total_values.copy()
    total_values.clear()
    value = random.randint(1, 400)
    arr_additions_losses = []
    return k