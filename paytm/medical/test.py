kewords_dict = {
    'levis jeans': 'brand type',
    'jeans': 'type',
    'pepe jeans': 'brand type',
    'shirt': 'type',
    'united color of benetton': 'brand',
    'united color of benetton shirt': 'brand type',
    't shirt': 'type',
    'levis': 'brand',
    "cotton shirt": 'tag',
    'clothes': 'tag'
}

input = 'levis jeans for men clothes'

input_1 = 'jeans for men clothes levis'

# output = {
#     'levis': 'brand',
#     'jeans': 'type',
#     'levis jeans': 'brand type',
#     'clothes': 'tag'
# }

import itertools


def get_c_items(c, list):
    result = []
    final_result = []
    for items in itertools.combinations(list, c):
        s = ""
        for item in items:
            s = s + item + " "
        s.strip()
        s.strip()
        result.append(s)
    for r in result:
        final_result.append(r.strip())

    return final_result


list1 = input.split()
size = len(list1)
output = {}
for item in list1:
    c = 1
    while c < size - 1:
        list3 = get_c_items(c, list1)
        for item2 in list3:
            if item != item2:  # and not already_visited(item + item2):
                output_item = kewords_dict.get(item + " " + item2)
                if output_item is not None:
                    output[item + " " + item2] = output_item

        c += 1
    # Run for single item
    output_item = kewords_dict.get(item)
    if output_item is not None:
        output[item] = output_item
print(output)


