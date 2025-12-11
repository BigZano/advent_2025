from typing import List

def main(path: str = "day_8/day_8_input.txt", k: int = 1000) -> int:
    """Process 3D points from file and find product of sizes of three largest groups"""
    from itertools import combinations
    import heapq
    from collections import Counter
    from functools import reduce
    from operator import mul

    with open(path, 'r') as f:
        points = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]

    n = len(points)
    if n == 0:
        return 0

    total_pairs = n * (n - 1) // 2
    k = min(k, total_pairs)

    # Generate pairwise squared distances lazily and pick k smallest efficiently.
    def pair_dist_iter():
        for i in range(n):
            xi, yi, zi = points[i]
            for j in range(i + 1, n):
                xj, yj, zj = points[j]
                d = (xi - xj) ** 2 + (yi - yj) ** 2 + (zi - zj) ** 2
                yield (d, i, j)


    smallest = heapq.nsmallest(k, pair_dist_iter(), key=lambda x: x[0])

    # Disjoint-set (union-find) with size
    parent = list(range(n))
    size = [1] * n

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        return True

    # Process the k smallest pairs in ascending distance order.
    smallest.sort(key=lambda x: x[0])
    for _, i, j in smallest:
        union(i, j)

    # Count component sizes
    roots = [find(i) for i in range(n)]
    counts = Counter(roots)
    sizes = sorted(counts.values(), reverse=True)

    # Debug prints
    print(f"All group sizes (desc): {sizes}")
    top3 = sizes[:3]
    print(f"Top 3 sizes: {top3}")

    if not top3:
        return 0
    return reduce(mul, top3, 1)

if __name__ == "__main__":
    print(main())