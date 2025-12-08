import itertools
import re


def repeating_pattern(s):
    n = len(s)
    for L in range(1, n // 2 + 1):
        if n % L == 0:
            sub = s[:L]
            if sub * (n // L) == s:
                return True
    return False



total_invalid_sum = 0

for start, end in list_of_ranges:
    for id_num in range(start, end + 1):
            s = str(id_num)
            if repeating_pattern(s):
                  total_invalid_sum += id_num




print(total_invalid_sum)