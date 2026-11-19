
def brute_force(amount, coins, stock):
    """
    Brute Force search for the minimum number of ATM notes.
    Uses a node limit to avoid excessive execution time.
    Returns the best result and whether the search completed.
    """

    coins = sorted(coins, reverse=True)  # arranged in denominators  sorts from largest to smallest
    best_result = None
    best_count = float('inf')
    nodes = 0
    max_nodes = 10000
    completed = True

    def solve(index, remaining, result, count):
        nonlocal best_result, best_count, nodes, completed

        nodes += 1

        if nodes > max_nodes:
            completed = False
            return

        if remaining == 0:
            if count < best_count:
                best_count = count
                best_result = result.copy()
            return

        if index == len(coins) or count >= best_count:
            return

        note = coins[index]
        available = stock.get(note, 0)
        maximum = min(remaining // note, available)

        for number in range(maximum, -1, -1):
            if not completed:
                return

            if number > 0:
                result[note] = number

            solve(
                index + 1,
                remaining - number * note,
                result,
                count + number
            )

            result.pop(note, None)

    solve(0, amount, {}, 0)

    return best_result, completed
