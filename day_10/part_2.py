import re
import pulp

def solve_min_presses(buttons, targets):
    m = len(targets)
    k = len(buttons)
    prob = pulp.LpProblem("MinPresses", pulp.LpMinimize)
    x = [pulp.LpVariable(f"x{j}", lowBound=0, cat='Integer') for j in range(k)]
    prob += pulp.lpSum(x)
    for p in range(m):
        prob += pulp.lpSum(x[j] for j in range(k) if p in buttons[j]) == targets[p]
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
    if status != 1:
        print("unsolvable, something went wrong")
        assert False
    return int(pulp.value(prob.objective))

def main():
    with open("input.txt", "r") as infile:
        data = infile.read().splitlines()

    presses_p2 = 0

    for lineno, line in enumerate(data, start=1):
        if not line or not line.strip():
            continue

        # parse indicator (not used for this part), buttons, and target vector
        m_ind = re.search(r"\[(.*?)\]", line)
        m_j = re.search(r"\{(.*?)\}", line)
        if not m_j:
            print(f"line {lineno}: missing target vector, skipping")
            continue

        wiring_groups = re.findall(r"\((.*?)\)", line)
        wiring = []
        for s in wiring_groups:
            nums = re.findall(r"\d+", s)
            if not nums:
                wiring.append([])
            else:
                wiring.append([int(x) for x in nums])

        joltage_ints = [int(x) for x in re.findall(r"\d+", m_j.group(1))]

        try:
            val = solve_min_presses(wiring, joltage_ints)
        except AssertionError:
            print(f"line {lineno}: unsolvable or solver error, skipping")
            continue
        except Exception as e:
            print(f"line {lineno}: solver raised exception: {e}")
            continue

        presses_p2 += val

    print(presses_p2)


if __name__ == "__main__":
    main()