from pathlib import Path
from typing import List


def parse_worksheet_part2(lines: List[str]) -> int:
    """Part 2: Read right-to-left, each column is a number (top=MSD, bottom=LSD)."""
    width = max(len(l) for l in lines)
    grid = [list(l.rstrip("\n").ljust(width)) for l in lines]
    h = len(grid)
    ops_row = grid[-1]
    
    # Identify problems: groups of columns separated by space-only columns
    problems = []
    x = 0
    while x < width:
        # Skip space-only columns (separator)
        if all(grid[r][x] == ' ' for r in range(h)):
            x += 1
            continue
        
        # Found start of problem block
        start = x
        op = None
        while x < width and not all(grid[r][x] == ' ' for r in range(h)):
            if ops_row[x] in '+*':
                op = ops_row[x]
            x += 1
        end = x
        
        if op:
            problems.append((start, end, op))
    
    # Process each problem RIGHT-TO-LEFT
    total = 0
    for start, end, op in reversed(problems):
        # Within this problem block, each column represents one number
        # Read top-to-bottom to get digits (MSD first)
        numbers = []
        
        for col in range(start, end):
            # Read this column top-to-bottom, collecting digits
            digits = []
            for r in range(h - 1):  # Skip operator row
                c = grid[r][col]
                if c.isdigit():
                    digits.append(c)
            
            # If we collected digits, form a number
            if digits:
                numbers.append(int(''.join(digits)))
        
        # Apply operation to all numbers in this problem
        if numbers:
            if op == '+':
                result = sum(numbers)
            else:
                result = 1
                for n in numbers:
                    result *= n
            total += result
    
    return total


def parse_worksheet(lines: List[str]) -> int:
    """Part 1: Read left-to-right, each problem is vertical numbers."""
    width = max(len(l) for l in lines)
    grid = [list(l.rstrip("\n").ljust(width)) for l in lines]
    h = len(grid)
    ops_row = grid[-1]

    # Find problems separated by space-only columns
    problems = []
    x = 0
    while x < width:
        if all(grid[r][x] == ' ' for r in range(h)):
            x += 1
            continue
        
        start = x
        op = None
        while x < width and not all(grid[r][x] == ' ' for r in range(h)):
            if ops_row[x] in '+*':
                op = ops_row[x]
            x += 1
        end = x
        
        if op:
            problems.append((start, end, op))
    
    total = 0
    for start, end, op in problems:
        numbers = []
        for r in range(h - 1):
            row_segment = ''.join(grid[r][start:end]).strip()
            if row_segment and row_segment.replace(' ', '').isdigit():
                num_str = row_segment.replace(' ', '')
                if num_str:
                    numbers.append(int(num_str))
        
        if numbers:
            if op == '+':
                result = sum(numbers)
            else:
                result = 1
                for n in numbers:
                    result *= n
            total += result
    
    return total
def main(path: str = "day_6.txt", part: int = 2) -> None:
    text = Path(path).read_text()
    lines = [ln for ln in text.splitlines() if ln.rstrip()]
    
    if part == 1:
        total = parse_worksheet(lines)
    else:
        total = parse_worksheet_part2(lines)
    
    print(total)
if __name__ == "__main__":
    import sys
    part = 2
    path = "day_6.txt"
    if len(sys.argv) > 1:
        if sys.argv[1] in ["1", "2"]:
            part = int(sys.argv[1])
            if len(sys.argv) > 2:
                path = sys.argv[2]
        else:
            path = sys.argv[1]
    main(path, part)