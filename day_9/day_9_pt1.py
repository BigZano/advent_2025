from importlib.resources import path
from unittest import result


def parse_file(path: str = "input.txt") -> list[tuple[int, int]]:
    with open(path, 'r') as f:
        lines = [line.rstrip('\n') for line in f]
    # Parse coordinates into (x, y) tuples
    points = []
    for line in lines:
        if line.strip():  # Skip empty lines
            x, y = map(int, line.split(','))
            points.append((x, y))
    return points

def get_max_area(points: list[tuple[int, int]]) -> int:
    """Find the maximum rectangle area from coordinate points."""
    if len(points) < 2:
        return 0
    
    max_area = 0
    n = len(points)
    
    # Try all pairs of points as opposite corners of a rectangle
    # Using inclusive coordinates (add 1 to each dimension)
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Calculate area with inclusive coordinates
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            
            max_area = max(max_area, area)
    
    return max_area
    
lines = parse_file("/home/bret/Work/Advent of Code 2025/day_9/input.txt")
result = get_max_area(lines)
print(f"Largest rectangle area: {result}")