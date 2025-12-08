
# Part 1
def parse_grid(paper_grid: str):
    return [list(line) for line in paper_grid.strip().splitlines()]  # turn grid into strings

def neighbors(x, y, w, h):   # Say hi to your neighbor
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                yield nx, ny

def accessible_count(grid, roll='@'):    # Count accessible positions
    h = len(grid)
    w = len(grid[0]) if h else 0
    total = 0
    for y in range(h):                   # "main loop", go through and add to total
        for x in range(w):
            if grid[y][x] != roll:
                continue
            n = sum(1 for nx, ny in neighbors(x, y, w, h) if grid[ny][nx] == roll)
            if n < 4:
                total += 1
    return total

# part 2
def parse_grid(paper_grid: str):
    return [list(line) for line in paper_grid.strip().splitlines()]            # grid to strings

def neighbors(x, y, w, h):       # Say hi again
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h:
                yield nx, ny

def accessible_count(grid, roll='@', threshold=4):     # count accessible positions, create variables to remove
    h = len(grid)
    w = len(grid[0]) if h else 0
    grid = [row[:] for row in grid]    # create copy of grid
    total_removed = 0
    while True:                       # while loop to keep removing
        to_remove = []
        for y in range(h):
            for x in range(w):
                if grid[y][x] != roll:
                    continue
                n = sum(1 for nx, ny in neighbors(x, y, w, h) if grid[ny][nx] == roll)
                if n < threshold:
                    to_remove.append((x, y))
        if not to_remove:
            break
        for x, y in to_remove:
            grid[y][x] = '.'
        total_removed += len(to_remove)
    return total_removed
    
if __name__ == "__main__":
    
    grid = parse_grid(paper_grid)
    print(accessible_count(grid))