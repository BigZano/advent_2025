from pprint import pprint
from heapq import heappop, heappush
from collections import defaultdict
from pathlib import Path


def read_input_file(file_path: str) -> list[str]:
    # Resolve paths relative to this script so the file is found
    # regardless of the current working directory when running.
    path = Path(file_path)
    if not path.is_absolute():
        path = Path(__file__).parent / path

    with open(path, mode="r") as input_file:
        lines = input_file.readlines()
        return [line.strip() for line in lines]


def measure_time(func):
    def wrapper(*args, **kwargs):
        from time import perf_counter
        start_time = perf_counter()
        result = func(*args, **kwargs)
        print(f'Time (ms): {(perf_counter() - start_time) * 1000}')
        return result
    return wrapper


def order(o1: int, o2: int) -> tuple:
    return (min(o1, o2), max(o1, o2))


@measure_time
def solution(lines: list[str]):
    tiles = [tuple(map(int, line.split(','))) for line in lines]

    v_segments = defaultdict(list)
    h_segments = defaultdict(list)

    areas = []
    rid_to_pair = {}

    rid = 0
    n = len(tiles)

    # Store Segments
    for i in range(n):
        x1, y1 = tiles[i]
        x2, y2 = tiles[(i+1) % n]

        if x1 == x2:
            v_segments[x1].append(order(y1, y2))
        else:
            h_segments[y1].append(order(x1, x2))

    # Push All Possible Areas In A Heap
    for i in range(n-1):
        for j in range(i+1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            area = (abs(x1-x2)+1) * (abs(y1-y2)+1)

            heappush(areas, (-area, rid))
            rid_to_pair[rid] = (tiles[i], tiles[j])
            rid += 1
    
    while areas:
        area, rid = heappop(areas)
        p1, p2 = rid_to_pair[rid]
        
        x1, y1 = p1
        x2, y2 = p2

        x_min, x_max = sorted((x1, x2))
        y_min, y_max = sorted((y1, y2))
        
        is_valid = True

        # Check Vertical Segments
        for x, segments in v_segments.items():
            if not (x_min < x < x_max):
                continue

            for ys, ye in segments:
                if ye > y_min and ys < y_max:
                    is_valid = False
                    break
            
            if not is_valid:
                break
        
        if not is_valid:
            continue

        # Check Horizontal Segments
        for y, segments in h_segments.items():
            if not (y_min < y < y_max):
                continue

            for xs, xe in segments:
                if xe > x_min and xs < x_max:
                    is_valid = False
                    break

            if not is_valid:
                break
        
        if not is_valid:
            continue

        print(-area, p1, p2, is_valid)
        break

lines = read_input_file(file_path="input.txt")
solution(lines)