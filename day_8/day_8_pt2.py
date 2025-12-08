from typing import List, Tuple


def find_last_connection(points: List[Tuple[int, int, int]]) -> int:
    n = len(points)
    if n < 2:
        return 0

    # Build list of all pairs (squared distance, i, j)
    pairs = []
    for i in range(n):
        xi, yi, zi = points[i]
        for j in range(i + 1, n):
            xj, yj, zj = points[j]
            d = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
            pairs.append((d, i, j))

    # Sort by distance (then by indices to break ties deterministically)
    pairs.sort()

    # Disjoint-set (union-find) with path compression and union by size
    parent = list(range(n))
    size = [1] * n

    def find(a: int) -> int:
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    components = n
    for _, i, j in pairs:
        if union(i, j):
            components -= 1
            if components == 1:
                # Return product of X coordinates of the final connected pair
                return points[i][0] * points[j][0]

    return 0


def main(path: str = "day_8/day_8_input.txt") -> int:
    with open(path, 'r') as f:
        points = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]
    return find_last_connection(points)


if __name__ == "__main__":
    print(main())