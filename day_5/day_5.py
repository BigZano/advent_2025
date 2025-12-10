def parse_allowed_ranges(allowed_ranges: str) -> list[tuple[int, int]]:
    ranges = []
    for line in allowed_ranges.strip().splitlines():
        start, end = tuple(map(int, line.split('-')))
        ranges.append((start, end))
    return ranges

def parse_available_ingredients(available_ingredients: str) -> list[int]:
    return [int(line) for line in available_ingredients.strip().splitlines()]

# Part 1: sum the bad stuff

# def ingredients_sum(allowed_ranges: list[tuple[int, int]], available_ingredients: list[int]) -> list[int]:
#     ingredients_sum = 0
#     for ingredient in available_ingredients:
#         for start, end in allowed_ranges:
#             if start <= ingredient <= end:
#                 ingredients_sum += 1
#                 break
#     return ingredients_sum

# part 1
# if __name__ == "__main__":
#     allowed_ranges_list = parse_allowed_ranges(allowed_ranges)
#     available_ingredients_list = parse_available_ingredients(available_ingredients)
#     result = ingredients_sum(allowed_ranges_list, available_ingredients_list)
#     print(f"Number of available ingredients within allowed ranges: {result}")


# part 2: sum the good stuff

def count_fresh_ids_from_ranges(allowed_ranges: list[tuple[int, int]]) -> int:
    if not allowed_ranges:
        return 0
    ranges = sorted(allowed_ranges)
    total = 0
    current_start, current_end = ranges[0]
    for s, e in ranges[1:]:
        if s <= current_end + 1:
            current_end = max(current_end, e)
        else:
            total += current_end - current_start + 1
            current_start, current_end = s, e
    total += current_end - current_start + 1
    return total

if __name__ == "__main__":
    allowed_ranges_list = parse_allowed_ranges(allowed_ranges)
    result = count_fresh_ids_from_ranges(allowed_ranges_list)
    print(f"Sum of available ingredients within allowed ranges: {result}")