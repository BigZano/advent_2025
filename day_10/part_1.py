
import os
import re
from typing import List, Optional, Tuple
from collections import defaultdict


def parse_line(line: str) -> Tuple[int, int, List[int]]:
    """Parse a single input line.

    Returns (n, target_mask, button_masks)
    - n: number of lights
    - target_mask: int with bit i set if target light i should be ON
    - button_masks: list of ints (length m) where bit i in button j indicates button j toggles light i
    """
    line = line.strip()
    if not line:
        return 0, 0, []
    # diagram between [ ]
    m_diag = re.search(r"\[([^\]]+)\]", line)
    if not m_diag:
        raise ValueError(f"No diagram found in line: {line}")
    diagram = m_diag.group(1)
    n = len(diagram)
    target_mask = 0
    for i, ch in enumerate(diagram):
        if ch == '#':
            target_mask |= 1 << i

    # find all button groups like (0,2,3)
    btns = re.findall(r"\(([^)]+)\)", line)
    button_masks: List[int] = []
    for b in btns:
        b = b.strip()
        if b == "":
            # empty parentheses (unlikely) -> no toggles
            button_masks.append(0)
            continue
        parts = [p.strip() for p in b.split(',') if p.strip() != '']
        mask = 0
        for p in parts:
            # indices are zero-based
            idx = int(p)
            if idx < 0 or idx >= n:
                # still accept but avoid crashing
                raise ValueError(f"Button index {idx} out of range for diagram length {n}")
            mask |= 1 << idx
        button_masks.append(mask)

    return n, target_mask, button_masks


def gauss_mod2(rows: List[int], rhs: List[int], m: int) -> Optional[Tuple[int, List[int]]]:
    """Gaussian elimination over GF(2).

    rows: list of row masks (length n), each mask has m bits for variables (buttons)
    rhs: list of right-hand side bits (length n)
    m: number of variables

    Returns (particular_solution_mask, nullspace_basis_list) or None if unsolvable.
    particular_solution_mask is an int of m bits (free vars = 0 by default)
    nullspace_basis_list is a list of int masks (each m bits)
    """
    n = len(rows)
    # make copies
    A = rows[:]  # row masks
    b = rhs[:]

    pivot_row_for_col = {}  # col -> row index
    r = 0
    for col in range(m):
        # find pivot
        pivot = None
        for i in range(r, n):
            if (A[i] >> col) & 1:
                pivot = i
                break
        if pivot is None:
            continue
        # swap
        A[r], A[pivot] = A[pivot], A[r]
        b[r], b[pivot] = b[pivot], b[r]
        pivot_row_for_col[col] = r
        # eliminate other rows
        for i in range(n):
            if i != r and ((A[i] >> col) & 1):
                A[i] ^= A[r]
                b[i] ^= b[r]
        r += 1

    # check for inconsistency: 0 == 1
    for i in range(r, n):
        if A[i] == 0 and b[i] == 1:
            return None

    # construct particular solution with free vars = 0
    x = 0
    for col, row in pivot_row_for_col.items():
        if b[row]:
            x |= 1 << col

    # nullspace basis: for each free col f, basis vector has 1 at f, and for each pivot col p
    # set bit p if pivot row has bit f set (because p depends on free variables)
    basis: List[int] = []
    pivot_cols = set(pivot_row_for_col.keys())
    for f in range(m):
        if f in pivot_cols:
            continue
        vec = 1 << f
        for p, row in pivot_row_for_col.items():
            if (A[row] >> f) & 1:
                vec |= 1 << p
        basis.append(vec)

    return x, basis


def min_weight_solution(particular: int, basis: List[int], cutoff: int = 26) -> int:
    """Enumerate the affine space particular + span(basis) to find minimal popcount.

    If the nullspace dimension is too large (> cutoff), this will still attempt enumeration
    but may be slow. Default cutoff is conservative; if you expect larger, increase it.
    Returns minimal popcount (number of button presses modulo parity).
    """
    k = len(basis)
    if k == 0:
        return particular.bit_count()
    if k > cutoff:
        # fallback: use meet-in-the-middle over the basis if dimension is reasonable
        if k <= 40:
            # we need to find v in span(basis) that minimizes popcount(particular ^ v)
            # do meet-in-the-middle on basis vectors: enumerate left/right spans and
            # for each left store map from xor -> minimal popcount of combined vector on that half,
            # then combine with right to compute full vector popcount.
            m = 0
            # determine number of bits in vectors (m) from highest bit in basis or particular
            for v in basis:
                if v:
                    m = max(m, v.bit_length())
            m = max(m, particular.bit_length())

            half = k // 2
            left = basis[:half]
            right = basis[half:]

            left_map = {}
            for s in range(1 << len(left)):
                xorv = 0
                i = 0
                ss = s
                while ss:
                    if ss & 1:
                        xorv ^= left[i]
                    ss >>= 1
                    i += 1
                vec = particular ^ xorv
                pc = vec.bit_count()
                if xorv not in left_map or pc < left_map[xorv]:
                    left_map[xorv] = pc

            best_w = None
            for s in range(1 << len(right)):
                xorv = 0
                i = 0
                ss = s
                while ss:
                    if ss & 1:
                        xorv ^= right[i]
                    ss >>= 1
                    i += 1
                # for this right xorv, combined vector is particular ^ xorv ^ xor_left
                # we need minimal over xor_left; iterate left_map entries
                for xor_left, pc_left in left_map.items():
                    total_pc = pc_left if xor_left == 0 else None
                    # Instead of recomputing fully, compute final popcount directly
                    cand_vec = particular ^ xor_left ^ xorv
                    total_pc = cand_vec.bit_count()
                    if best_w is None or total_pc < best_w:
                        best_w = total_pc
            return best_w if best_w is not None else particular.bit_count()
        # otherwise fall back to greedy hill-climb
        best = particular
        best_w = best.bit_count()
        improved = True
        while improved:
            improved = False
            for v in basis:
                cand = best ^ v
                w = cand.bit_count()
                if w < best_w:
                    best = cand
                    best_w = w
                    improved = True
        return best_w

    best = None
    best_w = None
    for mask in range(1 << k):
        s = particular
        msk = mask
        i = 0
        while msk:
            if msk & 1:
                s ^= basis[i]
            msk >>= 1
            i += 1
        w = s.bit_count()
        if best_w is None or w < best_w:
            best_w = w
            best = s
    return best_w if best_w is not None else 0


def mitm_min_presses(button_masks: List[int], target: int) -> int:
    """Meet-in-the-middle exact solver over the original buttons.

    Splits the buttons into two halves and finds the minimal total buttons pressed
    whose XOR equals the target.
    """
    m = len(button_masks)
    if m == 0:
        if target == 0:
            return 0
        raise ValueError("No buttons and non-zero target: unsolvable")
    m1 = m // 2
    left = button_masks[:m1]
    right = button_masks[m1:]

    left_map = {}
    for s in range(1 << len(left)):
        xorv = 0
        i = 0
        ss = s
        while ss:
            if ss & 1:
                xorv ^= left[i]
            ss >>= 1
            i += 1
        pc = s.bit_count()
        if xorv not in left_map or pc < left_map[xorv]:
            left_map[xorv] = pc

    best = None
    for s in range(1 << len(right)):
        xorv = 0
        i = 0
        ss = s
        while ss:
            if ss & 1:
                xorv ^= right[i]
            ss >>= 1
            i += 1
        need = target ^ xorv
        if need in left_map:
            total_pc = left_map[need] + s.bit_count()
            if best is None or total_pc < best:
                best = total_pc

    if best is None:
        raise ValueError("No combination of buttons achieves the target")
    return best


def solve_machine(line: str) -> int:
    """Solve one machine line and return minimal number of presses required."""
    n, target_mask, button_masks = parse_line(line)
    m = len(button_masks)
    if n == 0:
        return 0
    if m == 0:
        # no buttons: only solvable if target is zero
        if target_mask == 0:
            return 0
        raise ValueError("Unsolvable machine: no buttons but target requires lights on")

    # build rows: for each light i (0..n-1), set bits for buttons that toggle that light
    rows = []
    rhs = []
    for i in range(n):
        row = 0
        for j, bmask in enumerate(button_masks):
            if (bmask >> i) & 1:
                row |= 1 << j
        rows.append(row)
        rhs.append((target_mask >> i) & 1)

    # If number of buttons is moderate, use meet-in-the-middle directly (fast and exact).
    # This avoids enumerating the nullspace if it's large.
    if m <= 40:
        # build button_masks and call MITM directly
        try:
            return mitm_min_presses(button_masks, target_mask)
        except ValueError:
            # fall back to elimination to detect inconsistency more robustly
            pass

    res = gauss_mod2(rows, rhs, m)
    if res is None:
        raise ValueError("Unsolvable machine: inconsistent system")
    particular, basis = res
    return min_weight_solution(particular, basis)


def solve_file(path: str) -> int:
    total = 0
    with open(path, 'r') as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            total += solve_machine(line)
    return total


def main():
    here = os.path.dirname(__file__)
    input_path = os.path.join(here, 'input.txt')
    total = solve_file(input_path)
    print(total)


if __name__ == '__main__':
    main()
