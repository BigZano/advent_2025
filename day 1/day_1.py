def unlock_door(door_code):
    import re
    tokens = re.findall(r'([RL])\s*(\d+)', list_of_turns_raw)
    list_of_turns = [int(n) if d == 'R' else -int(n) for d, n in tokens]

    dial_position = 50
    zero_count = 0

    def hit_on_zero(p: int, amt: int) -> int:
        # count landings on 0s while moving and stopping
        a = abs(amt)
        if a == 0:
            return 0
        if amt > 0:
            i0 = (100 - p) % 100
        else:
            i0 = p % 100
        if i0 == 0:
            return 1 + (a - 1) // 100
        elif a <= i0:
            return 0
        else:
            return 1 + (a - i0 - 1) // 100
        
    for turn in list_of_turns:
        zero_count += hit_on_zero(dial_position, turn)
        dial_position = (dial_position + turn) % 100

    return zero_count

if __name__ == "__main__":
    result = unlock_door(None)
    print(f"Final zero count: {result}")

    