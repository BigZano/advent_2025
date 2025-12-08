# part 1
# total_joltage = 0
# 
# for bank in list_of_banks:  # loop for each bank, strip spaces, commas and quotes, confirm digits only
#     banks = bank.strip().rstrip(',')
#     digits = [int(ch) for ch in banks if ch.isdigit()]
# 
#     best = 0               # find best two-digit combination, walk left to right
#     max_left = -1
#     for d in digits:
#         if max_left >= 0:
#             candidate = max_left * 10 + d
#             if candidate > best:
#                 best = candidate
#         if d > max_left:      # Set max_left to largest digit seen so far
#             max_left = d
#     
#     total_joltage += best         # add best for this bank to total_joltage
# 
# print(total_joltage)



# part 2

total_joltage = 0
k = 12 # digits to turn per bank

for bank in list_of_banks:
    banks = bank.strip().rstrip(',')
    digits = [int(ch) for ch in banks if ch.isdigit()]

    # make stack and pop items for largest 12 digits
    needed = len(digits) - k
    stack = []
    for d in digits:
        while stack and needed > 0 and stack[-1] < d:
            stack.pop()
            needed -= 1
        stack.append(d)

    selected = stack[:k] # take first k items from stack
    best = 0
    for d in selected:
        best = best * 10 + d
    total_joltage += best
print(total_joltage)