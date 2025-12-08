"""
Repair manifold for challenge. input is provided in day_7_input.txt.

Analyze input doc and analyze how many times beam is split. 

S = start
. = default char
^ = splitter

when contacting a spliter, beam splits into immediate left and right of splitter exclusive. if a beam falls between two splitters, it is only the one beam.
"""

from typing import List

def main(path: str = "day_7_input.txt") -> int:
    with open(path, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    height = len(lines)
    width = max(len(l) for l in lines)
    grid = [list(l.ljust(width)) for l in lines]

    # Find the start column in the first row
    try:
        start_col = grid[0].index('S')
    except ValueError:
        raise ValueError("No start position 'S' found in the top row.")

    active_beams = {start_col}
    split_count = 0

    for row in range(1, height):
        next_beams = set()
        for col in active_beams:
            cell = grid[row][col]
            if cell == '.':
                next_beams.add(col)
            elif cell == '^':
                # Split left and right, if within bounds
                if col - 1 >= 0:
                    next_beams.add(col - 1)
                if col + 1 < width:
                    next_beams.add(col + 1)
                split_count += 1
            # If cell is ' ', beam is lost (do nothing)
        active_beams = next_beams

    print("Total splits:", split_count)
    return split_count
    

if __name__ == "__main__":
    main()