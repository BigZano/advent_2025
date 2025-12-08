from typing import List

def main(path: str = "./day_7/day_7_input.txt") -> int:
    with open(path, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    height = len(lines)
    width = max(len(l) for l in lines)
    grid = [list(l.ljust(width)) for l in lines]

    # Find the start column in first row
    try:
        start_col = grid[0].index('S')
    except ValueError:
        raise ValueError("No start position 'S' found in the top row.")

    # timeline_counts[row][col] = number of timelines at (row, col)
    timeline_counts = [ [0]*width for _ in range(height) ]
    timeline_counts[0][start_col] = 1

    for row in range(1, height):
        for col in range(width):
            count = timeline_counts[row-1][col]
            if count == 0:
                continue
            cell = grid[row][col]
            if cell == '.':
                timeline_counts[row][col] += count
            elif cell == '^':
                if col - 1 >= 0:
                    timeline_counts[row][col-1] += count
                if col + 1 < width:
                    timeline_counts[row][col+1] += count
            # if cell is ' ', beam is lost (do nothing)

    total_timelines = sum(timeline_counts[-1])
    print("Total timelines at bottom:", total_timelines)
    return total_timelines

if __name__ == "__main__":
    main()

